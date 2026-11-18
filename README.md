# AWS Cloud Automation with Python and Boto3

A small set of AWS account inventory utilities. The first utility exports EC2 instance details to CSV using the AWS SDK for Python.

## Included utility
`scripts/ec2_inventory.py`:
- Uses the standard AWS credential chain; no access keys are hard-coded
- Accepts an explicit AWS region
- Uses a Boto3 paginator to retrieve all pages
- Exports instance ID, state, type, AZ, private/public IP and Name tag
- Returns a non-zero exit code for AWS API or file errors

## Run locally
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
aws configure
python scripts/ec2_inventory.py --region ap-south-1 --output reports/ec2-inventory.csv
```

The IAM identity needs read-only EC2 permissions such as `ec2:DescribeInstances`. Prefer IAM Identity Center or an assumed role over long-lived access keys.

Generated reports are not committed. Treat infrastructure inventory as internal information.

## Status
Source and unit tests are included. The script has not been run against your AWS account and no account inventory is included here.
