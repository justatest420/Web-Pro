from flask import Flask, jsonify, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from functools import reduce

app = Flask(__name__)
app.config['FILE_DIRECTORY'] = '/'  # Configure your directory

@app.route('/')
def serve_html():
    return send_from_directory('Web', 'nepal.html') # /.html

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir_structure = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir_structure)
        parent[folders[-1]] = subdir
    return dir_structure

@app.route('/api/files', methods=['GET'])
def directory_structure():
    project_root = os.path.dirname(os.path.abspath(__file__))
    structure = get_directory_structure(project_root)
    return jsonify(structure)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
