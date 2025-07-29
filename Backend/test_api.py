#!/usr/bin/env python3
"""
PyCrypt API Test Script

Test script to verify that the API endpoints are working correctly.
Run this after starting the API server to test functionality.
"""

import requests
import json
import time
import base64

API_BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_text_encryption_decryption():
    """Test text encryption and decryption"""
    print("\n🔍 Testing text encryption/decryption...")
    
    test_text = "Hello, this is a secret message for testing! 🔐"
    test_password = "test_password_123"
    test_hint = "Test password hint"
    
    try:
        # Test encryption
        print("  📤 Testing text encryption...")
        encrypt_response = requests.post(f"{API_BASE_URL}/encrypt/text", json={
            "text": test_text,
            "password": test_password,
            "hint": test_hint
        })
        
        if encrypt_response.status_code != 200:
            print(f"❌ Encryption failed: {encrypt_response.status_code}")
            return False
        
        encrypt_data = encrypt_response.json()
        if not encrypt_data.get('success'):
            print(f"❌ Encryption failed: {encrypt_data.get('error')}")
            return False
        
        encrypted_content = encrypt_data['encrypted_content']
        print(f"✅ Text encrypted successfully (length: {len(encrypted_content)} chars)")
        
        # Test decryption
        print("  📥 Testing text decryption...")
        decrypt_response = requests.post(f"{API_BASE_URL}/decrypt/text", json={
            "encrypted_content": encrypted_content,
            "password": test_password
        })
        
        if decrypt_response.status_code != 200:
            print(f"❌ Decryption failed: {decrypt_response.status_code}")
            return False
        
        decrypt_data = decrypt_response.json()
        if not decrypt_data.get('success'):
            print(f"❌ Decryption failed: {decrypt_data.get('error')}")
            return False
        
        decrypted_text = decrypt_data['decrypted_text']
        
        if decrypted_text == test_text:
            print("✅ Text decryption successful - original text recovered!")
            return True
        else:
            print(f"❌ Decrypted text doesn't match original:")
            print(f"   Original: {test_text}")
            print(f"   Decrypted: {decrypted_text}")
            return False
            
    except Exception as e:
        print(f"❌ Text encryption/decryption error: {e}")
        return False

def test_file_encryption_decryption():
    """Test file encryption and decryption"""
    print("\n🔍 Testing file encryption/decryption...")
    
    # Create test file content
    test_content = "This is test file content for encryption!\nLine 2 of the test file.\n🔒 Security test!"
    test_password = "file_test_password_456"
    test_hint = "File test hint"
    
    try:
        # Test file encryption (simulate file upload)
        print("  📤 Testing file encryption...")
        files = {'file': ('test.txt', test_content, 'text/plain')}
        data = {'password': test_password, 'hint': test_hint}
        
        encrypt_response = requests.post(f"{API_BASE_URL}/encrypt/file", files=files, data=data)
        
        if encrypt_response.status_code != 200:
            print(f"❌ File encryption failed: {encrypt_response.status_code}")
            return False
        
        encrypt_data = encrypt_response.json()
        if not encrypt_data.get('success'):
            print(f"❌ File encryption failed: {encrypt_data.get('error')}")
            return False
        
        encrypted_content = encrypt_data['encrypted_content']
        filename = encrypt_data['filename']
        print(f"✅ File encrypted successfully: {filename}")
        
        # Test file decryption
        print("  📥 Testing file decryption...")
        decrypt_response = requests.post(f"{API_BASE_URL}/decrypt/file", json={
            "encrypted_content": encrypted_content,
            "password": test_password,
            "filename": filename
        })
        
        if decrypt_response.status_code != 200:
            print(f"❌ File decryption failed: {decrypt_response.status_code}")
            return False
        
        decrypt_data = decrypt_response.json()
        if not decrypt_data.get('success'):
            print(f"❌ File decryption failed: {decrypt_data.get('error')}")
            return False
        
        # Decode the decrypted content
        decrypted_content_b64 = decrypt_data['decrypted_content']
        decrypted_content = base64.b64decode(decrypted_content_b64).decode('utf-8')
        
        if decrypted_content.strip() == test_content.strip():
            print("✅ File decryption successful - original content recovered!")
            return True
        else:
            print(f"❌ Decrypted content doesn't match original:")
            print(f"   Original length: {len(test_content)}")
            print(f"   Decrypted length: {len(decrypted_content)}")
            return False
            
    except Exception as e:
        print(f"❌ File encryption/decryption error: {e}")
        return False

def test_wrong_password():
    """Test decryption with wrong password"""
    print("\n🔍 Testing wrong password handling...")
    
    test_text = "Secret message"
    correct_password = "correct_password"
    wrong_password = "wrong_password"
    
    try:
        # Encrypt with correct password
        encrypt_response = requests.post(f"{API_BASE_URL}/encrypt/text", json={
            "text": test_text,
            "password": correct_password
        })
        
        encrypt_data = encrypt_response.json()
        encrypted_content = encrypt_data['encrypted_content']
        
        # Try to decrypt with wrong password
        decrypt_response = requests.post(f"{API_BASE_URL}/decrypt/text", json={
            "encrypted_content": encrypted_content,
            "password": wrong_password
        })
        
        if decrypt_response.status_code == 200:
            decrypt_data = decrypt_response.json()
            if decrypt_data.get('success'):
                print("❌ Wrong password test failed - decryption should have failed!")
                return False
            else:
                print("✅ Wrong password correctly rejected")
                return True
        else:
            print("✅ Wrong password correctly rejected (HTTP error)")
            return True
            
    except Exception as e:
        print(f"❌ Wrong password test error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Starting PyCrypt API Tests")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_text_encryption_decryption,
        test_file_encryption_decryption,
        test_wrong_password
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the API server and try again.")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1) 