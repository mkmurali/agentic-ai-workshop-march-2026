"""
Module 0: Environment Setup Verification
=========================================
Run this script to verify your workshop environment is ready.

Usage:
    python module_00_setup/verify_setup.py
"""

import sys


def check_python_version():
    print(f"  Python version: {sys.version}")
    if sys.version_info < (3, 12):
        print("  [FAIL] Python 3.12+ is required")
        return False
    print("  [OK] Python version")
    return True


def check_strands():
    try:
        import strands  # noqa: F401
        print("  [OK] strands-agents installed")
        return True
    except ImportError:
        print("  [FAIL] strands-agents not installed. Run: pip install strands-agents")
        return False


def check_strands_tools():
    try:
        import strands_tools  # noqa: F401
        print("  [OK] strands-agents-tools installed")
        return True
    except ImportError:
        print("  [FAIL] strands-agents-tools not installed. Run: pip install strands-agents-tools")
        return False


def check_boto3():
    try:
        import boto3  # noqa: F401
        print("  [OK] boto3 installed")
        return True
    except ImportError:
        print("  [FAIL] boto3 not installed. Run: pip install boto3")
        return False


def check_aws_credentials():
    try:
        import boto3
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        print(f"  [OK] AWS credentials configured (Account: {identity['Account']})")
        return True
    except Exception as e:
        print(f"  [FAIL] AWS credentials not configured: {e}")
        print("  Run: aws configure")
        return False


def check_bedrock_access():
    try:
        import boto3
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        # Just check we can create the client - actual model access will be tested at runtime
        print(f"  [OK] Bedrock runtime client created (region: us-east-1)")
        del client
        return True
    except Exception as e:
        print(f"  [WARN] Could not create Bedrock client: {e}")
        return False


def check_mcp():
    try:
        import mcp  # noqa: F401
        print("  [OK] mcp package installed")
        return True
    except ImportError:
        print("  [FAIL] mcp not installed. Run: pip install mcp")
        return False


def check_opentelemetry():
    try:
        from opentelemetry import trace  # noqa: F401
        print("  [OK] opentelemetry installed")
        return True
    except ImportError:
        print("  [WARN] opentelemetry not installed (optional for Module 6)")
        return True  # Not a hard requirement


def main():
    print("=" * 60)
    print("  Agentic AI Workshop - Environment Verification")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Strands Agents SDK", check_strands),
        ("Strands Agents Tools", check_strands_tools),
        ("Boto3 (AWS SDK)", check_boto3),
        ("AWS Credentials", check_aws_credentials),
        ("Amazon Bedrock Access", check_bedrock_access),
        ("MCP Package", check_mcp),
        ("OpenTelemetry", check_opentelemetry),
    ]

    results = []
    for name, check_fn in checks:
        print(f"\nChecking {name}...")
        results.append(check_fn())

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"  Results: {passed}/{total} checks passed")

    if all(results):
        print("  Your environment is ready for the workshop!")
    else:
        print("  Please fix the issues above before the workshop starts.")
    print("=" * 60)


if __name__ == "__main__":
    main()
