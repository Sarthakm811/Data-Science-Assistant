#!/usr/bin/env python
"""
Start the Streamlit application on localhost:8501
"""
import subprocess
import sys
import os
import webbrowser
import time

def run_streamlit():
    """Start the Streamlit application"""
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=" * 80)
    print("🚀 Starting AI Data Science Research Assistant")
    print("=" * 80)
    print()
    print("📊 Project: Data Science Assistant with AI")
    print("🔗 Server: http://localhost:8501")
    print("📁 Location:", project_dir)
    print()
    print("To stop the server: Press Ctrl+C")
    print()
    print("=" * 80)
    print()
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:8501")
            print("✅ Browser opened automatically")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("   Please open http://localhost:8501 manually")
    
    # Start browser opener in background
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run Streamlit
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_enhanced.py"],
            cwd=project_dir
        )
    except KeyboardInterrupt:
        print("\n✅ Application stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_streamlit()
