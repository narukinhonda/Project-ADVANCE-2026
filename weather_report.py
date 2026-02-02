
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

def main():
    # --- 1. 設定（APIの宛先） ---
    key = "46757fbd0d6c2147a57bd6057906d971"
    city, country = "Tokyo", "JP"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={key}&lang=ja&units=metric"

    # --- 2. 日付の取得と「名前」の作成（FinOpsの必須技術！） ---
    # datetime.now() で「今この瞬間」を取得し、
    # .strftime("%Y%m%d") で「20260125」のような8桁の数字に変換します
    today_str = datetime.now().strftime("%Y%m%d")
    
    # ファイル名に日付を埋め込みます（例：weather_20260125.png）
    image_file = f"weather_{today_str}.png"
    json_file = f"weather_{today_str}.json"

    # --- 3. 取得（通信エラー対策） ---
    try:
        response = requests.get(url)
        response.raise_for_status() # サーバーエラーがあればここでキャッチ
        jsondata = response.json()
    except Exception as e:
        print(f"通信エラーが発生しました: {e}")
        return

    # --- 4. 抽出（提督流：直感的な for ループ） ---
    times, temps = [], []
    for dat in jsondata["list"]:
        times.append(dat["dt_txt"])        # 時刻をリストへ
        temp_val = dat["main"]["temp"]
        temps.append(temp_val)            # 気温をリストへ

    # --- 5. 可視化（上司にそのまま出せるレポート品質） ---
    plt.figure(figsize=(12, 6)) # 横長にして見やすく
    
    # データをプロット（点と線を描く）
    plt.plot(times, temps, marker=".", color="#1f77b4", linewidth=2)
    
    # X軸の設定：8個おき（3時間×8＝24時間）にラベルを表示してスッキリ
    plt.xticks(times[::8], rotation=30, ha='right')
    
    # タイトルにも日付を自動で入れます
    plt.title(f"Weather Forecast: {city}, {country} (Created: {today_str})", fontsize=14)
    plt.ylabel("Temperature (°C)")
    plt.xlabel("Date & Time")
    plt.grid(axis='y', linestyle='--', alpha=0.7) # 横線のみの補助線
    plt.tight_layout() # 余白の自動調整（文字切れ防止）

    # --- 6. 保存（ここが自動化の肝です） ---
    # plt.show() で画面に出す前に、作成したファイル名で保存します
    plt.savefig(image_file, dpi=300) # 300dpiという高画質で保存
    
    # 生データも日付付きでバックアップ
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(jsondata, f, ensure_ascii=False, indent=4)

    print(f"--- 処理完了: 画像 '{image_file}' と JSON '{json_file}' を生成しました ---")
    
    # 最後に画面に表示
    plt.show()

# このプログラムが「直接実行された時」だけ main() を動かすおまじない
if __name__ == "__main__":
    main()
