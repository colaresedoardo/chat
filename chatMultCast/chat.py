# -*- coding: utf-8 -*-
from tkinter import *
from sock import Sock
import sys
from threading import Thread

# falta como um try catch no sair e no receber. Após o usuário clicar em sair e gerada uma excessão.


class InterfaceGrafica(Frame,Thread):
    def __init__(self,master):
        Frame.__init__(self)
        Thread.__init__(self)

        self.font = ("Arial","12")
        self.pack(expand=YES, fill=BOTH)
        self.primeiroFrame = Frame(master)
        self.primeiroFrame['padx']= 20
        self.primeiroFrame['pady'] = 5
        self.primeiroFrame.pack()

        self.titulo = Label(self.primeiroFrame, text="Chat")
        self.titulo.pack()
        #Criando o campo de texto e o label do ip
        self.frameip = Frame(master)
        self.frameip.pack()
        self.campoip = Label(self.frameip,text="Digite o IP: ")
        self.campoip.pack(side=LEFT)
        self.entradaip = Entry(self.frameip)
        self.entradaip.insert(INSERT,"224.3.1.1")
        self.entradaip['width'] = 20
        self.entradaip.pack(side=LEFT)
        #criando o campo de texto da porta
        self.frameporta = Frame(master)
        self.frameporta.pack()
        self.campoporta = Label(self.frameporta, text="Digite a porta: ")
        self.campoporta.pack(side=LEFT)
        self.entradaporta= Entry(self.frameporta)
        self.entradaporta.insert(INSERT,"10000")
        self.entradaporta['width'] = 20
        self.entradaporta.pack(side=LEFT)

        # criando o campo para digitar o nome
        self.framenome = Frame(master)
        self.framenome.pack()
        self.camponome = Label(self.framenome, text="Digite seu nome : ")
        self.camponome.pack(side=LEFT)
        self.entradanome= Entry(self.framenome)

        self.entradanome['width'] = 20
        self.entradanome.pack(side=LEFT)


        #criando o botão entrar
        self.framebutton =Frame(master)
        self.framebutton.pack()
        self.entrar = Button(self.framebutton)
        self.entrar['text'] = "entrar"
        self.entrar['width'] = 12
        self.entrar['command'] = self.capturandoDados
        self.entrar.pack(side=LEFT)
        #criando o botão sair
        #self.framebutton = Frame(master)
        #self.framebutton.pack()
        self.sair = Button(self.framebutton)
        self.sair['text'] = "sair"
        self.sair['width'] = 12
        self.sair['command'] = self.sairSock
        self.sair.pack(side=RIGHT)

        # criando o campo de texto para enviar a msg
        self.framemsg = Frame(master)
        self.framemsg.pack()
        self.campomsg = Label(self.framemsg, text="Digite a menssagem ")
        self.campomsg.pack(side=LEFT)
        self.entradamsg = Entry(self.framemsg)
        self.entradamsg['width'] = 20
        self.entradamsg.pack(side=LEFT)

        #criando o botão para enviar a menssagem
        self.framebuttonMsg = Frame(master)
        self.framebuttonMsg.pack()
        self.enviar = Button(self.framebuttonMsg)
        self.enviar['text'] = "enviar"
        self.enviar['width'] = 12
        self.enviar['command'] = self.enviarMsg
        self.enviar.pack()


        # lista das respostas das msgs
        self.scrollbar = Scrollbar(master)
        self.scrollbar.set(100,100)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        #self.scrollbar.config(width=50)
        self.lista = Listbox(master, yscrollcommand=self.scrollbar.set)
        self.lista.pack(side=LEFT, fill=BOTH)
        self.lista.config(width=80)
        self.msg =""
        self.porta=0
        self.ip=""

        #criando a lista

    def capturandoDados(self):
        self.ip = self.entradaip.get()
        self.porta = int(self.entradaporta.get())
        self.sock = Sock(self.ip , self.porta)
        self.sock.enviar("entrou na sala hahaahahaah")
        self.sock.start()
        self.t1 = Thread(name='Atualizar lista', target=self.atualizarLista)
        self.t1.start()


    def atualizarLista(self):
        while True:

            self.sock.receber()

            #if (self.sock.data ==" "):
             #   self.lista.insert(0, "%s porta: %s Entrou.." % (self.sock.host, self.sock.myPort))

            #if self.sock.address != "":
            endereco, porta = self.sock.address
            data =  self.sock.data
            print("recebendo dados")
            print(data)
            data = data.decode("utf-8")

            self.lista.insert(0, "%s : %s " % (self.entradanome.get(),data))
            #print("É vdd este bilhete")


    def enviarMsg(self):
        msg = self.entradamsg.get()
        if msg != "":
            self.sock.enviar(msg)

    def sairSock(self):
        self.sock.enviar(" saindo da sala ")
        #self.sock.enviar("saindo..")
        self.t1
        self.sock.sair()


#Ultima atualização 02/09/2018
#problema: Não estou consguindo obter os paramêtros do servidor.


def main():
    root = Tk()
    #sock = Sock('224.3.1.1','10000')
    #sock.enviar("teste")
    #sock.start()

    interface  = InterfaceGrafica(root)
    interface.start()
    interface.mainloop()


if __name__ == "__main__":
    main()