# PyCrypt - Secure Encryption API

A secure, password-based file and text encryption/decryption REST API using AES-256, PBKDF2, and HMAC integrity verification. Perfect for integration with React applications and other web frontends.

## 🚀 Quick Start

### Installation
```bash
cd PyCrypt
pip install -r requirements.txt
```

### Start the API Server
```bash
python start_api.py
```

The API will be available at `http://localhost:5000`

### Test the API
```bash
python test_api.py
```

## 🔥 Features

### Security
- **AES-256-CBC encryption** with secure random IV
- **PBKDF2 key derivation** (200,000 iterations) 
- **HMAC-SHA256 verification** for integrity
- **Secure random salt generation**
- **Automatic cleanup** of temporary files
- **Password hints** support

### API Capabilities
- **Text encryption/decryption** via JSON
- **File upload encryption/decryption**
- **File download** (encrypted/decrypted)
- **CORS enabled** for web app integration
- **RESTful endpoints** with proper error handling
- **Base64 encoding** for binary-safe transfers

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/encrypt/text` | Encrypt text content |
| POST | `/api/decrypt/text` | Decrypt text content |
| POST | `/api/encrypt/file` | Encrypt uploaded file |
| POST | `/api/decrypt/file` | Decrypt file content |
| POST | `/api/download/encrypted` | Download encrypted file |
| POST | `/api/download/decrypted` | Download decrypted file |

## 📖 Usage Examples

### React/JavaScript Integration
```javascript
// Encrypt text
const encryptText = async (text, password) => {
  const response = await fetch('http://localhost:5000/api/encrypt/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      password: password,
      hint: 'Optional hint'
    })
  });
  return await response.json();
};

// Decrypt text
const decryptText = async (encryptedContent, password) => {
  const response = await fetch('http://localhost:5000/api/decrypt/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      encrypted_content: encryptedContent,
      password: password
    })
  });
  return await response.json();
};

// File encryption
const encryptFile = async (file, password) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('password', password);
  formData.append('hint', 'File hint');
  
  const response = await fetch('http://localhost:5000/api/encrypt/file', {
    method: 'POST',
    body: formData
  });
  return await response.json();
};
```

### Python Client Example
```python
import requests

# Encrypt text
response = requests.post('http://localhost:5000/api/encrypt/text', json={
    'text': 'Secret message',
    'password': 'my_password',
    'hint': 'Remember this!'
})
result = response.json()

# Decrypt text
response = requests.post('http://localhost:5000/api/decrypt/text', json={
    'encrypted_content': result['encrypted_content'],
    'password': 'my_password'
})
decrypted = response.json()
print(decrypted['decrypted_text'])
```

## 🏗️ Project Structure
```
PyCrypt/
├── api.py              # Main Flask API server
├── start_api.py        # API startup script
├── test_api.py         # API test suite
├── crypto/
│   ├── encryptor.py    # AES encryption logic
│   ├── decryptor.py    # AES decryption logic
│   └── utils.py        # Crypto utilities (salt, IV, HMAC)
├── API_DOCS.md         # Detailed API documentation
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔒 Security Details

### Encryption Process
1. **Random salt generation** (16 bytes)
2. **PBKDF2 key derivation** from password + salt
3. **Random IV generation** (16 bytes) 
4. **AES-256-CBC encryption** of content
5. **HMAC-SHA256 calculation** for integrity
6. **Secure file header** with magic bytes + version

### File Format
```
[MAGIC][VERSION][SALT][IV][HMAC][HINT][ENCRYPTED_DATA]
```

### Why This is Secure
- **No password storage** - passwords are only used for key derivation
- **Salt prevents rainbow tables** - unique salt per encryption
- **IV prevents pattern analysis** - unique IV per encryption  
- **HMAC prevents tampering** - any modification is detected
- **Strong key derivation** - 200k iterations makes brute force costly
- **Memory cleanup** - temporary files are securely wiped

## 🚀 Integration with React

This API is designed to work seamlessly with React applications:

1. **CORS enabled** - no cross-origin issues
2. **JSON responses** - easy to parse in JavaScript
3. **File upload support** - works with HTML file inputs
4. **Base64 encoding** - handles binary data safely
5. **Error handling** - consistent error response format

## 📚 Documentation

- **API_DOCS.md** - Complete endpoint documentation with examples
- **Built-in health check** - `/api/health` for monitoring
- **Comprehensive tests** - Run `python test_api.py` to verify functionality

## 🛠️ Development

### Running Tests
```bash
python test_api.py
```

### Environment
- **Python 3.9+** required
- **16MB max file size** (configurable)
- **Temporary file cleanup** automatic
- **Development mode** with debug logging

## 🎯 Use Cases

- **React web applications** needing client-side encryption
- **Secure file storage** with password protection  
- **API-based encryption services** for multiple frontends
- **Secure data transfer** between applications
- **Privacy-focused applications** requiring strong crypto

Built with security, simplicity, and React integration in mind! 🔐 