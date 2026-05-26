#!/usr/bin/env python3
"""External link checker for references/links.md files.

Walks the repo, finds every `references/links.md`, extracts https URLs,
and verifies each returns a non-error status. Uses urllib (no extra deps).

Usage:
  python scripts/link_check.py
  python scripts/link_check.py --quiet
  python scripts/link_check.py --topic 01_ai_native_mindset/topic_01_what_is_ai_native
"""

from __future__ import annotations

import argparse
import re
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES_ROOT = ROOT / "modules"
URL_RE = re.compile(r"https://[^\s)\"']+")
TIMEOUT = 8


def collect_urls(scope: Path) -> dict[str, list[Path]]:
    by_url: dict[str, list[Path]] = {}
    for f in scope.rglob("references/links.md"):
        text = f.read_text(encoding="utf-8")
        for u in URL_RE.findall(text):
            by_url.setdefault(u.rstrip(".,);"), []).append(f)
    return by_url


def check(url: str) -> tuple[str, bool, str]:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "nan-labs-link-check/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return url, 200 <= resp.status < 400, str(resp.status)
    except urllib.error.HTTPError as e:
        # Some sites reject HEAD; try GET as fallback for 405/403.
        if e.code in (403, 405):
            try:
                req = urllib.request.Request(url, method="GET", headers={"User-Agent": "nan-labs-link-check/1.0"})
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    return url, 200 <= resp.status < 400, str(resp.status)
            except Exception as e2:  # noqa: BLE001
                return url, False, f"GET-fallback {e2}"
        return url, False, f"HTTP {e.code}"
    except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
        return url, False, str(e)
    except Exception as e:  # noqa: BLE001
        return url, False, str(e)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--topic", help="restrict to a single topic path")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    scope = MODULES_ROOT / args.topic if args.topic else MODULES_ROOT
    if not scope.exists():
        print(f"scope not found: {scope}", file=sys.stderr)
        return 2

    by_url = collect_urls(scope)
    failed: list[tuple[str, str]] = []

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(check, u): u for u in by_url}
        for fut in as_completed(futures):
            url, ok, status = fut.result()
            if ok:
                if not args.quiet:
                    print(f"OK   {url}")
            else:
                failed.append((url, status))
                print(f"FAIL {url}  ({status})", file=sys.stderr)

    print(f"\n{len(by_url) - len(failed)}/{len(by_url)} URLs OK")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
