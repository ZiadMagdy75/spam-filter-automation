import subprocess
import time
from datetime import datetime


while True:
    print(f"\n============================")
    print(f" Spam Filter check started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
 
    subprocess.run(["python", "classify_emails.py"])
    
    print(f"Done. Next check after 6 hours.")
    print("============================\n")
    
    time.sleep(6 * 60 * 60)
