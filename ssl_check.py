import ssl
import socket
import yaml
import datetime
import smtplib
from email.mime.text import MIMEText

with open("config.yaml") as f:
    config = yaml.safe_load(f)

ALERT_DAYS = config["alert_before_days"]
DOMAINS = config["domains"]
EMAIL = config["email"]

def get_ssl_expiry(domain):
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            expiry_str = cert['notAfter']
            expiry_date = datetime.datetime.strptime(
                expiry_str, "%b %d %H:%M:%S %Y %Z"
            )
            return expiry_date

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "⚠ SSL Certificate Expiry Alert"
    msg["From"] = EMAIL["sender"]
    msg["To"] = EMAIL["receiver"]

    server = smtplib.SMTP(EMAIL["smtp_server"], EMAIL["smtp_port"])
    server.starttls()
    server.login(EMAIL["sender"], EMAIL["app_password"])
    server.send_message(msg)
    server.quit()

def main():
    today = datetime.datetime.utcnow()
    alerts = []

    for domain in DOMAINS:
        try:
            expiry = get_ssl_expiry(domain)
            days_left = (expiry - today).days

            print(f"{domain} expires in {days_left} days")

            if days_left <= ALERT_DAYS:
                alerts.append(f"{domain} expires on {expiry.date()} ({days_left} days left)")
        except Exception as e:
            alerts.append(f"{domain} - ERROR: {str(e)}")

    if alerts:
        message = "\n".join(alerts)
        send_email(message)
        print("Alert email sent")
    else:
        print("All certificates healthy")

if __name__ == "__main__":
    main()
