#!/usr/bin/env python3
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]\r\n]+)\]\((https?://(?:[^\s()]+|\([^\s()]+\))+)\)")


def escape_text(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def escape_url(url: str) -> str:
    return (
        url.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def format_telegram_summary(text: str) -> str:
    result = []
    last_end = 0
    for match in LINK_RE.finditer(text):
        start, end = match.span()
        result.append(escape_text(text[last_end:start]))

        label = escape_text(match.group(1))
        url = escape_url(match.group(2))
        result.append(f'<a href="{url}">{label}</a>')
        last_end = end

    result.append(escape_text(text[last_end:]))
    return "".join(result)


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        path = Path(sys.argv[1])
        if not path.is_file():
            return
        content = path.read_text(encoding="utf-8")
    else:
        content = sys.stdin.read()

    sys.stdout.write(format_telegram_summary(content))


if __name__ == "__main__":
    main()
