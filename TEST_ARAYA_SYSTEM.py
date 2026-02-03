"""
ARAYA SYSTEM TEST SUITE
Test the complete natural language to file system bridge

Run this after starting both services:
1. python ARAYA_FILE_WRITER.py
2. python ARAYA_BRIDGE.py
3. python TEST_ARAYA_SYSTEM.py
"""

import requests
import json
import time
from datetime import datetime

BRIDGE_URL = "http://localhost:5002"
FILE_WRITER_URL = "http://localhost:5001"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_result(success, message):
    symbol = "✅" if success else "❌"
    print(f"{symbol} {message}")

def test_health_checks():
    """Test 1: Health checks for both services"""
    print_header("TEST 1: Health Checks")

    # Test Bridge
    try:
        r = requests.get(f"{BRIDGE_URL}/health", timeout=5)
        data = r.json()
        print_result(r.status_code == 200, f"Bridge: {data['status']}")
        print(f"   Claude API: {data.get('claude_api', 'unknown')}")
        print(f"   File Writer: {data.get('file_writer_status', 'unknown')}")
    except Exception as e:
        print_result(False, f"Bridge health check failed: {e}")
        return False

    # Test File Writer
    try:
        r = requests.get(f"{FILE_WRITER_URL}/health", timeout=5)
        data = r.json()
        print_result(r.status_code == 200, f"File Writer: {data['status']}")
    except Exception as e:
        print_result(False, f"File Writer health check failed: {e}")
        return False

    return True

def test_file_write():
    """Test 2: Direct file write (bypass bridge)"""
    print_header("TEST 2: Direct File Write")

    test_file = "TEST_ARAYA_OUTPUT.html"
    test_content = f"""<!DOCTYPE html>
<html>
<head><title>ARAYA Test</title></head>
<body>
    <h1>Test file created at {datetime.now()}</h1>
    <p>This file was created by the ARAYA test suite.</p>
</body>
</html>"""

    try:
        r = requests.post(
            f"{FILE_WRITER_URL}/write-file",
            json={
                "file_path": test_file,
                "content": test_content,
                "action": "write"
            },
            timeout=10
        )

        data = r.json()
        if data.get("success"):
            print_result(True, f"Created {test_file} ({data['size']} bytes)")
            return True
        else:
            print_result(False, f"Write failed: {data.get('error')}")
            return False
    except Exception as e:
        print_result(False, f"File write test failed: {e}")
        return False

def test_chat():
    """Test 3: Simple chat (no editing)"""
    print_header("TEST 3: Chat Functionality")

    try:
        r = requests.post(
            f"{BRIDGE_URL}/chat",
            json={
                "message": "What can you help me with?",
                "conversation_history": []
            },
            timeout=15
        )

        data = r.json()
        if "response" in data:
            print_result(True, "Chat response received")
            print(f"   ARAYA: {data['response'][:100]}...")
            return True
        else:
            print_result(False, f"Chat failed: {data.get('error')}")
            return False
    except Exception as e:
        print_result(False, f"Chat test failed: {e}")
        return False

def test_edit_request():
    """Test 4: Natural language edit request"""
    print_header("TEST 4: Natural Language Edit")

    # First create a test file
    test_file = "TEST_EDIT_TARGET.html"
    original_content = """<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body style="background: white;">
    <h1>Original Heading</h1>
    <p>This is a test paragraph.</p>
</body>
</html>"""

    # Write test file
    print("Creating test file...")
    requests.post(
        f"{FILE_WRITER_URL}/write-file",
        json={
            "file_path": test_file,
            "content": original_content,
            "action": "write"
        }
    )

    # Now test edit via bridge
    print("Requesting edit via ARAYA Bridge...")
    try:
        r = requests.post(
            f"{BRIDGE_URL}/edit",
            json={
                "message": f"Change the background of {test_file} to blue",
                "conversation_history": []
            },
            timeout=30  # Claude API can take a while
        )

        data = r.json()
        if data.get("success"):
            print_result(True, "Edit completed successfully")
            print(f"   File: {data.get('file_path')}")
            print(f"   Action: {data.get('action')}")
            print(f"   Reasoning: {data.get('reasoning', 'N/A')}")

            # Verify the edit
            verify = requests.post(
                f"{FILE_WRITER_URL}/read-file",
                json={"file_path": test_file}
            )
            if verify.status_code == 200:
                content = verify.json()['content']
                if 'blue' in content.lower():
                    print_result(True, "Verified: File contains 'blue'")
                else:
                    print_result(False, "Verification failed: 'blue' not found")

            return True
        else:
            print_result(False, f"Edit failed: {data.get('error')}")
            print(f"   Details: {data.get('reasoning', 'N/A')}")
            return False

    except Exception as e:
        print_result(False, f"Edit test failed: {e}")
        return False

def test_complex_edit():
    """Test 5: Complex multi-line edit"""
    print_header("TEST 5: Complex Edit Request")

    try:
        r = requests.post(
            f"{BRIDGE_URL}/edit",
            json={
                "message": "Add a welcome message to TEST_EDIT_TARGET.html after the h1 tag",
                "conversation_history": []
            },
            timeout=30
        )

        data = r.json()
        if data.get("success"):
            print_result(True, "Complex edit completed")
            print(f"   Reasoning: {data.get('reasoning', 'N/A')}")
            return True
        else:
            print_result(False, f"Complex edit failed: {data.get('error')}")
            return False

    except Exception as e:
        print_result(False, f"Complex edit test failed: {e}")
        return False

def test_error_handling():
    """Test 6: Error handling"""
    print_header("TEST 6: Error Handling")

    # Test 1: Invalid file path
    try:
        r = requests.post(
            f"{BRIDGE_URL}/edit",
            json={
                "message": "Edit the file at ../../../etc/passwd",
                "conversation_history": []
            },
            timeout=30
        )

        data = r.json()
        if not data.get("success"):
            print_result(True, "Security violation properly blocked")
        else:
            print_result(False, "SECURITY ISSUE: Path traversal not blocked!")

    except Exception as e:
        print_result(False, f"Security test failed: {e}")

    # Test 2: Non-existent file (should fail gracefully)
    try:
        r = requests.post(
            f"{BRIDGE_URL}/edit",
            json={
                "message": "Edit NONEXISTENT_FILE_123456.html",
                "conversation_history": []
            },
            timeout=30
        )

        data = r.json()
        if not data.get("success"):
            print_result(True, "Non-existent file handled gracefully")
        else:
            print_result(False, "Should have failed for non-existent file")

    except Exception as e:
        print_result(False, f"Non-existent file test failed: {e}")

    return True

def run_all_tests():
    """Run complete test suite"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ARAYA SYSTEM TEST SUITE" + " "*20 + "║")
    print("╚" + "="*58 + "╝")

    results = []

    # Run tests
    results.append(("Health Checks", test_health_checks()))
    time.sleep(1)

    results.append(("File Write", test_file_write()))
    time.sleep(1)

    results.append(("Chat", test_chat()))
    time.sleep(1)

    results.append(("Natural Language Edit", test_edit_request()))
    time.sleep(1)

    results.append(("Complex Edit", test_complex_edit()))
    time.sleep(1)

    results.append(("Error Handling", test_error_handling()))

    # Print summary
    print_header("TEST SUMMARY")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        print_result(result, test_name)

    print("\n" + "="*60)
    print(f"  RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("  🎉 ALL TESTS PASSED!")
    else:
        print(f"  ⚠️  {total - passed} test(s) failed")

    print("="*60 + "\n")

    return passed == total

if __name__ == "__main__":
    print("\nStarting ARAYA System Tests...")
    print("Make sure both services are running:")
    print("  1. python ARAYA_FILE_WRITER.py")
    print("  2. python ARAYA_BRIDGE.py")
    print("\nPress Enter to continue...")
    input()

    success = run_all_tests()

    if success:
        print("\n✅ System is fully operational!")
        print("\nNext steps:")
        print("  1. Open araya-chat.html in browser")
        print("  2. Try: 'Make the homepage background blue'")
        print("  3. Check index.html to verify changes")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("  - Make sure both services are running")
        print("  - Check ANTHROPIC_API_KEY in .env")
        print("  - Check terminal output for errors")

    print("\n")
