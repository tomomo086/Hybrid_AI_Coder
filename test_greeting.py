# 挨拶アプリ

def greet(name):
    # 入力された名前に挨拶を返す
    return f"こんにちは, {name}さん！"

# ユーザーからの入力を取得
user_name = input("あなたの名前を入力してください: ")

# 関数呼び出しと結果の表示
print(greet(user_name))