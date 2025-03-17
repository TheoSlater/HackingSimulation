from typing import Dict

SERVERS: Dict[str, dict] = {
    "10.0.14.52": {
        "name": "AlphaNet",
        "security": 2,
        "password": "admin123",
        "money": 5000,
        "ports": {
            "80": {
                "name": "HTTP",
                "version": "Apache 2.4.49",
                "vulnerabilities": [
                    {
                        "cve": "CVE-2021-41773",
                        "description": "Path Traversal Vulnerability",
                        "version": "Apache 2.4.49"
                    }
                ]
            }
        },
        "files": {
            "report.txt": "Confidential report on system vulnerabilities.",
            "admin_creds.txt": "Username: admin\nPassword: 1234",
            "junk.log": "System logs and useless data."
        },
        "firewall": {
            "enabled": True,
            "strength": 3,
            "attempts": 0
        },
        "auth_type": "password",
        "sensitive_data": {
            "customer_records.csv": {
                "description": "Customer database with credit card info",
                "value": 5000
            },
            "source_code.zip": {
                "description": "Proprietary software source code",
                "value": 3000
            }
        },
        "status": "online"
    },
    "172.16.8.120": {
        "name": "BetaCorp",
        "security": 3,
        "password": "securepass",
        "money": 12000,
        "ports": {},
        "files": {
            "customer_data.db": "Encrypted database of customers. Requires decryption key.",
            "secret_key.pem": "PRIVATE KEY - DO NOT SHARE"
        },
        "firewall": {
            "enabled": False,
            "strength": 4,
            "attempts": 0
        },
        "auth_type": "ssh_key",
        "sensitive_data": {
            "trade_secrets.doc": {
                "description": "Corporate trade secrets",
                "value": 8000
            }
        },
        "status": "online"
    }
    # ... Copy rest of servers from servers.json ...
}

# Store current connection
current_server = None
