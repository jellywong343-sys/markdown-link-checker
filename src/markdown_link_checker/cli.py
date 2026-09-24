from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\((<[^>]+>|[^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")

@dataclass
class LinkResult:
    file: str
    line: int
    text: str
    url: str
    kind: str
    status: str
    detail: str = ""


def extract_links(path: Path) -> list[tuple[int, str, str]]:
    results = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for match in LINK_RE.finditer(line):
            url = match.group(2).strip("<>")
            results.append((number, match.group(1), url))
    return results


def local_target(markdown: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme or url.startswith("#") or url.startswith("mailto:"):
        return None
    clean_path = unquote(parsed.path)
    return (markdown.parent / clean_path).resolve()


def check_external(url: str, timeout: float) -> tuple[str, str]:
    headers = {"User-Agent": "markdown-link-checker/1.0"}
    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return ("ok" if response.status < 400 else "broken", f"HTTP {response.status}")
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405}:
                continue
            return "broken", f"HTTP {exc.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if method == "HEAD":
                continue
            return "error", str(exc)
    return "error", "Unable to check URL"


def inspect_file(path: Path, external: bool = False, timeout: float = 8.0) -> list[LinkResult]:
    path = path.resolve()
    output = []
    for line, text, url in extract_links(path):
        parsed = urlparse(url)
        if parsed.scheme in {"http", "https"}:
            status, detail = check_external(url, timeout) if external else ("unchecked", "Use --external to check")
            kind = "external"
        elif url.startswith("mailto:"):
            status, detail, kind = "skipped", "Email link", "email"
        elif url.startswith("#"):
            status, detail, kind = "skipped", "Document anchor", "anchor"
        else:
            target = local_target(path, url)
            status = "ok" if target and target.exists() else "broken"
            detail = str(target) if target else ""
            kind = "local"
        output.append(LinkResult(str(path), line, text, url, kind, status, detail))
    return output


def summary(results: list[LinkResult]) -> dict:
    statuses = Counter(item.status for item in results)
    urls = Counter(item.url for item in results)
    duplicates = sorted(url for url, count in urls.items() if count > 1)
    return {"total": len(results), "statuses": dict(statuses), "duplicate_urls": duplicates}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Markdown links without changing documents.")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--external", action="store_true", help="Make network requests for HTTP(S) links")
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()
    results = []
    for name in args.files:
        results.extend(inspect_file(Path(name), args.external, args.timeout))
    for item in results:
        marker = "OK" if item.status in {"ok", "skipped", "unchecked"} else "!!"
        print(f"{marker} {item.file}:{item.line} [{item.status}] {item.url}")
    report = {"summary": summary(results), "links": [asdict(item) for item in results]}
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if any(item.status in {"broken", "error"} for item in results):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
