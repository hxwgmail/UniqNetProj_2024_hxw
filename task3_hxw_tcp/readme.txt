1.reversetcpclient.py
	作用：实现TCP客户端，读取input_file.txt并分块发送文件内容到服务器，接收反转后的数据并保存。
	运行环境：win11pycharm，python3.10
	配置选项：运行时需提供服务器IP、端口、文件路径、最小块大小和最大块大小，如：python reversetcpclient.py <server_ip> <server_port> <file_path> <Lmin> <Lmax>

2.reversetcpserver.py
	作用：实现TCP服务器，接收客户端发送的文件块，反转后返回给客户端。
	运行环境：Ubuntu，pycahrm，python3.8
	配置选项：无需命令行参数，直接运行即可。

