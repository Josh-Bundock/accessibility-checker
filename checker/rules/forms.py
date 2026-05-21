from bs4 import BeautifulSoup, Tag
from checker.issue import Issue

AUTOCOMPLETE_FIELDS = {
    "name": "name",
    "fname": "given-name",
    "first_name": "given-name",
    "first-name": "given-name",
    "firstname": "given-name",
    "lname": "family-name",
    "last_name": "family-name",
    "last-name": "family-name",
    "lastname": "family-name",
    "email": "email",
    "e-mail": "email",
    "phone": "tel",
    "telephone": "tel",
    "tel": "tel",
    "mobile": "tel",
}

UNLABELLABLE_TYPES = {"hidden", "submit", "reset", "button", "image"}


def _snippet(tag: Tag) -> str:
    s = str(tag)
    return s[:200] + "…" if len(s) > 200 else s


def _has_accessible_name(inp: Tag, soup: BeautifulSoup) -> bool:
    inp_id = inp.get("id", "").strip()

    # aria-label
    if inp.get("aria-label", "").strip():
        return True

    # aria-labelledby
    labelledby = inp.get("aria-labelledby", "").strip()
    if labelledby:
        for ref_id in labelledby.split():
            el = soup.find(id=ref_id)
            if el and el.get_text(strip=True):
                return True

    # <label for="id">
    if inp_id:
        label = soup.find("label", attrs={"for": inp_id})
        if label and label.get_text(strip=True):
            return True

    # implicit label (input nested inside <label>)
    parent_label = inp.find_parent("label")
    if parent_label:
        # label text is everything except the input itself
        label_text = parent_label.get_text(strip=True)
        inp_text = inp.get("value", "") or inp.get("placeholder", "")
        # any text content in the label beyond the input value counts
        if label_text and label_text != inp_text:
            return True

    # title attribute (last resort — valid but not ideal)
    if inp.get("title", "").strip():
        return True

    return False


def check_forms(soup: BeautifulSoup) -> list[Issue]:
    issues: list[Issue] = []
    all_ids: set[str] = set()

    for inp in soup.find_all("input"):
        if not isinstance(inp, Tag):
            continue

        inp_type = inp.get("type", "text").strip().lower()
        if inp_type in UNLABELLABLE_TYPES:
            continue

        # 1.3.1 — missing label
        if not _has_accessible_name(inp, soup):
            issues.append(Issue(
                criterion="1.3.1",
                criterion_name="Info and Relationships",
                level="A",
                severity="error",
                title="Form input has no accessible label",
                description=(
                    f"This <input type=\"{inp_type}\"> has no associated <label>, "
                    "aria-label, or aria-labelledby."
                ),
                fix=(
                    "Add a <label for=\"id\"> linked to the input's id, or add "
                    "aria-label=\"...\" directly to the input."
                ),
                snippet=_snippet(inp),
            ))

        # 1.3.5 — missing autocomplete on common personal data fields
        name_attr = inp.get("name", "").strip().lower()
        id_attr = inp.get("id", "").strip().lower()
        autocomplete = inp.get("autocomplete", "").strip().lower()

        for key, expected_value in AUTOCOMPLETE_FIELDS.items():
            if key in name_attr or key in id_attr:
                if not autocomplete or autocomplete in ("", "on", "off"):
                    if inp_type in ("text", "email", "tel", "search", ""):
                        issues.append(Issue(
                            criterion="1.3.5",
                            criterion_name="Identify Input Purpose",
                            level="AA",
                            severity="warning",
                            title="Common field missing autocomplete attribute",
                            description=(
                                f"This field appears to collect '{key}' data but "
                                f"lacks a specific autocomplete value. "
                                f"Expected: autocomplete=\"{expected_value}\"."
                            ),
                            fix=(
                                f"Add autocomplete=\"{expected_value}\" to help "
                                "users with cognitive disabilities and autofill."
                            ),
                            snippet=_snippet(inp),
                        ))
                break

    # Check <select> and <textarea> for labels too
    for tag_name in ("select", "textarea"):
        for el in soup.find_all(tag_name):
            if not isinstance(el, Tag):
                continue
            if not _has_accessible_name(el, soup):
                issues.append(Issue(
                    criterion="1.3.1",
                    criterion_name="Info and Relationships",
                    level="A",
                    severity="error",
                    title=f"<{tag_name}> has no accessible label",
                    description=(
                        f"This <{tag_name}> has no associated <label>, "
                        "aria-label, or aria-labelledby."
                    ),
                    fix=(
                        "Add a <label for=\"id\"> or aria-label attribute."
                    ),
                    snippet=_snippet(el),
                ))

    return issues
