from bs4 import BeautifulSoup, Tag
from checker.issue import Issue

HEADING_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]


def _heading_level(tag: Tag) -> int:
    return int(tag.name[1])


def check_headings(soup: BeautifulSoup) -> list[Issue]:
    issues: list[Issue] = []

    headings = [
        tag for tag in soup.find_all(HEADING_TAGS)
        if isinstance(tag, Tag)
    ]

    # 2.4.6 — at least one h1
    h1s = [h for h in headings if h.name == "h1"]
    if not h1s:
        issues.append(Issue(
            criterion="2.4.6",
            criterion_name="Headings and Labels",
            level="AA",
            severity="error",
            title="Page has no <h1>",
            description="Every page should have exactly one <h1> as the main heading.",
            fix="Add an <h1> that describes the main topic of the page.",
        ))
    elif len(h1s) > 1:
        snippets = " | ".join(str(h)[:80] for h in h1s)
        issues.append(Issue(
            criterion="2.4.6",
            criterion_name="Headings and Labels",
            level="AA",
            severity="warning",
            title=f"Page has {len(h1s)} <h1> elements",
            description=(
                "Multiple <h1> elements make it harder for screen reader users "
                "to understand the page structure."
            ),
            fix="Use a single <h1> for the main page title. Use <h2>–<h6> for subsections.",
            snippet=snippets[:300],
        ))

    # 1.3.1 — heading hierarchy skips
    prev_level = 0
    for h in headings:
        level = _heading_level(h)
        if prev_level > 0 and level > prev_level + 1:
            s = str(h)
            issues.append(Issue(
                criterion="1.3.1",
                criterion_name="Info and Relationships",
                level="A",
                severity="error",
                title=f"Heading level skips from h{prev_level} to h{level}",
                description=(
                    f"Heading hierarchy jumped from h{prev_level} to h{level}, "
                    "skipping a level. This breaks the logical document outline."
                ),
                fix=(
                    f"Use h{prev_level + 1} here instead of h{level}, or restructure "
                    "the content so levels are not skipped."
                ),
                snippet=(s[:200] + "…" if len(s) > 200 else s),
            ))
        prev_level = level

    return issues
