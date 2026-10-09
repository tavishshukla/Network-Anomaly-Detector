import psutil
from collections import Counter

def snapshot():
    rows=[]
    for c in psutil.net_connections(kind="inet"):
        l=c.laddr
        r=c.raddr
        rows.append({
            "local":f"{l.ip}:{l.port}" if l else None,
            "remote":f"{r.ip}:{r.port}" if r else None,
            "remote_ip":r.ip if r else None,
            "remote_port":r.port if r else None,
            "status":c.status,
            "pid":c.pid,
        })
    return rows
