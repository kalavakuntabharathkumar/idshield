from app.policy import compile_policy, evaluate_policy

def test_parses_allow_role():
    rules = compile_policy("ALLOW role=analyst")
    assert rules[0][0] == "allow_role"
    assert rules[0][1] == "analyst"

def test_denies_old_access_key():
    result = evaluate_policy("DENY access_key_age>90", {"username": "x", "access_key_age": 120, "mfa": True, "role": "analyst"})
    assert result["passed"] is False

def test_accepts_recent_key():
    result = evaluate_policy("DENY access_key_age>90", {"username": "x", "access_key_age": 20, "mfa": True, "role": "analyst"})
    assert result["passed"] is True

def test_requires_mfa():
    result = evaluate_policy("REQUIRE mfa=true", {"username": "x", "access_key_age": 20, "mfa": False, "role": "analyst"})
    assert result["passed"] is False

def test_multiple_rules():
    policy = "ALLOW role=analyst\nDENY access_key_age>90\nREQUIRE mfa=true"
    result = evaluate_policy(policy, {"username": "x", "access_key_age": 20, "mfa": True, "role": "analyst"})
    assert result["passed"] is True
