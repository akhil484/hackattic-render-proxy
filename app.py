from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/presence', methods=['POST'])
def make_presence_request():
    try:
        data = request.get_json()
        if not data or 'presence_token' not in data:
            return jsonify({
                'success': False,
                'error': 'presence_token is required',
                'region': 'render-com'
            }), 400
            
        presence_token = data['presence_token']
        
        # Make request to hackattic from Render's servers
        hackattic_url = f'https://hackattic.com/_/presence/{presence_token}'
        response = requests.get(hackattic_url, timeout=20)
        
        return jsonify({
            'success': True,
            'countries': response.text.strip(),
            'region': 'render-com',
            'status_code': response.status_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'region': 'render-com'
        }), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'message': 'Hackattic Render Proxy',
        'status': 'running',
        'endpoints': ['/presence (POST)']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
