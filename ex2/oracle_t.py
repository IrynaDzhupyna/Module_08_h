import os
import sys
from dotenv import load_dotenv


def get_config(required_keys: list[str]) -> dict[str, str]:
    config = {}

    for key in required_keys:
        config[key] = os.getenv(key)

    return config


def validate_config(config: dict[str, str]) -> list[str]:

    missing = []

    for key, value in config.items():
        if not value:
            missing.append(key)

    return missing


def print_config(config: dict[str, str]) -> None:
    print("\nConfigurations loaded:")

    mode = config["MATRIX_MODE"]
    
    print(f"Mode: {mode}")
    if mode == "production":
        print("Database: Connected to production instance")
        print("API Access: Production authenticated")
    else:
        print("Database: Connected to local instance")
        print(f"Zion Network: {config['ZION_ENDPOINT']}")

    print(f"Log Level:{config['LOG_LEVEL']}")
    print(f"Zion Network: {config['ZION_ENDPOINT']}")


def check_no_hardcoded_secrets(config: dict[str, str],
        source_path: str) -> bool:

    secret_keys = {"API_KEY", "DATABASE_URL"}

    with open(source_path, "r") as file:
        source = file.read()

    for key, value in config.items():
        if key in secret_keys and value in source:
            return False

    return True


def check_env_file_configured(env_path: str, gitignore_path: str) -> bool:
    env_exist = os.path.isfile(env_path)

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r") as file:
            return env_exist and ".env" in file.read()

    return False


def check_production_override(config: dict[str, str],
        pre_dotenv_env: set[str]) -> list[str]:
    overriden = []

    for key in config:
        if key in pre_dotenv_env:
            overriden.append(key)
    return overriden


def security_check(config: dict[str, str],
        pre_dotenv_env: set[str]) -> None:
    print("\nEnviroment security check:")

    if check_no_hardcoded_secrets(config, __file__):
        print("[OK] No hardcoded secrets detected")
    else:
        print("[WARNING] Hardcoded secrets detected")

    if check_env_file_configured(".env", ".gitignore"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env missing or not in .gitignore")

    if check_production_override(config, pre_dotenv_env):
        print("[OK] Production overrides available")
    else:
        print("[INFO] No production override detected")


def main() -> None:
    pre_dotenv_env = set(os.environ.keys())
    load_dotenv()
    
    print("ORACLE STATUS: Reading the Matrix...")
    required_keys = [
            "MATRIX_MODE",
            "DATABASE_URL",
            "API_KEY",
            "LOG_LEVEL",
            "ZION_ENDPOINT"]
    config = get_config(required_keys)

    missing = validate_config(config)
    if missing:
        print("\nWARNING: Missing configurations!\n")
        for element in missing:
            print(f" - {element}")

        print("\nCreate a .env file or define the missing enviroment variables.")
        sys.exit(1)
    print_config(config)
    security_check(config, pre_dotenv_env)


if __name__ == "__main__":
    main()
