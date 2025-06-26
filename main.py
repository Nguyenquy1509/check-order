import requests
from bs4 import BeautifulSoup
import time

COOKIE = "_ga=GA1.1.1691476287.1720638186; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InZQa0pMWVF0Y0VmdkJiQ0I2MkxIZ3c9PSIsInZhbHVlIjoiVzlWMTQ4OXRtWEZPTW02ck5FbFM0eU9GaEFEUnk5OG1sOU1xakRFQ3BVZnlQTkxHWERxU0pkV1EyL1pDdm1PTjI2dGVHaHB6WTdnN0pjZWVIdEwzeWoxM1hXMjF6ZFFWamVaWWZXa1hjNGw3OHR0TTk5NktBcVRPdEw1RWxvSHdBVE5lVTAwQTdqZlZQUG1yWUlxTHRXbDYwMGc5Z1dmWWtkN0o2WnlWckl2RUVjNzc4MGY3K2d2c05udk5GSE5vVVpjS1M3WThjWVJHYk9Yd3hWZXNlUFNGU1J3bFJMMnAvVUJobDRvcFFpZz0iLCJtYWMiOiI3Mjc4ZWM5OGMxNjE4YzZlZTRkYWJlYmE0MGIwZjNiMWJjM2E5OTg3ZWMzNDIwOThlM2QxZjQ1MDRlNTFlZWVjIn0%3D; _gcl_au=1.1.1493105183.1744235302; PHPSESSID=sds2ndp3khngjorvdmlhut4p90; XSRF-TOKEN=eyJpdiI6InpqMmQvcEJXb2ZqZ0NOdzZCVEo3UEE9PSIsInZhbHVlIjoiNUVnRDhROE11WHlRcngwYmp6VXRvbW9KcmZ0V05jRW05V0xtOFgybzR1ak4rWTFPVi93TU9jN0pZZG9BV1FuMW1pRWhsSExwZVVlOHJ1WXZ4RGRiVEJ4enl6b1h5aTZGaGFjTkdSYVd4LzAxK2NDUHBTZlZJWmZXWWZ1eCtmRFEiLCJtYWMiOiI3NWVhNDcwYzUxM2I5OTZlYzNkZTQwNTIyYzkyZGM0NDc5ZTExYzVhZTVhOWNjYjFlOTU0ZDVmMTk2YmIwYjA4In0%3D; laravel_session=eyJpdiI6InA2ZXlTMlJrNEIwaWJFbVJYakFiU3c9PSIsInZhbHVlIjoiRTVSS3RJV0NqdGdqa0NmbVhLeHlKY0lmMDl3OXpUTlE4VDVVbUZGaVVmcCtzL2wvUjF3dDFDNC9ObWUzWlVMSVA5Q3NkUHF5SG0ybTkwbEJ2ZFZWMjhhZExpcUpMSFkvN09xT21XNTZBNDVESTdEcmRIaURkS0NZRTV1a2RjU1giLCJtYWMiOiIzNTgzZTVlYjc2Njk0MDcyOWQ1YWJhMWJmM2UzNDY2NTFhN2E5YjQyYjhmOGIxYjQ0Nzc2ODVmYjBjNGY2MmZlIn0%3D; _ga_VVJV46RGMW=GS2.1.s1750904046$o1046$g1$t1750908483$j59$l0$h0; _ga_Z01XXVF947=GS2.1.s1750904046$o1041$g1$t1750908483$j59$l0$h0"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://wutheringshop.vn/user/history/money",
    "Origin": "https://wutheringshop.vn",
    "Cookie": COOKIE
}

def send_to_discord(acc_id, amount, time_str, discord_user_id):
    webhook_url = "https://discord.com/api/webhooks/1387637043563331594/wti2TT1ro7KsyjQ_jVyB_43UhSmo_xYxMy5r3dCSfYWKUNi6r3onKKFYn4u_FdkoNTq_"
    message = (
        f"🛒 **Đã bán acc `#{acc_id}`** lúc **{time_str}**\n"
        f"💰 Giá: `{amount}`\n"
        f"👤 <@{799655734395535360}>"
    )
    requests.post(webhook_url, json={"content": message})


last_seen_id = None  # Giao dịch mới nhất đã thấy

def check_new_orders():
    global last_seen_id

    res = requests.get("https://wutheringshop.vn/user/history/money", headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table tbody tr")

    if not rows:
        print("⚠️ Không tìm thấy giao dịch.")
        return

    first_row = rows[0].find_all("td")
    trans_id = first_row[0].text.strip()
    amount = first_row[1].text.strip()
    content = first_row[3].text.strip()
    acc_type = first_row[4].text.strip()
    time_str = first_row[5].text.strip()

    if trans_id != last_seen_id:
        if "mua tài khoản" in content.lower():
            # Lấy mã acc được bán từ nội dung
            acc_code = content.split("#")[1].split(" ")[0]
            print(f"🛒 Đã bán acc #{acc_code} ({acc_type}) lúc {time_str} — Số tiền: {amount}")
            send_to_discord(acc_code, amount, time_str, 799655734395535360)  # Thay bằng user_id của bạn
        else:
            print(f"ℹ️ Giao dịch mới không phải bán acc: {content}")

        last_seen_id = trans_id
    else:
        print("✅ Không có giao dịch mới.")

# Kiểm tra mỗi 60 giây
while True:
    check_new_orders()
    time.sleep(30)

