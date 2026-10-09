from collector.network import snapshot
from baseline.model import Baseline
from detector.engine import AnomalyDetector
import argparse, time

def main():
    p=argparse.ArgumentParser(description="Read-only local network anomaly detector")
    p.add_argument("mode",choices=["baseline","monitor"],nargs="?",default="monitor")
    p.add_argument("--seconds",type=int,default=30)
    a=p.parse_args()
    b=Baseline()
    if a.mode=="baseline":
        print("Learning baseline from local connections...")
        end=time.time()+a.seconds
        while time.time()<end:
            b.observe(snapshot()); time.sleep(1)
        b.save(); print(f"Baseline saved: {b.summary()}")
        return
    b.load()
    d=AnomalyDetector(b)
    print("Monitoring local network connections (read-only). Ctrl+C to stop.")
    while True:
        events=snapshot()
        for e in d.check(events):
            print(f"[{e['severity']}] {e['reason']} | {e['details']}")
        time.sleep(2)

if __name__=="__main__": main()
