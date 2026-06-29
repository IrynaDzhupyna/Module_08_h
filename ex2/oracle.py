import os
import sys
from dotenv import load_dotenv, dotenv_values


def main() -> None:
	load_dotenv()
	print(os.environ)
	print("ORACLE STATUS: Reading the Matrix...\n")
	load_dotenv()
	print(f"MATRIX_MODE =", dotenv_values('MATRIX_MODE'))


if __name__ == "__main__":
    main()
