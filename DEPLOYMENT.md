# GPS OBD2 Tracker Flask API Deployment Guide

This guide will help you deploy the GPS OBD2 Tracker Flask API to various free hosting platforms.

## Prerequisites

- Python 3.10
- Git
- A free account on one of the hosting platforms below

## Files Created for Deployment

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Process file for Heroku/Railway
- `runtime.txt` - Python version specification
- `wsgi.py` - WSGI entry point
- `.gitignore` - Git ignore file

## Free Hosting Options

### 1. Railway (Recommended)

Railway offers free hosting with Python 3.10 support and easy deployment.

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up
2. Connect your GitHub repository
3. Railway will automatically detect the Python app
4. Deploy!

**Environment Variables (if needed):**
- No environment variables required for basic functionality

### 2. Render

Render provides free hosting with automatic deployments.

**Steps:**
1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub repository
3. Choose "Web Service"
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Python Version:** 3.10

### 3. Heroku (Limited Free Tier)

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

### 4. PythonAnywhere

**Steps:**
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create a free account
3. Upload your files via the web interface
4. Configure a web app with Flask
5. Set the source code directory and WSGI file path

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Test the API
curl "http://localhost:5000/get-device-location?id=9176502935&password=123456"
```

## API Usage

### Endpoints

- `GET /` - API information and usage examples
- `GET /health` - Health check
- `GET /get-device-location?id=<device_id>&password=<password>` - Get device location
- `POST /get-device-location` - Get device location (JSON body with id and password)

### Example Requests

**GET Request:**
```bash
curl "https://your-app-url.com/get-device-location?id=9176502935&password=123456"
```

**POST Request:**
```bash
curl -X POST "https://your-app-url.com/get-device-location" \
  -H "Content-Type: application/json" \
  -d '{"id": "9176502935", "password": "123456"}'
```

### Response Format

```json
{
  "success": true,
  "device_id": "9176502935",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "speed": 25.5,
    "course": 180,
    "is_gps": true,
    "is_stop": false,
    "battery": 85,
    "battery_status": "Normal",
    "position_time": "2024-01-01T12:00:00Z",
    "status": "Online",
    "device_name": "My GPS Tracker",
    "serial_number": "SN123456",
    "vin": "VIN123456789",
    "iccid": "ICCID123456789"
  }
}
```

## Troubleshooting

### Common Issues

1. **Import Errors:** Make sure all dependencies are in `requirements.txt`
2. **Port Issues:** The app uses `$PORT` environment variable for production
3. **Async Issues:** The app uses `asyncio.run()` to handle async operations
4. **Memory Issues:** Free tiers have memory limits; monitor usage

### Logs

Check the hosting platform's logs for debugging:
- Railway: Dashboard → Deployments → View Logs
- Render: Dashboard → Service → Logs
- Heroku: `heroku logs --tail`

## Security Notes

- The API accepts device credentials as parameters
- Consider adding authentication/authorization for production use
- Use HTTPS in production
- Consider rate limiting for public APIs

## Customization

You can modify the Flask app in `app.py` to:
- Add authentication
- Add more endpoints
- Modify response format
- Add caching
- Add logging
