import subprocess
import os
from cryptography.fernet import Fernet

directory_name = "ransomware test_folder"
dir_files = os.listdir("ransomware test_folder")

with open("key.key", "rb") as key_file:
    decryption_key = key_file.read()
key = Fernet(decryption_key)

with open("metadata.mm", "rb") as metafile:
    encr_meta = metafile.read()
    decr_meta = key.decrypt(encr_meta)

with open("metadata.txt", "wb") as metafile:
    metafile.write(decr_meta)
    os.remove("metadata.mm")

with open("metadata.txt", "r") as metafile:
    metadata = metafile.readlines()

extensions = []
for meta in metadata:
    file_name = meta.split(",")[0]
    file_ext = meta.split(",")[1]
    extensions.append((file_name, file_ext.strip()))

for index, file in enumerate(dir_files):
    file_name = os.path.splitext(file)[0]
    existing_path = os.path.join(directory_name, file)
    new_file = file_name + str(extensions[index][1])
    new_file_path = os.path.join(directory_name, new_file)
    with open(existing_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
        decrypted_data = key.decrypt(encrypted_data)
    with open(new_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
    os.remove(existing_path)

os.remove("metadata.txt")
os.remove("key.key")
os.remove("Readme.txt")