# 🏢 Winwood Business Research Tool

Advanced Business Intelligence & Data Analytics Platform

## 🚀 Features

- **📊 Data Upload & Processing**: Support for CSV and Excel files
- **🤖 AI Chat Interface**: Interactive AI assistant for data insights
- **📈 Quick Visualizations**: Interactive charts and data analysis
- **🗺️ Business Research**: Advanced business intelligence and mapping
- **📧 Email Outreach**: Campaign management and outreach tools

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Cloud Deployment**: Railway-optimized
- **Session Management**: Cloud-based state management

## 🌐 Railway Deployment

### Prerequisites
- Railway account
- GitHub repository (this repo)
- Environment variables configured

### Environment Variables Required
```
GROQ_API_KEY=your_groq_api_key_here
```

### Deployment Steps

1. **Connect to Railway**:
   - Go to [Railway](https://railway.app)
   - Create new project
   - Connect this GitHub repository

2. **Configure Build Settings**:
   - Runtime: Python 3.11+
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - Or use the included `Procfile`

3. **Set Environment Variables**:
   - Add `GROQ_API_KEY` in Railway dashboard
   - Other environment variables as needed

4. **Deploy**:
   - Railway will automatically build and deploy
   - Monitor logs for any issues

### Health Check
The app includes a health check endpoint at `/?health=check`

### Memory Requirements
- Minimum: 512MB RAM
- Recommended: 1GB+ RAM for larger datasets

## 🏗️ Architecture

### Cloud-Optimized Design
- **Session Management**: In-memory storage with automatic cleanup
- **State Management**: Cloud-optimized state persistence
- **File Handling**: Efficient file processing with memory management
- **Auto-Detection**: Automatically detects Railway environment

### Application Structure
```
├── app.py                      # Main application entry point
├── Procfile                    # Railway deployment configuration
├── requirements.txt            # Python dependencies
├── railway_config.py           # Railway-specific configuration
├── cloud_state_management.py   # Cloud session management
├── health_check.py            # Health monitoring
├── controllers.py             # Navigation controllers
├── state_management.py        # Local state (fallback)
├── services/                  # Business logic services
│   ├── cloud_session_manager.py
│   └── __init__.py
├── utils/                     # Utility functions
│   ├── layout.py
│   ├── winwood_styling.py
│   └── __init__.py
└── pages/                     # Application pages
    ├── upload.py
    ├── ai_chat.py
    ├── quick_visualizations.py
    ├── business_research.py
    ├── email_outreach.py
    └── __init__.py
```

## 🎯 Usage

1. **Upload Data**: Start by uploading your business data (CSV/Excel)
2. **AI Chat**: Interact with AI to understand your data
3. **Visualizations**: Explore data with interactive charts
4. **Business Research**: Conduct advanced business intelligence
5. **Email Outreach**: Manage email campaigns and outreach

## 🔧 Development

### Local Development
```bash
# Clone repository
git clone https://github.com/RamForexTrade/winwood-business-research.git
cd winwood-business-research

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Environment Setup
Create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
```

## 📊 Performance

- **Cloud-Optimized**: Designed for Railway's ephemeral storage
- **Memory Efficient**: Smart memory management and cleanup
- **Session Management**: Automatic session cleanup and optimization
- **Scalable**: Handles multiple concurrent users

## 🛡️ Security

- Environment variable protection
- Session isolation
- Automatic cleanup of sensitive data
- Cloud deployment best practices

## 📱 Mobile Support

- Responsive design
- Mobile-friendly interface
- Touch-optimized controls

## 🔄 Updates & Maintenance

- **Automatic Deployment**: Push to main branch triggers deployment
- **Health Monitoring**: Built-in health checks
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed application logging

## 📞 Support

For deployment issues or questions:
- Check Railway deployment logs
- Verify environment variables
- Monitor application health check endpoint

## 📄 License

© 2024 Winwood Technology Solutions. All rights reserved.

---

**Powered by Winwood Technology Solutions**  
*Advanced Business Intelligence & Data Analytics*