udpclient.py
作用：实现UDP客户端，模拟TCP的三次握手和四次挥手，发送请求包，接收服务器响应，并计算RTT。
运行环境：win11pycharm，python3.10
配置选项：运行时需提供服务器IP和端口，如：python udpclient.py <server_ip> <server_port>

udpserver.py
作用：实现UDP服务器，处理客户端连接请求，模拟丢包并返回响应包。
运行环境：Ubuntu，pycahrm，python3.8
配置选项：需要在code中修改指定本机的serverIp