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
usage: ffmpeg-tools [-h] [-v] {chapters-split,concat,stack} ...
```

## Shell-Completion

To get temporary shell completion (for your running shell-instance)
```bash
eval "$(ffmpeg-tools --shell-completion)"
```
For permanent shell completion you can add the line above to `~/.bashrc`.
This would increase your shell startup time by a good margin so it's not recommended.
The recommended way would be to pipe the completion-script to a file and sourcing that.
```bash
mkdir -p "~/.bash_completion.d/"
ffmpeg-tools --shell-completion > "~/.bash_completion.d/ffmpeg-tools.completion.sh"
echo "source \"~/.bash_completion.d/ffmpeg-tools.completion.sh\"" >> ~/.bashrc
```
The middle-command has to be redone when updating this project.
