#!/usr/bin/env python3
"""
Test script to verify .env file loading
Save this as test_env.py in your project root
"""

import os
from dotenv import load_dotenv

def test_env_loading():
    print("=== Environment Loading Test ===")
    
    # Show current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Check if .env file exists
    env_path = os.path.join(current_dir, '.env')
    print(f"Looking for .env at: {env_path}")
    print(f".env file exists: {os.path.exists(env_path)}")
    
    if os.path.exists(env_path):
        print("\n=== .env file contents ===")
        with open(env_path, 'r') as f:
            content = f.read()
            print(content)
    
    # Try to load .env
    print("\n=== Loading .env ===")
    result = load_dotenv(env_path)
    print(f"load_dotenv result: {result}")
    
    # Check environment variables
    print("\n=== Environment Variables ===")
    api_key = os.getenv("GOOGLE_API_KEY")
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    enable_tts = os.getenv("ENABLE_TTS")
    
    print(f"GOOGLE_API_KEY: {'Found' if api_key else 'NOT FOUND'}")
    if api_key:
        print(f"  Value: {api_key[:20]}...")  # Show first 20 chars only
    
    print(f"GOOGLE_APPLICATION_CREDENTIALS: {creds_path}")
    print(f"ENABLE_TTS: {enable_tts}")
    
    # Check if google-credentials.json exists
    if creds_path:
        if creds_path.startswith('./'):
            full_creds_path = os.path.join(current_dir, creds_path[2:])
        else:
            full_creds_path = creds_path
            
        print(f"Google credentials file exists: {os.path.exists(full_creds_path)}")
        print(f"Full path: {full_creds_path}")

if __name__ == "__main__":
    test_env_loading()