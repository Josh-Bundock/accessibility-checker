from bs4 import BeautifulSoup, Tag
from checker.issue import Issue


def _snippet(tag: Tag) -> str:
    s = str(tag)
    return s[:200] + "…" if len(s) > 200 else s


def check_images(soup: BeautifulSoup) -> list[Issue]:
    issues: list[Issue] = []

    for img in soup.find_all("img"):
        if not isinstance(img, Tag):
            continue

        # 1.1.1 — missing alt entirely
        if img.get("alt") is None:
            issues.append(Issue(
                criterion="1.1.1",
                criterion_name="Non-text Content",
                level="A",
                severity="error",
                title="Image missing alt attribute",
                description="This <img> has no alt attribute at all.",
                fix=(
                    "Add alt=\"\" if the image is decorative, or a meaningful "
                    "description if it conveys information."
                ),
                snippet=_snippet(img),
            ))
            continue

        # 1.1.1 — empty alt that isn't clearly decorative
        alt = img.get("alt", "").strip()
        role = img.get("role", "").strip().lower()
        aria_hidden = img.get("aria-hidden", "").strip().lower()

        if alt == "" and role not in ("presentation", "none") and aria_hidden != "true":
            # Check if inside a <figure> that has a <figcaption>
            figure = img.find_parent("figure")
            has_figcaption = figure and figure.find("figcaption") is not None

            if not has_figcaption:
                issues.append(Issue(
                    criterion="1.1.1",
                    criterion_name="Non-text Content",
                    level="A",
                    severity="warning",
                    title="Image with empty alt — review if decorative",
                    description=(
                        "This image has alt=\"\" but is not marked as "
                        "role=\"presentation\", aria-hidden=\"true\", or inside a "
                        "<figure> with a <figcaption>. If it conveys information, "
                        "it needs a descriptive alt."
                    ),
                    fix=(
                        "If decorative: add role=\"presentation\" or "
                        "aria-hidden=\"true\". If informative: add a meaningful alt."
                    ),
                    snippet=_snippet(img),
                ))

        # 4.1.2 — <input type="image"> without alt
        # (handled in forms.py but also catches standalone cases)

    # input[type=image] without alt
    for inp in soup.find_all("input", attrs={"type": "image"}):
        if not isinstance(inp, Tag):
            continue
        if inp.get("alt") is None or inp.get("alt", "").strip() == "":
            issues.append(Issue(
                criterion="4.1.2",
                criterion_name="Name, Role, Value",
                level="A",
                severity="error",
                title="<input type=\"image\"> missing alt",
                description=(
                    "Image inputs act as buttons and must have an alt attribute "
                    "describing their action."
                ),
                fix="Add alt=\"[description of the button action]\".",
                snippet=_snippet(inp),
            ))

    return issues
