import argparse
import sys
import time
from runner import run_scan

def main():
    parser = argparse.ArgumentParser(description="Autonomous Bug Bounty CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Scan Command
    scan_p = subparsers.add_parser("scan")
    scan_p.add_argument("target")
    scan_p.add_argument("--fast", action="store_true")
    scan_p.add_argument("--output", default="results")

    # Continuous Monitor Command
    mon_p = subparsers.add_parser("monitor")
    mon_p.add_argument("target")
    mon_p.add_argument("--interval", type=int, default=3600, help="Seconds between scans (default 1hr)")

    args = parser.parse_args()

    if args.command == "scan":
        run_scan(args.target, args.fast, args.output)
    elif args.command == "monitor":
        print(f"[*] Starting continuous monitoring for: {args.target}")
        print(f"[*] Interval: {args.interval} seconds. Press Ctrl+C to stop.")
        try:
            while True:
                run_scan(args.target, False, "monitor_logs")
                print(f"[*] Scan cycle complete. Waiting for {args.interval}s...")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[*] Monitoring stopped by user.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
