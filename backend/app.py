from flask import Flask, request, jsonify, redirect, render_template
from database import DB
from models import ShortenedURL
import validators
from config import SECRET_KEY, BASE_URL

app = Flask(__name__)
app.secret_key = SECRET_KEY
db = DB()

@app.route('/')
def home():
    return render_template('index.html', base_url=BASE_URL)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    custom_code = data.get('custom_code')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    if not validators.url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    if custom_code:
        if db.get_url_by_short_code(custom_code):
            return jsonify({'error': 'Custom code already in use'}), 400
        short_code = custom_code
    else:
        short_code = db.generate_unique_short_code(original_url)

    shortened_url = ShortenedURL(
        short_code=short_code,
        original_url=original_url
    )
    db.save_url(shortened_url)

    return jsonify({
        'short_url': f"{BASE_URL}/{short_code}",
        'original_url': original_url,
        'short_code': short_code
    })

@app.route('/<short_code>')
def redirect_to_original(short_code):
    url = db.get_url_by_short_code(short_code)
    if not url:
        return jsonify({'error': 'URL not found'}), 404

    db.increment_click_count(short_code)
    return redirect(url.original_url)

@app.route('/info/<short_code>')
def get_url_info(short_code):
    url = db.get_url_by_short_code(short_code)
    if not url:
        return jsonify({'error': 'URL not found'}), 404

    return jsonify({
        'short_url': f"{BASE_URL}/{short_code}",
        'original_url': url.original_url,
        'click_count': url.click_count,
        'created_at': url.created_at.isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
