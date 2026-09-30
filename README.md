# Markdown Link Checker

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Check Markdown documents for broken local links, duplicate destinations, and optional external HTTP failures.

## Highlights

- Local file checks require no network connection.
- External requests are opt-in with `--external`.
- Reports exact file and line numbers.
- JSON export for CI or documentation workflows.
- Does not modify Markdown files.

## Install

```bash
git clone https://github.com/jellywong343-sys/markdown-link-checker.git
cd markdown-link-checker
python -m pip install -e .
```

## Usage

```bash
md-link-check README.md
md-link-check README.md docs/index.md --json links.json
md-link-check README.md --external --timeout 5
```

External checking sends requests to the URLs in the document. It is disabled by default.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT




