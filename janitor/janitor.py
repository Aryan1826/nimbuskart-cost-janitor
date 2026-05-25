import boto3
import json
import sys
from datetime import datetime, UTC

# AWS LocalStack Connection
ec2 = boto3.client(
    "ec2",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    endpoint_url="http://localhost:4566"
)

# Command-line Modes
dry_run = "--dry-run" in sys.argv
delete_mode = "--delete" in sys.argv

# Required Tags
required_tags = ["Project", "Environment", "Owner"]

# Findings List
findings = []

# =========================
# Detect Orphan EBS Volumes
# =========================

volume_response = ec2.describe_volumes()

for volume in volume_response["Volumes"]:

    if volume["State"] == "available":

        tags = {}

        if "Tags" in volume:
            for tag in volume["Tags"]:
                tags[tag["Key"]] = tag["Value"]

        protected = tags.get("Protected", "false").lower()

        if protected == "true":
            continue

        finding = {
            "resource_id": volume["VolumeId"],
            "resource_type": "ebs_volume",
            "reason": "unattached",
            "age_days": 0,
            "estimated_monthly_cost_usd": 8.0,
            "tags": tags,
            "suggested_action": "delete",
            "safe_to_auto_delete": True
        }

        findings.append(finding)

# =========================
# Detect EC2 Issues
# =========================

instance_response = ec2.describe_instances()

for reservation in instance_response["Reservations"]:

    for instance in reservation["Instances"]:

        state = instance["State"]["Name"]

        tags = {}

        if "Tags" in instance:
            for tag in instance["Tags"]:
                tags[tag["Key"]] = tag["Value"]

        protected = tags.get("Protected", "false").lower()

        # Skip protected resources
        if protected == "true":
            continue

        # =========================
        # Detect Stopped Instances
        # =========================

        if state == "stopped":

            finding = {
                "resource_id": instance["InstanceId"],
                "resource_type": "ec2_instance",
                "reason": "stopped_instance",
                "age_days": 14,
                "estimated_monthly_cost_usd": 15.0,
                "tags": tags,
                "suggested_action": "terminate",
                "safe_to_auto_delete": False
            }

            findings.append(finding)

        # =========================
        # Detect Missing Tags
        # =========================

        missing_tags = []

        for required_tag in required_tags:
            if required_tag not in tags:
                missing_tags.append(required_tag)

        if len(missing_tags) > 0:

            finding = {
                "resource_id": instance["InstanceId"],
                "resource_type": "ec2_instance",
                "reason": "missing_tags",
                "age_days": 0,
                "estimated_monthly_cost_usd": 5.0,
                "tags": tags,
                "suggested_action": "add_required_tags",
                "safe_to_auto_delete": False
            }

            findings.append(finding)

# =========================
# Detect Unused Elastic IPs
# =========================

address_response = ec2.describe_addresses()

for address in address_response["Addresses"]:

    if "InstanceId" not in address:

        finding = {
            "resource_id": address.get("AllocationId", "unknown"),
            "resource_type": "elastic_ip",
            "reason": "unused_elastic_ip",
            "age_days": 0,
            "estimated_monthly_cost_usd": 3.0,
            "tags": {},
            "suggested_action": "release",
            "safe_to_auto_delete": True
        }

        findings.append(finding)

# =========================
# Generate Report
# =========================

report = {
    "scan_timestamp": datetime.now(UTC).isoformat(),
    "account_id": "000000000000",
    "region": "us-east-1",
    "summary": {
        "total_findings": len(findings),
        "estimated_monthly_waste_usd": sum(
            item["estimated_monthly_cost_usd"]
            for item in findings
        )
    },
    "findings": findings
}

# Save JSON Report
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

# Save Markdown Summary
with open("summary.md", "w") as file:

    file.write("# NimbusKart Cost Janitor Report\n\n")

    file.write(f"Scan Timestamp: {report['scan_timestamp']}\n\n")

    file.write("## Summary\n\n")

    file.write(
        f"- Total Findings: {report['summary']['total_findings']}\n"
    )

    file.write(
        f"- Estimated Monthly Waste: "
        f"${report['summary']['estimated_monthly_waste_usd']}\n\n"
    )

    file.write("## Findings\n\n")

    for finding in findings:

        file.write(f"### {finding['resource_type']}\n")

        file.write(
            f"- Resource ID: {finding['resource_id']}\n"
        )

        file.write(
            f"- Reason: {finding['reason']}\n"
        )

        file.write(
            f"- Estimated Cost: "
            f"${finding['estimated_monthly_cost_usd']}\n"
        )

        file.write(
            f"- Suggested Action: "
            f"{finding['suggested_action']}\n\n"
        )

# Console Messages
if dry_run:
    print("Running in DRY-RUN mode")

if delete_mode:

    print("Running in DELETE mode")

    for finding in findings:

        if finding["safe_to_auto_delete"]:

            resource_type = finding["resource_type"]
            resource_id = finding["resource_id"]

            try:

                # Delete orphan EBS volume
                if resource_type == "ebs_volume":

                    ec2.delete_volume(
                        VolumeId=resource_id
                    )

                    print(f"Deleted EBS Volume: {resource_id}")

                # Release Elastic IP
                elif resource_type == "elastic_ip":

                    ec2.release_address(
                        AllocationId=resource_id
                    )

                    print(f"Released Elastic IP: {resource_id}")

            except Exception as error:

                print(
                    f"Failed to delete {resource_id}: {error}"
                )

print("Report generated successfully!")

print(json.dumps(report, indent=4))