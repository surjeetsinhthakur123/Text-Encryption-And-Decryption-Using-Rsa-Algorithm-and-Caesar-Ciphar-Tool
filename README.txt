***RSA algorithm is an asymmetric cryptography algorithm. Asymmetric actually means that it works on two different keys i.e. Public Key and Private Key. As the name describes that the Public Key is given to everyone and the Private key is kept private.

-An example of asymmetric cryptography: 

A client (for example browser) sends its public key to the server and requests some data.
The server encrypts the data using the client’s public key and sends the encrypted data.
The client receives this data and decrypts it.
Since this is asymmetric, nobody else except the browser can decrypt the data even if a third party has the public key of the browser.

The idea! The idea of RSA is based on the fact that it is difficult to factorize a large integer. The public key consists of two numbers where one number is a multiplication of two large prime numbers. And private key is also derived from the same two prime numbers. So if somebody can factorize the large number, the private key is compromised. Therefore encryption strength totally lies on the key size and if we double or triple the key size, the strength of encryption increases exponentially. RSA keys can be typically 1024 or 2048 bits long, but experts believe that 1024-bit keys could be broken in the near future. But till now it seems to be an infeasible task.

Let us learn the mechanism behind the RSA algorithm : >> Generating Public Key: 

Select two prime no's. Suppose P = 53 and Q = 59.
Now First part of the Public key  : n = P*Q = 3127.
 We also need a small exponent say e : 
But e Must be 
An integer.
Not be a factor of F(n). 
1 < e < F(n) [F(n) is discussed below], 
Let us now consider it to be equal to 3.
    Our Public Key is made of n and e

>> Generating Private Key: 

We need to calculate F(n) :
Such that F(n) = (P-1)(Q-1)     
      so,  F(n) = 3016
    Now calculate Private Key, d : 
d = (k*F(n) + 1) / e for some integer k
For k = 2, value of d is 2011.


Now we are ready with our – Public Key ( n = 3127 and e = 3) and Private Key(d = 2011) Now we will encrypt “HI”:


Convert letters to numbers : H  = 8 and I = 9
    Thus Encrypted Data c = (89e)mod n 
Thus our Encrypted Data comes out to be 1394
Now we will decrypt 1394 : 
    Decrypted Data = (cd)mod n
Thus our Encrypted Data comes out to be 89
8 = H and I = 9 i.e. "HI"


***Caesar Cipher in Cryptography

The Caesar cipher is a simple encryption technique that was used by Julius Caesar to send secret messages to his allies. It works by shifting the letters in the plaintext message by a certain number of positions, known as the “shift” or “key”.
The Caesar Cipher technique is one of the earliest and simplest methods of encryption technique. It’s simply a type of substitution cipher, i.e., each letter of a given text is replaced by a letter with a fixed number of positions down the alphabet. For example with a shift of 1, A would be replaced by B, B would become C, and so on. The method is apparently named after Julius Caesar, who apparently used it to communicate with his officials.
Thus to cipher a given text we need an integer value, known as a shift which indicates the number of positions each letter of the text has been moved down. 
The encryption can be represented using modular arithmetic by first transforming the letters into numbers, according to the scheme, A = 0, B = 1,…, Z = 25. Encryption of a letter by a shift n can be described mathematically as. 
For example, if the shift is 3, then the letter A would be replaced by the letter D, B would become E, C would become F, and so on. The alphabet is wrapped around so that after Z, it starts back at A.
Here is an example of how to use the Caesar cipher to encrypt the message “HELLO” with a shift of 3:
Write down the plaintext message: HELLO
Choose a shift value. In this case, we will use a shift of 3.
Replace each letter in the plaintext message with the letter that is three positions to the right in the alphabet.
         H becomes K (shift 3 from H)

         E becomes H (shift 3 from E)

         L becomes O (shift 3 from L)

         L becomes O (shift 3 from L)

         O becomes R (shift 3 from O)

      4.The encrypted message is now “KHOOR”.

To decrypt the message, you simply need to shift each letter back by the same number of positions. In this case, you would shift each letter in “KHOOR” back by 3 positions to get the original message, “HELLO”.
 