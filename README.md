# Security SOAR Playbook Engine & Interactive ChatOps Pipeline 🚨

## 📌 Project Overview
This repository contains a production-ready, decoupled Security Orchestration, Automation, and Response (SOAR) playbook engine designed to eliminate manual intervention in Tier-1 triage cycles. The automation script programmatically intercepts critical telemetry infrastructure alerts, automatically enriches indicators via threat intelligence parameters, executes active perimeter containment procedures, and broadcasts interactive notification cards to Security Operations Center (SOC) engineering teams via secure ChatOps webhooks.

By separating logic from configuration, the engine dynamically routes alerts according to an independent JSON specification matrix while maintaining a zero-trust model that protects sensitive enterprise infrastructure endpoints.

## 🛠️ Core Capabilities & Automated Workflows
* **Decoupled Alert Routing Specification:** Utilizes an infrastructure mapping profile (`config/webhook_routing_spec.json`) to programmatically parse severity thresholds, target destinations, and layout configurations.
* **Fail-Safe Threat Intelligence Profiling:** Features a defensive dual-mode architecture that extracts active reputations via the VirusTotal API, with an integrated automated simulation fallback loop to maintain operational uptime if access keys are missing.
* **Active Boundary Remediation:** Automatically triggers platform-native playbook infrastructure (`playbooks/automated_ip_containment.bat`) to instantly isolate and block high-risk adversary IPs at the perimeter.
* **Structured ChatOps Escalation:** Standardizes inbound network payloads to broadcast real-time, color-coded Incident Response cards straight to dedicated engineering channels via webhook gateways.

## 📁 Repository Structure
```text
security-soar-playbook-engine/
│
├── config/
│   └── webhook_routing_spec.json     # Declarative incident severity & layout schema
│
├── playbooks/
│   └── automated_ip_containment.bat   # Windows-native perimeter isolation playbook
│
├── .env.example                      # Public template detailing required variables
├── .gitignore                        # Defensive gatekeeper preventing credential leaks
├── requirements.txt                  # Engine runtime dependencies (requests)
├── soar_playbook_engine.py           # Core Python automation & orchestration runner
└── README.md                         # Technical engineering specification brief
```

## 🚀 Deployment & Local Verification

### 1. Initialize the Environment Workspace
Clone the repository and verify that your local environment has the required runtime modules installed:
```bash
pip install -r requirements.txt
```

### 2. Configure Your Infrastructure Secrets
To prevent hardcoded data leaks, the engine leverages secure environment variables. Create a local file named `.env` in the root directory (this file is pre-configured in your `.gitignore` to never leak to GitHub):
```ini
DISCORD_WEBHOOK_URL="https://discord.com"
VIRUSTOTAL_API_KEY="your_optional_virustotal_api_key"
```
*Note: If no `VIRUSTOTAL_API_KEY` is provided, the engine gracefully initiates a simulation loop to safely verify data parsing structures without crashing.*

### 3. Launch the Orchestration Engine
Execute the master script inside your terminal window panel to witness the automated containment cycle play out:
```powershell
python soar_playbook_engine.py
```

### 📊 Expected Terminal Output Pipeline
```text
[!] No valid VirusTotal API key detected. Initiating simulation mode for IP: 198.51.100.72
[+] Launching dynamic infrastructure containment playbook: playbooks\automated_ip_containment.bat
[*] Initiating Playbook Workflow for Incident: sess_4412
[+] Establishing connection to boundary defense infrastructure...
[+] Injecting dynamic network drops for threat vector: 198.51.100.72
[SUCCESS] Dynamic containment rules successfully applied. Traffic from 198.51.100.72 isolated.
[+] Establishing active network connect
