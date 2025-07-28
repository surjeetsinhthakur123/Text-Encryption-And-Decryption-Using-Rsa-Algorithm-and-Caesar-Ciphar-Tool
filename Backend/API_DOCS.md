# PyCrypt Flask API Documentation

A REST API for secure file and text encryption/decryption using AES encryption with PBKDF2 key derivation and HMAC verification.

## Getting Started

### Installation
```bash
cd PyCrypt
pip install -r requirements.txt
```

### Running the Server
```bash
python api.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
**GET** `/api/health`

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "PyCrypt API",
  "version": "1.0.0"
}
```

### Text Encryption
**POST** `/api/encrypt/text`

Encrypt text content with a password.

**Request Body (JSON):**
```json
{
  "text": "Your secret message here",
  "password": "your_strong_password",
  "hint": "Optional password hint"
}
```

**Response:**
```json
{
  "success": true,
  "encrypted_content": "base64_encoded_encrypted_data",
  "hint": "Optional password hint"
}
```

### Text Decryption
**POST** `/api/decrypt/text`

Decrypt text content with a password.

**Request Body (JSON):**
```json
{
  "encrypted_content": "base64_encoded_encrypted_data",
  "password": "your_strong_password"
}
```

**Response:**
```json
{
  "success": true,
  "decrypted_text": "Your secret message here"
}
```

### File Encryption
**POST** `/api/encrypt/file`

Encrypt an uploaded file with a password.

**Request (multipart/form-data):**
- `file`: The file to encrypt
- `password`: Encryption password
- `hint`: Optional password hint

**Response:**
```json
{
  "success": true,
  "filename": "original_filename.txt",
  "encrypted_content": "base64_encoded_encrypted_data",
  "hint": "Optional password hint"
}
```

### File Decryption
**POST** `/api/decrypt/file`

Decrypt file content with a password.

**Request Body (JSON):**
```json
{
  "encrypted_content": "base64_encoded_encrypted_data",
  "password": "your_strong_password",
  "filename": "original_filename.txt"
}
```

**Response:**
```json
{
  "success": true,
  "filename": "original_filename.txt",
  "decrypted_content": "base64_encoded_decrypted_data"
}
```

### Download Encrypted File
**POST** `/api/download/encrypted`

Download encrypted content as a file.

**Request Body (JSON):**
```json
{
  "encrypted_content": "base64_encoded_encrypted_data",
  "filename": "encrypted_file.enc"
}
```

**Response:** File download

### Download Decrypted File
**POST** `/api/download/decrypted`

Download decrypted content as a file.

**Request Body (JSON):**
```json
{
  "decrypted_content": "base64_encoded_decrypted_data",
  "filename": "decrypted_file.txt"
}
```

**Response:** File download

## Usage Examples

### React/JavaScript Example

```javascript
// Encrypt text
const encryptText = async (text, password) => {
  const response = await fetch('http://localhost:5000/api/encrypt/text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
      password: password,
      hint: 'My secret hint'
    })
  });
  
  const result = await response.json();
  return result;
};

// Decrypt text
const decryptText = async (encryptedContent, password) => {
  const response = await fetch('http://localhost:5000/api/decrypt/text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      encrypted_content: encryptedContent,
      password: password
    })
  });
  
  const result = await response.json();
  return result;
};

// Encrypt file
const encryptFile = async (file, password) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('password', password);
  formData.append('hint', 'File encryption hint');
  
  const response = await fetch('http://localhost:5000/api/encrypt/file', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  return result;
};
```

### Python Example

```python
import requests
import base64

# Encrypt text
def encrypt_text(text, password):
    response = requests.post('http://localhost:5000/api/encrypt/text', json={
        'text': text,
        'password': password,
        'hint': 'My secret hint'
    })
    return response.json()

# Decrypt text
def decrypt_text(encrypted_content, password):
    response = requests.post('http://localhost:5000/api/decrypt/text', json={
        'encrypted_content': encrypted_content,
        'password': password
    })
    return response.json()

# Example usage
result = encrypt_text("Hello, World!", "my_password")
print(f"Encrypted: {result['encrypted_content']}")

decrypted = decrypt_text(result['encrypted_content'], "my_password")
print(f"Decrypted: {decrypted['decrypted_text']}")
```

## Security Features

- **AES-256 encryption** in CBC mode
- **PBKDF2** key derivation with 200,000 iterations
- **HMAC-SHA256** for integrity verification
- **Secure random salt and IV** generation
- **Automatic cleanup** of temporary files
- **Password-based encryption** with optional hints

## Error Handling

All endpoints return JSON responses with error information when something goes wrong:

```json
{
  "error": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing required fields)
- `500`: Internal Server Error

## CORS Support

The API includes CORS support for cross-origin requests, making it easy to integrate with React applications running on different ports. 