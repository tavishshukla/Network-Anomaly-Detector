# Network Anomaly Detector

A read-only local network anomaly detector written in Python. It learns a simple baseline of your computer's normal network connections and flags unusual connection counts, new destination IPs, and new remote ports.

## Features

- Read-only network telemetry using `psutil`
- Baseline learning
- New destination detection
- New remote-port detection
- Connection-count anomaly detection
- Continuous monitoring
- Automated tests
- No packet interception
- No credential collection
- No attacks
- No firewall modification

## Requirements

- Windows, Linux, or macOS
- Python **3.11 or newer**
- Git

## 1. Install Python

Download Python from:

https://www.python.org/downloads/

On Windows, make sure **Add Python to PATH** is checked during installation.

Verify:

```bash
python --version
```

Linux/macOS may use:

```bash
python3 --version
```

## 2. Install Git

Download Git from:

https://git-scm.com/downloads

Verify:

```bash
git --version
```

## 3. Clone the repository

```bash
git clone https://github.com/tavishshukla/Network-Anomaly-Detector.git
cd Network-Anomaly-Detector
```

## 4. Create a virtual environment

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

## 5. Install dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install requirements:

```bash
python -m pip install -r requirements.txt
```

You do not normally need to install pip separately because Python includes it.

## 6. Learn a baseline

Before monitoring, let the program observe your normal network activity.

For one minute:

```bash
python main.py baseline --seconds 60
```

For a shorter test:

```bash
python main.py baseline --seconds 30
```

The baseline is saved locally in:

```
baseline.json
```

For the most useful results, create the baseline while your computer is behaving normally.

## 7. Start monitoring

Run:

```bash
python main.py monitor
```

The program checks local network connections every few seconds.

If something unusual is detected, it prints an alert such as:

```
[MEDIUM] New destination observed | ...
```

Press `Ctrl+C` to stop.

## 8. Run the tests

```bash
python -m pytest
```

## How detection works

The current detector compares live local connection information against the learned baseline.

It can flag:

### High connection count

If the current number of connections becomes significantly higher than the learned normal level.

### New destination

A previously unseen remote IP address appearing repeatedly.

### New remote port

A remote port that was not present in the learned baseline.

These are anomaly indicators, not proof that an attack is happening. A completely legitimate application can create a new connection and trigger an alert.

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

## Troubleshooting

### Permission/access errors

Some operating systems restrict access to certain network connection information. Run the program only with permissions appropriate for your own machine.

### No alerts appear

That can be completely normal. The detector is looking for deviations from your baseline.

Try creating a fresh baseline:

```bash
python main.py baseline --seconds 60
```

Then start monitoring again.

### Missing module

Run:

```bash
python -m pip install -r requirements.txt
```

## Security model

This is a defensive local monitoring tool. It does not intercept packets, collect passwords, attack remote hosts, modify firewalls, or bypass security controls.
