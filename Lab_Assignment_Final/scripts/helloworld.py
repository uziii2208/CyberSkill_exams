import os
import psutil
import time
import gzip
import shutil
import logging
from collections import Counter
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib

# Tải các biến môi trường từ file .env
load_dotenv()

# Các thư mục và file log đầu ra
LOG_DIR = "logs"
ACCESS_LOG_FILE = os.path.join(LOG_DIR, "access.log") # File log truy cập
CPU_MEM_LOG_FILE = os.path.join(LOG_DIR, "cpu_mem_usage.log") # File log sử dụng CPU và RAM
ANALYZED_LOG_FILE = os.path.join(LOG_DIR, "analyzed_log.log") # File log phân tích
COMPRESSED_LOG_FILE = os.path.join(LOG_DIR, "daily_logs.gz") # File log nén hàng ngày
EMAIL_LOG_FILE = os.path.join(LOG_DIR, "email_notifications.log") # File log thông báo email

# Ngưỡng tỉ lệ lỗi để gửi thông báo qua email
ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 0.1))

# Cấu hình email từ các biến môi trường
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Cấu hình ghi log
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "script.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_email_notification(subject, body):
    """
    Sends an email notification with user-provided credentials.
    """
    try:
        if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SENDER_EMAIL, RECEIVER_EMAIL]):
            logging.error("SMTP configuration is incomplete. Email will not be sent.")
            return

        # Create the email message
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        logging.info(f"Email sent: {subject}")
        print("Email sent successfully.")

    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        print(f"Failed to send email: {e}")
        raise

# Monitor CPU and memory usage
def monitor_cpu_memory():
    try:
        with open(CPU_MEM_LOG_FILE, "a") as f:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            log_entry = f"CPU: {cpu_usage}% | Memory: {memory_usage}%\n"
            f.write(log_entry)
            logging.info(f"Logged CPU and memory usage: {log_entry.strip()}")
    except Exception as e:
        logging.error(f"Error monitoring CPU and memory usage: {e}")

# Compress log file daily
def compress_logs():
    try:
        with open(CPU_MEM_LOG_FILE, "rb") as f_in, gzip.open(COMPRESSED_LOG_FILE, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        open(CPU_MEM_LOG_FILE, "w").close()  # Clear original log file
        logging.info("Logs compressed successfully.")
    except Exception as e:
        logging.error(f"Error compressing logs: {e}")

# Analyze access logs from file
def analyze_access_logs():
    try:
        if not os.path.exists(ACCESS_LOG_FILE):
            logging.warning("Access log file not found.")
            return

        with open(ACCESS_LOG_FILE, "r") as f:
            logs = f.readlines()

        ip_counter = Counter()
        endpoint_counter = Counter()
        total_requests = 0
        error_count = 0

        for log in logs:
            total_requests += 1
            parts = log.split()
            if len(parts) < 9:
                continue

            ip = parts[0]
            endpoint = parts[6]
            status_code = parts[8]

            ip_counter[ip] += 1
            endpoint_counter[endpoint] += 1

            if status_code.startswith("4") or status_code.startswith("5"):
                error_count += 1

        error_rate = error_count / total_requests if total_requests > 0 else 0

        # Generate insights
        insights = {
            "top_ips": ip_counter.most_common(5),
            "top_endpoints": endpoint_counter.most_common(5),
            "error_rate": error_rate
        }

        with open(ANALYZED_LOG_FILE, "w") as f:
            f.write(f"Top IPs: {insights['top_ips']}\n")
            f.write(f"Top Endpoints: {insights['top_endpoints']}\n")
            f.write(f"Error Rate: {insights['error_rate'] * 100:.2f}%\n")

        logging.info(f"Log analysis complete. Insights: {insights}")

        # Send email if error rate exceeds threshold
        if error_rate > ERROR_RATE_THRESHOLD:
            subject = "High Error Rate Alert"
            body = (
                f"The error rate in web server logs has exceeded the threshold of {ERROR_RATE_THRESHOLD * 100:.2f}%\n"
                f"Current Error Rate: {error_rate * 100:.2f}%\n"
                f"Check the analyzed log file for details: {ANALYZED_LOG_FILE}"
            )
            send_email_notification(subject, body)
    except Exception as e:
        logging.error(f"Error analyzing access logs: {e}")

# Worker function to repeatedly monitor CPU and memory
def monitor_worker():
    github_info = "GitHub : https://github.com/uziii2208"
    print(github_info)
    while True:
        for i in range(4):  # Cycle through "..."
            dots = "." * i
            print(f"\rScript is running{dots}   \r", end="")
            time.sleep(0.5)
        monitor_cpu_memory()
        time.sleep(60 - 2)  # Adjust for inner sleep timing

if __name__ == "__main__":
    try:
        from multiprocessing import Process

        # Start CPU and memory monitoring in a separate process
        monitor_process = Process(target=monitor_worker)
        monitor_process.start()

        # Run compression and analysis every 24 hours
        while True:
            time.sleep(86400)  # Wait 24 hours = 86400 seconds
            compress_logs()
            analyze_access_logs()

    except KeyboardInterrupt:
        if monitor_process:
            monitor_process.terminate()
        logging.info("Script terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
