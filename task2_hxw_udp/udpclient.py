import socket
import sys
import time
import struct
import statistics

# 获取服务器IP和端口
if len(sys.argv) != 3:
    print("Usage: python3 udpclient.py <server_ip> <server_port>")
    sys.exit(1)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

# 创建UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.1)  # 设置超时时间100ms

def establish_connection(sock, server_ip, server_port):
    """
    模拟TCP连接建立过程（三次握手）
    """
    try:
        print("发送SYN报文...")
        sock.sendto('SYN'.encode(), (server_ip, server_port))
        data, addr = sock.recvfrom(2048)
        print(f"收到数据: {data.decode()} 来自 {addr}")
        if data.decode() == 'SYN-ACK':
            print("收到SYN-ACK报文...")
            sock.sendto('ACK'.encode(), (server_ip, server_port))
            print("连接建立成功")
    except socket.timeout:
        print("建立连接超时")
        sys.exit(1)
    except ConnectionResetError as e:
        print(f"连接被远程主机强制关闭: {e}")
        sys.exit(1)

establish_connection(sock, server_ip, server_port)

def send_request(sock, server_ip, server_port, seq_no):
    """
    发送请求数据包
    """
    version = 2
    payload = b'A' * 200  # 填充数据
    packet = struct.pack('!H B 200s', seq_no, version, payload)
    sock.sendto(packet, (server_ip, server_port))
    return time.time()

def receive_response(sock, start_time, seq_no):
    """
    接收响应数据包并计算RTT
    """
    try:
        data, _ = sock.recvfrom(2048)
        end_time = time.time()
        rtt = (end_time - start_time) * 1000  # RTT in ms
        seq, ver, server_time = struct.unpack('!H B 200s', data)
        if seq != seq_no:
            print(f"序列号不匹配: 期望 {seq_no}, 但收到 {seq}")
            return None
        print(f"序列号: {seq_no}, 服务器时间: {server_time.decode().strip()}, RTT: {rtt:.2f} ms")
        return rtt
    except socket.timeout:
        print(f"序列号: {seq_no}, 请求超时")
        return None
    except ConnectionResetError as e:
        print(f"连接被远程主机强制关闭: {e}")
        return None

rtts = []
received_packets = 0

for seq_no in range(1, 13):
    attempts = 0
    while attempts < 3:
        start_time = send_request(sock, server_ip, server_port, seq_no)
        rtt = receive_response(sock, start_time, seq_no)
        if rtt is not None:
            rtts.append(rtt)
            received_packets += 1
            break
        attempts += 1

if rtts:
    max_rtt = max(rtts)
    min_rtt = min(rtts)
    avg_rtt = sum(rtts) / len(rtts)
    stddev_rtt = statistics.stdev(rtts)
    print(f"接收到的UDP包数量: {received_packets}")
    print(f"丢包率: {(12 - received_packets) / 12 * 100:.2f}%")
    print(f"最大RTT: {max_rtt:.2f} ms")
    print(f"最小RTT: {min_rtt:.2f} ms")
    print(f"平均RTT: {avg_rtt:.2f} ms")
    print(f"RTT标准差: {stddev_rtt:.2f} ms")

def release_connection(sock, server_ip, server_port):
    """
    模拟TCP连接释放过程（四次挥手）
    """
    try:
        print("发送FIN报文...")
        sock.sendto('FIN'.encode(), (server_ip, server_port))
        data, addr = sock.recvfrom(2048)
        print(f"收到数据: {data.decode()} 来自 {addr}")
        if data.decode() == 'ACK':
            print("收到ACK报文...")
            sock.sendto('FIN'.encode(), (server_ip, server_port))
            data, addr = sock.recvfrom(2048)
            if data.decode() == 'ACK':
                print("连接释放成功")
    except socket.timeout:
        print("释放连接超时")
    except ConnectionResetError as e:
        print(f"连接被远程主机强制关闭: {e}")

release_connection(sock, server_ip, server_port)
