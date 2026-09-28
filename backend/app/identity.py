def sample_identities():
    return [
        {"username": "alice", "role": "analyst", "mfa": True, "access_key_age": 20},
        {"username": "bob", "role": "analyst", "mfa": False, "access_key_age": 120},
        {"username": "carol", "role": "admin", "mfa": True, "access_key_age": 45},
    ]

def list_iam_users():
    # AWS adapter boundary. Replace the local fixture with boto3 in an AWS environment.
    import boto3
    iam = boto3.client("iam")
    return iam.list_users().get("Users", [])
