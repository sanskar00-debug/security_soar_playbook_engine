import os
import json
import subprocess
import requests

# --- SECURE CREDENTIAL FALLBACK ROUTING ---
# 1. First, check if a local hidden .env file exists on the computer disk
DISCORD_WEBHOOK_URL = "MOCK_MODE"
if os.path.exists(".env"):
    try:
        with open(".env", "r") as env_file:
            for line in env_file:
                if line.startswith("DISCORD_WEBHOOK_URL"):
                    # Extract the URL cleanly, stripping away outer quotes or whitespace
                    raw_val = line.split("=", 1)[1].strip()
                    DISCORD_WEBHOOK_URL = raw_val.strip('"').strip("'")
    except Exception:
        pass

# 2. If the file approach wasn't used, check the standard system session environment
if DISCORD_WEBHOOK_URL == "MOCK_MODE":
    DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "MOCK_MODE")

# 3. Default fallback value for the missing threat intelligence key
VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY", "")

def enrich_threat_indicator(ip_address):
    """
    Enriches threat indicators via VirusTotal.
    Gracefully falls back to mock simulation data if an API key is missing.
    """
    # Defensive programming check for placeholder keys or missing values
    if not VIRUSTOTAL_API_KEY or "INSERT_YOUR" in VIRUSTOTAL_API_KEY:
        print(f"[!] No valid VirusTotal API key detected. Initiating simulation mode for IP: {ip_address}")
        return {
            "malicious_votes": 42,
            "harmless_votes": 1,
            "owner": "Malicious Cloud Infrastructure Provider Ltd (Simulated)",
            "country": "Unknown / Proxy Network"
        }
    
    # Active API execution loop if a valid key is provided
    print(f"[+] Querying live VirusTotal intelligence infrastructure for: {ip_address}")
    url = f"https://virustotal.com{ip_address}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
            owner = data.get('data', {}).get('attributes', {}).get('as_owner', 'Unknown Provider')
            return {
                "malicious_votes": stats.get('malicious', 0),
                "harmless_votes": stats.get('harmless', 0),
                "owner": owner,
                "country": data.get('data', {}).get('attributes', {}).get('country', 'Global')
            }
        else:
            print(f"[-] VT API returned status: {response.status_code}. Falling back to default baseline.")
    except Exception as e:
        print(f"[-] API connection window tracking error: {e}")
        
    return {"malicious_votes": 0, "harmless_votes": 0, "owner": "Unknown Operational Infrastructure", "country": "Global"}

def execute_containment_playbook(ip_address, incident_id):
    """Programmatically triggers the firewall isolation script."""
    playbook_path = os.path.join("playbooks", "automated_ip_containment.bat")
    print(f"[+] Launching dynamic infrastructure containment playbook: {playbook_path}")
    
    try:
        # Executes the bash script and passes variables into arguments
        result = subprocess.run([playbook_path, ip_address, incident_id], 
                                capture_output=True, text=True, check=True, shell=True)
        print(result.stdout.strip())
    except Exception as e:
        print(f"[-] Script orchestration tracking error: {e}")

def broadcast_chatops_alert(alert_log, threat_intel, config_rules):
    """Parses JSON layout parameters to broadcast real-time metrics to Discord."""
    risk_vector = alert_log.get("risk_level", "LOW_RISK_SCANNER")
    
    # Extract structural UI layout profiles from our loaded config file
    rule_profile = config_rules.get("routing_rules", {}).get(risk_vector, {
        "embed_color_hex": 3447003,
        "require_immediate_escalation": False
    })

    if DISCORD_WEBHOOK_URL == "MOCK_MODE" or "YOUR_DISCORD" in DISCORD_WEBHOOK_URL:
        print("[!] Execution terminated: No target Discord webhook URL mapped to configuration.")
        return

    payload = {
        "username": "SOC Automation Bot",
        "embeds": [{
            "title": f"🚨 ACTION REQUIRED: Automated Incident Mitigation Triggered",
            "color": rule_profile.get("embed_color_hex"),
            "fields": [
                {"name": "Incident Vector", "value": f"`{risk_vector}`", "inline": True},
                {"name": "Target Host IP", "value": str(alert_log.get('source_ip')), "inline": True},
                {"name": "Session ID", "value": str(alert_log.get('session_id')), "inline": True},
                {"name": "Payload Transferred", "value": f"{alert_log.get('payload_mb')} MB", "inline": True},
                {"name": "Threat Reputation", "value": f"{threat_intel['malicious_votes']} Malicious Flags", "inline": True},
                {"name": "Infrastructure Owner", "value": str(threat_intel['owner']), "inline": False},
                {"name": "Playbook Execution Status", "value": "✅ `playbooks/automated_ip_containment.sh` successfully executed.", "inline": False}
            ],
            "footer": {"text": "SOAR Engine Automated Playbook Active • Production Lab Instance"}
        }]
    }

   # --- SECURE NETWORK EXCEPTION HANDLER ---
    try:
        print("[+] Establishing active network connection window to ChatOps gateway...")
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        
        if response.status_code == 204 or response.status_code == 200:
            print("[SUCCESS] ChatOps Incident Notification broadcasted successfully to Discord.")
        else:
            print(f"[-] Discord gateway returned an unhandled status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[!] Network Error: Unable to reach Discord server infrastructure. Verify your internet connectivity.")
        print("[*] SOAR Engine Notice: Playbook ran completely, but telemetry message broadcast was skipped.")
    except Exception as error:
        print(f"[-] Unexpected alerting orchestration tracking error: {error}")
        
def main():
    # Load configuration structures safely
    try:
        with open(os.path.join("config", "webhook_routing_spec.json"), "r") as cfg:
            config_rules = json.load(cfg)
    except Exception as e:
        print(f"[-] Failed to load routing specification config: {e}")
        return

    # Mocked alert item extracted from your upstream detection engine output
    sample_alert_log = {
        "session_id": "sess_4412",
        "source_ip": "198.51.100.72",
        "failed_logins": 1,
        "payload_mb": 4210.8,
        "risk_level": "CRITICAL_EXFILTRATION"
    }

    # Pipeline Processing
    threat_intel = enrich_threat_indicator(sample_alert_log["source_ip"])
    execute_containment_playbook(sample_alert_log["source_ip"], sample_alert_log["session_id"])
    broadcast_chatops_alert(sample_alert_log, threat_intel, config_rules)

if __name__ == "__main__":
    main()
