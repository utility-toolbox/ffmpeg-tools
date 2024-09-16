[![CodeQL](https://github.com/utility-toolbox/ffmpeg-tools/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/utility-toolbox/ffmpeg-tools/actions/workflows/github-code-scanning/codeql)

# ffmpeg-tools
ffmpeg-tools offers helpful ffmpeg commands

<!-- TOC -->
* [ffmpeg-tools](#ffmpeg-tools)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Shell-Completion](#shell-completion)
<!-- TOC -->

## Installation

```bash
sudo apt install ffmpeg python3 python3-venv git pipenv
```

```bash
git clone https://github.com/utility-toolbox/ffmpeg-tools  # get code
cd ffmpeg-tools
python3 -m venv .venv  # virtual-environment
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
