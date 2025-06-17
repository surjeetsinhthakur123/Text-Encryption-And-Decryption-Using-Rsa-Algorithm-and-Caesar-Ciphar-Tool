# app.py
from flask import Flask, render_template, request, jsonify, send_file, flash
import os
from math import gcd

app = Flask(__name__)

# Encryption alphabet for Caesar cipher
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
              '<': '81', '>': '82', '/': '83', '?': '84', '~': '85', '`': '86', '\n': '87'}

# Decryption alphabet for Caesar cipher
alphabet_d = {n: c for c, n in alphabet_e.items()}

# Generate encryption keys, e, and d for RSA
def generate_keys(p, q):
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both p and q must be prime numbers.")
        
    n = p * q
    N0 = (p - 1) * (q - 1)
    for i in range(2, N0):
        if gcd(i, N0) == 1:
            e = i
            break
    if e is None:
        raise ValueError("No valid public exponent 'e' found for the given primes. Try larger primes.")

    for i in range(0, N0):
        if ((e * i) % N0) == 1:
            d = i
            break
    
    return n, e, d

# Encrypt character using RSA
def encrypt(char, N, e):
    return str((int(char) ** e) % N).zfill(2)

# Decrypt character using RSA
def decrypt(char, N, d):
    return str((int(char) ** d) % N).zfill(2)

# Encrypt message using RSA
def encrypt_message(msg, N, e):
    encrypted = []
    for char in msg:
        if char in alphabet_e:
            encrypted_char = encrypt(alphabet_e[char], N, e)
            encrypted.append(encrypted_char)
        else:
            encrypted.append(char)
    return ' '.join(encrypted)

def decrypt_message(msg, N, d):
    decrypted = []
    i = 0
    while i < len(msg):
        if msg[i:i+2].isdigit():
            decrypted_char = decrypt(msg[i:i+2], N, d)
            decrypted.append(decrypted_char)
            i += 2
        else:
            if msg[i] == ' ':
                i += 1
                continue
            decrypted.append(msg[i])
            i += 1
    
    decrypted_text = ''
    for char in decrypted:
        if char.isdigit():
            decrypted_text += alphabet_d[char]
        else:
            decrypted_text += char
    
    return decrypted_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_keys', methods=['POST'])
def generate_keys_route():
    try:
        p = int(request.form['p'])
        q = int(request.form['q'])
        N, e, d = generate_keys(p, q)
        return jsonify({
            'success': True,
            'N': N,
            'e': e,
            'd': d
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

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
        
        encrypted = encrypt_message(message, N, e)
        
        # Save to a temporary file
        with open('encrypted.txt', 'w') as f:
            f.write(encrypted)
        
        return jsonify({
            'success': True,
            'encrypted': encrypted,
            'download_link': '/download/encrypted.txt'
        })
    except Exception as ex:
        return jsonify({
            'success': False,
            'error': str(ex)
        })

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    try:
        N = int(request.form['N'])
        d = int(request.form['d'])
        message = request.form['message']
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                message = file.read().decode('utf-8')
        
        decrypted = decrypt_message(message, N, d)
        
        # Save to a temporary file
        with open('decrypted.txt', 'w') as f:
            f.write(decrypted)
        
        return jsonify({
            'success': True,
            'decrypted': decrypted,
            'download_link': '/download/decrypted.txt'
        })
    except Exception as ex:
        return jsonify({
            'success': False,
            'error': str(ex)
        })

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
