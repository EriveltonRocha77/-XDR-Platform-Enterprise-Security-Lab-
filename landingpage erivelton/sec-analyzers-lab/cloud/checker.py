import yaml
import json
import os
import sys

def check_k8s(filepath):
    results = []
    with open(filepath, 'r') as f:
        try:
            docs = yaml.safe_load_all(f)
            for doc in docs:
                if not doc: continue
                if doc.get('kind') == 'Pod':
                    containers = doc.get('spec', {}).get('containers', [])
                    for container in containers:
                        sec = container.get('securityContext', {})
                        if sec.get('privileged') == True:
                            results.append({"type": "K8S_PRIVILEGED_POD", "severity": "HIGH", "detail": f"Container '{container.get('name')}' is running in privileged mode!"})
                        if sec.get('runAsUser') == 0 or 'runAsUser' not in sec:
                            results.append({"type": "K8S_ROOT_USER", "severity": "MEDIUM", "detail": f"Container '{container.get('name')}' runs without explicit non-root restrictions."})
        except yaml.YAMLError as exc:
            results.append({"type": "YAML_PARSE_ERROR", "detail": str(exc)})
    return results

def check_aws_s3(filepath):
    results = []
    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
            if data.get('Type') == 'AWS::S3::Bucket':
                props = data.get('Properties', {})
                pacb = props.get('PublicAccessBlockConfiguration', {})
                if 'BlockPublicAcls' not in pacb or pacb.get('BlockPublicAcls') == False:
                    results.append({"type": "AWS_PUBLIC_BUCKET", "severity": "CRITICAL", "detail": "S3 bucket is configured with potential public access (BlockPublicAcls is False/Missing)."})
        except json.JSONDecodeError as exc:
            results.append({"type": "JSON_PARSE_ERROR", "detail": str(exc)})
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
         print(json.dumps([{"error": "Usage: cloud/checker.py <target_file_yaml_or_json>"}]), file=sys.stderr)
         sys.exit(1)
         
    target = sys.argv[1]
    reports = []
    
    if target.endswith('.yaml') or target.endswith('.yml'):
        reports.extend(check_k8s(target))
    elif target.endswith('.json'):
        reports.extend(check_aws_s3(target))
    else:
        reports.append({"type": "UNSUPPORTED_FILE", "detail": "Only JSON or YAML configurations are supported."})
        
    print(json.dumps(reports, indent=2))
