import ast
import re
import sys
import json

def analyze_file(filepath):
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [{"type": "FILE_ERROR", "detail": str(e)}]
    
    secret_pattern = re.compile(r'(?i)(password|secret|api_key|token|aws)[-_]*[a-z0-9]*\s*=?\s*[\'"][^\'"]*[\'"]')
    for i, line in enumerate(content.split('\n'), 1):
        if secret_pattern.search(line):
            results.append({"type": "HARDCODED_SECRET", "line": i, "detail": "Potential hardcoded credentials detected"})
    
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']:
                    results.append({"type": "DANGEROUS_FUNCTION", "line": getattr(node, 'lineno', '?'), "detail": f"Usage of dangerous function {node.func.id}()"})
                
                if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
                    results.append({"type": "POTENTIAL_SQLI", "line": getattr(node, 'lineno', '?'), "detail": "Database execute() call found, verify query parameterization to prevent SQLi"})
    except SyntaxError as e:
        results.append({"type": "SYNTAX_ERROR", "detail": f"Could not parse code: {e}"})

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps([{"error": "Usage: sast/engine.py <target_file>"}]), file=sys.stderr)
        sys.exit(1)
        
    findings = analyze_file(sys.argv[1])
    print(json.dumps(findings, indent=2))
