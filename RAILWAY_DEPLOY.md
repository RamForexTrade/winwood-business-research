# Railway Deployment Configuration

## Environment Variables Required
GROQ_API_KEY=your_groq_api_key_here

## Railway Build Settings
# Runtime: Python 3.11
# Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0

## Health Check Endpoint
# The app includes a health check at /?health=check

## Memory Requirements
# Recommended: 1GB RAM minimum for data processing
# 2GB+ recommended for large datasets

## Features
- Auto-detects Railway environment
- Cloud-optimized session management  
- Production logging enabled
- Automatic HTTPS support