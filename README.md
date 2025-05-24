# local-chat-messenger
---
### 【概要】

サーバーとクライアントでソケット通信を行う。
クライアントの入力に応じて、サーバーがメッセージを返す。

メッセージの生成は、pythonのfakerパッケージを使用。ランダムに、name,address,textを生成し、ユーザーに返す。

## 【実施手順】
1.先に「local_chat_server.py」を実行。

2.その後「local_chat_client.py」を別ターミナルで実行し、name,address,textのいずれかを入力。
