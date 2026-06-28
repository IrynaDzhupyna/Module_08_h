import sys
import site
import os


def main() -> None:
    print("\nMATRIX STATUS: ", end='')
    if sys.prefix == sys.base_prefix:
        print("You're still plugged in\n")
        print(f"Current Python: {sys.executable}")
        print("Virtual Enviroment: None detected\n")
        print("WARNING: You're in global enviroment!")
        print("The machines can see everything you install.\n")
        print("To enter the constract, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate #On Unix")
        print("matrix_env\\Scripts\\activate #On Windows\n")
        print("Then run this program again.")
    else:
        print("Welcome to the construct\n")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Enviroment: {os.path.basename(sys.prefix)}")
        print(f"Enviroment path: {sys.prefix}\n")
        print("SUCCESS: You're in an isolated enviroment!")
        print("Safe to install packages"
              "without affecting the global system.\n")
        print("Package installation path:")
        print(site.getsitepackages()[0])


if __name__ == "__main__":
    main()
