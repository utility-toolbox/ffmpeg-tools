[![CodeQL](https://github.com/utility-toolbox/ffmpeg-tools/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/utility-toolbox/ffmpeg-tools/actions/workflows/github-code-scanning/codeql)

# ffmpeg-tools
ffmpeg-tools offers helpful ffmpeg commands

## Installation

```bash
sudo apt install python3
```

```bash
git clone https://github.com/utility-toolbox/ffmpeg-tools  # get code
cd ffmpeg-tools
python3 -m venv .venv  # virtual-environment
pip3 install pipenv  # install pipenv-manager
pipenv install  # install dependencies
echo "export \"\$PATH:`pwd`\"" >> ~/.bashrc  # add to path
source ~/.bashrc  # or restart your shell
```

## Usage

```bash
usage: ffmpeg-tools [-h] [-v] {chapters-split,concat} ...
```

## Shell-Completion

```bash
eval "$(ffmpeg-tools --shell-completion)"
```
