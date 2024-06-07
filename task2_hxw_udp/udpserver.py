import socket
import random
import time
import threading

# 配置服务器IP和端口
server_ip = '192.168.108.129'  # 替换为你的虚拟机IP地址
server_port = 12345

# 创建UDP socket并绑定到IP和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))

print(f"服务器启动，监听 {server_ip}:{server_port}")

clients = {}

def handle_client(sock, addr):
    """
    处理单个客户端连接
    """
    print(f"处理客户端 {addr}")
    while True:
        data, addr = sock.recvfrom(2048)
        if not data:
            continue
        if data.decode() == 'FIN':
            print(f"收到来自 {addr} 的FIN报文")
            sock.sendto('ACK'.encode(), addr)
            sock.sendto('FIN'.encode(), addr)
            data, addr = sock.recvfrom(2048)
            if data.decode() == 'ACK':
                print(f"与 {addr} 断开连接")
                break
        seq_no = data[:2]
        ver = data[2:3]
        print(f"收到消息: {data} 来自 {addr}")

        # 模拟丢包
        if random.random() < 0.2:  # 20% 丢包率
            print(f"丢弃来自 {addr} 的数据包")
            continue

        # 添加处理延迟来模拟真实网络环境
        start_time = time.time()
        time.sleep(0.1)
        processing_time = time.time() - start_time

        # 构建响应报文，包含序列号、版本号和服务器系统时间
        response = seq_no + ver + time.strftime("%H:%M:%S").encode().ljust(200)
        sock.sendto(response, addr)
        print(f"处理时间: {processing_time * 1000:.2f} ms")

def establish_connection(sock):
    """
    模拟TCP连接建立过程（三次握手），并为每个客户端创建一个线程
    """
    while True:
        data, addr = sock.recvfrom(2048)  # 接收初始连接请求
        if data.decode() == 'SYN':
            print(f"收到来自 {addr} 的SYN报文")
            sock.sendto('SYN-ACK'.encode(), addr)
            data, addr = sock.recvfrom(2048)
            if data.decode() == 'ACK':
                print(f"与 {addr} 建立连接")
                if addr not in clients:
                    client_thread = threading.Thread(target=handle_client, args=(sock, addr))
                    clients[addr] = client_thread
                    client_thread.start()
                else:
                    print(f"客户端 {addr} 已连接")

# 监听客户端连接请求
print("等待客户端连接请求...")
establish_connection(sock)
