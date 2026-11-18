#!/usr/bin/env python3
"""Export EC2 instance inventory to CSV using the active AWS credential chain."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

FIELDS = [
    "instance_id", "state", "instance_type", "availability_zone",
    "private_ip", "public_ip", "name",
]


def instance_name(tags: list[dict] | None) -> str:
    for tag in tags or []:
        if tag.get("Key") == "Name":
            return tag.get("Value", "")
    return ""


def collect_instances(region: str) -> list[dict[str, str]]:
    ec2 = boto3.client("ec2", region_name=region)
    paginator = ec2.get_paginator("describe_instances")
    rows: list[dict[str, str]] = []

    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                rows.append({
                    "instance_id": instance.get("InstanceId", ""),
                    "state": instance.get("State", {}).get("Name", ""),
                    "instance_type": instance.get("InstanceType", ""),
                    "availability_zone": instance.get("Placement", {}).get("AvailabilityZone", ""),
                    "private_ip": instance.get("PrivateIpAddress", ""),
                    "public_ip": instance.get("PublicIpAddress", ""),
                    "name": instance_name(instance.get("Tags")),
                })
    return rows


def write_csv(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", required=True, help="AWS region, e.g. ap-south-1")
    parser.add_argument("--output", type=Path, default=Path("reports/ec2-inventory.csv"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = collect_instances(args.region)
        write_csv(rows, args.output)
    except (BotoCoreError, ClientError) as exc:
        print(f"AWS API request failed: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Could not write report: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {len(rows)} EC2 instance records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
