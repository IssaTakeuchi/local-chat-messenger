import socket
import os
from faker import Faker

# UNIXソケットをストリームモードで作成
sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

fake = Faker()

server_address = '/tmp/socket_file'

# 以前の接続が残っている場合に備えて、サーバアドレスをアンリンク（削除）する
try:
    os.unlink(server_address)
# サーバアドレスが存在しない場合は例外を無視する
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

# サーバーアドレスにソケットをバインド（接続）する
sock.bind(server_address)

# ソケットが接続要求するようにする
sock.listen(1)

# 無限ループでクライアントからの接続を待ち続ける
while True:
    # クライアントからの接続を受け入れます
    connection,client_address = sock.accept()

    try:
        print('connection from',client_address)

        while True:
            # ここでサーバは接続からデータを読み込む
            # 16は一度に読み込む最大バイト数
            data = connection.recv(16)
            # 受け取ったデータはバイナリ形式なので、それを文字列に変換する
            data_str = data.decode('utf-8')

            # 受け取ったデータを表示
            print('Received ' + data_str)
            
            # もしデータがあれば、以下の処理をする
            # 処理したメッセージをクライアントに送り返す
            # ここでメッセージをバイナリ形式（エンコード）に戻してから送信する
            if data:
                if data_str == "address":
                    response = 'Processing' + fake.address()
                    connection.sendall(response.encode())
                elif data_str == 'name':
                    response = 'Processing' + fake.name()
                    connection.sendall(response.encode())
                elif data_str == 'text':
                    response = 'Processing' + fake.text()
                    connection.sendall(response.encode())

            # クライアントからデータが送られてこなければ、ループを終了する
            else:
                print('no data from',client_address)
                break
            
    # 最終的に接続を閉じる
    finally:
        print("Closing current connection")
        connection.close()