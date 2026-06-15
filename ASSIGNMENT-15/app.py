import sys
from datetime import datetime
from zoneinfo import ZoneInfo

now = datetime.now(ZoneInfo("Asia/Kolkata"))

print("=" * 50)
print(f"Python Version : {sys.version}")
print(f"Current Date   : {now.strftime('%Y-%m-%d')}")
print(f"Current Time   : {now.strftime('%H:%M:%S')}")
print("=" * 50)