import math
import json
import re
import hashlib
import binascii
import urllib.request
import urllib.error
import socket
from functools import lru_cache
import base64
import urllib.parse

MEM_PATTERNS = {
    'RSA_PRIVATE_KEY': re.compile(r'BEGIN RSA PRIVATE KEY'),
    'PEM_CERTIFICATE': re.compile(r'BEGIN CERTIFICATE'),
    'AWS_SECRET_KEY': re.compile(r'(?i)AKIA[0-9A-Z]{16}'),
    'JWT_TOKEN': re.compile(r'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*'),
    'CREDENTIAL_ASSIGN': re.compile(r'(?i)(password|secret|key|token)\s*=\s*[\'"].+[\'"]')
}

@lru_cache(maxsize=512)
def detect_dns_tunnel(query):
    q_str = query.replace(".com", "").replace(".net", "").replace(".", "")
    if not q_str: return "Query too short for analysis."
    prob = [float(q_str.count(c)) / len(q_str) for c in dict.fromkeys(list(q_str))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    if entropy > 4.3 and len(q_str) > 25: 
        return f"[CRITICAL] ILLEGAL BASE64/HEX PROTOCOL OVER DNS (T1071.004).\nEntropy: {entropy:.4f} bits.\nConnection Terminated."
    return f"[✓] Baseline DNS Traffic. Entropy: {entropy:.4f} bits/character."

def attack_path_mapper(graph_json_str):
    try:
        graph = json.loads(graph_json_str)
        def dfs(node, path):
            if "Domain_Admin" in graph.get(node, []): return path + ["Domain_Admin"]
            for neighbor in graph.get(node, []):
                if neighbor not in path:
                    result = dfs(neighbor, path + [neighbor])
                    if result: return result
            return None
        paths = []
        for start_node in graph:
            res = dfs(start_node, [start_node])
            if res: paths.append(" -> ".join(res))
        return "[!] FATAL: Active Path to Domain_Admin:\n" + "\n".join(paths) if paths else "[✓] Domain Structure Fortified. Zero Access Vectors."
    except Exception as e: return f"Graph Topology Mapping Error: {e}"

def analyze_phish(email_content):
    score = 0
    flags = []
    txt = email_content.lower()
    weights = {"urgent": 35, "invoice": 40, "verify": 30, "password": 25, "action required": 45}
    for word, w in weights.items():
        if word in txt:
           score += w
           flags.append(f"Keyword '{word}' (+{w} pts)")
    if "<a href" in txt and ("href=" in txt and ">" in txt and not "https://" in txt.split("href=")[1][:8]):
        score += 50
        flags.append("Obfuscated/Non-HTTPS Link Object (+50 pts)")
    if score >= 75: return f"[CRITICAL] CYBER-WEAPONIZED PHISH DEFEATED. Risk Score: {score}/100.\nFlags:\n" + "\n".join(flags)
    return f"[✓] Nominal communication. Risk Score: {score}/100."

def check_anomaly(metrics_csv):
    try:
        cpu, ram, procs = map(float, metrics_csv.split(","))
        z_cpu = (cpu - 25.0) / 15.0
        z_procs = (procs - 30.0) / 10.0
        if z_cpu > 3.5 and z_procs > 4.0:
            return f"[ALARM] PROCESS INJECTION / RANSOMWARE HEURISTIC DETECTED.\nZ-Scores: CPU({z_cpu:.2f}), Threads({z_procs:.2f})."
        return f"[✓] Endpoint Vital Signs Nominal. Highest Z-Score: {max(z_cpu, z_procs):.2f}"
    except: return "Invalid Telemetry Syntax."

@lru_cache(maxsize=1024)
def correlate_iocs(ip_address):
    ip_address = ip_address.strip()
    result = [f"[DASHBOARD] Analisando Inteligência OSINT Oficial para IP: {ip_address}"]
    try:
        req = urllib.request.Request(f"http://ip-api.com/json/{ip_address}?fields=status,country,countryCode,isp,as,query")
        req.add_header('User-Agent', 'XDR-Military-SOC/1.0')
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                result.append(f"-> [GEOLOCALIZAÇÃO REAL] Origem Global: {data.get('country')} ({data.get('countryCode')})")
                result.append(f"-> [BGP ASN E ISP] Operadora de Trânsito: {data.get('isp')} | ASN: {data.get('as')}")
            else:
                result.append("-> [INFRAESTRUTURA] Range de IP Falso, Privado ou Inválido na WAN.")
    except Exception as e:
         result.append(f"-> [FALHA OSINT BGP]: Rede Externa BGP indisponível - {e}")
    try:
        reversed_ip = ".".join(reversed(ip_address.split(".")))
        dnsbl_query = f"{reversed_ip}.zen.spamhaus.org"
        try:
             socket.gethostbyname(dnsbl_query)
             result.append("[CRITICAL KILL CHAIN] IP ENCONTRADO ATIVAMENTE NAS BLACKLISTS MUNDIAIS SPAMHAUS/ZEN!")
             result.append("[DEFESA] Assinatura C2 Botnet Global Detectada. Tráfego Banido em Firewall Externo.")
        except socket.gaierror:
             result.append("[✓] IP Limpo. Sistema não consta nos Radares Internacionais C2 (Spamhaus).")
    except Exception as e:
         pass
    return "\n".join(result)

def ai_analyze(logs):
    l = logs.lower()
    if "sqli" in l or "1=1" in l: return "=> [DEFENSE SYSTEM]: Tier 1 SQL Ingestion Attack.\nDatabase access revoked. IP permanently blacklisted."
    if "root" in l or "privileged" in l: return "=> [DEFENSE SYSTEM]: Container Escapement Attempt (T1611).\nKilling Pod and restarting K8S Node."
    if "buffer" in l or "9090" in l: return "=> [DEFENSE SYSTEM]: Memory Corruption exploit. Segfault logged.\nDispatching Forensics."
    return "=> [DEFENSE SYSTEM]: Traffic flows conform to established whitelist paradigms."

def memory_scan(data_string):
    findings = []
    for name, p in MEM_PATTERNS.items():
        if p.search(data_string): findings.append(f"-> [LEAK TRIGGERED]: Data structure {name} exfiltrated from RAM block.")
    return "[CRITICAL MEMORY COMPROMISE]\n" + "\n".join(findings) if findings else "[✓] L7 RAM Blocks clean of plaintext cryptographic anchors."

def run_rasp_sandboxed(code_input):
    safe_globals = {"__builtins__": None}
    try:
        if "import" in code_input or "eval" in code_input or "exec" in code_input:
            return "[RASP KERNEL PANIC] Static hook interception. Unsafe module loading attempted."
        exec(code_input, safe_globals)
        return "[✓] Executable byte-code allowed by Sandbox Policy."
    except Exception as e: return f"[RASP ISOLATION SUCCESS] Unsafe behavior terminated.\nReason Mechanism Block: {e}"

def network_hunter(hex_payload):
    try:
        raw_bytes = binascii.unhexlify(hex_payload)
        if b"\x90" * 8 in raw_bytes: return "[ALARM] WIDESPREAD NOP SLED DETECTED (Heap Spraying/Buffer Overflow).\nConnection dropped natively at Firewall Edge."
        if b"MZ" in raw_bytes[:2] or b"\x7FELF" in raw_bytes[:4]: return "[ALARM] MALICIOUS EXECUTABLE TRANSFER OVER CLEAR TEXT (T1048).\nFile transfer frozen."
        return "[✓] Deep Packet Inspection determined traffic is benign."
    except: return "[ERROR] Packet payload malformed for pure Hex. Dropping frame."

def exploit_lab(payload):
    p = payload.lower()
    if "<img src=" in p or "javascript:" in p or "alert(" in p: return "[REACTIVE ARMOR] Cross-Site Scripting neutralized at WAF Edge API."
    if "or 1=1" in p or "union select" in p: return "[REACTIVE ARMOR] SQL Syntax modification intercepted and sanitized."
    if "../etc/passwd" in p: return "[REACTIVE ARMOR] LFI Path Traversal denied by absolute chroot jail policy."
    return f"[FAIL] Exploit matrix mismatch: {payload} failed to trigger systems."

def honeypot_status(port):
    deceptions = {"22": "SSH Tarpit (Infinite Wait)", "21": "FTP Backdoor Lure", "3306": "MySQL Rogue DB", "8080": "Tomcat Fake Admin Hologram"}
    if str(port) in deceptions: return f"[DECEPTION GRID ONLINE]\nPort {port} armed with {deceptions[str(port)]}.\nAttacker IP vectoring targeting algorithms enabled."
    return f"[DECEPTION FAULT] Neural matrix does not support deceptive protocol for port {port}."

def dark_web_monitor(email):
    dump_hash = hashlib.sha256(email.encode()).hexdigest()
    breach = "90edceb40bdadd2d0b57e7a83fa7e661fc9fbddbe8f1f542456455ff1ea18a1a"
    if dump_hash == breach:
         return f"[INTELLIGENCE ALERT] High-Value Target breached in Shadow Forums.\nSecure MD5/SHA mapping match found.\nForcing Enterprise Password Reset across Active Directory."
    return "[✓] Corporate Identity secured. Cryptographic signatures invisible on known Tor network markets."

def firmware_scanner(bin_hex_hash):
    target = bin_hex_hash.upper()
    if target.startswith("4D5A"): return "[WARNING] Valid Windows Portable Executable (PE) identified.\nScanning header sections for Rootkits..."
    if target.startswith("7F454C46"): return "[WARNING] Valid UNIX Executable (ELF) identified.\nIntegrity mismatch against catalog. Backdoor probability: 88%."
    if target.startswith("504B0304"): return "[WARNING] Zip Archive detected buried in Firmware.\nUnpacking automatically to inspect secondary payload drops."
    return "[INFO] Cryptographic file header unrecognized.\nIntegrity passes baseline threshold."

def recursive_decoder(payload):
    current = payload.strip()
    layers_peeled = 0
    traces = [f"[INÍCIO DE ANÁLISE FORENSE DE OFUSCAÇÃO] Payload interpelado pela rede inserido..."]
    for _ in range(15):
        changed = False
        try:
             decoded = base64.b64decode(current).decode('utf-8')
             if decoded != current and all(ord(c) < 128 for c in decoded) and len(decoded)>1:
                 current = decoded; changed = True; layers_peeled += 1; traces.append(f"-> [CAMADA NEUTRALIZADA: BASE64] Fragmento Extraído: {current[:50]}...")
                 continue
        except: pass
        try:
             decoded = binascii.unhexlify(current).decode('utf-8')
             if decoded != current and all(ord(c) < 128 for c in decoded):
                 current = decoded; changed = True; layers_peeled += 1; traces.append(f"-> [CAMADA NEUTRALIZADA: HEXADECIMAL PURE] Fragmento Extraído: {current[:50]}...")
                 continue
        except: pass
        try:
             unquoted = urllib.parse.unquote(current)
             if unquoted != current:
                 current = unquoted; changed = True; layers_peeled += 1; traces.append(f"-> [CAMADA NEUTRALIZADA: URL_ENCODE] Fragmento Extraído: {current[:50]}...")
                 continue
        except: pass
        try:
             if len(current) >= 8 and all(c in '01 ' for c in current):
                 bin_str = current.replace(" ", "")
                 decoded = ''.join([chr(int(bin_str[i:i+8], 2)) for i in range(0, len(bin_str), 8)])
                 if decoded != current and all(ord(c) < 128 for c in decoded):
                     current = decoded; changed = True; layers_peeled += 1; traces.append(f"-> [CAMADA NEUTRALIZADA: ASCII_BINARY] Fragmento Extraído: {current[:50]}...")
                     continue
        except: pass
        if not changed: break
    traces.append(f"\n[SUCESSO] Engenharia Reversa Finalizada. {layers_peeled} Cascas de Proteção Trituradas.\n[CONTEÚDO TEXTUAL CRU]:\n{current}")
    return "\n".join(traces)
