# This is a programm which will encrypt all the data in a file using the encryption algorythm of AES-256. 
# Its one of the most secure encryption algorythms in the world. 
# Used by many TechGiants like Google and Microsoft to protect their customer's data!

# I am importing the module aes-256 written by me which has the encrypt and decrypt methods
import aes_256
import json
from getpass import getpass
import chk_password
import time
import os

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

new = False

# Program logic starts here
master_password = ""
usr_key = ""
flg_file_empty = False
creds_store = {}

os.system("clear")
print("")
print("=================================================================================================")
print("                               Welcome to Password Manager 1.0")
print("=================================================================================================")
print("")

try:
    with open("data") as d:
        d.readline()
        
except Exception:
    print("")
    print("Initiating Program Setup...")
    
    print("")
    print("You are about to set the master password and the encryption key")
    print("Here are some instructions: ")
    print("The password must have atleast:")
    print("1) 1 special character")
    print("2) 1 integer")
    print("3) 1 small alphabet")
    print("4) 1 capital alphabet")
    print("5) Password must have atleast 8 character") 
    print(" ")
    print("Step-1: Set your master password")
    print("")
    master_password = getpass("\tMaster password: ")
    master_password_retake = getpass("\tEnter master password again: ")

    if master_password == master_password_retake:
        
        if_pass_complx = chk_password.chk_complxty_password(master_password)
        if if_pass_complx == False:
            print("\tError: Sorry, the password you set was not complex enough! Aborting setup")
            print("")
            exit()

        print("\tSuccess: Master password is now set")
    else:
        print("\tError: The entered passwords do not match. Aborting setup")
        print("")
        exit()

    print("")
    print("Step-2: Set your encryption key")
    print("")

    usr_key = getpass("\tEncryption key: ")
    confirm_usr_key = getpass("\tEnter encryption key again: ")
    new = True




    if usr_key == confirm_usr_key:
        if_pass_complx = chk_password.chk_complxty_password(usr_key)
        if if_pass_complx == False:
            print("\tError: Sorry, the key you set was not complex enough! Aborting setup")
            print("")
            exit()
        print("\tSuccess: Encryption key set successfully")
    else:
        print("\tError: The entered key values do not match. Aborting setup")
        print("")
        exit()

    print("")
    print("Program setup complete. Please note some safety instructions:")
    print("")
    print(" - Please keep the master password & the encryption key at a safe location.")
    print(" - If either of these secrets are lost, your data will remain encrypted forever")
    print(" - The program does not offer any recovery option for these secrets")
    print("")
    
    enter = getpass("Hit enter to continue :")


try:
    if master_password == "":
        master_password = getpass("Enter your master password: ")


    print("Initialising creds_store...")
    creds_store = decrypt_file(master_password)

except FileNotFoundError:
    encrypt_file(json.dumps({}),master_password)

except Exception:
    print("Error: Master password incorrect. Please try again")
    print("")
    exit()

flg = 0
while True:
    try:
        with open("data") as d:
            d.readline()

    except Exception:
        if flg == 0:
            time.sleep(8)
            flg = 1
    os.system("clear")

    print("")
    print("=================================================================================================")
    print("                                      Application Menu")
    print("=================================================================================================")
    print("")

    print("Please select what you want to do")
    print("1) Add a credential")
    print("2) Get a credential")
    print("3) Update credentials")
    print("4) Exit")

    try:
        usr_choice = int(input("Your choice: "))
    except Exception:
        print("Error: Invalid choice. Please try again")
        time.sleep(2)
        continue
        


    if usr_choice == 1: 
        user_key = getpass("Enter your encryption key: ")
        if new == True:
            if usr_key == user_key:
                print("Key entered matches")
            else:
                print("The key is incorrect... Aborting.....")
                exit()

        if bool(creds_store) != False:
            latest_add = 0
            for i in creds_store.keys():
                latest_add = i
                break
            app_creds = creds_store.get(latest_add)
            passw = app_creds[1]
            salt = passw[0:24]
            nonce = passw[24:48]
            tag = passw[48:72]
            cipher_text = passw[72:]
            passw_encr_data = {}
            passw_encr_data["salt"] = salt
            passw_encr_data["nonce"] = nonce
            passw_encr_data["tag"] = tag
            passw_encr_data["cipher_text"] = cipher_text

            try:
                aes_256.decrypt(passw_encr_data,user_key)

            except Exception:
                print("The key you entered was different. The key should be same to encrypt all the data.")
                exit()

        print("Preparing to add a credential in the secret store")
        app_name = input("Which app you need to add credentials for? Enter the name of the app: ")
        usr_name = input("What is the username? ")
        app_pass = getpass(f"Enter the Password for '{usr_name}': ")
        app_pass_retake = getpass("Enter password again: ")

        if app_pass != app_pass_retake:
            print("Passwords do not match! Please try again.")
            continue


        passwd_encr_data = aes_256.encrypt(app_pass,user_key)
        encr_passwd = passwd_encr_data.get("salt") + passwd_encr_data.get("nonce") + passwd_encr_data.get("tag") + passwd_encr_data.get("cipher_text")

        usrname_encr_data = aes_256.encrypt(usr_name, user_key)
        encr_usrname = usrname_encr_data.get("salt") + usrname_encr_data.get("nonce") + usrname_encr_data.get("tag") + usrname_encr_data.get("cipher_text")

        creds_store[app_name] = [encr_usrname,encr_passwd]
        str_creds_store = json.dumps(creds_store)

        encrypt_file(str_creds_store,master_password)
        flg_file_empty = False





    elif usr_choice == 2:
        print("Retrieve credentials")
        usr_app = input(f"Please enter the app name {[ key for key in creds_store.keys()]}: ")
        key = getpass("Enter the encryption key: ")

        app_creds = creds_store.get(usr_app)

        if app_creds == None:
            print(f"Error: No entry found for app by name '{usr_app}'!")
            print(" ")
            enter = getpass("Hit enter to continue :")
        else:

            encr_new_passwd = app_creds[1]

            salt = encr_new_passwd[0:24]
            nonce = encr_new_passwd[24:48]
            tag = encr_new_passwd[48:72]
            cipher_text = encr_new_passwd[72:]

            passwd_encr_data = {}

            passwd_encr_data["salt"] = salt
            passwd_encr_data["nonce"] = nonce
            passwd_encr_data["tag"] = tag
            passwd_encr_data["cipher_text"] = cipher_text

            encr_usrname = app_creds[0]
            salt = encr_usrname[0:24]
            nonce = encr_usrname[24:48]
            tag = encr_usrname[48:72]
            cipher_text = encr_usrname[72:]

            usrname_encr_data = {}

            usrname_encr_data["salt"] = salt
            usrname_encr_data["nonce"] = nonce
            usrname_encr_data["tag"] = tag
            usrname_encr_data["cipher_text"] = cipher_text

            try:
                userid = aes_256.decrypt(usrname_encr_data,key).decode('utf-8')
                passwd = aes_256.decrypt(passwd_encr_data,key).decode('utf-8')

                print(f"Your creds for '{usr_app}' are: {userid}/{passwd}")
                print(" ")
                enter = getpass("Hit enter to continue :")
            except Exception:
                print('Error: Failed to decrpt data. Key provided seems to be incorrect. Please try again')
                print("")
                exit()





    elif usr_choice == 3:
        print("Updating credentials")
        app_name = input(f"Please enter the app name {creds_store.keys()}: ")
        key = getpass("Enter the encryption key: ")
        new_passw = getpass("Please enter the new password: ")

        app_creds = creds_store.get(app_name)

        if len(creds_store.keys()) == 0:
            print(f"Error: No entry found for app by name '{app_name}'! Please try again!")
            print(" ")
            enter = getpass("Hit enter to continue :")
            continue
            
        else:

            try:
                prev_passw = app_creds[1]
                salt = prev_passw[0:24]
                nonce = prev_passw[24:48]
                tag = prev_passw[48:72]
                cipher_text = prev_passw[72:]
                prev_passw_encr_data = {}
                prev_passw_encr_data["salt"] = salt
                prev_passw_encr_data["nonce"] = nonce
                prev_passw_encr_data["tag"] = tag
                prev_passw_encr_data["cipher_text"] = cipher_text

                aes_256.decrypt(prev_passw_encr_data,key)

            except Exception:
                print("Error: Incorrect key!")
                exit()


            new_passwd_encr_data = aes_256.encrypt(new_passw,key)
            encr_new_passwd = new_passwd_encr_data.get("salt") + new_passwd_encr_data.get("nonce") + new_passwd_encr_data.get("tag") + new_passwd_encr_data.get("cipher_text")

            usrname = app_creds[0]
            creds_store[app_name] = [usrname, encr_new_passwd]

            str_creds_store = json.dumps(creds_store)
            encrypt_file(str_creds_store, master_password)


    elif usr_choice == 4:
        print("Thank you for using Password Manager 1.0. Visit again!!")
        print("")
        exit()

    else:
        print("Error: Invalid choice. Please try again")
        time.sleep(2)
        continue