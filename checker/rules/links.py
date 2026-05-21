from bs4 import BeautifulSoup, Tag
from checker.issue import Issue


def _snippet(tag: Tag) -> str:
    s = str(tag)
    return s[:200] + "…" if len(s) > 200 else s


def _get_accessible_name(tag: Tag, soup: BeautifulSoup) -> str:
    """Return the accessible name of an interactive element, or empty string."""
    # aria-label
    label = tag.get("aria-label", "").strip()
    if label:
        return label

    # aria-labelledby
    labelledby = tag.get("aria-labelledby", "").strip()
    if labelledby:
        parts = []
        for ref_id in labelledby.split():
            el = soup.find(id=ref_id)
            if el:
                parts.append(el.get_text(strip=True))
        combined = " ".join(parts).strip()
        if combined:
            return combined

    # title
    title = tag.get("title", "").strip()
    if title:
        return title

    # text content (including alt text of child images)
    text_parts = []
    for node in tag.descendants:
        if isinstance(node, Tag):
            if node.name == "img":
                alt = node.get("alt", "").strip()
                if alt:
                    text_parts.append(alt)
        elif hasattr(node, "string") and node.string:
            t = node.string.strip()
            if t:
                text_parts.append(t)

    return " ".join(text_parts).strip()


def check_links(soup: BeautifulSoup) -> list[Issue]:
    issues: list[Issue] = []

    # 4.1.2 — <a> and <button> with no accessible name
    for tag in soup.find_all(["a", "button"]):
        if not isinstance(tag, Tag):
            continue

        # Skip <a> without href — they're placeholders, not links
        if tag.name == "a" and not tag.get("href"):
            continue

        aria_hidden = tag.get("aria-hidden", "").strip().lower()
        if aria_hidden == "true":
            continue

        name = _get_accessible_name(tag, soup)
        if not name:
            issues.append(Issue(
                criterion="4.1.2",
                criterion_name="Name, Role, Value",
                level="A",
                severity="error",
                title=f"<{tag.name}> has no accessible name",
                description=(
                    f"This <{tag.name}> element has no text content, aria-label, "
                    "aria-labelledby, or title that would give it an accessible name."
                ),
                fix=(
                    "Add descriptive text content, an aria-label attribute, or "
                    "an aria-labelledby pointing to a visible label."
                ),
                snippet=_snippet(tag),
            ))

    return issues
