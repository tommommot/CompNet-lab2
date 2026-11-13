from socket import *
import sys

# D3 用：从文件里读 2000 字节发出去（别把 2000 字节硬编码在代码里）
serverName = '127.0.0.1'
serverPort = 5201
SIZE = 2000

if len(sys.argv) < 2:
    print("用法: python udpclient_big.py <文件路径> [每次字节数]")
    sys.exit(1)

path = sys.argv[1]
if len(sys.argv) > 2:
    SIZE = int(sys.argv[2])

with open(path, 'rb') as f:
    payload = f.read(SIZE)

if len(payload) < SIZE:
    print("[警告] 文件只有 %d 字节，补零到 %d" % (len(payload), SIZE))
    payload = payload + b'\x00' * (SIZE - len(payload))

print("本次发送 %d 字节" % len(payload))

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(3)
clientSocket.sendto(payload, (serverName, serverPort))

try:
    data, addr = clientSocket.recvfrom(4096)
    print("[收到回复 %d 字节]" % len(data))
except timeout:
    print("[3 秒内没有回复]（server 不在线时，Windows 上常抛 ConnectionResetError，见 D4）")
except ConnectionResetError as e:
    print("[ConnectionResetError] 通常是收到了 ICMP Port Unreachable: %s" % e)

clientSocket.close()
