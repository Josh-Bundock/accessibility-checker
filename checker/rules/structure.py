from bs4 import BeautifulSoup, Tag
from checker.issue import Issue
from collections import Counter

# Tags that indicate real text/interactive content (not just nav links)
RICH_CONTENT_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6",
                     "img", "input", "select", "textarea", "article",
                     "section", "main", "figure", "blockquote", "li"}

# Attributes/IDs that indicate a JS framework root element
FRAMEWORK_SIGNALS = [
    {"id": "root"},
    {"id": "app"},
    {"id": "__next"},
    {"id": "nuxt"},
    {"data-reactroot": True},
    {"ng-version": True},
]


def _is_js_rendered(soup: BeautifulSoup) -> bool:
    """Return True if the page looks like a client-side-rendered SPA."""
    script_count = len(soup.find_all("script"))

    # Any custom element (tag name contains a hyphen) = Web Components / framework
    custom_elements = [
        t for t in soup.find_all(True)
        if isinstance(t, Tag) and "-" in t.name
    ]
    if custom_elements:
        return True

    # Known framework root element
    for attrs in FRAMEWORK_SIGNALS:
        query = {k: (True if v is True else v) for k, v in attrs.items()}
        if soup.find(attrs=query):
            return True

    # Very few rich content elements but many scripts
    rich_count = sum(1 for t in soup.find_all(RICH_CONTENT_TAGS) if isinstance(t, Tag))
    if rich_count < 5 and script_count >= 3:
        return True

    return False


def check_js_rendering(soup: BeautifulSoup) -> bool:
    return _is_js_rendered(soup)


def check_structure(soup: BeautifulSoup) -> list[Issue]:
    issues: list[Issue] = []

    # 2.4.2 — page title
    title_tag = soup.find("title")
    if not title_tag or not title_tag.get_text(strip=True):
        issues.append(Issue(
            criterion="2.4.2",
            criterion_name="Page Titled",
            level="A",
            severity="error",
            title="Page has no <title> or title is empty",
            description=(
                "Every page must have a descriptive <title> so users can identify it "
                "in browser tabs and history."
            ),
            fix="Add a meaningful <title> inside <head>, e.g. <title>Page Name – Site Name</title>.",
        ))

    # 3.1.1 — html lang
    html_tag = soup.find("html")
    if isinstance(html_tag, Tag):
        lang = html_tag.get("lang", "").strip()
        if not lang:
            issues.append(Issue(
                criterion="3.1.1",
                criterion_name="Language of Page",
                level="A",
                severity="error",
                title="<html> element missing lang attribute",
                description=(
                    "Screen readers use the lang attribute to select the correct "
                    "pronunciation engine. Without it, speech output may be wrong."
                ),
                fix="Add lang=\"en\" (or the appropriate language code) to <html>.",
            ))

    # 4.1.1 — duplicate id attributes
    all_ids = [
        tag["id"]
        for tag in soup.find_all(id=True)
        if isinstance(tag, Tag)
    ]
    counts = Counter(all_ids)
    for id_val, count in counts.items():
        if count > 1:
            issues.append(Issue(
                criterion="4.1.1",
                criterion_name="Parsing",
                level="A",
                severity="error",
                title=f"Duplicate id=\"{id_val}\" ({count} occurrences)",
                description=(
                    f"The id \"{id_val}\" appears {count} times. IDs must be unique; "
                    "duplicate IDs break label associations, aria-labelledby, and "
                    "fragment navigation."
                ),
                fix=f"Ensure id=\"{id_val}\" is used on exactly one element.",
                snippet=f'id="{id_val}"',
            ))

    # 1.3.1 — tables without <th> or scope
    for table in soup.find_all("table"):
        if not isinstance(table, Tag):
            continue
        has_th = bool(table.find("th"))
        has_scope = any(
            td.get("scope") for td in table.find_all("td") if isinstance(td, Tag)
        )
        if not has_th and not has_scope:
            s = str(table)
            issues.append(Issue(
                criterion="1.3.1",
                criterion_name="Info and Relationships",
                level="A",
                severity="error",
                title="Data table has no <th> or scope attributes",
                description=(
                    "This <table> contains no <th> elements and no scope attributes. "
                    "Screen readers cannot associate data cells with headers."
                ),
                fix=(
                    "Add <th> elements for row/column headers, or add "
                    "scope=\"col\" / scope=\"row\" to header cells."
                ),
                snippet=(s[:200] + "…" if len(s) > 200 else s),
            ))

    return issues
