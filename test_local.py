#!/usr/bin/env python3
"""
Local testing script for Google Cloud Function
Run this to test the function locally before deploying
"""

import json
import os
import sys
from unittest.mock import Mock

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_mock_request(method='GET', path='/', body=None, headers=None):
    """Create a mock Flask request object"""
    request = Mock()
    request.method = method
    request.path = path
    request.get_data = lambda: json.dumps(body).encode() if body else b'{}'
    request.get_json = lambda: body if body else {}
    request.headers = headers or {}
    return request

def test_function():
    """Test the Google Cloud Function locally"""
    
    try:
        from main import chat
        
        print("✅ Successfully imported function handler")
        
        # Test 1: GET request to root path (should return HTML)
        print("\n🧪 Test 1: GET request to root path")
        request = create_mock_request('GET', '/')
        
        response = chat(request)
        if isinstance(response, tuple):
            body, status_code, headers = response
            print(f"Status: {status_code}")
            print(f"Content-Type: {headers.get('Content-Type', 'N/A')}")
            print(f"Body length: {len(body)} characters")
            
            if status_code == 200 and 'text/html' in headers.get('Content-Type', ''):
                print("✅ HTML response successful")
            else:
                print("❌ HTML response failed")
        else:
            print("❌ Unexpected response format")
        
        # Test 2: Health endpoint
        print("\n🧪 Test 2: Health endpoint")
        request = create_mock_request('GET', '/health')
        
        response = chat(request)
        if isinstance(response, tuple):
            body, status_code, headers = response
            print(f"Status: {status_code}")
            print(f"Content-Type: {headers.get('Content-Type', 'N/A')}")
            
            if status_code == 200:
                try:
                    data = json.loads(body)
                    print("✅ Health endpoint working")
                    print(f"Project: {data.get('project', 'N/A')}")
                    print(f"Location: {data.get('location', 'N/A')}")
                    print(f"Status: {data.get('status', 'N/A')}")
                except json.JSONDecodeError:
                    print("❌ Health response not valid JSON")
            else:
                print("❌ Health endpoint failed")
        else:
            print("❌ Unexpected response format")
        
        # Test 3: POST chat request
        print("\n🧪 Test 3: POST chat request")
        request = create_mock_request('POST', '/', {'message': 'Hello Ray!'})
        
        response = chat(request)
        if isinstance(response, tuple):
            body, status_code, headers = response
            print(f"Status: {status_code}")
            print(f"Content-Type: {headers.get('Content-Type', 'N/A')}")
            
            if status_code == 200:
                try:
                    data = json.loads(body)
                    if 'message' in data:
                        print("✅ Chat response successful")
                        print(f"Response: {data['message'][:100]}...")
                    else:
                        print("❌ Chat response missing message")
                except json.JSONDecodeError:
                    print("❌ Chat response not valid JSON")
            else:
                print("❌ Chat request failed")
        else:
            print("❌ Unexpected response format")
        
        # Test 4: OPTIONS request (CORS)
        print("\n🧪 Test 4: CORS preflight")
        request = create_mock_request('OPTIONS', '/')
        
        response = chat(request)
        if isinstance(response, tuple):
            body, status_code, headers = response
            print(f"Status: {status_code}")
            print(f"CORS Headers: {headers}")
            
            if status_code == 200 and 'Access-Control-Allow-Origin' in headers:
                print("✅ CORS preflight successful")
            else:
                print("❌ CORS preflight failed")
        else:
            print("❌ Unexpected response format")
        
        print("\n🎉 All tests completed!")
        
    except ImportError as e:
        print(f"❌ Failed to import function: {e}")
        print("Make sure you're running this from the project root directory")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_function()
