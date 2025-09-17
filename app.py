from flask import Flask, request, jsonify
import asyncio
import logging
from obdtracker import api, location

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/get-device-location', methods=['GET', 'POST'])
def get_device_location():
    """
    Get device location endpoint
    Parameters:
    - id: Device ID (required)
    - password: Device password (required)
    """
    try:
        # Get parameters from request
        if request.method == 'GET':
            device_id = request.args.get('id')
            password = request.args.get('password')
        else:  # POST
            data = request.get_json() or {}
            device_id = data.get('id') or request.form.get('id')
            password = data.get('password') or request.form.get('password')
        
        # Validate required parameters
        if not device_id or not password:
            return jsonify({
                'error': 'Missing required parameters',
                'message': 'Both id and password parameters are required'
            }), 400
        
        # Run the async function
        result = asyncio.run(get_location_data(device_id, password))
        
        if result.get('error'):
            return jsonify(result), 500
        
        return jsonify({
            'success': True,
            'device_id': device_id,
            'location': result
        })
        
    except Exception as e:
        logger.error(f"Error getting device location: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

async def get_location_data(device_id, password):
    """
    Async function to get location data from the GPS tracker
    """
    try:
        # Initialize API with the server URL
        ai = api.API("https://en.aika168.com/")
        
        # Login to the device
        await ai.doLogin(device_id, password)
        
        # Get location data
        loc = location.Location(ai)
        await loc.getTracking()
        
        # Extract relevant location information
        location_data = {
            'latitude': getattr(ai, 'lat', None),
            'longitude': getattr(ai, 'lng', None),
            'speed': getattr(ai, 'speed', None),
            'course': getattr(ai, 'course', None),
            'is_gps': getattr(ai, 'isGPS', None),
            'is_stop': getattr(ai, 'isStop', None),
            'battery': getattr(ai, 'battery', None),
            'battery_status': getattr(ai, 'batteryStatus', None),
            'position_time': getattr(ai, 'positionTime', None),
            'status': getattr(ai, 'status', None),
            'device_name': getattr(ai, 'deviceName', None),
            'serial_number': getattr(ai, 'serialNumber', None),
            'vin': getattr(ai, 'VIN', None),
            'iccid': getattr(ai, 'ICCID', None)
        }
        
        return location_data
        
    except Exception as e:
        logger.error(f"Error in get_location_data: {str(e)}")
        return {'error': str(e)}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'GPS OBD2 Tracker API'
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'service': 'GPS OBD2 Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'GET /get-device-location': 'Get device location (parameters: id, password)',
            'POST /get-device-location': 'Get device location (JSON body: {id, password})',
            'GET /health': 'Health check',
            'GET /': 'This information'
        },
        'example_usage': {
            'GET': '/get-device-location?id=9176502935&password=123456',
            'POST': '/get-device-location with JSON body {"id": "9176502935", "password": "123456"}'
        }
    })

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=5000, debug=True)
