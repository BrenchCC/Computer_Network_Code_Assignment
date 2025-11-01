# Message Board Client - 使用指南

## 项目文件说明

- **message_board_client.py**: 主客户端程序（作业提交文件）
- **test_server.py**: 测试服务器（用于本地测试，非作业要求）
- **readme.txt**: 英文说明文档（作业要求）
- **USAGE_GUIDE.md**: 中文使用指南（本文件）

## 快速开始

### 1. 测试环境准备

首先启动测试服务器（在一个终端窗口）：

```bash
python3 test_server.py -p 12345
```

### 2. 运行客户端

在另一个终端窗口运行客户端：

```bash
python3 message_board_client.py --host 127.0.0.1 --port 12345
```

或使用短选项：

```bash
python3 message_board_client.py -H 127.0.0.1 -p 12345
```

## 命令详细说明

### POST 命令 - 发布消息

```
> POST
Enter message content (end with '#' on a new line):
这是第一行消息
这是第二行消息
可以输入多行
#
OK
```

**注意事项：**
- 输入 `POST` 后按回车
- 继续输入消息内容，可以多行
- 单独一行输入 `#` 表示结束
- 服务器返回 `OK` 表示成功

### GET 命令 - 获取所有消息

```
> GET
ID: 0000
Time: 2025-10-21 14:30:15
Message:
这是第一行消息
这是第二行消息
可以输入多行
----------------------------------------
ID: 0001
Time: 2025-10-21 14:31:20
Message:
另一条消息
----------------------------------------
```

**注意事项：**
- 直接输入 `GET` 即可
- 显示所有历史消息
- 包含消息ID、时间戳和内容

### DELETE 命令 - 删除消息

```
> DELETE
Enter message IDs to delete (one per line, end with '#'):
0000
0001
#
OK
```

**注意事项：**
- 输入 `DELETE` 后按回车
- 每行输入一个消息ID
- 单独一行输入 `#` 表示结束
- 成功返回 `OK`，失败返回 `ERROR - Wrong ID`

### QUIT 命令 - 退出程序

```
> QUIT
OK
[INFO] Closing connection...
[INFO] Socket closed successfully
```

**注意事项：**
- 直接输入 `QUIT` 即可
- 服务器确认后自动关闭连接

## 命令行参数说明

### 必需参数

- `-H, --host`: 服务器IP地址或主机名
- `-p, --port`: 服务器端口号

### 可选参数

- `-b, --buffer-size`: 接收缓冲区大小（默认：4096字节）
- `-h, --help`: 显示帮助信息

### 使用示例

1. **连接到本地服务器：**
   ```bash
   python3 message_board_client.py -H 127.0.0.1 -p 12345
   ```

2. **连接到远程服务器：**
   ```bash
   python3 message_board_client.py -H 192.168.1.100 -p 8080
   ```

3. **使用自定义缓冲区：**
   ```bash
   python3 message_board_client.py -H localhost -p 9000 -b 8192
   ```

4. **查看帮助：**
   ```bash
   python3 message_board_client.py --help
   ```

## 代码结构说明

### 五大核心任务实现

#### 任务 1：套接字初始化
```python
def create_socket(self):
    """Initialize and create TCP socket."""
```
- 创建 TCP socket
- 错误处理和日志记录

#### 任务 2：发起连接请求
```python
def connect_to_server(self):
    """Establish connection to server."""
```
- 使用用户提供的 host 和 port
- 建立 TCP 连接
- 处理连接失败情况

#### 任务 3：向服务器发送命令
```python
def send_command(self, command):
    """Send command to server based on command type."""
```
- 处理不同命令类型（POST、GET、DELETE、QUIT）
- POST 和 DELETE 需要多行输入
- GET 和 QUIT 直接发送

#### 任务 4：接收服务器消息
```python
def receive_response(self, command):
    """Receive and process server response."""
```
- 根据命令类型处理不同响应
- POST：显示 OK
- GET：显示所有消息
- DELETE：显示 OK 或 ERROR
- QUIT：关闭连接

#### 任务 5：关闭套接字
```python
def close_socket(self):
    """Close socket connection."""
```
- 在 QUIT 命令后执行
- 清理资源
- 错误处理

## 代码质量特点

### 1. 模块化设计
- 主类 `MessageBoardClient` 包含所有核心功能
- 辅助方法处理具体细节
- 单一职责原则

### 2. 注释规范
- 所有函数都有英文文档字符串
- 说明参数、返回值和功能
- 关键代码段有行内注释

### 3. 变量命名
- 使用有意义的变量名（`host`, `port`, `buffer_size`）
- 遵循 Python 命名规范
- 避免无意义缩写

### 4. 错误处理
- 所有网络操作都有 try-except
- 检查函数返回值
- 友好的错误信息

### 5. 无全局变量
- 所有数据封装在类中
- 函数参数传递数据
- 避免命名冲突

## 测试步骤

### 完整测试流程

1. **启动服务器：**
   ```bash
   python3 test_server.py -p 12345
   ```

2. **启动客户端：**
   ```bash
   python3 message_board_client.py -H 127.0.0.1 -p 12345
   ```

3. **测试 POST 命令