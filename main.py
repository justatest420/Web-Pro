from flask import Flask, jsonify, request, send_from_directory
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['FILE_DIRECTORY'] = '/'  # Configure your directory

@app.route('/')
def serve_html():
    return send_from_directory('HTML', 'nepal.html') # /.html

@app.route('/api/files', methods=['GET'])
def list_files():
    try:
        # Optional query parameters
        file_type = request.args.get('type', None)
        sort_by = request.args.get('sort', 'name')
        
        files = []
        for item in os.listdir(app.config['FILE_DIRECTORY']):
            item_path = os.path.join(app.config['FILE_DIRECTORY'], item)
            
            if os.path.isfile(item_path):
                # Skip if file type filter doesn't match
                if file_type and not item.lower().endswith(file_type.lower()):
                    continue
                    
                files.append({
                    'name': item,
                    'size': os.path.getsize(item_path),
                    'modified': os.path.getmtime(item_path),
                    'type': os.path.splitext(item)[1][1:].lower() or 'unknown'
                })
        
        # Sort results
        reverse_sort = sort_by.startswith('-')
        sort_key = sort_by.lstrip('-')
        files.sort(key=lambda x: x.get(sort_key, ''), reverse=reverse_sort)
        
        return jsonify({
            'path': app.config['FILE_DIRECTORY'],
            'count': len(files),
            'files': files
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
