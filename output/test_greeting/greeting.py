def greet(name):
    return f"こんにちは、{name} さん！"

if __name__ == "__main__":
    name = input("名前を入力してください：")
    print(greet(name))