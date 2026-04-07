import urllib.request
import urllib.error
import sys
import json

def scan_url(target_url):
    results = []
    
    try:
        req = urllib.request.Request(target_url, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = response.info()
            if 'Content-Security-Policy' not in headers:
                results.append({"type": "MISSING_HEADER", "detail": "Content-Security-Policy header is missing, exposure to XSS"})
            if 'X-Frame-Options' not in headers:
                results.append({"type": "MISSING_HEADER", "detail": "X-Frame-Options header is missing, exposure to Clickjacking"})
                
    except urllib.error.URLError as e:
        results.append({"type": "CONNECTION_ERROR", "detail": f"Target not responding: {str(e)}"})
        return results

    fuzz_payload = "?id=1' OR '1'='1"
    try:
        req = urllib.request.Request(target_url + fuzz_payload)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8', errors='ignore')
            if "syntax error" in body.lower() or "mysql" in body.lower() or "sqlite" in body.lower():
                results.append({"type": "SQLI_VULNERABILITY", "detail": "Database error reflected in response using SQLi payload"})
    except urllib.error.HTTPError as e:
        if e.code in [500, 502, 503]:
             results.append({"type": "POTENTIAL_DOS_OR_VULN", "detail": f"Payload {fuzz_payload} triggered an HTTP {e.code} error"})
    except Exception as e:
         results.append({"type": "ERROR", "detail": str(e)})

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps([{"error": "Usage: dast/scanner.py <target_url>"}]), file=sys.stderr)
        sys.exit(1)
        
    findings = scan_url(sys.argv[1])
    print(json.dumps(findings, indent=2))
