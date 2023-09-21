import rsa

#this file is trying things out not to submit.
#A requirements.txt file (if you installed any packages using PIP)
#(to install rsa in command prompt) pip install rsa
# Using rsa https://www.geeksforgeeks.org/rsa-algorithm-cryptography/
#planning using "rb" and "wb" https://intellipaat.com/blog/tutorial/python-tutorial/python-file-handling-i-o/
#rb opens a binary-formatted file just for reading.
#wb opens a  binary-formatted file just for writing

public_key, private_key = rsa.newkeys(1024)

with open("\Project2\keys", "wb") as f:
    f.write(public_key.save_pkcs1("PEM")) 

with open("\Project2\keys", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))