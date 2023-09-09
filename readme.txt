###########
# Group 3 #
###########
  --------------------------------------------------------------------------------------
  | by: Hamid Choucha, Chantel Rose Walia, Xavier Martinez, Vira Shankar, Trey Carroll |
  --------------------------------------------------------------------------------------
*************DISCLAIMER*************:
  An issue can appear when running this code on GIT HUB Workspace VS a normal Python environment like (VS code) for the file path
    If you are using workspace then change the file path in Block.py to this ON LINES 41-43:
      -pending = "./src/pending/"
      -processed = "./src/processed/"
      -blocks = "./src/blocks/"
    If you are using something like VScode then change the file path in Block.py to this ON LINES 41-43:
      -pending = "../src/pending/"
      -processed = "../src/processed/"
      -blocks = "../src/blocks/"


How to run the code:
  Open up your terminal and get to the folder called: "src"
    Then make sure that inside you find:
      -Block.py
      -Transaction.py
      -Main.py
      -Folder called: "pending"
      -Folder called: "block"
      -Folder called: "Processing"
  Once everything is there you go back to the terminal and run Python3 main.py or Python main.py:
      The user will be prompted if they want to have the code print the block or not by typing either (yes or no...)
      Then the user will select to make a transaction by choosing choice one where they type in the following information that was asked by the code in the terminal.
      Once the user has created the transactions desired then they can choose choice 2 to exit out of the code.

#################################################################################################### EXPLANATION OF THE PYTHON FILES #########################################################################################################################################
  
Transaction.py -
      The goal of the transaction code is to get information that is required for creating a hash file that can be used to create a block.
    The code asks the user to input the following information:
        1. Who is the transaction from?
        2. Who is the transaction to?
        3. Amount of transaction?
        4. What is the timestamp (date, current time)
    Once the code has all the information required it then turns the following into a JSON dictionary object. The code then 
    used that object using a hash library to perform the SHA-256 hashing algorithm on it. 
    Then the code can return the name of the transaction file that has been created from the hash.
  
      Links used:
      1. https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing
      2. https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
  
Block.py - 
      The goal of the transaction code is to get the transaction information and hash to create what is called a block. The 
    block has a header component, height component, and body component. The code inputs the Transactions or Transaction that 
    have been created. Once the code receives the hash file it then extracts the hash. Give the hash the attribute of the 
    new current timestamp and a body list( which will store other hash of transactions). The code then grabs the next 
    transaction from the pending folder to check if there is another block If there is it will add onto to the height of the 
    block if not it reads "NA".It will then go into a processed folder waiting for more transactions to occur. Once all the 
    transactions are complete the block will appear in the block folder with the height, timestamp, and information from the 
    Hashes as well as the new hash for the block as the file name.
    
      Links used:
      1. https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
      2. https://docs.python.org/3/library/hashlib.html
      3. https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing
      4. https://www.geeksforgeeks.org/important-blockchain-terminologies/?ref=gcse
      5. https://www.learndatasci.com/solutions/python-typeerror-sequence-item-n-expected-string-list-found/
      6. https://stackoverflow.com/questions/123198/how-to-copy-files
      7. https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
      8. https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/
