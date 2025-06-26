import requests
from bs4 import BeautifulSoup
import time
import os

COOKIE = os.environ.get("COOKIE")

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://wutheringshop.vn/user/history/money",
    "Origin": "https://wutheringshop.vn",
    "Cookie": COOKIE
}

def check_new_order():
    res = requests.get("https://wutheringshop.vn/user/history/money", headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table tbody tr")
    if not rows:
        print("❌ Không có đơn nào.")
        return
    row = rows[0].find_all("td")
    id_ = row[0].text.strip()
    amount = row[1].text.strip()
    content = row[3].text.strip()
    time_ = row[5].text.strip()
    if "mua tài khoản" in content.lower():
        acc_id = content.split("#")[1].split(" ")[0]
        print(f"🛒 Đã bán acc #{acc_id} lúc {time_} — Giá: {amount}")
    else:
        print(f"ℹ️ Giao dịch khác: {content}")

# 💫 Lặp vô hạn 5 phút/lần
while True:
    check_new_order()
    print("🕒 Đợi 30s kiểm tra lại...\n")
    time.sleep(30)
