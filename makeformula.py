from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import subprocess
import sys

DEFAULT_PYTHON_VERSION = "3.11"

# Initialize the Jinja2 environment and load template
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("harbor-cli.rb.j2")


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


def main() -> None:
    if sys.argv[1:]:
        if sys.argv[1] in ["--help", "-h"]:
            print("Usage: makeformula.py [python_version]")
            exit(0)
        else:
            python_version = sys.argv[1]
    else:
        python_version = DEFAULT_PYTHON_VERSION

    # TODO: parse python versions to ensure they are valid

    requirements = subprocess.check_output(
        ["poet", "-r", "harbor-cli"], universal_newlines=True
    )
    requirements = remove_harbor_cli_pypi_resource(requirements)

    output = template.render(python_version=python_version, requirements=requirements)

    fp = Path("harbor-cli.rb")
    with open(fp, "w") as f:
        f.write(output)
        print(f"Saved {fp.resolve()}", file=sys.stderr)


if __name__ == "__main__":
    main()
