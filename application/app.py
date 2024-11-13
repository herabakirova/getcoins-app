from flask import Flask, jsonify, redirect, url_for
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def home():
    html = """
    <h1>Welcome to the Crypto Price Service</h1>
    <p>Use the links below to fetch the current prices:</p>
    <ul>
        <li><a href="/bitcoin">Bitcoin Price</a></li>
        <li><a href="/ethereum">Ethereum Price</a></li>
    </ul>
    """
    return html, 200

@app.route('/bitcoin', methods=['GET'])
def get_bitcoin_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        response.raise_for_status()
        data = response.json()
        logging.info("Fetched Bitcoin data successfully")
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Bitcoin data: {e}")
        return jsonify({'error': 'Could not fetch Bitcoin data'}), 500

@app.route('/ethereum', methods=['GET'])
def get_ethereum_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        response.raise_for_status()
        data = response.json()
        logging.info("Fetched Ethereum data successfully")
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Ethereum data: {e}")
        return jsonify({'error': 'Could not fetch Ethereum data'}), 500

@app.route('/ready')
def ready():
    return 'Ready', 200

@app.route('/healthz')
def healthz():
    return 'Healthy', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
