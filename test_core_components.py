#!/usr/bin/env python3
"""
Test script to verify the ETA Agent System core backend components
"""

import asyncio
import sys
import os

# Add backend to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_prompt_manager():
    """Test prompt configuration system"""
    print("🧪 Testing Prompt Manager...")
    
    try:
        from app.config.prompt_manager import prompt_manager
        
        # Test loading driver prompt
        driver_prompt = prompt_manager.get_prompt_for_role("driver", version="v1")
        print(f"✅ Driver prompt loaded: {driver_prompt['model_name']}")
        
        # Test loading user prompt
        user_prompt = prompt_manager.get_prompt_for_role("user", version="v1")
        print(f"✅ User prompt loaded: {user_prompt['model_name']}")
        
        # Test parameter substitution
        test_context = {
            "origin": "New York",
            "destination": "Los Angeles",
            "timestamp_of_anomaly": "2024-01-15 10:30:00",
            "current_eta": "2024-01-16 14:00:00"
        }
        
        substituted_prompt = prompt_manager.get_prompt_for_role("driver", version="v1", **test_context)
        print(f"✅ Parameter substitution working")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt Manager test failed: {e}")
        return False

async def test_weather_client():
    """Test weather client"""
    print("🌤️ Testing Weather Client...")
    
    try:
        from app.clients.weather_client import OpenMeteoClient
        
        async with OpenMeteoClient() as client:
            # Test current weather (New York coordinates)
            weather = await client.get_current_weather(40.7128, -74.0060)
            
            if weather.get("success"):
                print(f"✅ Weather data retrieved successfully")
                current = weather["data"].get("current", {})
                temp = current.get("temperature_2m", "N/A")
                print(f"   Temperature in NYC: {temp}°C")
            else:
                print(f"❌ Weather data retrieval failed: {weather.get('error')}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Weather Client test failed: {e}")
        return False

async def test_traffic_client():
    """Test traffic client"""
    print("🚗 Testing Traffic Client...")
    
    try:
        from app.clients.traffic_client import OpenRouteServiceClient
        
        async with OpenRouteServiceClient() as client:
            # Test geocoding
            geo_result = await client.geocode("New York")
            
            if geo_result.get("success"):
                print(f"✅ Geocoding working")
                features = geo_result["data"].get("features", [])
                if features:
                    coords = features[0].get("geometry", {}).get("coordinates", [])
                    print(f"   NYC coordinates: {coords}")
            else:
                print(f"❌ Geocoding failed: {geo_result.get('error')}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Traffic Client test failed: {e}")
        return False

async def test_agent_services():
    """Test agent services"""
    print("🤖 Testing Agent Services...")
    
    try:
        from app.services.driver_agent import DriverAgentService
        from app.services.user_agent import UserAgentService
        
        # Test service initialization
        driver_service = DriverAgentService()
        user_service = UserAgentService()
        
        print(f"✅ Driver Agent Service initialized")
        print(f"✅ User Agent Service initialized")
        
        # Test service methods (without OpenAI calls for now)
        test_context = {
            "origin": "New York",
            "destination": "Los Angeles",
            "conversation_history": "Test conversation",
            "current_location": "New York"
        }
        
        # Test message analysis
        analysis = await driver_service._analyze_driver_message("I need help with my route", test_context)
        print(f"✅ Message analysis working: {analysis}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent Services test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚚 ETA Agent System - Core Components Test")
    print("=" * 50)
    
    tests = [
        ("Prompt Manager", test_prompt_manager),
        ("Weather Client", test_weather_client),
        ("Traffic Client", test_traffic_client),
        ("Agent Services", test_agent_services)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        result = await test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core components are working correctly!")
        print("\n🚀 Ready for Phase 3: Frontend Development")
        return True
    else:
        print("❌ Some components need attention")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 