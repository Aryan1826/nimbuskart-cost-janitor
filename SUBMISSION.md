# NimbusKart Cost Janitor — Submission Summary

# Candidate Information

Name: Aryan Patel

Project: NimbusKart Cost Janitor

---

# Project Overview

NimbusKart Cost Janitor is a FinOps and cloud governance automation project built using Terraform, Python, LocalStack, and GitHub Actions.

The system provisions AWS-like infrastructure locally and scans resources to identify:
- stopped EC2 instances
- unattached EBS volumes
- missing required tags
- unused Elastic IPs

The tool generates:
- JSON reports
- Markdown summaries
- cleanup recommendations

---

# Implemented Features

## Terraform Infrastructure
- VPC
- Public Subnets
- Security Groups
- EC2 Instances
- S3 Bucket
- Orphan EBS Volume
- Terraform modules

## Python Janitor
- EC2 scanning
- EBS scanning
- Elastic IP scanning
- Missing tag detection
- Protected=true support
- Dry-run mode
- Delete mode

## Reporting
- report.json
- summary.md

## CI/CD
- GitHub Actions workflow
- Terraform validation
- Python validation

---

# Design Highlights

- LocalStack used for local AWS emulation
- Terraform modules used for reusable infrastructure
- Safe auto-delete restrictions implemented
- Governance-focused tagging enforcement added

---

# Known Limitations

Due to LocalStack Community Edition limitations:
- S3 lifecycle APIs were partially unsupported
- S3 versioning APIs caused DNS resolution issues on macOS

These behaviors were documented clearly instead of bypassed unsafely.

---

# Repository

GitHub Repository:
https://github.com/Aryan1826/nimbuskart-cost-janitor

---

# Final Notes

The project was designed to simulate real-world FinOps automation and cloud governance workflows while remaining safe for local execution and testing.