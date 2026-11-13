#!/usr/bin/env python3
# webget.py —— 手搓 HTTP 客户端
# GitHub: https://github.com/tommommot/CompNet-lab2
import socket
import sys
import os


def usage():
    print("用法: python webget.py <host> <path> [port]")
    print("例:   python webget.py www.bjfu.edu.cn /")
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        usage()

    host = sys.argv[1]
    path = sys.argv[2]
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 80

    req = (
        "GET %s HTTP/1.1\r\n"
        "Host: %s\r\n"
        "User-Agent: webget/1.0\r\n"
        "Accept: */*\r\n"
        "Accept-Encoding: identity\r\n"
        "Connection: close\r\n"
        "\r\n" % (path, host)
    ).encode("ascii")

    print(req.decode("ascii"))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, port))
    s.sendall(req)

    buf = b""
    count = 0
    sizes = []
    header_end = -1
    content_length = None
    status_line = ""
    headers = {}

    while True:
        data = s.recv(4096)
        if not data:
            break
        count += 1
        sizes.append(len(data))
        buf += data

        if header_end < 0:
            i = buf.find(b"\r\n\r\n")
            if i >= 0:
                header_end = i + 4
                lines = buf[:i].decode("iso-8859-1").split("\r\n")
                status_line = lines[0]
                for ln in lines[1:]:
                    k, _, v = ln.partition(":")
                    if k.strip():
                        headers[k.strip().lower()] = v.strip()
                cl = headers.get("content-length")
                if cl and cl.isdigit():
                    content_length = int(cl)

        if content_length is not None and len(buf) - header_end >= content_length:
            break

    s.close()
    body = buf[header_end:] if header_end >= 0 else b""

    print("=" * 50)
    print("状态行:", status_line)
    print("响应头:")
    for k in headers:
        print("   %s: %s" % (k, headers[k]))
    print("=" * 50)
    print("recv 次数:", count)
    print("每次字节数:", sizes)
    print("body 长度:", len(body))

    name = os.path.basename(path.rstrip("/")) or "index.html"
    with open(name, "wb") as f:
        f.write(body)
    print("已保存:", name)


if __name__ == "__main__":
    main()