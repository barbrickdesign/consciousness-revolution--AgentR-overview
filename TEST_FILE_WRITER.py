"""
TEST: ARAYA FILE WRITER
Runs tests against the file writer endpoint
"""

import requests
import json
import os

BASE_URL = "http://localhost:5001"
TEST_FILE = "test_araya_write.html"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing health endpoint...")
    resp = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
    return resp.status_code == 200

def test_write_file():
    """Test writing a file"""
    print("\n✍️ Testing write file...")

    content = """<!DOCTYPE html>
<html>
<head><title>ARAYA Test</title></head>
<body>
    <h1>ARAYA wrote this file!</h1>
    <p>Timestamp: 2025-12-24</p>
</body>
</html>"""

    resp = requests.post(f"{BASE_URL}/write-file", json={
        "file_path": TEST_FILE,
        "content": content,
        "action": "write"
    })

    print(f"   Status: {resp.status_code}")
    result = resp.json()
    print(f"   Response: {json.dumps(result, indent=2)}")

    # Verify file exists
    full_path = f"C:/Users/dwrek/100X_DEPLOYMENT/{TEST_FILE}"
    exists = os.path.exists(full_path)
    print(f"   File exists: {exists}")

    return resp.status_code == 200 and exists

def test_read_file():
    """Test reading the file back"""
    print("\n📖 Testing read file...")

    resp = requests.post(f"{BASE_URL}/read-file", json={
        "file_path": TEST_FILE
    })

    print(f"   Status: {resp.status_code}")
    result = resp.json()
    print(f"   Content length: {result.get('size', 0)}")
    print(f"   First 100 chars: {result.get('content', '')[:100]}")

    return resp.status_code == 200

def test_append_file():
    """Test appending to file"""
    print("\n➕ Testing append...")

    resp = requests.post(f"{BASE_URL}/write-file", json={
        "file_path": TEST_FILE,
        "content": "\n<p>ARAYA appended this line!</p>",
        "action": "append"
    })

    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")

    return resp.status_code == 200

def test_edit_file():
    """Test editing a file"""
    print("\n✏️ Testing edit (replace)...")

    resp = requests.post(f"{BASE_URL}/write-file", json={
        "file_path": TEST_FILE,
        "action": "edit",
        "old_string": "ARAYA wrote this file!",
        "new_string": "ARAYA EDITED this file!"
    })

    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")

    return resp.status_code == 200

def test_security():
    """Test security (try to write outside allowed root)"""
    print("\n🔒 Testing security...")

    resp = requests.post(f"{BASE_URL}/write-file", json={
        "file_path": "C:/Users/dwrek/Desktop/HACKER.txt",
        "content": "Should fail",
        "action": "write"
    })

    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")

    # Should be 403 Forbidden
    return resp.status_code == 403

def test_list_files():
    """Test listing files"""
    print("\n📂 Testing list files...")

    resp = requests.post(f"{BASE_URL}/list-files", json={
        "dir_path": "."
    })

    print(f"   Status: {resp.status_code}")
    result = resp.json()
    print(f"   Files found: {len(result.get('files', []))}")
    print(f"   First 5 files: {[f['name'] for f in result.get('files', [])[:5]]}")

    return resp.status_code == 200

def cleanup():
    """Remove test file"""
    print("\n🧹 Cleaning up...")
    try:
        os.remove(f"C:/Users/dwrek/100X_DEPLOYMENT/{TEST_FILE}")
        print("   Test file removed")
    except:
        print("   Test file not found (already cleaned)")

if __name__ == '__main__':
    print("=" * 60)
    print("ARAYA FILE WRITER - TEST SUITE")
    print("=" * 60)

    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except:
        print("\n❌ Server not running!")
        print("   Start it with: python ARAYA_FILE_WRITER.py")
        exit(1)

    tests = [
        ("Health Check", test_health),
        ("Write File", test_write_file),
        ("Read File", test_read_file),
        ("Append File", test_append_file),
        ("Edit File", test_edit_file),
        ("List Files", test_list_files),
        ("Security Check", test_security),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS:")
    print("=" * 60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    cleanup()

    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    print(f"\n{passed_count}/{total_count} tests passed")
    print("=" * 60)
