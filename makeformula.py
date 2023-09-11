from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import subprocess
import sys

# Initialize the Jinja2 environment and load templates from the 'templates' directory
env = Environment(loader=FileSystemLoader("."))

# Load the template file
template = env.get_template("harbor-cli.rb.j2")

MAIN_VERSION = "3.11"
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]
FORMULA_DIR = Path("Formula")


def remove_harbor_cli_pypi_resource(requirements: str) -> str:
    """poet adds the harbor-cli from pypi, but we
    Remove it from the requirements string."""
    lines = requirements.split("\n")
    try:
        start_line = lines.index('  resource "harbor-cli" do')
    except ValueError:
        print(
            "Could not find start of harbor-cli resource in poet output",
            file=sys.stderr,
        )
        exit(1)

    for i, line in enumerate(lines, start=start_line):
        if line.startswith("  end"):
            end_line = i
            break
    else:
        print(
            "Could not find end of harbor-cli resource in poet output", file=sys.stderr
        )
        exit(1)

    del lines[start_line : end_line + 2]  # including 'end' and extra newline
    return "\n".join(lines)


def save_template(filename: str, output: str) -> None:
    FORMULA_DIR.mkdir(exist_ok=True)
    p = FORMULA_DIR / filename
    with open(p, "w") as f:
        f.write(output)
        print(f"Saved {p.resolve()}", file=sys.stderr)


def render_template(python_version: str, requirements: str) -> str:
    output = template.render(python_version=python_version, requirements=requirements)

    # Save the rendered template to a new file
    save_template(f"harbor-cli@{python_version}.rb", output)

    # Save unversioned file if python version is the main version
    if python_version == MAIN_VERSION:
        save_template(f"harbor-cli.rb", output)


def main() -> None:
    if sys.argv[1:]:
        if sys.argv[1] in ["--help", "-h"]:
            print("Usage: makeformula.py [python_versions...]")
            exit(0)
        else:
            python_versions = sys.argv[1:]
    else:
        python_versions = PYTHON_VERSIONS

    # TODO: parse python versions to ensure they are valid

    requirements = subprocess.check_output(
        ["poet", "-r", "harbor-cli"], universal_newlines=True
    )
    requirements = remove_harbor_cli_pypi_resource(requirements)

    for version in python_versions:
        render_template(version, requirements)


if __name__ == "__main__":
    main()
