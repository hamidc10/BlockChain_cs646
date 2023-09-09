Group 3: Trey Carroll,  Hamid Choucha, Xavier Martinez, Chantel Rose Walia, Vira Shankar
README

Transaction.py -
This our transaction code file, we used SHA256 to hash everything. We took a dictionary and made it into a str with no space and then hashed it using hashlib. After hashing, file will be saved as a JSON with the hash as the filename. It has 4 requirements to what we consider a transaction.
1. Who is the transaction from?
2. Who is the transaction to?
3. Amount of transaction?
4. What is timestamp (date, current time, etc.)

Links used:
1. https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing
2. https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

Block.py - 
Receives transaction file name and then parses it and stores information into a dictionary which is saved as a JSON file. Before the file is saved, it is hashed using SHA256. After hashing, it is stored as an str with no space with the file being saved as the hash we created.

Links used:
1. https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
2. https://docs.python.org/3/library/hashlib.html
3. https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing
4. https://www.geeksforgeeks.org/important-blockchain-terminologies/?ref=gcse
5. https://www.learndatasci.com/solutions/python-typeerror-sequence-item-n-expected-string-list-found/
6. https://stackoverflow.com/questions/123198/how-to-copy-files
7. https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
8. https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/
