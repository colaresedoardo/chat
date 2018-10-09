from threading import Thread
import socket
import struct
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
class Sock(Thread):
    def __init__(self,ip, porta):
        self.criptografia = CriptografiaAES('limao')
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
        print("dados")
        self.data = self.criptografia.decrypt(self.data)

        print( self.data)
        print("Dados recebidos %s do %s " % (self.address))
    def enviar(self,msg):

        self.msg = msg.encode()

        self.msg= self.criptografia.encrypt(self.msg)
        self.sock.sendto(self.msg, self.multicast_group)
        #self.sock.sendto(msg, self.address)

    def sair(self):
        #self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()



class CriptografiaAES():

    def __init__(self,key):
        self.bs =16
        self.pad = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        self.key = hashlib.sha256(key.encode()).digest()
    def encrypt(self, raw):
        raw = self._pad(raw)
        print("pritando o raw")
        print(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        base64.b64encode(iv + cipher.encrypt(raw))
       # return base64.b64encode(iv+cipher.encrypt(raw))

    def decrypt(self,enc):
        enc = base64.b64encode(enc)

        iv = enc[:AES.block_size]
        print(iv)
        cipher = AES.new(self.key,AES.MODE_CBC, iv)
        #print(cipher.decrypt(enc[:AES.block_size:]))

        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self,s):

       # print( self.bs - len(s) % self.bs )
       #3 return (s + b"\0"*(self.bs - len(s) % self.bs) * (self.bs - len(s) % self.bs))
        print(s)
        print("tamanho do bloco %s, tamanho da msg %s "%(AES.block_size,len(s)))
        return b"\0"+s +  (AES.block_size - (len(s) % AES.block_size)*chr(AES.block_size - len(s) % AES.block_size))
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]





