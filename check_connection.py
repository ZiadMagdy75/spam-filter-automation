import imaplib
import email
from email.header import decode_header

EMAIL_USER = "magdyzeyad54@gmail.com"
EMAIL_PASS = "sjwjinfqpzyizrcj"
IMAP_SERVER = "imap.gmail.com"

def connect_gmail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    print("[+] Login successful!")
    return mail

def fetch_inbox(mail):
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    print(f" Found {len(mail_ids)} messages in inbox.")

    for i in mail_ids[-5:]:
        status, data = mail.fetch(i, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")
        print(f" - {subject}")

    mail.logout()

if __name__ == "__main__":
    mail = connect_gmail()
    fetch_inbox(mail)
