import json, os
from collections import Counter

PATH="baseline.json"

class Baseline:
    def __init__(self): self.ports=Counter(); self.ips=Counter(); self.counts=[]
    def observe(self, rows):
        self.counts.append(len(rows))
        for r in rows:
            if r["remote_port"]: self.ports[str(r["remote_port"])]+=1
            if r["remote_ip"]: self.ips[r["remote_ip"]]+=1
    def save(self):
        with open(PATH,"w") as f: json.dump({"ports":self.ports,"ips":self.ips,"counts":self.counts},f)
    def load(self):
        if not os.path.exists(PATH): return
        with open(PATH) as f: d=json.load(f)
        self.ports=Counter(d["ports"]); self.ips=Counter(d["ips"]); self.counts=d["counts"]
    def summary(self): return f"{len(self.ports)} ports, {len(self.ips)} remote IPs, {len(self.counts)} samples"
