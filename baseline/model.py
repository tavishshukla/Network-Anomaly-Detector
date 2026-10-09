import json
from collections import Counter
from pathlib import Path

PATH = Path("baseline.json")

class Baseline:
    def __init__(self, path: Path | str = PATH):
        self.path = Path(path)
        self.ports = Counter()
        self.ips = Counter()
        self.counts = []

    def observe(self, rows):
        self.counts.append(len(rows))
        for row in rows:
            port = row.get("remote_port")
            ip = row.get("remote_ip")
            if port:
                self.ports[str(port)] += 1
            if ip:
                self.ips[str(ip)] += 1

    def save(self):
        payload = {
            "ports": dict(self.ports),
            "ips": dict(self.ips),
            "counts": self.counts,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self):
        if not self.path.exists():
            return False
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.ports = Counter(data.get("ports", {}))
        self.ips = Counter(data.get("ips", {}))
        self.counts = list(data.get("counts", []))
        return True

    def average_connections(self):
        return sum(self.counts) / len(self.counts) if self.counts else 0.0

    def summary(self):
        if not self.counts:
            return "empty baseline"
        return (
            f"{len(self.ports)} ports, {len(self.ips)} remote IPs, "
            f"{len(self.counts)} samples, "
            f"{self.average_connections():.1f} average connections, "
            f"range {min(self.counts)}-{max(self.counts)}"
        )
