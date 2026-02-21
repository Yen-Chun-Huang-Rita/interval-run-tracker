import time
import datetime
import csv
import os

def countdown_timer(seconds, phase_name):
    """倒數計時器"""
    print(f"\n--- 開始 {phase_name} ---")
    for i in range(seconds, 0, -1):
        print(f"{phase_name} 剩餘時間: {i} 秒", end="\r")
        time.sleep(1)
    print(f"\n{phase_name} 結束！\a") 

def log_workout(run_sec, rest_sec, sets, total_time):
    """將運動紀錄存入 CSV 檔案"""
    filename = 'workout_log.csv'
    file_exists = os.path.isfile(filename)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['日期', '跑步設定(秒)', '休息設定(秒)', '總組數', '總花費時間(秒)'])
        writer.writerow([date_str, run_sec, rest_sec, sets, total_time])
        
    print(f"\n✅ 您的運動紀錄已成功保存至 {filename}。")

def main():
    print("🏃 歡迎使用間歇跑訓練程式 🏃")
    print("-------------------------------")
    
    try:
        run_sec = int(input("請輸入單次「跑步」時間（秒）："))
        rest_sec = int(input("請輸入單次「休息/快走」時間（秒）："))
        sets = int(input("請輸入要進行的「組數」："))
    except ValueError:
        print("輸入錯誤！請輸入整數數字。")
        return

    print("\n準備開始訓練... (3秒後開始)")
    time.sleep(3)

    for i in range(1, sets + 1):
        print(f"\n=== 第 {i} 組 / 共 {sets} 組 ===")
        countdown_timer(run_sec, "🏃 高強度跑步")
        
        if i < sets:
            countdown_timer(rest_sec, "🚶 休息/快走")

    print("\n🎉 訓練完成！太棒了！辛苦了！")

    total_time = (run_sec * sets) + (rest_sec * (sets - 1))
    log_workout(run_sec, rest_sec, sets, total_time)

if __name__ == "__main__":
    main()
