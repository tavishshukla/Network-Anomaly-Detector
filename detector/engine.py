from collections import Counter

class AnomalyDetector:
    def __init__(self, baseline): self.b=baseline
    def check(self, rows):
        out=[]; ports=Counter(); ips=Counter()
        for r in rows:
            if r["remote_port"]: ports[r["remote_port"]]+=1
            if r["remote_ip"]: ips[r["remote_ip"]]+=1
        if len(rows)>max(20, int(sum(self.b.counts)/len(self.b.counts)*2)) if self.b.counts else len(rows)>50:
            out.append({"severity":"HIGH","reason":"connection-count anomaly","details":f"{len(rows)} active connections"})
        for ip,n in ips.items():
            if ip not in self.b.ips and n>=2: out.append({"severity":"MEDIUM","reason":"new destination","details":f"{ip} seen {n} times"})
        unusual=[p for p in ports if str(p) not in self.b.ports]
        if unusual: out.append({"severity":"LOW","reason":"new remote port","details":", ".join(map(str,unusual[:10]))})
        return out
