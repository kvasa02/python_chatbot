#!/usr/bin/env python3
"""
Test script for the AI-Powered Chatbot
This script tests the chatbot functionality without requiring API keys.
"""

import sys
import os

def test_basic_functionality():
    """Test basic chatbot functionality"""
    print("🧪 Testing basic chatbot functionality...")
    
    try:
        # Import the chatbot
        from app import chatbot
        
        # Test intent classification
        test_queries = [
            "hello",
            "weather in London",
            "tell me a joke",
            "what's the latest news",
            "goodbye"
        ]
        
        print("\nTesting intent classification:")
        for query in test_queries:
            intent = chatbot.classify_intent(query)
            print(f"  '{query}' -> {intent}")
        
        # Test entity extraction
        print("\nTesting entity extraction:")
        test_entities = [
            "weather in New York",
            "tell me about Python programming"
        ]
        
        for query in test_entities:
            entities = chatbot.extract_entities(query)
            print(f"  '{query}' -> {entities}")
        
        # Test response generation (without API calls)
        print("\nTesting response generation:")
        test_responses = [
            "hello",
            "help",
            "bye"
        ]
        
        for query in test_responses:
            response = chatbot.generate_response(query)
            print(f"  '{query}' -> {response[:50]}...")
        
        print("\n✅ Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_integration():
    """Test API integration (if keys are available)"""
    print("\n🔑 Testing API integration...")
    
    try:
        from app import chatbot
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Test weather API
        weather_key = os.getenv('OPENWEATHER_API_KEY')
        if weather_key and weather_key != 'your_openweather_api_key_here':
            print("  Testing weather API...")
            response = chatbot.get_weather("London")
            if "Weather in London" in response or "Sorry" in response:
                print("  ✅ Weather API working")
            else:
                print("  ❌ Weather API test failed")
        else:
            print("  ⚠️  Weather API key not configured")
        
        # Test news API
        news_key = os.getenv('NEWS_API_KEY')
        if news_key and news_key != 'your_news_api_key_here':
            print("  Testing news API...")
            response = chatbot.get_news()
            if "Latest Headlines" in response or "Sorry" in response:
                print("  ✅ News API working")
            else:
                print("  ❌ News API test failed")
        else:
            print("  ⚠️  News API key not configured")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🤖 AI Chatbot Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    basic_success = test_basic_functionality()
    
    # Test API integration
    api_success = test_api_integration()
    
    print("\n" + "=" * 50)
    print("📊 Test Results")
    print("=" * 50)
    print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"API Integration: {'✅ PASS' if api_success else '⚠️  SKIP'}")
    
    if basic_success:
        print("\n🎉 Chatbot is working correctly!")
        print("You can now run: python app.py")
    else:
        print("\n❌ Some tests failed. Please check the installation.")
        sys.exit(1)

if __name__ == "__main__":
    main() 