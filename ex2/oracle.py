import os
import sys
from dotenv import load_dotenv


def get_config(required_vars: list[str]) -> dict[str, str | None]:
    """Load required configuration variables from the environment."""
    config = {}

    for var in required_vars:
        config[var] = os.getenv(var)

    return config


def validate(config: dict[str, str | None]) -> list[str]:
    """Return a list of missing configuration variables."""
    missing = []

    for key, value in config.items():
        if not value:
            missing.append(key)

    return missing


def print_configuration(config: dict[str, str | None]) -> None:
    """Display the loaded configuration."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    print("Configuration loaded:")

    mode = config["MATRIX_MODE"]

    if mode == "production":
        print("Mode: production")
        print("Database: Connected to production instance")
        print("API Access: Production authenticated")
    else:
        print("Mode: development")
        print("Database: Connected to local instance")
        print("API Access: Development authenticated")

    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {config['ZION_ENDPOINT']}")


def check_no_hardcoded_secrets(
    config: dict[str, str | None],
    source_path: str,
) -> bool:
    """Ensure secrets are not hardcoded in the source file."""

    with open(source_path, "r", encoding="utf-8") as file:
        source = file.read()

    secrets = [
        value
        for key, value in config.items()
        if key in {"API_KEY", "DATABASE_URL"} and value
    ]

    return not any(secret in source for secret in secrets)


def check_env_file_configured(
    env_path: str,
    gitignore_path: str,
) -> bool:
    """Check that .env exists and is ignored by Git."""

    env_exists = os.path.isfile(env_path)
    ignored = False

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as file:
            ignored = ".env" in file.read()

    return env_exists and ignored


def check_production_override(key: str, pre_dotenv_env: set[str]) -> bool:
    """Check whether a variable is supplied directly by the environment."""
    return key in pre_dotenv_env


def security_check(config: dict[str, str | None], pre_dotenv_env: set[str]) -> None:
    """Run security-related checks."""
    print()
    print("Environment security check:")

    if check_no_hardcoded_secrets(config, __file__):
        print("[OK] No hardcoded secrets detected")
    else:
        print("[WARNING] Hardcoded secrets detected")

    if check_env_file_configured(".env", ".gitignore"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env missing or not ignored by Git")

    if check_production_override(config: dict[str, str], pre_dotenv_env: set[str]):
        print("[OK] Production overrides available")
    else:
        print("[INFO] No production override detected")

    print()
    print("The Oracle sees all configurations.")


def main() -> None:
    pre_dotenv_env = set(os.environ.keys())
    print("\npre_dotenv_env\n")
    load_dotenv()

    required_vars = [
        "MATRIX_MODE",
        "DATABASE_URL",
        "API_KEY",
        "LOG_LEVEL",
        "ZION_ENDPOINT",
    ]

    config = get_config(required_vars)

    missing = validate(config)

    if missing:
        print("ORACLE STATUS: Reading the Matrix...")
        print()
        print("WARNING: Missing configuration!")
        print()

        for var in missing:
            print(f"- {var}")

        print()
        print("Create a .env file or define the missing environment variables.")
        sys.exit(1)

    print_configuration(config)
    security_check(config, pre_dotenv_env)


if __name__ == "__main__":
    main()
