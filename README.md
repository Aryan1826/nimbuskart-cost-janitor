# NimbusKart Cost Janitor

NimbusKart Cost Janitor is a FinOps and cloud governance automation tool built using Terraform, Python, LocalStack, and GitHub Actions.

The project provisions AWS infrastructure locally using LocalStack and scans cloud resources to identify cost optimization opportunities such as:
- Stopped EC2 instances
- Unattached EBS volumes
- Missing required tags
- Unused Elastic IPs

The tool generates:
- JSON reports
- Markdown summaries
- Automated cleanup recommendations

---

# Features

## Infrastructure Provisioning
- VPC
- Public Subnets
- Security Groups
- EC2 Instances
- S3 Bucket
- Orphan EBS Volume

## FinOps Detection
- Stopped EC2 detection
- Unattached EBS detection
- Missing tag detection
- Unused Elastic IP detection

## Governance
- Protected=true resource skipping
- Dry-run mode
- Safe auto-delete logic

## Reporting
- report.json
- summary.md

## CI/CD
- GitHub Actions workflow
- Terraform validation
- Python validation

---

# Tech Stack

- Terraform
- Python
- boto3
- LocalStack
- GitHub Actions
- AWS CLI

---

# Project Structure

```text
nimbuskart-cost-janitor/
│
├── terraform/
├── janitor/
├── docs/
├── samples/
└── .github/workflows/
```

---

# How To Run

## Start LocalStack

```bash
docker run --rm -it -p 4566:4566 localstack/localstack:3.0
```

---

## Terraform Setup

```bash
cd terraform

tflocal init

tflocal apply -auto-approve
```

---

## Run Janitor

```bash
cd janitor

python3 janitor.py
```

---

## Dry Run Mode

```bash
python3 janitor.py --dry-run
```

---

## Delete Mode

```bash
python3 janitor.py --delete
```

---

# Design Decisions

- LocalStack Community Edition was used instead of real AWS to avoid cloud costs.
- S3 lifecycle/versioning APIs were partially excluded due to LocalStack compatibility limitations.
- Protected=true tag prevents accidental deletion of important resources.
- Only safe resources are auto-deleted.

---

# Future Improvements

- Slack notifications
- Email reporting
- Multi-region scanning
- Cost Explorer integration
- Lambda deployment
- Kubernetes support

---

---

# AI Usage Disclosure

AI tools were used during development to accelerate debugging, infrastructure setup guidance, and boilerplate generation.

## Tools Used
- ChatGPT:
  - Terraform debugging
  - LocalStack troubleshooting
  - Python boto3 integration guidance
  - GitHub Actions workflow setup
  - Documentation drafting

## One Incorrect AI Suggestion
One incorrect suggestion involved using S3 lifecycle and versioning APIs directly with LocalStack Community Edition. During implementation, these APIs caused compatibility and DNS resolution issues on macOS. This was identified through repeated Terraform apply failures and LocalStack limitations documentation, after which the unsupported sections were safely removed and documented.

## One Section Implemented Manually
The final Janitor scanning logic and reporting structure were manually adjusted and cleaned to ensure proper resource filtering, Protected=true handling, and readable report formatting. This part was refined manually to better understand the workflow and ensure the logic matched the assignment requirements.

# Author

Aryan Rangani
