import tkinter as tk
from tkinter import messagebox, filedialog

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

# Euclidean Algorithm: Find GCD of two numbers
def gcd(a, b):
    if b == 0:
        return abs(a)
    else:
        return gcd(b, a % b)

# Generate encryption keys, e, and d for RSA
def generate_keys(p, q):
    n = p * q
    N0 = (p - 1) * (q - 1)
    for i in range(2, N0):
        if gcd(i, N0) == 1:
            e = i
            break
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

# Function to generate keys and show them in a dialog box
def generate_keys_dialog():
    p = int(p_entry.get())
    q = int(q_entry.get())
    try:
        N, e, d = generate_keys(p, q)
        key_info = f"Public key:\nN: {N}\ne: {e}\n\nPrivate key:\nN: {N}\nd: {d}"
        messagebox.showinfo("Key Pair Generated", key_info)
    except:
        messagebox.showerror("Error", "Invalid Primes")

# Function to encrypt a message from a file using RSA
def encrypt_file_dialog():
    N = int(N_entry.get())
    e = int(e_entry.get())
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    try:
        with open(file_path, "r") as file:
            message = file.read()
            encrypted_message = encrypt_message(message, N, e)
            with open("encrypted.txt", "w") as encrypted_file:
                encrypted_file.write(encrypted_message)
        messagebox.showinfo("Encryption Successful", "File encrypted successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")

# Function to decrypt a message from a file using RSA
def decrypt_file_dialog():
    N = int(N_entry.get())
    d = int(d_entry.get())
    file_path = filedialog.askopenfilename(title="Select File to Decrypt")
    try:
        with open(file_path, "r") as file:
            message = file.read()
            decrypted_message = decrypt_message(message, N, d)
            with open("decrypted.txt", "w") as decrypted_file:
                decrypted_file.write(decrypted_message)
        messagebox.showinfo("Decryption Successful", "File decrypted successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")

# Create the main application window
root = tk.Tk()
root.title("RSA Encryption/Decryption")

# Labels
p_label = tk.Label(root, text="Enter the first prime number:")
p_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

q_label = tk.Label(root, text="Enter the second prime number:")
q_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

N_label = tk.Label(root, text="Enter key N:")
N_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

e_label = tk.Label(root, text="Enter key e:")
e_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

d_label = tk.Label(root, text="Enter key d:")
d_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

# Entry fields
p_entry = tk.Entry(root)
p_entry.grid(row=0, column=1, padx=5, pady=5)

q_entry = tk.Entry(root)
q_entry.grid(row=1, column=1, padx=5, pady=5)

N_entry = tk.Entry(root)
N_entry.grid(row=2, column=1, padx=5, pady=5)

e_entry = tk.Entry(root)
e_entry.grid(row=3, column=1, padx=5, pady=5)

d_entry = tk.Entry(root)
d_entry.grid(row=4, column=1, padx=5, pady=5)

# Buttons
generate_keys_button = tk.Button(root, text="Generate Keys", command=generate_keys_dialog)
generate_keys_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

encrypt_file_button = tk.Button(root, text="Encrypt File", command=encrypt_file_dialog)
encrypt_file_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

decrypt_file_button = tk.Button(root, text="Decrypt File", command=decrypt_file_dialog)
decrypt_file_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Run the application
root.mainloop()
