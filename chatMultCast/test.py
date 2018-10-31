import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    print("mostrando dados")
    print(data)
    print("mostrando base65")
    print( base64.b64encode(data).decode("utf-8") if encode else data)
    return base64.b64encode(data).decode("utf-8") if encode else data

def decrypt(key, source, decode=True):
    print("mosntrando a entrada")
    print(source)
    if decode:
        source = base64.b64decode(source.encode("utf-8"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    print("descriptando")
    print(data)
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    print("DATA PADDING")
    print(data[-padding:])
    print("Padding calculado")
    print(bytes([padding]) * padding)
    print("bytes from bytes")
    print(bytes(padding))

    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding




my_password = b"secret_AES_key_string_to_encrypt/decrypt_with"
my_data = "input_string_to_encrypt/decrypt"
my_data= my_data.encode()
print("key:  {}".format(my_password))
print("data: {}".format(my_data))
encrypted = encrypt(my_password, my_data,False)
print("dadaos criptografados")


print("mostrando enc")
print(encrypted)
decrypted = decrypt(my_password, encrypted,False)
print("dec:  {}".format(decrypted))
