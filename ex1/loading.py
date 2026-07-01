import importlib
import importlib.metadata
import sys


class DependencyInfo:
    def __init__(
            self: "DependencyInfo", name: str,
            available: bool,
            description: str,
            version: str | None = None,
            module: object | None = None) -> None:

        self.name = name
        self.available = available
        self.version = version
        self.description = description
        self.module = module

    def show_info(self: "DependencyInfo") -> None:
        if self.available:
            print(f"[OK] {self.name} "
                  "({self.version}) - {self.description} ready")
        else:
            print(f"[MISSING] {self.name} - package not installed")


def check_dependencies(
        dependencies: list[tuple[str, str]]) -> dict[
            str, DependencyInfo] | None:
    print("Checking dependencies:")
    all_deps: dict[str, DependencyInfo] = {}

    for key, value in dependencies:
        try:
            module = importlib.import_module(key)
        except ImportError:
            all_deps[key] = DependencyInfo(
                key, available=False,
                description=value, version=None, module=None)
            continue

        try:
            version = importlib.metadata.version(key)
        except importlib.metadata.PackageNotFoundError:
            version = None

        all_deps[key] = DependencyInfo(
            key, available=True,
            description=value, version=version, module=module)

    for dep in all_deps.values():
        dep.show_info()

    for dep in all_deps.values():
        if not dep.available:
            if dep.name == "requests":
                continue
            print("\nSome dependencies are missing.")
            print("Install them using pip or poetry!")
            compare_pip_poetry()
            return None
    return all_deps


def compare_pip_poetry() -> None:
    print("\nDependency Management Comparison:")

    print("\nUsing pip")
    print("-" * 20)
    print("Virtual enviroment managed separately. Activate before installing")
    print(" -Install venv: python3 -m venv <venv_name>")
    print(" -Activate venv: source <venv_name>/bin/activate")
    print("Dependencies listed in requirements.txt")
    print("Install dependencies: pip install -r requirements.txt")

    print("\nUsing poetry")
    print("-" * 20)
    print("Automatically manages virtual enviroment.")
    print("Dependencies listed in pyproject.toml")
    print("Install - poetry install")
    print("Run script: poetry run python3 <script_name.py>")
    print("Creates a poetry.lock file for reproducible installs")


def check_dependency_managment_tool_used() -> None:
    print(f"- Python executable: {sys.executable}")

    if sys.prefix != sys.base_prefix:
        print(" - Running inside virtual environment")
        if "pypoetry" in sys.executable or "virtualenvs" in sys.executable:
            print(" - This is Poetry-managed environment")
        else:
            print(" - This is pip/venv-managed environment")
    else:
        print("No virtual environment detected. You are in global scope.")


def generate_matrix_data(n: int, numpy_module: object) -> object:
    print("\nAnalyzing Matrix data...")
    generator = numpy_module.random.default_rng()  # type: ignore[attr-defined]
    data = generator.normal(size=n)
    return data


def build_dataframe(data: object, pandas_module: object) -> object:
    print(f"Processing {len(data)} data points...")  # type: ignore[arg-type]
    data_frame = pandas_module.DataFrame(  # type: ignore[attr-defined]
        {"signal": data})
    data_frame["rolling_mean"] = data_frame["signal"].rolling(window=10).mean()
    return data_frame


def generate_visualization(data_frame: object,
                           matplotlib_module: object) -> str:
    print("Generating visualization...")
    importlib.import_module("matplotlib.pyplot")
    plt = matplotlib_module.pyplot  # type: ignore[attr-defined]
    fig, ax = plt.subplots()
    ax.plot(data_frame["signal"])  # type: ignore[index]
    ax.set_title("Matrix Data Analysis")
    output_path = "matrix_analysis.png"
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")
    dependencies: list[tuple[str, str]] = [
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical computation"),
        ("matplotlib", "Visualization"),
    ]

    all_deps = check_dependencies(dependencies)
    if not all_deps:
        return

    # check_dependency_managment_tool_used()
    n = 1000
    data = generate_matrix_data(n, all_deps["numpy"].module)
    data_frame = build_dataframe(data, all_deps["pandas"].module)
    output_file = generate_visualization(
        data_frame, all_deps["matplotlib"].module)
    print("\nAnalysis complete!")
    print(f"Result saved to: {output_file}")


if __name__ == "__main__":
    main()
