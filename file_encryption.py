import hashlib
import os
import sys
import getpass
from AESCipher import *

SHA512_LEN = 64  # Length of the hashed password (SHA-512)

def encrypt_file(path, password, hashed_pass):
    """
    Encrypts a file with AES encryption and stores the result in a new file with the '.encr' extension.

    Args:
        path (str): Path to the file to be encrypted.
        password (str): User's password for AES encryption.
        hashed_pass (bytes): The hashed password to store alongside the encrypted data.

    Returns:
        None
    """
    print(path)
    aes = AESCipher(password)  # Initialize the AES cipher with the password

    # Read the file data to encrypt
    with open(path, 'rb') as file:
        data = file.read()
        
    # Encrypt the data and prepend the hashed password and salt
    enc = hashed_pass + aes.encrypt(data) + aes.salt
    
    # Write the encrypted data to a new file with a .encr extension
    with open(path + '.encr', 'wb') as file:
        file.write(enc)

    # Optionally delete the original file after encryption (commented out)
    # os.remove(path)

def decrypt_file(path, password):
    """
    Decrypts an encrypted file and restores it to its original form.

    Args:
        path (str): Path to the encrypted file.
        password (str): User's password for AES decryption.

    Returns:
        None
    """
    # Open and read the encrypted file
    with open(path, 'rb') as file:
        data = file.read()

    # Extract the salt and hashed password from the encrypted data
    salt = data[-SALT_LEN:]  # Salt length is assumed to be defined elsewhere
    file_pass = data[:SHA512_LEN]  # Extracted hashed password
    enc = data[SHA512_LEN:-SALT_LEN]  # Extracted encrypted content
    
    # Initialize the AES cipher with the password and salt
    aes = AESCipher(password, salt)
    
    # Decrypt the data
    dec = aes.decrypt(enc)

    # Write the decrypted data back to a new file (original filename without .encr)
    with open(path[:-5], 'wb') as file:
        file.write(dec)

    # Optionally delete the encrypted file after decryption (commented out)
    # os.remove(path)

def password_input(salt):
    """
    Prompts the user to enter a password, hashes it with the provided salt, and returns the hashed password.

    Args:
        salt (str): A salt to combine with the password before hashing.

    Returns:
        tuple: A tuple containing the plain password (str) and the hashed password (bytes).
    """
    print('Enter password: ')
    password = getpass.getpass()  # Secure password input
    hashed_pass = password + salt  # Combine password and salt
    hashed_pass = hashlib.sha512(hashed_pass.encode()).digest()  # Hash the combined password with SHA-512
    return (password, hashed_pass)

def main():
    """
    Main function to handle locking and unlocking files based on user input.

    Usage:
        python script.py lock [filename]   - Encrypt the file
        python script.py unlock [filename] - Decrypt the file

    Returns:
        None
    """
    salt = 'somesalt'  # Predefined salt (could be improved by making it dynamic)

    # Ensure correct usage of the script
    if len(sys.argv) != 3:
        print(f'Usage is "{sys.argv[0]} [lock/unlock] filename"')
        return
        
    # Handle the 'lock' case for file encryption
    elif sys.argv[1] == 'lock':
        password, hashed_password = password_input(salt)  # Get the password and hashed password
        path = sys.argv[2]  # Path to the file to encrypt
        try:
            encrypt_file(path, password, hashed_password)  # Encrypt the file
            print('File encrypted')
        except Exception as ex:
            if type(ex).__name__ == 'FileNotFoundError':
                print(f'File {path} not found')
            else:
                print('Unknown error occurred')
                print(f'{ex.args}')
            sys.exit()
                
    # Handle the 'unlock' case for file decryption
    elif sys.argv[1] == 'unlock':
        password, hashed_password = password_input(salt)  # Get the password and hashed password
        path = sys.argv[2]  # Path to the file to decrypt
        file_hashed_pass = ''
        try:
            with open(path, 'rb') as file:
                data = file.read()
            file_hashed_pass = data[:SHA512_LEN]  # Extract the stored hashed password from the encrypted file
        except Exception as ex:
            if type(ex).__name__ == 'FileNotFoundError':
                print(f'File {path} not found')
            else:
                print('Unknown error occurred')
            sys.exit()
            
        # Check if the entered password matches the hashed password stored in the file
        if hashed_password == file_hashed_pass:
            try:
                decrypt_file(path, password)  # Decrypt the file
                print('File decrypted')
            except Exception as ex:
                print('Unknown error occurred')
        else:
            print('Wrong password or not an encrypted file!')
    
    else:
        print(f'Usage is "{sys.argv[0]} [lock/unlock] filename"')

if __name__ == '__main__':
    main()  # Execute the main function if the script is run
