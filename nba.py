import json
import random
import tkinter as tk
import pygame
from tkinter import simpledialog
from PIL import Image, ImageTk
from sys import exit

# 球員照片的資料庫
player_images = {
    1: {
        "Stephen Curry": "level/1/curry.jpg",
        "Devin Booker": "level/1/booker.jpg",
        "Kevin Durant": "level/1/durant.jpg",
        "James Harden": "level/1/harden.jpg",
        "Kobe Bryant": "level/1/kobe.jpg"
    },
    2: {
        "Tyler Herro": "level/2/herro.jpg",
        "Ja Morant": "level/2/ja.jpg",
        "Michael Jordan" :"level/2/jordan.jpg",
        "Klay Thompson" :"level/2/thompson.jpg",
        "Zach Lavine": "level/2/lavine.jpg",
        "Luka Doncic": "level/2/doncic.jpg",
        "Lebron James": "level/2/lebron.jpg"
        
    },
    3: {
        "Jayson Tatum": "level/3/tatum.jpg",
        "Jaylen Brown": "level/3/brown.jpg",
        "Jamal Murray": "level/3/murray.jpg",
        "Deandre Ayton": "level/3/ayton.jpg",
        "Derrick Rose": "level/3/rose.jpg",
        "Kyrie Irving": "level/3/irving.jpg",
    },
    4: {
        "Anthony Edwards": "level/4/edwards.jpg",
        "Anthony Davis": "level/4/davis.jpg",
        "Zion Williamson": "level/4/williamson.jpg",
        "Deaaron Fox":"level/4/fox.jpg",
        "Jalen Green": "level/4/green.jpeg",  
    },
    5: {
        "Nikola Jokic": "level/5/jokic.jpg",
        "Giannis Antetokounmpo": "level/5/antetokounmpo.jpg",
        "Kawhi Leonard": "level/5/leonard.jpg",
        "Shaquille Oneal": "level/5/oneal.jpg",
        "Austin Reaves": "level/5/reaves.jpg",
    }
}

def show_image():
    image_path = player_images[current_difficulty][current_player]
    image = Image.open(image_path)
    image = image.resize((700, 500))
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo

def check_answer():
    player_answer = entry.get()
    if player_answer == current_player:
        result_label.config(text="正確答案！", fg="green")
        next_player()
    else:
        error_counts[player_name] += 1
        result_label.config(text="答案錯誤！", fg="red")
        error_count_label.config(text=f"錯誤次數：{error_counts[player_name]}")


def next_player():
    global current_difficulty, current_player
    current_difficulty += 1
    if current_difficulty > 5:
        end_game()
    else:
        difficulty_label.config(text=f"難度：{current_difficulty}")
        current_player = random.choice(list(player_images[current_difficulty].keys()))
        entry.delete(0, tk.END) #刪除對話框線有文本
        result_label.config(text="")
        show_image()


def end_game():
    global window
    window.destroy()
    pygame.mixer.music.stop()
    window = tk.Tk()
    window.title("排行榜")
    window.geometry("1920x1080")
    RankBG = Image.open('background_set/Rank_BG.jpg')
    RankBG = RankBG.resize((1920, 1080))
    RankBG_photo = ImageTk.PhotoImage(RankBG)
    canvas = tk.Canvas(window, width=1920, height=1080, highlightthickness=0)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=RankBG_photo)

    title = tk.Label(window, text="排行榜", font=("Arial", 20))
    title.pack(pady=10)
    title.place(relx=0.5, rely=0.04, anchor=tk.CENTER)

    scores = sorted(error_counts.items(), key=lambda x: x[1])
    scores_text = ""
    rank = 1
    prev_errors = -1
    player_rank = 1
    for player, errors in scores:
        if errors != prev_errors:
            rank = scores.index((player, errors)) + 1
        if player == player_name:
            player_rank = rank
        if errors == 0:
            scores_text += f"{rank}. {player}: {errors} error\n"   
        else:
            scores_text += f"{rank}. {player}: {errors} errors\n"
        prev_errors = errors
    scores_label = tk.Label(window, text=scores_text, font=("Arial", 14))
    scores_label.pack(pady=60)
    scores_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
    player_rank_label = tk.Label(window, text=f"你排在第 {player_rank} 名", font=("Arial", 14))
    player_rank_label.pack(pady=10)
    player_rank_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    with open('error_counts.json', 'w') as file:
        json.dump(error_counts, file)
    window.mainloop()

def show_hint():
    num = random.choice([0, 1])
    hint = current_player.split()[num]
    tk.messagebox.showinfo("提示", "球員提示：" + hint)
    hint_button.config(state=tk.DISABLED)

def giveup():
    tk.messagebox.showinfo("警告", "已放棄遊戲(遜bad)")
    pygame.mixer.music.stop()
    window.destroy()

# 讀取錯誤次數紀錄檔案，如果檔案不存在則創建一個空字典
try:
    with open('error_counts.json', 'r') as f:
        try:
            error_counts = json.load(f)
        except json.JSONDecodeError:
            error_counts = {}
except FileNotFoundError:
    error_counts = {}

# 創建視窗
window = tk.Tk()
window.title("NBA猜名遊戲")
window.geometry("1920x1080")
pygame.init()
pygame.mixer.music.load('background_set/background_music.mp3')
pygame.mixer.music.play(-1)  # -1代表無限循環播放
background_image = Image.open('background_set/background.jpg')
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(window, width=1920, height=1080, highlightthickness=0)
canvas.pack()
background_label = canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
window.lower()

# 在遊戲開始時，請玩家輸入名字
player_name = simpledialog.askstring(
    "NBA猜名遊戲", 
    "1.此NBA猜名遊戲共有五個難度，答對會往下一個難度前進\n\n"
    "2.輸入時球員的姓和名需要大寫且中間要空格，輸入完按下enter即可\n\n"
    "3.有一次提示可以使用，提示球員名稱的姓或名\n\n"
    "4.按下放棄按鈕可以立即結束遊戲\n\n"
    "5.若通過五關則可以進入排行榜，排行榜以輸入錯誤次數進行排行\n\n"
    "6.請輸入你的名稱來開始遊戲:\n"
)

#cancel 要退出
if player_name is None:
    pygame.mixer.music.stop()
    window.destroy()
    exit()
error_counts[player_name] = 0

# 隨機選擇一位球員和難度
current_difficulty = 1
current_player = random.choice(list(player_images[current_difficulty].keys()))

# 放棄按鈕
giveup_buttton = tk.Button(window, text="放棄", command=giveup)
giveup_buttton.pack(pady=5)
giveup_buttton.place(relx=0.63, rely=0.7, anchor=tk.CENTER)

# 提示按鈕
hint_button = tk.Button(window, text="提示", command=show_hint)
hint_button.pack(pady=5)
hint_button.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

image_label = tk.Label(window)
image_label.pack(pady=50)
show_image()
canvas.create_window(610, 100, anchor=tk.NW, window=image_label)

#球員名字的輸入框
entry = tk.Entry(window, font=("Arial", 14))
entry.pack(pady=10)
entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
entry.bind('<Return>', lambda event=None: check_answer())

result_label = tk.Label(window, font=("Arial", 14))
result_label.pack(pady=10)

# 目前難度
difficulty_label = tk.Label(window, text=f"難度：{current_difficulty}", font=("Arial", 14))
difficulty_label.pack(pady=5)
difficulty_label.place(relx=0.5, rely=0.03, anchor=tk.CENTER)

# 錯誤次數
error_count_label = tk.Label(window, text="錯誤次數：0", font=("Arial", 14))
error_count_label.pack(pady=5)
error_count_label.place(relx=0.5, rely=0.64, anchor=tk.CENTER)

window.mainloop()
