#!/usr/bin/env python3
"""
PyCrypt API Startup Script

Simple script to start the PyCrypt Flask API server with proper configuration.
"""

import os
import sys
from api import app

def main():
    """Start the PyCrypt API server"""
    print("🔐 Starting PyCrypt API Server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("📖 API Documentation: Check API_DOCS.md for endpoint details")
    print("🔄 CORS enabled for React app integration")
    print("💾 Max file size: 16MB")
    print()
    print("Available endpoints:")
    print("  GET  /api/health           - Health check")
    print("  POST /api/encrypt/text     - Encrypt text")
    print("  POST /api/decrypt/text     - Decrypt text") 
    print("  POST /api/encrypt/file     - Encrypt file")
    print("  POST /api/decrypt/file     - Decrypt file")
    print("  POST /api/download/encrypted - Download encrypted file")
    print("  POST /api/download/decrypted - Download decrypted file")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 