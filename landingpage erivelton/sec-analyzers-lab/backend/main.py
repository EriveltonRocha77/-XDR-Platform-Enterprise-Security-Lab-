from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
import datetime
import subprocess
import advanced_engines

app = FastAPI(title="XDR SIEM Core", description="Threat Intelligence & Correlation Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

time_series_db = []

@app.post("/api/v1/ingest")
async def ingest_telemetry(request: Request):
    payload = await request.json()
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.now().isoformat(),
        "engine": payload.get("engine", "UNKNOWN_SENSOR"),
        "severity": payload.get("severity", "LOW"),
        "data": payload
    }
    time_series_db.append(event)
    print(f"[SIEM INGEST] {event['severity']} alert registered from {event['engine']}")
    return {"status": "indexed", "event_id": event["event_id"]}

@app.get("/api/v1/threats")
async def get_threats():
    return {
        "status": "operational",
        "total_events": len(time_series_db),
        "incidents": sorted(time_series_db, key=lambda x: x["timestamp"], reverse=True)
    }

@app.get("/api/v1/run/{module}")
async def run_module(module: str, target: str = ""):
    targets = {
        "sast": "/lab_root/tests/vuln_app.py",
        "dast": "http://waf-engine:8081",
        "cloud": "/lab_root/tests/bad_pod.yaml"
    }
    
    cmd_target = target if target else targets.get(module, "")
    script_path = f"/lab_root/{module}/engine.py" if module == "sast" else f"/lab_root/{module}/scanner.py" if module == "dast" else f"/lab_root/cloud/checker.py"
    
    try:
        if module in ["sast", "dast", "cloud"]:
            cmd = ["python", script_path, cmd_target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = result.stdout if result.stdout else result.stderr
        elif module == "dns": output = advanced_engines.detect_dns_tunnel(target)
        elif module == "bloodhound": output = advanced_engines.attack_path_mapper(target)
        elif module == "phishing": output = advanced_engines.analyze_phish(target)
        elif module == "endpoint": output = advanced_engines.check_anomaly(target)
        elif module == "ioc": output = advanced_engines.correlate_iocs(target)
        elif module == "ai-soc": output = advanced_engines.ai_analyze(target)
        elif module == "memory": output = advanced_engines.memory_scan(target)
        elif module == "rasp": output = advanced_engines.run_rasp_sandboxed(target)
        elif module == "network": output = advanced_engines.network_hunter(target)
        elif module == "exploit": output = advanced_engines.exploit_lab(target)
        elif module == "honeypot": output = advanced_engines.honeypot_status(target)
        elif module == "darkweb": output = advanced_engines.dark_web_monitor(target)
        elif module == "firmware": output = advanced_engines.firmware_scanner(target)
        elif module == "decoder": output = advanced_engines.recursive_decoder(target)
        elif module == "crack":
            cracking_logic = "import sys, hashlib\nhsh=sys.argv[1]\nwords=['123456','admin','password','qwerty', 'root', 'cyber']\nprint(f'[+] Loaded {len(words)} common passwords from dict.')\nfor w in words:\n  if hashlib.md5(w.encode()).hexdigest()==hsh:\n    print(f'[!] CRACKED! Password is: {w}')\n    sys.exit(0)\nprint('[-] Hash not found in short dictionary.')"
            cmd = ["python", "-c", cracking_logic, target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            output = result.stdout if result.stdout else result.stderr
        else:
            output = "Error: Engine module not mapped in Backend Orchestrator."
            
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}
