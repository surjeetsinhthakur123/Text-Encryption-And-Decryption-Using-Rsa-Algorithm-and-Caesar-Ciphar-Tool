from flask import Flask, render_template, request, jsonify, send_file
import os
from math import gcd
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
import base64
import random
from sympy import randprime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file limit

# Encryption alphabet for RSA (custom mapping) 
alphabet_e = {'a': '01', 'b': '02', 'c': '03', 'd': '04', 'e': '05', 'f': '06', 'g': '07', 'h': '08',
              'i': '09', 'j': '10', 'k': '11', 'l': '12', 'm': '13', 'n': '14', 'o': '15', 'p': '16',
              'q': '17', 'r': '18', 's': '19', 't': '20', 'u': '21', 'v': '22', 'w': '23', 'x': '24',
              'y': '25', 'z': '26', 'A': '27', 'B': '28', 'C': '29', 'D': '30', 'E': '31', 'F': '32',
              'G': '33', 'H': '34', 'I': '35', 'J': '36', 'K': '37', 'L': '38', 'M': '39', 'N': '40',
              'O': '41', 'P': '42', 'Q': '43', 'R': '44', 'S': '45', 'T': '46', 'U': '47', 'V': '48',
              'W': '49', 'X': '50', 'Y': '51', 'Z': '52', ' ': '53', '.': '54', ',': '55', '?': '56',
              '!': '57', '@': '58', '#': '59', '$': '60', '%': '61', '^': '62', '&': '63', '*': '64',
              '(': '65', ')': '66', '-': '67', '_': '68', '=': '69', '+': '70', '[': '71', ']': '72',
              '{': '73', '}': '74', '|': '75', '\\': '76', ':': '77', ';': '78', '"': '79', '\'': '80',
              '<': '81', '>': '82', '/': '83', '~': '85', '`': '86', '\n': '87'}

alphabet_d = {v: k for k, v in alphabet_e.items()}

# --- Secure RSA Implementation ---
def generate_large_prime(bits=512):
    """Generate a large prime number using PyCryptodome's method"""
    return RSA.generate(bits, Random.new().read).p

def generate_keys(p, q):
    """Generate RSA keys with proper security"""
    # Validate inputs
    if not isinstance(p, int) or not isinstance(q, int) or p <= 0 or q <= 0:
        raise ValueError("p and q must be positive integers")
    
    # Generate proper RSA key pair
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Use standard exponent 65537
    e = 65537
    
    # Ensure e is coprime with phi
    if gcd(e, phi) != 1:
        raise ValueError("e is not coprime with phi(n). Try different primes.")
    
    # Calculate modular inverse for d
    d = pow(e, -1, phi)
    
    # Return components needed for our operations
    return n, e, d, p, q

def rsa_encrypt(message, public_key):
    """Encrypt using RSA with OAEP padding"""
    e, n = public_key
    key = RSA.construct((n, e))
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    encrypted = cipher.encrypt(message.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def rsa_decrypt(encrypted_message, private_key):
    """Decrypt using RSA with OAEP padding"""
    d, n, p, q = private_key
    key = RSA.construct((n, 65537, d, p, q))
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    encrypted = base64.b64decode(encrypted_message)
    return cipher.decrypt(encrypted).decode('utf-8')

# --- Caesar Cipher Functions (unchanged) ---
def caesar_encrypt(message, shift):
    result = ''
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = chr((ord(char) - base + shift) % 26 + base)
            result += shifted
        else:
            result += char
    return result

def caesar_decrypt(message, shift):
    return caesar_encrypt(message, -shift)

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_keys', methods=['POST'])
def generate_keys_route():
    try:
        p = int(request.form['p'])
        q = int(request.form['q'])
        N, e, d, p_val, q_val = generate_keys(p, q)
        return jsonify({
            'success': True, 
            'N': N, 
            'e': e, 
            'd': d,
            
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    try:
        N = int(request.form['N'])
        e = int(request.form['e'])
        message = request.form['message']
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                message = file.read().decode('utf-8')
        
        encrypted = rsa_encrypt(message, (e, N))
        
        with open('encrypted.txt', 'w') as f:
            f.write(encrypted)
            
        return jsonify({
            'success': True, 
            'encrypted': encrypted, 
            'download_link': '/download/encrypted.txt',
            
        })
    except Exception as ex:
        return jsonify({'success': False, 'error': str(ex)})

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    try:
        N = int(request.form['N'])
        d = int(request.form['d'])
        p = int(request.form.get('p', 0))
        q = int(request.form.get('q', 0))
        message = request.form['message']
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                message = file.read().decode('utf-8')
        
        # We need p and q for proper key construction
        if p == 0 or q == 0:
            raise ValueError("p and q are required for decryption")
        
        decrypted = rsa_decrypt(message, (d, N, p, q))
        
        with open('decrypted.txt', 'w') as f:
            f.write(decrypted)
            
        return jsonify({
            'success': True, 
            'decrypted': decrypted, 
            'download_link': '/download/decrypted.txt',
           
        })
    except Exception as ex:
        return jsonify({'success': False, 'error': str(ex)})

@app.route('/encrypt_caesar', methods=['POST'])
def encrypt_caesar():
    try:
        shift = int(request.form['shift'])
        message = request.form['message']
        
        # No need for file handling logic from the original here
        
        encrypted = caesar_encrypt(message, shift)
        
        # Simply return the result as JSON, no file writing needed
        return jsonify({'success': True, 'encrypted': encrypted})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decrypt_caesar', methods=['POST'])
def decrypt_caesar():
    try:
        shift = int(request.form['shift'])
        message = request.form['message']
        
        decrypted = caesar_decrypt(message, shift)
        
        # Simply return the result as JSON
        return jsonify({'success': True, 'decrypted': decrypted})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/random_prime')
def random_prime():
    # You can adjust the range as needed for your application
    prime = randprime(100, 1000)
    return jsonify({'prime': prime})

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)