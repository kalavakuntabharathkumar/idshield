from lark import Lark, Transformer

GRAMMAR = r"""
start: statement+
statement: "ALLOW" "role=" WORD      -> allow_role
         | "DENY" "access_key_age>" INT -> deny_age
         | "REQUIRE" "mfa=true"       -> require_mfa
WORD: /[A-Za-z0-9_-]+/
INT: /[0-9]+/
%import common.WS
%ignore WS
"""

parser = Lark(GRAMMAR, parser="lalr")

class PolicyTransformer(Transformer):
    def allow_role(self, items):
        return ("allow_role", str(items[0]))
    def deny_age(self, items):
        return ("deny_age", int(items[0]))
    def require_mfa(self, items):
        return ("require_mfa", True)

def compile_policy(source: str):
    return PolicyTransformer().transform(parser.parse(source)).children

def evaluate_policy(source: str, identity: dict):
    rules = compile_policy(source)
    checks = []
    for rule, value in rules:
        if rule == "allow_role":
            checks.append(identity.get("role") == value)
        elif rule == "deny_age":
            checks.append(identity.get("access_key_age", 0) <= value)
        elif rule == "require_mfa":
            checks.append(identity.get("mfa") is True)
    return {
        "username": identity["username"],
        "passed": all(checks) if checks else True,
        "checks": checks,
    }
