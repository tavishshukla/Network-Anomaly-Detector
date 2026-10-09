# Network Anomaly Detector

A read-only local network anomaly detector written in Python. It learns a simple baseline of your computer's normal network connections and flags unusual connection counts, new destination IPs, and new remote ports.

## Features

- Read-only network telemetry using `psutil`
- Configurable baseline duration and sampling interval
- Configurable baseline file location
- Connection-count anomaly detection
- New destination detection
- New remote-port detection
- Clear monitoring output
- Graceful Ctrl+C shutdown
- Automated tests
- No packet interception
- No credential collection
- No attacks
- No firewall modification

## Requirements

- Windows, Linux, or macOS
- Python **3.11 or newer**
- Git

## Setup

Install Python from https://www.python.org/downloads/ and Git from https://git-scm.com/downloads/.

Verify:

```bash
python --version
git --version
```

Clone the project:

```bash
git clone https://github.com/tavishshukla/Network-Anomaly-Detector.git
cd Network-Anomaly-Detector
```

Create and activate a virtual environment.

### Windows

```bat
python -m venv .venv
.venv\\Scripts\\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Learn a baseline

Run this while your computer is behaving normally:

```bash
python main.py baseline --seconds 60
```

The default baseline is saved as `baseline.json`.

You can choose another location:

```bash
python main.py baseline --seconds 60 --interval 1 --baseline-file data/my-baseline.json
```

## Monitor

```bash
python main.py monitor
```

Choose a custom interval and baseline if needed:

```bash
python main.py monitor --interval 2 --baseline-file data/my-baseline.json
```

Stop with `Ctrl+C`.

If no baseline exists, the program explains how to create one instead of crashing.

## How detection works

The detector compares current local connection telemetry with the learned baseline.

- **HIGH — connection-count anomaly:** current connections are substantially above the learned average.
- **MEDIUM — new destination:** an unseen remote IP appears repeatedly.
- **LOW — new remote port:** a remote port not present in the baseline is observed.

These are anomaly indicators, not proof of malicious activity. Normal software can create new connections.

## Tests

```bash
python -m pytest
```

## Project structure

```
Network-Anomaly-Detector/
├── main.py
├── requirements.txt
├── README.md
├── collector/
│   └── network.py
├── baseline/
│   └── model.py
├── detector/
│   └── engine.py
└── tests/
    └── test_detector.py
```

## Security model

This is a defensive local monitoring tool. It does not intercept packets, collect passwords, attack remote hosts, modify firewalls, or bypass security controls.

## Recommended workflow

Learn a baseline while the computer is doing normal work with `python main.py baseline --seconds 60`, then start `python main.py monitor`. Keep the baseline from a normal period rather than creating it during unusual activity.

## Alert metadata

Detector findings include machine-readable `observed` and `threshold` values where applicable. This makes the output easier to consume from a future dashboard or automation layer while keeping the detector read-only.
