from collector.network import snapshot
from baseline.model import Baseline
from detector.engine import AnomalyDetector
import argparse
import time


def main():
    parser = argparse.ArgumentParser(
        description="Read-only local network anomaly detector"
    )
    parser.add_argument(
        "mode",
        choices=["baseline", "monitor"],
        nargs="?",
        default="monitor",
    )
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument(
        "--baseline-file",
        default="baseline.json",
        help="Path used to save/load the baseline",
    )
    args = parser.parse_args()

    if args.seconds <= 0:
        parser.error("--seconds must be greater than 0")
    if args.interval <= 0:
        parser.error("--interval must be greater than 0")

    baseline = Baseline(args.baseline_file)

    if args.mode == "baseline":
        print("Learning baseline from local connections...")
        end = time.time() + args.seconds
        while time.time() < end:
            baseline.observe(snapshot())
            time.sleep(args.interval)
        baseline.save()
        print(f"Baseline saved to {args.baseline_file}")
        print(baseline.summary())
        return

    if not baseline.load():
        print("No baseline found. Run:")
        print(f"  python main.py baseline --seconds 60 --baseline-file {args.baseline_file}")
        return

    detector = AnomalyDetector(baseline)
    print("Monitoring local network connections (read-only). Ctrl+C to stop.")
    print(f"Using baseline: {args.baseline_file}")

    try:
        while True:
            rows = snapshot()
            for event in detector.check(rows):
                print(
                    f"[{event['severity']}] "
                    f"{event['reason']} | {event['details']}"
                )
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
