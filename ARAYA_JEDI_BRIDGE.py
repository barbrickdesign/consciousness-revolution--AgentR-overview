"""
ARAYA-JEDI ALLIANCE BRIDGE
==========================
Connects ARAYA to the Jedi Alliance Router for multi-AI routing.
Import this into ARAYA_UNIFIED_API.py when ready.

Usage:
    from ARAYA_JEDI_BRIDGE import route_to_alliance, get_alliance_status
"""

import sys
sys.path.insert(0, 'C:/Users/dwrek/.consciousness')

# Try to load Jedi Alliance
try:
    from JEDI_ALLIANCE_ROUTER import JediAllianceRouter
    ALLIANCE = JediAllianceRouter()
    AVAILABLE = True
    print("[JEDI BRIDGE] Alliance Router connected")
except Exception as e:
    ALLIANCE = None
    AVAILABLE = False
    print(f"[JEDI BRIDGE] Alliance not available: {e}")

def route_to_alliance(message: str, provider: str = None, swarm: bool = False) -> dict:
    """
    Route a message through Jedi Alliance for multi-AI routing.

    Args:
        message: The user message/task
        provider: Force specific provider (optional)
        swarm: Use multi-AI swarm mode (optional)

    Returns:
        dict with 'response', 'provider', 'complexity', 'success'
    """
    if not AVAILABLE or not ALLIANCE:
        return {
            'response': None,
            'provider': None,
            'complexity': 0,
            'success': False,
            'error': 'Jedi Alliance not available'
        }

    try:
        result = ALLIANCE.query(message, provider=provider, swarm=swarm)
        return {
            'response': result.get('result', ''),
            'provider': result.get('provider', 'unknown'),
            'complexity': result.get('complexity', 0),
            'success': True,
            'execution_time': result.get('execution_time', 0)
        }
    except Exception as e:
        return {
            'response': None,
            'provider': None,
            'complexity': 0,
            'success': False,
            'error': str(e)
        }

def get_alliance_status() -> dict:
    """Get current Jedi Alliance status"""
    if not AVAILABLE:
        return {
            'available': False,
            'providers': [],
            'stats': {}
        }

    try:
        providers = ALLIANCE.list_providers() if hasattr(ALLIANCE, 'list_providers') else []
        stats = ALLIANCE.get_stats() if hasattr(ALLIANCE, 'get_stats') else {}
        return {
            'available': True,
            'providers': providers,
            'stats': stats
        }
    except Exception as e:
        return {
            'available': True,
            'providers': [],
            'stats': {},
            'error': str(e)
        }

def analyze_complexity(message: str) -> int:
    """Analyze message complexity (1-10)"""
    if not AVAILABLE or not ALLIANCE:
        return 5  # Default to medium

    try:
        if hasattr(ALLIANCE, 'analyze_complexity'):
            return ALLIANCE.analyze_complexity(message)
        else:
            # Basic complexity analysis
            complexity = 5
            if len(message) > 500:
                complexity += 2
            if any(word in message.lower() for word in ['design', 'architect', 'analyze']):
                complexity += 2
            if any(word in message.lower() for word in ['simple', 'what is', 'define']):
                complexity -= 2
            return max(1, min(10, complexity))
    except:
        return 5

# Test if run directly
if __name__ == '__main__':
    print("\n=== ARAYA-JEDI BRIDGE TEST ===\n")

    status = get_alliance_status()
    print(f"Alliance Available: {status['available']}")

    if status['available']:
        # Test simple query
        result = route_to_alliance("What is 2+2?")
        print(f"\nSimple query result:")
        print(f"  Provider: {result.get('provider')}")
        print(f"  Complexity: {result.get('complexity')}")
        print(f"  Success: {result.get('success')}")

        # Test complexity analysis
        complexity = analyze_complexity("Design a microservices architecture for 10 million users")
        print(f"\nComplex task complexity: {complexity}/10")
    else:
        print("Alliance not available - check JEDI_ALLIANCE_ROUTER.py")

    print("\n=== BRIDGE TEST COMPLETE ===")
