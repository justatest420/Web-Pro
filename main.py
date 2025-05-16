from flask import Flask, jsonify, request, send_from_directory, Blueprint
import os

app = Flask(__name__, static_folder='Web', static_url_path='')

webs = Blueprint('webs', __name__, static_folder='Web', static_url_path='/Web')
app.register_blueprint(webs)

images = Blueprint('images', __name__, static_folder='Images', static_url_path='/Images')
app.register_blueprint(images)


@app.route('/')
def serve_html():
    return send_from_directory('Web', 'nepal.html') # /.html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
