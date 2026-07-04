#!/usr/bin/env python3
"""
Purpose: Identify unattached EBS volumes. Dry-run by default; pass --delete to remove them.
Inputs:
  --region       AWS region (default: from AWS config or environment)
  --profile      AWS credential profile
  --delete       Actually delete unattached volumes
  --tag-to-skip  Tag key that marks a volume as protected (default: DoNotDelete)
Outputs: List of unattached volume IDs and deletion status.
Risks: --delete destroys data. Ensure snapshots/backups exist before deleting.
"""

from __future__ import annotations

import argparse
import sys

import boto3
from botocore.exceptions import ClientError


def get_volumes(client):
    paginator = client.get_paginator("describe_volumes")
    volumes = []
    for page in paginator.paginate():
        volumes.extend(page["Volumes"])
    return volumes


def is_unattached(volume: dict) -> bool:
    return not volume.get("Attachments")


def is_protected(volume: dict, tag_key: str) -> bool:
    tags = {tag["Key"]: tag["Value"] for tag in volume.get("Tags", [])}
    return tag_key in tags


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find (and optionally delete) unattached EBS volumes."
    )
    parser.add_argument("--region", help="AWS region")
    parser.add_argument("--profile", help="AWS credential profile")
    parser.add_argument(
        "--delete", action="store_true", help="Delete unattached volumes"
    )
    parser.add_argument(
        "--tag-to-skip",
        default="DoNotDelete",
        help="Tag key that protects a volume from deletion",
    )
    args = parser.parse_args()

    session_kwargs: dict[str, str] = {}
    if args.profile:
        session_kwargs["profile_name"] = args.profile
    if args.region:
        session_kwargs["region_name"] = args.region

    session = boto3.Session(**session_kwargs)
    ec2 = session.client("ec2")

    volumes = get_volumes(ec2)
    unattached = [
        volume
        for volume in volumes
        if is_unattached(volume) and not is_protected(volume, args.tag_to_skip)
    ]

    if not unattached:
        print("No unattached, unprotected volumes found.")
        return 0

    print(f"Found {len(unattached)} unattached volume(s) (dry-run={not args.delete}):")
    for volume in unattached:
        vid = volume["VolumeId"]
        size = volume["Size"]
        state = volume["State"]
        print(f"  {vid}: {size}GiB, state={state}")

    if not args.delete:
        print("Rerun with --delete to remove these volumes.")
        return 0

    print("Deleting volumes...")
    for volume in unattached:
        vid = volume["VolumeId"]
        try:
            ec2.delete_volume(VolumeId=vid)
            print(f"  Deleted {vid}")
        except ClientError as exc:
            print(f"  Failed to delete {vid}: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
