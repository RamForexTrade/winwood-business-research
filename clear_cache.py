"""
Cache Clearing Utility
=====================
Utility script to clear Streamlit cache and reset session state.
"""

import streamlit as st
import os
import shutil
import sys

def clear_streamlit_cache():
    """Clear Streamlit cache directories."""
    try:
        # Get Streamlit cache directory
        cache_dir = st.cache_data.clear()
        st.cache_resource.clear()
        print("✅ Streamlit cache cleared")
        return True
    except Exception as e:
        print(f"❌ Error clearing Streamlit cache: {e}")
        return False

def clear_temp_files():
    """Clear temporary files created by the application."""
    try:
        temp_dir = "temp_files"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"✅ Temporary files cleared: {temp_dir}")
        else:
            print(f"ℹ️ No temporary files found: {temp_dir}")
        return True
    except Exception as e:
        print(f"❌ Error clearing temporary files: {e}")
        return False

def clear_session_state():
    """Clear session state if running in Streamlit."""
    try:
        if 'streamlit' in sys.modules:
            # Clear all session state keys
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            print("✅ Session state cleared")
        else:
            print("ℹ️ Not running in Streamlit, session state not applicable")
        return True
    except Exception as e:
        print(f"❌ Error clearing session state: {e}")
        return False

def main():
    """Main cache clearing function."""
    print("🧹 Starting cache clearing process...")
    
    success_count = 0
    
    if clear_streamlit_cache():
        success_count += 1
    
    if clear_temp_files():
        success_count += 1
    
    if clear_session_state():
        success_count += 1
    
    print(f"\n🎯 Cache clearing completed: {success_count}/3 operations successful")
    
    if success_count == 3:
        print("✨ All caches cleared successfully!")
    else:
        print("⚠️ Some operations failed. Check the errors above.")

if __name__ == "__main__":
    main()
