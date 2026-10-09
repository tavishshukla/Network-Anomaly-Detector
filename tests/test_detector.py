from baseline.model import Baseline
from detector.engine import AnomalyDetector

def test_new_destination():
    b=Baseline(); b.observe([{"remote_ip":"1.1.1.1","remote_port":443}])
    d=AnomalyDetector(b)
    out=d.check([{"remote_ip":"2.2.2.2","remote_port":1234},{"remote_ip":"2.2.2.2","remote_port":1234}])
    assert any(x["reason"]=="new destination" for x in out)
