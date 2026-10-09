# Random

A collection of useful small tools and experiments by D3F4ULT64.

## Included tools

### `rfind.py` — recursive file finder

A dependency-free command-line file finder for quickly locating files in a project.

```bash
python rfind.py "*.py" . --stats
```

Useful options:

- `--min-size BYTES` — only show files at least this large
- `--max-size BYTES` — only show files at most this large
- `--all` — include hidden directories and files
- `--no-ignore` — search dependency/build directories too
- `--stats` — show the number and total size of matches

It automatically skips common noisy directories such as `.git`, `node_modules`, virtual environments, and `__pycache__`.

## Requirements

- Python 3.10+
- No third-party packages

## Status

Active — more useful small tools can be added here over time.
