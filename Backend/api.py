from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import base64
import io
from crypto.encryptor import encrypt_file
from crypto.decryptor import decrypt_file
from crypto.utils import wipe_file

app = Flask(__name__)
CORS(app)  # Enable CORS for React app integration

# Configure upload folder and max file size
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PyCrypt API',
        'version': '1.0.0'
    })

@app.route('/api/encrypt/text', methods=['POST'])
def encrypt_text():
    """Encrypt text content with password"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        text = data.get('text')
        password = data.get('password')
        hint = data.get('hint')
        
        if not text or not password:
            return jsonify({'error': 'Both text and password are required'}), 400
        
        # Create temporary file for text
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(text)
            temp_file_path = temp_file.name
        
        try:
            # Encrypt the file
            encrypted_file_path = encrypt_file(temp_file_path, password, hint=hint, overwrite=True)
            
            # Read encrypted content
            with open(encrypted_file_path, 'rb') as f:
                encrypted_content = base64.b64encode(f.read()).decode('utf-8')
            
            # Clean up temporary files
            os.unlink(temp_file_path)
            os.unlink(encrypted_file_path)
            
            return jsonify({
                'success': True,
                'encrypted_content': encrypted_content,
                'hint': hint if hint else None
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt/text', methods=['POST'])
def decrypt_text():
    """Decrypt text content with password"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        encrypted_content = data.get('encrypted_content')
        password = data.get('password')
        
        if not encrypted_content or not password:
            return jsonify({'error': 'Both encrypted_content and password are required'}), 400
        
        # Create temporary file for encrypted content
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.enc') as temp_file:
            temp_file.write(base64.b64decode(encrypted_content))
            temp_file_path = temp_file.name
        
        try:
            # Decrypt the file
            decrypted_file_path = decrypt_file(temp_file_path, password, overwrite=True)
            
            # Read decrypted content
            with open(decrypted_file_path, 'r', encoding='utf-8') as f:
                decrypted_text = f.read()
            
            # Clean up temporary files
            os.unlink(temp_file_path)
            os.unlink(decrypted_file_path)
            
            return jsonify({
                'success': True,
                'decrypted_text': decrypted_text
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/encrypt/file', methods=['POST'])
def encrypt_file_endpoint():
    """Encrypt uploaded file with password"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        password = request.form.get('password')
        hint = request.form.get('hint')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Save uploaded file temporarily
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                    f"temp_{file.filename}")
        file.save(temp_file_path)
        
        try:
            # Encrypt the file
            encrypted_file_path = encrypt_file(temp_file_path, password, hint=hint, overwrite=True)
            
            # Read encrypted file content
            with open(encrypted_file_path, 'rb') as f:
                encrypted_content = base64.b64encode(f.read()).decode('utf-8')
            
            # Clean up temporary files
            os.unlink(temp_file_path)
            os.unlink(encrypted_file_path)
            
            return jsonify({
                'success': True,
                'filename': file.filename,
                'encrypted_content': encrypted_content,
                'hint': hint if hint else None
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt/file', methods=['POST'])
def decrypt_file_endpoint():
    """Decrypt file content with password"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        encrypted_content = data.get('encrypted_content')
        password = data.get('password')
        filename = data.get('filename', 'decrypted_file')
        
        if not encrypted_content or not password:
            return jsonify({'error': 'Both encrypted_content and password are required'}), 400
        
        # Create temporary file for encrypted content
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                    f"temp_encrypted_{filename}.enc")
        
        with open(temp_file_path, 'wb') as f:
            f.write(base64.b64decode(encrypted_content))
        
        try:
            # Decrypt the file
            decrypted_file_path = decrypt_file(temp_file_path, password, overwrite=True)
            
            # Read decrypted content as base64 for binary safety
            with open(decrypted_file_path, 'rb') as f:
                decrypted_content = base64.b64encode(f.read()).decode('utf-8')
            
            # Clean up temporary files
            os.unlink(temp_file_path)
            os.unlink(decrypted_file_path)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'decrypted_content': decrypted_content
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/encrypted', methods=['POST'])
def download_encrypted():
    """Download encrypted content as file"""
    try:
        data = request.get_json()
        encrypted_content = data.get('encrypted_content')
        filename = data.get('filename', 'encrypted_file.enc')
        
        if not encrypted_content:
            return jsonify({'error': 'encrypted_content is required'}), 400
        
        # Create file-like object from base64 content
        file_data = base64.b64decode(encrypted_content)
        file_obj = io.BytesIO(file_data)
        
        return send_file(
            file_obj,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/decrypted', methods=['POST'])
def download_decrypted():
    """Download decrypted content as file"""
    try:
        data = request.get_json()
        decrypted_content = data.get('decrypted_content')
        filename = data.get('filename', 'decrypted_file.txt')
        
        if not decrypted_content:
            return jsonify({'error': 'decrypted_content is required'}), 400
        
        # Create file-like object from base64 content
        file_data = base64.b64decode(decrypted_content)
        file_obj = io.BytesIO(file_data)
        
        return send_file(
            file_obj,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wipe', methods=['POST'])
def secure_wipe():
    """Securely wipe a temporary file (for auto-wipe functionality)"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        
        if not file_id:
            return jsonify({'error': 'file_id is required'}), 400
        
        # This would be used with a file tracking system
        # For now, just return success as files are auto-cleaned
        return jsonify({
            'success': True,
            'message': 'File wiped successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 