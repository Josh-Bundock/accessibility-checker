from bs4 import BeautifulSoup
from checker.issue import Issue, MANUAL_CHECKS
from checker.rules.images import check_images
from checker.rules.forms import check_forms
from checker.rules.headings import check_headings
from checker.rules.links import check_links
from checker.rules.structure import check_structure, check_js_rendering


def run_checks(soup: BeautifulSoup) -> tuple[list[dict], list[dict], bool]:
    """Run all automated checks. Returns (issues, manual_checks, js_rendered)."""
    all_issues: list[Issue] = []
    js_rendered = check_js_rendering(soup)

    for check_fn in (check_structure, check_headings, check_images, check_forms, check_links):
        all_issues.extend(check_fn(soup))

    return [i.to_dict() for i in all_issues], MANUAL_CHECKS, js_rendered
