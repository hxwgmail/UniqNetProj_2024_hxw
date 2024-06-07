import socket
import struct
import threading
import select

# 报文类型定义
TYPE_INITIALIZATION = 1
TYPE_AGREE = 2
TYPE_REVERSE_REQUEST = 3
TYPE_REVERSE_ANSWER = 4


def handle_client(client_socket):
    """
    处理单个客户端连接
    """
    try:
        # 接收 Initialization 报文
        data = client_socket.recv(6)
        if len(data) != 6:
            print("接收 Initialization 报文失败")
            client_socket.close()
            return
        msg_type, num_blocks = struct.unpack('!HI', data)
        if msg_type != TYPE_INITIALIZATION:
            print("无效的 Initialization 报文")
            client_socket.close()
            return

        # 发送 agree 报文
        agree_msg = struct.pack('!H', TYPE_AGREE)
        client_socket.send(agree_msg)

        # 处理每个块的 reverse 请求
        for i in range(num_blocks):
            # 接收 reverseRequest 报文头
            header = client_socket.recv(6)
            if len(header) != 6:
                print("接收 reverseRequest 报文头失败")
                client_socket.close()
                return
            msg_type, length = struct.unpack('!HI', header)
            if msg_type != TYPE_REVERSE_REQUEST:
                print("无效的 reverseRequest 报文")
                client_socket.close()
                return

            # 接收数据块
            data = client_socket.recv(length)
            if len(data) != length:
                print("接收数据块失败")
                client_socket.close()
                return
            reversed_data = data[::-1]

            # 发送 reverseAnswer 报文
            response = struct.pack('!HI', TYPE_REVERSE_ANSWER, length) + reversed_data
            client_socket.send(response)

            print(f"第{i + 1}块：{reversed_data.decode('utf-8')}")

        client_socket.close()
    except Exception as e:
        print(f"异常: {e}")
        client_socket.close()


def start_server(server_ip, server_port):
    """
    启动服务器并监听指定IP和端口
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"服务器启动，监听 {server_ip}:{server_port}")

    inputs = [server_socket]
    while True:
        readable, _, _ = select.select(inputs, [], [])
        for s in readable:
            if s is server_socket:
                client_socket, client_address = server_socket.accept()
                print(f"新连接: {client_address}")
                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                client_thread.start()
            else:
                data = s.recv(1024)
                if not data:
                    inputs.remove(s)
                    s.close()


# 启动服务器，IP地址和端口号需要根据具体情况设置
start_server('192.168.108.129', 54321)
