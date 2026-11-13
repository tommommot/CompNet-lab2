from socket import *

serverPort = 5201
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("TCP server 已启动，监听端口 %d" % serverPort)

while True:
    # accept 会阻塞，直到有 client 完成三次握手
    connectionSocket, addr = serverSocket.accept()
    print("[连接建立] 对方地址 %s" % (addr,))
    sentence = connectionSocket.recv(1024).decode('utf-8')
    print("[收到] %s" % sentence)
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode('utf-8'))
    connectionSocket.close()      # 这一行会让 server 先发 FIN，抓包里看得见
