from socket import *

serverPort = 5201
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("UDP server 已启动，监听端口 %d" % serverPort)

while True:
    # recvfrom 一次收一个完整的数据报（保留报文边界）
    message, clientAddress = serverSocket.recvfrom(2048)
    text = message.decode('utf-8')
    print("[收到] 来自 %s 的消息: %s" % (clientAddress, text))   # A1 验收：这句要打出来
    modifiedMessage = text.upper()
    serverSocket.sendto(modifiedMessage.encode('utf-8'), clientAddress)
