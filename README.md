# 🔐 Text Encryption & Decryption Web App

A Flask-based web application that allows users to **encrypt and decrypt text** using two well-known cryptographic techniques: **RSA Algorithm** and **Caesar Cipher**. This app is designed for educational purposes to demonstrate both symmetric and asymmetric encryption in a beginner-friendly interface.

---

## 🌟 Features

- 🧠 Implements **RSA (Asymmetric Encryption)**
- 🔁 Supports **Caesar Cipher (Symmetric Encryption)**
- 🌐 Clean **web interface** using Flask & HTML templates
- 🧪 Encrypt and decrypt both messages and characters
- 📦 Easy to run locally (no database required)

---

## 🔐 Algorithms Overview

### ✅ RSA Algorithm

RSA is an **asymmetric cryptographic algorithm**, meaning it uses a **public key** for encryption and a **private key** for decryption.

#### How it works:

1. Select two prime numbers `P = 53` and `Q = 59`
2. Compute `n = P * Q = 3127`
3. Compute φ(n) = (P - 1)(Q - 1) = 3016
4. Choose a public exponent `e = 3` such that `1 < e < φ(n)` and `e` is coprime to φ(n)
5. Compute private key `d` such that `d = (k * φ(n) + 1) / e`, for some integer `k`

**Example:**
- Plaintext: "HI" → 8 9
- Encrypted: `c = (89^3) % 3127 = 1394`
- Decrypted: `p = (1394^2011) % 3127 = 89` → "HI"

---

### ✅ Caesar Cipher

A **substitution cipher** that shifts each letter by a fixed number (`shift`) in the alphabet.

#### Example:
- Plaintext: `HELLO`
- Shift: `3`
- Encrypted: `KHOOR`
- Decrypted: `HELLO` (by shifting back)

---


## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.x
- Flask

### 📦 Installation

```bash
git clone https://github.com/surjeetsinhthakur123/Text-Encryption-And-Decryption-Using-Rsa-Algorithm-and-Caesar-Ciphar-Tool.git
cd Text-Encryption-And-Decryption-Using-Rsa-Algorithm-and-Caesar-Ciphar-Tool
pip install flask
```

Run the app:
```bash
python app.py
```

Then visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📸 Screenshots

> ![image](https://github.com/user-attachments/assets/098f6c3c-e280-4dab-afae-d0e4d7e37385)


---

## 💡 Use Cases

- Learn and visualize basic cryptographic methods  
- Understand the difference between symmetric & asymmetric encryption  
- Educational tool for Python + Flask + Cryptography

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository  
2. **Create a new branch**  
3. **Make your changes**  
4. **Submit a pull request**

---

## 👥 Contributors

Thanks to these amazing people for their contributions:

| Name               | GitHub Profile                                                 |
|--------------------|----------------------------------------------------------------|
| Surjeet Sinh Thakur | [@surjeetsinhthakur123](https://github.com/surjeetsinhthakur123) |
| Mili Parashar       | [@m1ss-chief](https://github.com/m1ss-chief) (Contributor) |

> *Feel free to add your name here via a pull request if you contribute!*

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙋 Author

**Surjeet Sinh Thakur**  
🔗 [GitHub Profile](https://github.com/surjeetsinhthakur123)

