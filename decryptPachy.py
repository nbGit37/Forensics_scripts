import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def list_file_content(File_path):
    content = []
    with open(File_path, 'r') as file:
        for line in file:
            content.append(line.strip()) #rajoute chaque ligne du fichier comme un élément
    return content


def decrypt(encrypted_file_path, keys, ivs):
    for key, iv in zip(keys, ivs):
        try:
            key = bytes.fromhex(key)
            iv = bytes.fromhex(iv)

            cipher = AES.new(key, AES.MODE_CBC, iv)

            with open(encrypted_file_path, 'rb') as file:
                ciphertext = file.read()
                decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

            decrypted_file_path = encrypted_file_path[:-6]  # Supprime la partie ".pachy"
            with open(decrypted_file_path, 'wb') as output_file:
                output_file.write(decrypted_data) #écrit les données déchiffrées dans le nouveau fichier

            print(f"\tDECRYPTED : '{encrypted_file_path}' with key-IV : {key.hex()}   -   {iv.hex()}\n")
        except:
            pass
            


if __name__ == "__main__":
    target_directory_path = "../pachy_files"
    keys_file_path = "keys.txt"
    ivs_file_path = "ivs.txt"

    keys = list_file_content(keys_file_path)
    ivs = list_file_content(ivs_file_path)

    if keys and ivs:  # si ivs et keys ont été remplis
        for file_name in os.listdir(target_directory_path):
            if file_name.endswith(".pachy"):
                print(f"Traitement de {file_name} :")
                encrypted_file_path = os.path.join(target_directory_path, file_name)
                decrypt(encrypted_file_path, keys, ivs)
            else:
                pass
    else:
        print("Reading keys/IVs failed.\n")
