import socket
import struct
import sys
import random

# 报文类型定义
TYPE_INITIALIZATION = 1
TYPE_AGREE = 2
TYPE_REVERSE_REQUEST = 3
TYPE_REVERSE_ANSWER = 4


def send_initialization(sock, num_blocks):
    """
    发送 Initialization 报文
    """
    msg = struct.pack('!HI', TYPE_INITIALIZATION, num_blocks)
    sock.send(msg)


def send_reverse_request(sock, block_data):
    """
    发送 reverseRequest 报文
    """
    length = len(block_data)
    msg = struct.pack('!HI', TYPE_REVERSE_REQUEST, length) + block_data
    sock.send(msg)


def receive_reverse_answer(sock):
    """
    接收 reverseAnswer 报文
    """
    header = sock.recv(6)
    if len(header) != 6:
        print("接收 reverseAnswer 报文头失败")
        return None
    msg_type, length = struct.unpack('!HI', header)
    if msg_type != TYPE_REVERSE_ANSWER:
        print("无效的 reverseAnswer 报文")
        return None
    data = sock.recv(length)
    if len(data) != length:
        print("接收反转数据失败")
        return None
    return data


def main(server_ip, server_port, file_path, Lmin, Lmax):
    """
    客户端主逻辑
    """
    # 读取文件内容
    with open(file_path, 'r') as f:
        file_data = f.read()

    # 分块
    blocks = []
    while file_data:
        block_size = random.randint(Lmin, Lmax)
        block = file_data[:block_size]
        blocks.append(block.encode('utf-8'))
        file_data = file_data[block_size:]

    num_blocks = len(blocks)

    # 连接服务器
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    # 发送 Initialization 报文
    send_initialization(sock, num_blocks)

    # 接收 agree 报文
    data = sock.recv(2)
    if len(data) != 2:
        print("接收 agree 报文失败")
        sock.close()
        return
    msg_type = struct.unpack('!H', data)[0]
    if msg_type != TYPE_AGREE:
        print("未收到 agree 报文")
        sock.close()
        return

    reversed_blocks = []

    # 发送并接收每个数据块
    for i, block in enumerate(blocks):
        send_reverse_request(sock, block)
        reversed_data = receive_reverse_answer(sock)
        if reversed_data:
            print(f"第{i + 1}块：{reversed_data.decode('utf-8')}")
            reversed_blocks.append(reversed_data)

    # 输出反转后的文件
    with open('reversed_file.txt', 'w') as reversed_file:
        for reversed_block in reversed_blocks:
            reversed_file.write(reversed_block.decode('utf-8'))

    sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python reversetcpclient.py <server_ip> <server_port> <file_path> <Lmin> <Lmax>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    file_path = sys.argv[3]
    Lmin = int(sys.argv[4])
    Lmax = int(sys.argv[5])

    main(server_ip, server_port, file_path, Lmin, Lmax)
