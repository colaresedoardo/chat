from threading import Thread
import socket
import struct

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
class Sock(Thread):
    def __init__(self,ip, porta):
        self.criptografia = CriptografiaAES(b'limao')
        Thread.__init__(self)
        porta = int(porta)

        self.multicast_group = (ip, porta)
        self.host =socket.gethostbyname(socket.gethostname())

        self.server_address = ("", porta)
        # Create the datagram socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.server_address))


        self.data, self.address = ("","")
        self.msg=""
        group = socket.inet_aton(ip)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.myPort = porta
        print("retornado do get sock %s" % self.myPort)
    def run(self):
            print("executando thread")


    def receber(self):

        self.data, self.address = self.sock.recvfrom(1024)
        print("dados fazendo o encode")
        dataCifrado = self.data
        print(dataCifrado)
        print("Dados recebidos %s do %s " % (self.address))
        self.data = self.criptografia.decrypt(dataCifrado, False)


    def enviar(self,msg):

        #self.msg = msg.encode()
        self.msg = msg.encode()
        print("show the message")
        print(self.msg)
        msgCifrada= self.criptografia.encrypt(self.msg, False)
        print("Encript data")


        print(msgCifrada)


        self.sock.sendto(msgCifrada, self.multicast_group)


    def sair(self):
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()



class CriptografiaAES():

    def __init__(self,key):
        self.bs =16
        self.pad = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

        self.key =  SHA256.new(key).digest()
    def encrypt(self, texto, encode=True):

        key = SHA256.new(self.key).digest()  # use SHA-256 over our key to get a proper-sized AES key
        IV = Random.new().read(AES.block_size)  # generate IV
        encryptor = AES.new(key, AES.MODE_CBC, IV)
        padding = AES.block_size - len(texto) % AES.block_size  # calculate needed padding
        texto += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
        data = IV + encryptor.encrypt(texto)  # store the IV at the beginning and encrypt
        print("mostrando dados")
        print(data)
        print("mostrando base65")
        print(base64.b64encode(data).decode("utf-8") if encode else data)
        return base64.b64encode(data).decode("utf-8") if encode else data

    def decrypt(self,texto, decode=True):
        print("mosntrando a entrada")
        print(texto)
        if decode:
            source = base64.b64decode(texto.encode("utf-8"))
        key = SHA256.new(self.key).digest()  # use SHA-256 over our key to get a proper-sized AES key
        IV = texto[:AES.block_size]  # extract the IV from the beginning
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        data = decryptor.decrypt(texto[AES.block_size:])  # decrypt
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







