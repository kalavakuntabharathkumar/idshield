# Cloud Identity and Data Protection Reporting Platform

A runnable demonstration of an AWS-oriented data protection reporting service built with Python/FastAPI, a small Lark policy language, React UI, Terraform, pytest, GitHub Actions, and OpenAPI.

## Architecture

- FastAPI exposes policy/audit/report APIs.
- `identity.py` contains an AWS IAM-compatible adapter with a local fallback.
- `policy.py` parses a small rule language using Lark.
- `report.py` evaluates policy rules against identity records.
- React dashboard displays report results.
- Terraform provisions the conceptual AWS IAM/Lambda/S3/DynamoDB/CloudWatch resources.
- GitHub Actions runs tests and API checks.

## Run backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

## Run tests

```bash
cd backend
pytest
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

## Policy language

Example:

```text
ALLOW role=analyst
DENY access_key_age>90
REQUIRE mfa=true
```

The parser turns these rules into executable checks.

## AWS deployment

The Terraform is intentionally conservative and demonstrates the resources and relationships without requiring production credentials. Review variables and IAM permissions before applying in a real AWS account.
