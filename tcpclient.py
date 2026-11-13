from socket import *

serverName = '127.0.0.1'
serverPort = 5201

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))   # <-- UDP 客户端没有这一行，区别就在这儿
sentence = input('输入一句小写的话: ')
clientSocket.send(sentence.encode('utf-8'))
modifiedSentence = clientSocket.recv(1024)
print("[来自 server] %s" % modifiedSentence.decode('utf-8'))
clientSocket.close()
