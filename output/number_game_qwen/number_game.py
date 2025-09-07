import random
# 1から100までのランダムな数字を生成
secret_number = random.randint(1, 100)
# ユーザーの入力を受け取る関数
def get_user_guess():
    while True:
        try:
            guess = int(input("1から100までの数字を当ててください: "))
            if 1 <= guess <= 100:
                return guess
            else:
                print("1から100までの範囲で入力してください。")
        except ValueError:
            print("数字を入力してください。")
# ゲームのメインループ
def play_game():
    attempts = 0
    while True:
        guess = get_user_guess()
        attempts += 1
        if guess < secret_number:
            print("もっと大きい数字です。")
        elif guess > secret_number:
            print("もっと小さい数字です。")
        else:
            print(f"正解です！あなたは{attempts}回で数字を当てました。")
            break
# ゲームの開始
play_game()