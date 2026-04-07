import time
import urllib.request
import random

WAF_TARGET = "http://waf-engine:8081"

# The attack payload generator pretending to be Anonymous
payloads = [
    "/index.php", # Normal traffic
    "/login.php",
    "/index.php?id=1 UNION SELECT * FROM users", # SQLi
    "/search?q=<script>alert(1)</script>", # XSS
    "/images/../../../../etc/passwd", # LFI
    "/api/data?token=A3f9", 
    "/admin.php?agent=nikto" # Scanner bot
]

def fire_payload():
    path = random.choice(payloads)
    url = f"{WAF_TARGET}{path}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            print(f"[ATTACK BOT] Miss -> {path} (Allowed, {resp.status})")
    except Exception as e:
        print(f"[ATTACK BOT] Blocked by WAF -> {path} ({e})")

if __name__ == "__main__":
    print("Autonomous Attack Simulator Started! Blasting WAF every 15 seconds.")
    time.sleep(10) # Wait for infrastructure to load
    while True:
        fire_payload()
        time.sleep(15)
