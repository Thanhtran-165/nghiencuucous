#!/usr/bin/env python3
"""
generate_toc_xref.py — Generate TOC sidebar items + convert "Section N" → clickable xref links.

Input: HTML file đã có sections (`<section id="sec-...">`)
Output: 2 thứ:
  1. TOC sidebar items HTML (list của `<a class="toc-sidebar-item">`)
  2. HTML với "Section N" trong text chunks → `<a class="xref">Section N</a>`

Usage:
  python3 generate_toc_xref.py input.html > output.html
  python3 generate_toc_xref.py ~/ZCodeProject/nem-deploy/index.html > ~/ZCodeProject/nem-deploy/index_fixed.html

Sau khi chạy:
- Copy TOC items vào `<ul class="toc-sidebar-list">{{TOC_SIDEBAR_ITEMS}}</ul>`
- Replace original file với output (đã có xref)
"""

import sys
import re
from pathlib import Path


# Canonical section order (must match dashboard_design.md Section A)
SECTION_MAP = [
    (1, "sec-hero", "Tổng quan & KPI"),
    (2, "sec-exec", "Tóm tắt điều hành"),
    (3, "sec-biz", "Business 101"),
    (4, "sec-industry", "Vị trí ngành"),
    (5, "sec-history", "Lịch sử tài chính"),
    (6, "sec-segment", "Phân tích mảng"),
    (7, "sec-thesis", "Luận điểm đầu tư"),
    (8, "sec-valuation", "Định giá"),
    (9, "sec-peer", "So sánh peer"),
    (10, "sec-bs", "BS & FCF"),
    (11, "sec-risk", "Ma trận rủi ro"),
    (12, "sec-33k", "Góc nhìn vốn"),
    (13, "sec-scenario", "Kịch bản"),
    (14, "sec-checklist", "Checklist"),
    (15, "sec-insight", "★ Insight 1"),
    (16, "sec-moat", "★ Insight 2"),
    (17, "sec-supply", "★ Insight 3"),
    (18, "sec-tech", "Kỹ thuật ACTIVE"),
    (19, "sec-tech-profile", "Kỹ thuật PROFILE"),
    (20, "sec-analyst", "Analyst"),
    (21, "sec-glossary", "📖 Thuật ngữ"),
    (22, "sec-source", "Nguồn & Data"),
]

NUM_TO_ID = {num: sid for num, sid, _ in SECTION_MAP}


def generate_toc_items() -> str:
    """Generate sidebar TOC items HTML."""
    items = []
    for num, sid, label in SECTION_MAP:
        items.append(
            f'    <li><a class="toc-sidebar-item" href="#{sid}">'
            f'<span class="toc-sidebar-num">{num}</span>'
            f'<span class="toc-sidebar-label">{label}</span></a></li>'
        )
    return "\n".join(items)


def is_in_tag(html: str, pos: int) -> bool:
    """Check if position is inside an HTML tag."""
    # Look backward for < or >
    last_open = html.rfind("<", 0, pos)
    last_close = html.rfind(">", 0, pos)
    return last_open > last_close


def convert_xref(html: str) -> str:
    """Convert 'Section N' in text chunks to clickable xref links.
    Skip if inside HTML tags, or if part of a range (Section 5-10).
    """
    # Pattern: "Section N" or "Section N.M"
    pattern = re.compile(r'(Section\s+(\d{1,2})(\.\d+)?)')

    result = []
    last_end = 0
    for m in pattern.finditer(html):
        start, end = m.span()
        full_match = m.group(1)
        num = int(m.group(2))

        # Skip if inside tag
        if is_in_tag(html, start):
            result.append(html[last_end:end])
            last_end = end
            continue

        # Skip ranges: check if followed by "-" or "–" or "—" + digit
        after = html[end:end + 5]
        if re.match(r'^\s*[-–—]\s*\d', after):
            result.append(html[last_end:end])
            last_end = end
            continue

        # Skip if num not in our map (out of range)
        if num not in NUM_TO_ID:
            result.append(html[last_end:end])
            last_end = end
            continue

        # Convert to xref
        sid = NUM_TO_ID[num]
        xref = f'<a href="#{sid}" class="xref">{full_match}</a>'
        result.append(html[last_end:start])
        result.append(xref)
        last_end = end

    result.append(html[last_end:])
    return "".join(result)


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_toc_xref.py input.html > output.html", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"ERROR: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    html = input_path.read_text()

    # 1. Generate TOC items (stderr — user copy paste vào template)
    toc_items = generate_toc_items()
    print("=== TOC SIDEBAR ITEMS (paste vào <ul class='toc-sidebar-list'>) ===", file=sys.stderr)
    print(toc_items, file=sys.stderr)
    print("", file=sys.stderr)

    # 2. Convert xref
    converted = convert_xref(html)

    # 3. Count conversions
    xref_count = converted.count('class="xref"') - html.count('class="xref"')
    print(f"=== Converted {xref_count} 'Section N' → xref links ===", file=sys.stderr)

    # 4. Output converted HTML to stdout
    sys.stdout.write(converted)


if __name__ == "__main__":
    main()
