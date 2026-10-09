from baseline.model import Baseline
from detector.engine import AnomalyDetector

def test_new_destination():
    b=Baseline(); b.observe([{"remote_ip":"1.1.1.1","remote_port":443}])
    d=AnomalyDetector(b)
    out=d.check([{"remote_ip":"2.2.2.2","remote_port":1234},{"remote_ip":"2.2.2.2","remote_port":1234}])
    assert any(x["reason"]=="new destination" for x in out)


# Additional regression coverage for an empty baseline.
def test_empty_baseline_has_no_false_connection_threshold():
    class EmptyBaseline:
        ips = {}
        ports = {}
        def average_connections(self):
            return 0
    from detector.engine import AnomalyDetector
    detector = AnomalyDetector(EmptyBaseline())
    rows = [{"remote_ip": "10.0.0.1", "remote_port": 443}]
    alerts = detector.check(rows)
    assert any(a["reason"] == "new remote port" for a in alerts)
