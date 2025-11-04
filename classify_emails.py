import imaplib
import email
from email.header import decode_header
from joblib import load
import re
import time

EMAIL_USER = "magdyzeyad54@gmail.com"
EMAIL_PASS = "sjwjinfqpzyizrcj"
IMAP_SERVER = "imap.gmail.com"

vectorizer = load("vectorizer.pkl")
model = load("model.pkl")

def clean_text(s):
    if not isinstance(s, str): return ""
    s = s.lower()
    s = re.sub(r"http\S+|www\.\S+", " URL ", s)
    s = re.sub(r"\d+", " NUM ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def connect_gmail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    print("[+] Connected to Gmail.")
    return mail

def get_inbox_messages(mail, limit=20):
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")  
    mail_ids = messages[0].split()
    
    print(f" Found {len(mail_ids)} unread messages.")

    for i in mail_ids[-limit:]:
        status, data = mail.fetch(i, "(RFC822)")

        if not data or not data[0]:
            print(" Skipping an empty message...")
            continue

        msg = email.message_from_bytes(data[0][1])

        subject, enc = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(enc or "utf-8", errors="ignore")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body += part.get_payload(decode=True).decode(errors="ignore")
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            except:
                pass

        full_text = clean_text(subject + " " + body)
        X = vectorizer.transform([full_text])
        pred = model.predict(X)[0]

        print(f"\n Subject: {subject[:70]}")
        print(f" → Prediction: {pred}")

        if pred.lower() == "spam":
            move_to_spam(mail, i)
            print("  Moved to Spam Folder")

    mail.logout()
    print("\n Done checking messages.")

def move_to_spam(mail, msg_id):
    mail.copy(msg_id, "[Gmail]/Spam")
    mail.store(msg_id, '+FLAGS', '\\Deleted')
    mail.expunge()

if __name__ == "__main__":
    mail = connect_gmail()
    get_inbox_messages(mail, limit=50)
