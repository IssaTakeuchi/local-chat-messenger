import socket
import sys

def get_valid_user_messege():
    # ユーザーから｛name,text,address｝のいずれかの入力のみ受け付ける
    allowed_message = ["name","address","text"]

    # ユーザーに入力を促す
    while True:
        user_input = input(f"以下のいずれかを入力してください。({','.join(allowed_message)}):").strip().lower()

        if user_input in allowed_message:
            return user_input
        else:
            print(f"エラー： '{user_input}'は無効な入力です。'{','.join(allowed_message)}'のいずれかを入力してください。")

# TCP/IPソケットを作成する
sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

# サーバが待ち受けている特定の場所にソケットを接続
server_address = '/tmp/socket_file'
print('connecting to {}'.format(server_address))

# サーバに接続を試みます
# 問題があればエラーメッセージを表示してプログラムを終了
try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    # プログラムをすぐに終了
    sys.exit(1)

# サーバに接続できたら、サーバにメッセージを送信します
try:
    # ユーザーからの入力を待ちます
    # utf-8でエンコードしてサーバに送信
    message = get_valid_user_messege()
    sock.sendall(message.encode('utf-8'))

    # サーバからの応答を待つ時間を2秒間に設定します。
    sock.settimeout(2)

    # サーバからの応答を待ち、応答があればそれを表示する
    try:
        while True:
            # 受け取るデータの最大量は1024バイトとする
            data = sock.recv(1024)

            # もしデータがあれば、それを表示しなければループ終了
            if data:
                print('Server response: ' + data.decode('utf-8'))
            else:
                break

    # 2秒間サーバからの応答がなければ、タイムアウトエラーとなり、エラーメッセージを表示
    except(TimeoutError):
        print('Socket timeout, ending listenig for server message')

# 全ての操作が完了したら、最後にソケットを閉じて通信を終了
finally:
    print('closing socket')
    sock.close()

