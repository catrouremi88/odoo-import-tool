from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/xmlrpc/<path:path>', methods=['POST', 'OPTIONS'])
def proxy(path):
    target = request.headers.get('X-Odoo-URL')
    if not target:
        return {'error': 'Missing X-Odoo-URL header'}, 400

    url = f"{target.rstrip('/')}/xmlrpc/{path}"
    resp = requests.post(url, data=request.data,
                         headers={'Content-Type': 'text/xml'}, timeout=30)
    return Response(resp.content, status=resp.status_code,
                    content_type='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
