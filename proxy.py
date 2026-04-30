from flask import Flask, request, Response
import requests

app = Flask(__name__)

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Odoo-URL'
    return response

@app.after_request
def after_request(response):
    return add_cors(response)

@app.route('/xmlrpc/<path:path>', methods=['POST', 'OPTIONS'])
def proxy(path):
    if request.method == 'OPTIONS':
        return Response('', status=200)

    target = request.headers.get('X-Odoo-URL')
    if not target:
        return Response('Missing X-Odoo-URL header', status=400)

    url = f"{target.rstrip('/')}/xmlrpc/{path}"
    try:
        resp = requests.post(
            url,
            data=request.data,
            headers={'Content-Type': 'text/xml'},
            timeout=30
        )
        return Response(resp.content, status=resp.status_code, content_type='text/xml')
    except Exception as e:
        return Response(str(e), status=500)

@app.route('/')
def index():
    return Response('Odoo XML-RPC Proxy is running ✓', status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
