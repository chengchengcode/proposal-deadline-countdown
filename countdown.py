import tkinter as tk
import pytz
from datetime import datetime, timedelta

# 设置各个截止日期和时区
deadlines = {
    "TAP": ("23:59 19 September 2024", "Asia/Shanghai", "Comments"),
    "ESO": ("12:00 26 September 2024", "Europe/Berlin", "Comments"),
    "GTC": ("17:00 30 September 2024", "Asia/Shanghai", "Comments"),
    "Gemini/Chile": ("23:59 30 September 2024", "Chile/Continental", "Comments"),
    "Gemini/US": ("23:59 30 September 2024", "America/Denver", "Comments"),
    "JWST": ("20:00 16 October 2024", "America/New_York", "Comments"),
}

def format_time(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} day, {hours:02}:{minutes:02}:{seconds:02}"

def update_countdown():
    current_time = datetime.now(pytz.utc)
    
    for name, (target_time_str, target_tz_str, comment) in deadlines.items():
        target_tz = pytz.timezone(target_tz_str)
        target_time = target_tz.localize(datetime.strptime(target_time_str, "%H:%M %d %B %Y"), is_dst=None)
        remaining_time = target_time - current_time.astimezone(target_tz)

        countdown_label = countdown_labels[name]
        comment_label = comment_labels[name]

        if remaining_time <= timedelta(0):
            countdown_label.config(text=f"{name:<{max_length}} : 0 day, 00:00:00", fg="grey", font=("Courier New", 24, "overstrike"))
            comment_label.config(text=comment, font=("Courier New", 24, "overstrike"))
        else:
            countdown_label.config(text=f"{name:<{max_length}} : {format_time(remaining_time)}", fg="black")
            comment_label.config(text=comment)

            if remaining_time < timedelta(days=1):
                countdown_label.config(fg="darkred")
            elif remaining_time < timedelta(weeks=1):
                countdown_label.config(fg="#003DA5")

    window.after(1000, update_countdown)

# 计算最长望远镜名字的长度
max_length = max(len(name) for name in deadlines.keys()) + 5  # 增加一些额外的空白

# 创建窗口
window = tk.Tk()
window.title("2025A Deadlines Countdown")

countdown_labels = {}
comment_labels = {}

# 为每个截止日期创建标签
for name in deadlines.keys():
    countdown_frame = tk.Frame(window)
    countdown_frame.pack(pady=2)  # 紧凑的间距
    countdown_label = tk.Label(countdown_frame, font=("Courier New", 24))  # 使用等宽字体
    countdown_label.pack(side=tk.LEFT)
    countdown_labels[name] = countdown_label

    comment_label = tk.Label(countdown_frame, font=("Courier New", 24))  # 使用相同的等宽字体
    comment_label.pack(side=tk.LEFT, padx=(10, 0))  # 左侧间距
    comment_labels[name] = comment_label

update_countdown()
window.mainloop()
