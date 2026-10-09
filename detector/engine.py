from collections import Counter


class AnomalyDetector:
    def __init__(self, baseline):
        self.b = baseline

    def check(self, rows):
        out = []
        ports = Counter()
        ips = Counter()

        for row in rows:
            port = row.get("remote_port")
            ip = row.get("remote_ip")
            if port:
                ports[port] += 1
            if ip:
                ips[ip] += 1

        average = self.b.average_connections()
        threshold = max(20, int(average * 2)) if average else 50

        if len(rows) > threshold:
            out.append({
                "severity": "HIGH",
                "reason": "connection-count anomaly",
                "details": f"{len(rows)} active connections (threshold {threshold})",
            })

        for ip, count in ips.items():
            if ip not in self.b.ips and count >= 2:
                out.append({
                    "severity": "MEDIUM",
                    "reason": "new destination",
                    "details": f"{ip} seen {count} times",
                })

        unusual = [port for port in ports if str(port) not in self.b.ports]
        if unusual:
            out.append({
                "severity": "LOW",
                "reason": "new remote port",
                "details": ", ".join(map(str, unusual[:10])),
            })

        return out
