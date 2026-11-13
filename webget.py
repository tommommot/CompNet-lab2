#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webget.py —— 手搓 HTTP 客户端（实验 2 Part D）
GitHub 仓库: https://github.com/<你的账号>/<仓库名>

用法:
    python webget.py <host> <path> [port]
例:
    python webget.py www.bjfu.edu.cn /
    python webget.py www.bjfu.edu.cn /index.html 80

只用 Python 标准库 socket + sys + os + time。
"""
import socket
import sys
import os
import time


def usage():
    print("用法: python webget.py <host> <path> [port]")
    print("例:   python webget.py www.bjfu.edu.cn /")
    print("      python webget.py www.bjfu.edu.cn /index.html 80")
    sys.exit(1)


def build_request(host, path, port):
    """
    构造 HTTP/1.1 请求。
    两个关键头：
      Host:               HTTP/1.1 必带，否则虚拟主机服务器不知道你要哪个站点
      Connection: close   让服务器在 body 发完后关连接，
                          这样没有 Content-Length 时 recv 循环也能靠“收到 0 字节”结束
    Accept-Encoding: identity 是故意写的：不让服务器 gzip，body 才是可读的原文。
    """
    host_header = host if port == 80 else "%s:%d" % (host, port)
    lines = [
        "GET %s HTTP/1.1" % path,
        "Host: %s" % host_header,
        "User-Agent: webget/1.0 (BFU-CompNet-lab2)",
        "Accept: */*",
        "Accept-Encoding: identity",
        "Connection: close",
    ]
    return ("\r\n".join(lines) + "\r\n\r\n").encode("ascii")


def main():
    if len(sys.argv) < 3:
        usage()

    host = sys.argv[1]
    path = sys.argv[2]
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 80

    req = build_request(host, path, port)
    print(">>> 发出请求（%d 字节）:" % len(req))
    print(req.decode("ascii"))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)          # 防止挂在坏服务器上（附录 B-3）
    t0 = time.time()
    s.connect((host, port))
    s.sendall(req)

    buf = b""                   # 已经收到的全部字节
    recv_count = 0              # T1 验收：recv 调用次数
    sizes = []                  # T1 验收：每次收到的字节数
    header_end = -1             # 响应头结束位置
    status_line = ""
    headers = {}
    content_length = None

    while True:
        try:
            data = s.recv(4096)
        except socket.timeout:
            print("!! recv 超时：服务器既没关连接、也没给 Content-Length")
            break
        if not data:
            # 结束条件②：对端关闭连接（此刻 recv 返回 b''，不是抛异常）
            break

        recv_count += 1
        sizes.append(len(data))
        buf += data

        if header_end < 0:
            i = buf.find(b"\r\n\r\n")
            if i == -1:
                continue        # 头还没收全，继续收
            header_end = i + 4
            head = buf[:i].decode("iso-8859-1")   # 头是 ASCII/ISO-8859-1，别用 utf-8
            lines = head.split("\r\n")
            status_line = lines[0]
            for ln in lines[1:]:
                k, _, v = ln.partition(":")
                if k.strip():
                    headers[k.strip().lower()] = v.strip()
            cl = headers.get("content-length")
            if cl and cl.isdigit():
                content_length = int(cl)

        # 结束条件①：body 已经收够 Content-Length 个字节
        if content_length is not None and len(buf) - header_end >= content_length:
            break

    s.close()
    elapsed = time.time() - t0

    body = buf[header_end:] if header_end >= 0 else b""

    print("=" * 62)
    print("状态行 : %s" % status_line)
    print("-" * 62)
    print("响应头 :")
    for k, v in headers.items():
        print("    %-20s %s" % (k + ":", v))
    print("=" * 62)
    print("recv 次数 : %d" % recv_count)
    print("每次字节数: %s" % sizes)
    print("body 长度 : %d 字节" % len(body))
    print("总耗时    : %.3f s" % elapsed)

    if content_length is not None and len(body) > content_length:
        body = body[:content_length]     # 可能多收了下一条响应的开头，截掉

    name = os.path.basename(path.rstrip("/")) or "index.html"
    with open(name, "wb") as f:          # 必须 wb：文本模式会把 \r\n 改写成 \n、还可能截断在 0x1A
        f.write(body)
    print("body 已保存: %s (%d 字节)" % (name, len(body)))


if __name__ == "__main__":
    main()
