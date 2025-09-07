#!/usr/bin/env python3
"""
Startup script for Summarify AI
"""

import uvicorn
import sys
import os
from config import HOST, PORT

def main():
    """Main entry point"""
    print("🚀 Starting Summarify AI...")
    print(f"📡 Server will be available at: http://{HOST}:{PORT}")
    print(f"📊 Dashboard: http://{HOST}:{PORT}")
    print(f"🔧 API docs: http://{HOST}:{PORT}/docs")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=HOST,
            port=PORT,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Summarify AI...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
