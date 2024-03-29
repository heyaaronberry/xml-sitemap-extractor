from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS  # Import CORS from flask_cors module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

def extract_urls_from_sitemap(sitemap_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(sitemap_url, headers=headers, timeout=60)
    soup = BeautifulSoup(response.content, 'xml')
    urls = []
    for loc in soup.find_all('loc'):
        urls.append(loc.text)
    return urls

@app.route('/extract-sitemap', methods=['GET'])
def extract_sitemap():
    sitemap_url = request.args.get('url')

    if not sitemap_url:
        return jsonify({'error': 'No sitemap URL provided'}), 400

    try:
        urls = extract_urls_from_sitemap(sitemap_url)
        return jsonify({'urls': urls}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
