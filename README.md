# Homebrew Formula for Harbor CLI

This repo contains the Homebrew formula for Harbor CLI.

To add the Harbor CLI tap and install the CLI, run:

```bash
brew tap pederhan/harbor-cli
brew install harbor-cli
```

If you want to use the fully qualified formula name, you can use:

```bash
brew install pederhan/harbor-cli/harbor-cli
```

## Update formulas

Make a virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Due to harbor-cli not being on PyPI yet, we have to wrangle poet a little bit to create the proper formula.
To faciliate this, run the following command:

```bash
python makeformula.py
```

This will generate a new formula for the latest version of harbor-cli and save it to `harbor-cli.rb`.


## TODO

- [ ] Validate Python version args
- [ ] Fetch URL for newest version of harbor-cli from GitHub
    - [ ] Validate URL
    - [ ] Get checksum
    - [ ] Render commit sha as version in formula

