# Spell Checker (Flow.Launcher.Plugin.SpellChecker)

A [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher) plugin that checks spelling and can show a short meaning for a word.

## About

Type one or more words and the plugin will check whether each word is spelled correctly.

For correctly spelled words, the plugin can also show a one-line definition when available.

## Requirements

To use Python plugins within Flow you'll need Python 3.5 or later installed on your system.
You also may need to select your Python installation directory in the Flow Launcher settings.
As of v1.8, Flow Launcher should take care of the installation of Python for you if it is not on your system.

This plugin depends on the following Python packages:

- `flowlauncher`
- `pyspellchecker`
- `pyperclip`
- `nltk` (optional, for WordNet-based definitions)

If you want to use WordNet-based definitions, download the WordNet data:

```bash
python -m nltk.downloader wordnet
```

If WordNet is not installed, definition lookup will fall back to the available dictionary source or return a simple "WordNet is not installed. Run: python -m nltk.downloader wordnet" message.

## Installation

The easiest way to install the required packages manually is to open a terminal, navigate into the plugin folder, and run:

```bash
pip install -r requirements.txt -t ./lib
```

After installing or updating the plugin, restart Flow Launcher.

## Usage

| Keyword        | Description                                                                     |
| -------------- | ------------------------------------------------------------------------------- |
| `spell {word}` | check whether a word is spelled correctly and show a short meaning if available |

Examples:

- `spell death`
- `spell accomodate`
- `spell hello world`

## Notes

Words are checked one by one.
If a word is misspelled, the plugin shows spelling suggestions instead of a definition.

## Problems, errors and feature requests

Open an issue in this repository.
