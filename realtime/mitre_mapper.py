MITRE_MAP = {
    "Brute Force": {
        "tactic": "Credential Access",
        "technique": "T1110",
        "technique_name": "Brute Force",
        "kill_chain": "Exploitation"
    },
    "DDoS": {
        "tactic": "Impact",
        "technique": "T1499",
        "technique_name": "Endpoint Denial of Service",
        "kill_chain": "Actions on Objectives"
    },
    "Port Scan": {
        "tactic": "Discovery",
        "technique": "T1046",
        "technique_name": "Network Service Scanning",
        "kill_chain": "Reconnaissance"
    },
    "Malware": {
        "tactic": "Execution",
        "technique": "T1059",
        "technique_name": "Command and Scripting Interpreter",
        "kill_chain": "Delivery"
    },
    "Normal": {
        "tactic": "None",
        "technique": "None",
        "technique_name": "None",
        "kill_chain": "None"
    }
}

def map_to_mitre(attack):
    return MITRE_MAP.get(attack, {
        "tactic": "Unknown",
        "technique": "Unknown",
        "technique_name": "Unknown",
        "kill_chain": "Unknown"
    })
