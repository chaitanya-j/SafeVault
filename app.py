# This is a programm which will encrypt all the data in a file using the encryption algorythm of AES-256. 
# Its one of the most secure encryption algorythms in the world. 
# Used by many TechGiants like Google and Microsoft to protect their customer's data!

# I am importing the module aes-256 written by me which has the encrypt and decrypt methods
import aes_256
import json
from getpass import getpass
import os
import base64

path = "data"

master_password = getpass("Master password:")
try:
    with open("data") as d:
        d.readline()
        
except Exception:
    master_password_retake = getpass("Please enter your password again: ")

    if master_password == master_password_retake:
        print("Both password were correct!")
        print("Some safety information:")
        print("=================================================================================================")
        print("")
        print("NEVER EVER forget your master password your data will remain encrypted forever")
        print("NO forgot password option is availlable")
        print("")
        print("=================================================================================================")

    else:
        print("The passwords do not match please try again!!!")
        exit()


def encrypt_file(str_creds,master_passw):
    with open("data","w") as data:
        try:
            
            file_enc_dict = aes_256.encrypt(str_creds,master_passw)
            conc_file_enc_dict = file_enc_dict.get("salt") + file_enc_dict.get("nonce") + file_enc_dict.get("tag") + file_enc_dict.get("cipher_text")
            data.write(conc_file_enc_dict)
        
        except Exception:
            print("Nothings in file!")

def decrypt_file(master_passw):
    with open("data") as d:
        data = d.readline()
        salt = data[0:24]
        nonce = data[24:48]
        tag = data[48:72]
        cipher_text = data[72:]
        file_data_dict = {}
        file_data_dict["salt"] = salt
        file_data_dict["nonce"] = nonce
        file_data_dict["tag"] = tag
        file_data_dict["cipher_text"] = cipher_text

    decrypted_file = aes_256.decrypt(file_data_dict,master_passw)
    secret_data = json.loads(decrypted_file)
    
    # print('>> Decrypted data:', secret_data)

    return secret_data

try:
    decrypt_file(master_password)
except FileNotFoundError:
    print("File not found")
    encrypt_file(json.dumps({}),master_password)

except Exception:
    print("Master password incorrect. Please try again")
    exit()


print("Hey User! Pleaase select what you want to do from the menu!")
print("1) Add a password")
print("2) Get a password")
print("3) Update values")
print("4) Exit")

usr_opinion = int(input("1, 2, 3 or 4? : "))

if usr_opinion == 1:
    usr_key = getpass("Dear user please enter the key: ")
    if os.stat(path).st_size == 0:
        confirm_usr_key = getpass("Dear user please enter the key again: ")
        if usr_key == confirm_usr_key:
            print("Both passwords are same!")
        else:
            print("=========================================================================================================")
            print("")
            print("Dear user, the second password you entered was not the same as the first one please try again!!!")
            print("")
            print("=========================================================================================================")
            exit()

    app_name = input("Please enter the app name: ")
    usr_name = input("Please enter your usr name: ")
    app_pass = input("Please enter the app login password: ")

    try:
        creds = decrypt_file(master_password)
    except Exception:
        creds = {}
    
    encrypted_password = aes_256.encrypt(app_pass,usr_key)
    encr_conc_passw = encrypted_password.get("salt") + encrypted_password.get("nonce") + encrypted_password.get("tag") + encrypted_password.get("cipher_text")
    encrypted_name = aes_256.encrypt(usr_name, usr_key)
    encr_conc_name = encrypted_name.get("salt") + encrypted_name.get("nonce") + encrypted_name.get("tag") + encrypted_name.get("cipher_text")
        
    creds[app_name] = [encr_conc_name,encr_conc_passw]
    str_creds = json.dumps(creds)
    encrypt_file(str_creds,master_password)



if usr_opinion == 2:
    usr_app = input("Dear user please the the app of which you want the password: ")
    key = getpass("Please enter the key by which you encrypted the data: ")

    cred_dict = decrypt_file(master_password)
    encrp_passw = cred_dict.get(usr_app)[-1]
    salt = encrp_passw[0:24]
    nonce = encrp_passw[24:48]
    tag = encrp_passw[48:72]
    cipher_text = encrp_passw[72:]

    encr_data_passw = {}

    encr_data_passw["salt"] = salt
    encr_data_passw["nonce"] = nonce
    encr_data_passw["tag"] = tag
    encr_data_passw["cipher_text"] = cipher_text

    encrp_name = cred_dict.get(usr_app)[0]
    salt = encrp_name[0:24]
    nonce = encrp_name[24:48]
    tag = encrp_name[48:72]
    cipher_text = encrp_name[72:]

    encr_data_name = {}

    encr_data_name["salt"] = salt
    encr_data_name["nonce"] = nonce
    encr_data_name["tag"] = tag
    encr_data_name["cipher_text"] = cipher_text

    try:
        userid = aes_256.decrypt(encr_data_name,key).decode('utf-8')
        passwd = aes_256.decrypt(encr_data_passw,key).decode('utf-8')

        print(f"Your creds are: {userid}/{passwd}")

    except Exception:
        print('Incorrect key!!! Please try again')
        exit()
    
        
if usr_opinion == 3:
    app_name = input("Please enter the app name of the password you want to enter: ")
    new_passw = input("Please enter the new password: ")
    key = getpass("Please enter the key: ")

    
    cred_dict = decrypt_file(master_password)

    try:
        encrp_passw = cred_dict.get(app_name)[-1]
    except Exception:
        print("This app does not exist please add it or try again")
        exit()

    try:
        prev_passw = cred_dict.get(app_name)[-1]
        salt = prev_passw[0:24]
        nonce = prev_passw[24:48]
        tag = prev_passw[48:72]
        cipher_text = prev_passw[72:]
        prev_passw_dict = {}
        prev_passw_dict["salt"] = salt
        prev_passw_dict["nonce"] = nonce
        prev_passw_dict["tag"] = tag
        prev_passw_dict["cipher_text"] = cipher_text

        aes_256.decrypt(prev_passw_dict,key)

    except Exception:
        print("Oops! Dear user the key you entered was wrong!")
        exit()


    encryp_passw = aes_256.encrypt(new_passw,key)
    encr_passw = encryp_passw.get("salt") + encryp_passw.get("nonce") + encryp_passw.get("tag") + encryp_passw.get("cipher_text")

    app_n = cred_dict.get(app_name)[0]
    cred_dict[app_name] = [app_n,encr_passw]
    str_upd_creds = json.dumps(cred_dict)
    encrypt_file(str_upd_creds,master_password)




if usr_opinion == 4:
    exit()





