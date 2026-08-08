import re
import subprocess
import sys
from pathlib import Path

_HEADING_RE = re.compile(r"^#\s*-{2,}\s*(.+?)\s*-{2,}\s*$")
_BULLET_RE = re.compile(r"^#\s*--\s+(.*)$")
_LABEL_RE = re.compile(r"^[A-Z][A-Za-z /]{1,30}:(\s|$)")
_NUMBERED_RE = re.compile(r"^\d+\.\s")
_TREE_CHARS = ("+--", "|--", "└", "├", "─", "│")
_SPARSE_DIAGRAM_RE = re.compile(r"^[\d\s/\\]+$")


def _line_shape(raw):
    """(rest-after-#, stripped content, indent) for a non-heading/bullet line."""
    rest = raw[1:]
    content = rest.strip()
    indent = len(rest) - len(rest.lstrip(" "))
    return rest, content, indent


def _find_diagram_lines(comment_lines):
    # ASCII tree diagrams (e.g. "BaseException / +-- Exception / +-- ValueError")
    # are 2D structure, not prose -- flag them so they get a preformatted block
    # instead of being folded into a bullet/paragraph.
    n = len(comment_lines)
    is_diagram = [False] * n
    for i, raw in enumerate(comment_lines):
        if _HEADING_RE.match(raw) or _BULLET_RE.match(raw):
            continue
        _, content, _ = _line_shape(raw)
        if content and (
            any(tc in content for tc in _TREE_CHARS)
            or _SPARSE_DIAGRAM_RE.match(content)
        ):
            is_diagram[i] = True

    for i in range(n):
        if is_diagram[i] and i > 0 and not is_diagram[i - 1]:
            prev = comment_lines[i - 1]
            if not (_HEADING_RE.match(prev) or _BULLET_RE.match(prev)):
                _, prev_content, _ = _line_shape(prev)
                # a root label (e.g. "BaseException", "A") is short and bare;
                # it may be indented for visual centering above the diagram,
                # so indent isn't the signal -- word count and lack of
                # sentence-ending punctuation is what distinguishes it from a
                # genuine lead-in sentence (e.g. "Tree looks like this:").
                if (
                    prev_content
                    and len(prev_content.split()) <= 3
                    and not prev_content.rstrip().endswith((":", ".", "!", "?"))
                ):
                    is_diagram[i - 1] = True

    changed = True
    while changed:
        changed = False
        for i in range(1, n):
            if is_diagram[i] or not is_diagram[i - 1]:
                continue
            raw = comment_lines[i]
            if _HEADING_RE.match(raw) or _BULLET_RE.match(raw):
                continue
            _, content, indent = _line_shape(raw)
            if content and indent > 1:
                is_diagram[i] = True
                changed = True
    return is_diagram


def _comment_block_to_markdown(comment_lines):
    # kind: heading|bullet|para|diagram. A bullet's `bkind` controls how the
    # NEXT line is classified relative to it:
    #  - "double_dash" ("-- " marker): any indent >= 2 continues it, since a
    #    sibling item would need its own "-- " marker to start.
    #  - "single_dash" ("- " marker, incl. numbered "1. "): a sibling needs
    #    its own marker too, so a marker-less line only continues if it's
    #    indented DEEPER than the marker; same-or-shallower breaks to a new
    #    paragraph (the list has ended, this is prose again).
    #  - "bare" (indent alone implies the item, no marker at all, e.g. a
    #    "term -> definition" line): there's no marker to require, so a
    #    marker-less line at the SAME indent is a new sibling item.
    # A paragraph also tracks its own starting indent: a later line indented
    # DEEPER than that starts a nested bare bullet; same-or-shallower is a
    # wrapped continuation of that same paragraph.
    blocks = []
    current = None
    bullet_indent = None
    bullet_kind = None
    para_indent = None

    def start_para(content, indent):
        nonlocal current, para_indent
        current = ("para", [content])
        blocks.append(current)
        para_indent = indent

    def start_bullet(content, indent, kind):
        nonlocal current, bullet_indent, bullet_kind
        current = ("bullet", [content])
        blocks.append(current)
        bullet_indent = indent
        bullet_kind = kind

    is_diagram = _find_diagram_lines(comment_lines)

    for i, raw in enumerate(comment_lines):
        if is_diagram[i]:
            rest = raw[1:]
            line_content = rest[1:] if rest[:1] == " " else rest
            if current is not None and current[0] == "diagram":
                current[1].append(line_content)
            else:
                current = ("diagram", [line_content])
                blocks.append(current)
            continue

        heading_match = _HEADING_RE.match(raw)
        if heading_match:
            blocks.append(("heading", [heading_match.group(1)]))
            current = None
            continue
        bullet_match = _BULLET_RE.match(raw)
        if bullet_match:
            start_bullet(bullet_match.group(1), indent=2, kind="double_dash")
            continue

        rest = raw[1:]  # strip leading '#'
        content = rest.strip()
        if not content:
            current = None
            continue
        indent = len(rest) - len(rest.lstrip(" "))
        # the author already wrote a markdown-style "- " bullet (or a "1. "
        # numbered one). Strip a literal "- " (so the renderer's own "- "
        # prefix doesn't double up) and ALWAYS start a fresh item here --
        # this is what lets a nested list (a "-- " bullet whose body is
        # itself a list of "- " sub-items) work, since otherwise an explicit
        # bullet just swallows every deeper line as plain continuation text.
        if content.startswith("- ") or _NUMBERED_RE.match(content):
            if content.startswith("- "):
                content = content[2:].lstrip()
            start_bullet(content, indent, kind="single_dash")
        elif current is not None and current[0] == "bullet":
            if bullet_kind == "double_dash":
                if indent >= 2:
                    current[1].append(content)
                else:
                    start_para(content, indent)
            elif bullet_kind == "single_dash":
                if indent > bullet_indent:
                    current[1].append(content)
                else:
                    start_para(content, indent)
            elif indent > bullet_indent:
                current[1].append(content)
            elif indent == bullet_indent:
                start_bullet(content, indent, kind="bare")
            else:
                start_para(content, indent)
        elif current is not None and current[0] == "para":
            # a short "Label: ..." one-liner (e.g. "BAD: ...", "Go: ...") is
            # its own item, not a continuation of the previous sentence.
            if indent > para_indent:
                start_bullet(content, indent, kind="bare")
            elif _LABEL_RE.match(content):
                start_para(content, indent)
            else:
                current[1].append(content)
        elif indent >= 2:
            start_bullet(content, indent, kind="bare")
        else:
            start_para(content, indent)

    parts = []
    for kind, text_parts in blocks:
        if kind == "heading":
            parts.append(f"### {text_parts[0]}")
        elif kind == "bullet":
            parts.append("- " + " ".join(text_parts))
        elif kind == "diagram":
            parts.append("```text\n" + "\n".join(text_parts) + "\n```")
        else:
            parts.append(" ".join(text_parts))
    return "\n\n".join(parts)


def lesson_markdown(py_path):
    """Split a course .py file into alternating prose/code Markdown, so
    explanatory comment blocks render as text and code blocks keep only
    their direct inline comments. The `if __name__` demo block is excluded;
    pair with run_output() to show its printed output instead."""
    source = Path(py_path).read_text()
    main_idx = source.find("\nif __name__")
    body = source if main_idx == -1 else source[:main_idx]
    lines = body.splitlines()

    segments = []  # (kind, [lines]) where kind is prose|code
    mode = None
    buf = []

    def flush():
        if buf:
            segments.append((mode, list(buf)))
            buf.clear()

    prev_blank = True
    for line in lines:
        if line.strip() == "":
            if mode == "code":
                buf.append(line)
            elif mode == "prose":
                flush()
                mode = None
            prev_blank = True
            continue

        is_top_level = not line.startswith((" ", "\t"))
        is_comment = is_top_level and line.lstrip().startswith("#")
        # A comment line reached mid-code-block with no blank line setting it
        # off (e.g. "# s[0] = 'x'  # TypeError: ...") is commented-out code
        # being shown inline, not a new explanatory block -- keep it as code.
        if is_comment and (mode != "code" or prev_blank):
            if mode == "code":
                flush()
            mode = "prose"
            buf.append(line)
        else:
            if mode == "prose":
                flush()
            mode = "code"
            buf.append(line)
        prev_blank = False
    flush()

    out = []
    for kind, seg_lines in segments:
        if kind == "prose":
            out.append(_comment_block_to_markdown(seg_lines))
        else:
            code = "\n".join(seg_lines).strip("\n")
            out.append("```python\n" + code + "\n```")
    return "\n\n".join(out)


def run_output(py_path):
    result = subprocess.run(
        [sys.executable, str(py_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout
