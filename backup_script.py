import os
import shutil
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Hàm gửi mail (theo code bạn đã cho)
def send_email(sender, receiver, subject, body, password):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = message.as_string()
        server.sendmail(sender, receiver, text)
        print(f"Email đã được gửi đến: {receiver}")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")
    finally:
        server.quit()

# Hàm backup database
def backup_database():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # Đọc cấu hình từ .env
        sender_email = os.getenv('SENDER_EMAIL')
        app_password = os.getenv('APP_PASSWORD')
        receiver_email = os.getenv('RECEIVER_EMAIL')

        source_folder = 'databases'
        backup_folder = 'backup'

        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        files = [f for f in os.listdir(source_folder) if f.endswith('.sql') or f.endswith('.sqlite3')]

        if not files:
            raise Exception("Không có file .sql hoặc .sqlite3 nào để backup.")

        for file in files:
            src = os.path.join(source_folder, file)
            dest = os.path.join(backup_folder, f"{datetime.now().strftime('%Y%m%d_%H%M%S_')}{file}")
            shutil.copy2(src, dest)

        subject = "Backup Database Thành Công"
        body = f"✅ Backup database thành công lúc {now}.\nSố lượng file đã backup: {len(files)}."
        send_email(sender_email, receiver_email, subject, body, app_password)

    except Exception as e:
        subject = "Backup Database Thất Bại"
        body = f"❌ Backup database thất bại lúc {now}.\nLỗi: {e}"
        send_email(sender_email, receiver_email, subject, body, app_password)

# Main
if __name__ == "__main__":
    # Load biến môi trường
    load_dotenv()

    # Đặt lịch backup lúc 00:00 mỗi ngày
    schedule.every().day.at("00:00").do(backup_database)

    print("Đang chạy backup tự động...")

    while True:
        schedule.run_pending()
        time.sleep(60)  # kiểm tra mỗi phút