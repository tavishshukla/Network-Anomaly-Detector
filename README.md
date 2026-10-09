# Network Anomaly Detector

Read-only local network anomaly detector using psutil. Learns a simple baseline and flags unusual connection counts, new destinations, and new ports.

## Run
`python -m pip install -r requirements.txt`
`python main.py baseline --seconds 60`
`python main.py monitor`
`python -m pytest`

Only monitors the machine you run it on. No packet interception, credential collection, attacks, or firewall changes.