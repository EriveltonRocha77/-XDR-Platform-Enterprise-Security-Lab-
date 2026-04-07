from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import re
import json

SIEM_URL = "http://backend:8000/api/v1/ingest"

class WAFShield(BaseHTTPRequestHandler):
    def parse_anomaly(self, path):
        patterns = [
            (r"(union|select|insert|drop)\s", "SQL_INJECTION"),
            (r"(<script>|javascript:)", "CROSS_SITE_SCRIPTING"),
            (r"(\.\./\.\./|etc/passwd)", "LOCAL_FILE_INCLUSION"),
            (r"(nmap|nikto|curl)", "AUTOMATED_SCANNER")
        ]
        path_lower = path.lower()
        for regex, threat_type in patterns:
            if re.search(regex, path_lower):
                return threat_type
        return None

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        threat = self.parse_anomaly(self.path)
        
        if threat:
            print(f"[WAF SHIELD] Blocked {threat} at {self.path}")
            
            self.send_response(403)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"waf": "blocked", "reason": "anomaly detected"}')
            
            alert = {
                "engine": "WAF_ANOMALY_DETECTOR",
                "severity": "CRITICAL",
                "attack_vector": threat,
                "target_uri": self.path,
                "client_ip": self.client_address[0]
            }
            try:
                req = urllib.request.Request(SIEM_URL, data=json.dumps(alert).encode('utf-8'), headers={'Content-Type':'application/json'})
                urllib.request.urlopen(req, timeout=2)
            except Exception as e:
                pass
            return
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Clean Traffic Passed to Internal App')

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8081), WAFShield)
    print("WAF Anomaly Engine Active on port 8081")
    server.serve_forever()
