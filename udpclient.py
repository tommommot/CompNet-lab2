from socket import *

serverName = '127.0.0.1'      # 同机就在本机；虚拟机组网时写宿主机的 vmnet8 地址
serverPort = 5201

# 注意：UDP 客户端没有 connect()，第一句网络动作就是 sendto
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('输入一句小写的话: ')
clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print("[回复] %s" % modifiedMessage.decode('utf-8'))
clientSocket.close()
