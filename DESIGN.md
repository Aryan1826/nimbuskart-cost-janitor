# NimbusKart Cost Janitor — Design Document

# Overview

NimbusKart Cost Janitor is a lightweight FinOps automation solution designed to identify potentially wasteful cloud resources and improve governance practices.

The system provisions infrastructure using Terraform and scans resources using a Python-based Janitor engine powered by boto3.

LocalStack is used to emulate AWS services locally.

---

# Architecture

## Infrastructure Layer

Terraform provisions:
- VPC
- Public Subnets
- Security Groups
- EC2 Instances
- S3 Bucket
- Orphan EBS Volume

Terraform modules were used to improve:
- reusability
- maintainability
- scalability

---

# Scanning Layer

The Python Janitor script scans:
- EC2 Instances
- EBS Volumes
- Elastic IPs

The scanner detects:
- stopped EC2 instances
- unattached EBS volumes
- missing required tags
- unused Elastic IPs

---

# Governance Model

The system enforces governance through:
- mandatory tagging validation
- Protected=true resource protection
- safe auto-delete filtering

Resources tagged with:

```text
Protected=true
```

are skipped from automated cleanup.

---

# Reporting System

The Janitor generates:
- report.json
- summary.md

The reports include:
- estimated monthly waste
- findings summary
- suggested actions
- resource metadata

---

# Cleanup Strategy

The system supports:
- dry-run mode
- delete mode

Dry-run mode:
- scans resources
- generates reports
- performs no destructive action

Delete mode:
- removes only safe-to-delete resources
- skips protected resources
- catches deletion exceptions safely

---

# CI/CD Workflow

GitHub Actions validates:
- Terraform formatting
- Terraform syntax
- Python syntax

This ensures code quality during every push and pull request.

---

# Key Design Decisions

## Why LocalStack?

LocalStack was selected because:
- no AWS billing required
- safe local experimentation
- easier reproducibility
- faster testing cycle

---

## Why Terraform Modules?

Terraform modules improve:
- code organization
- scalability
- reuse capability

---

## Why Protected Tags?

Protected tags prevent accidental deletion of:
- critical infrastructure
- production workloads
- sensitive resources

---

# Known Limitations

Due to LocalStack Community Edition limitations:
- S3 lifecycle APIs were partially unsupported
- S3 versioning APIs caused DNS resolution issues on macOS

These limitations were documented instead of bypassed unsafely.

---

# Future Enhancements

- Multi-region support
- Slack/Teams notifications
- Lambda scheduling
- Kubernetes resource scanning
- AWS Cost Explorer integration
- Automated tagging remediation