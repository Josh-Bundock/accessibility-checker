import pytest
from bs4 import BeautifulSoup
from checker.rules.headings import check_headings


def soup(html):
    return BeautifulSoup(html, "lxml")


def test_no_headings_at_all():
    issues = check_headings(soup("<p>Some text</p>"))
    assert any(i.criterion == "2.4.6" and i.severity == "error" for i in issues)


def test_single_h1():
    issues = check_headings(soup("<h1>Main title</h1>"))
    assert issues == []


def test_multiple_h1():
    html = "<h1>Title one</h1><h1>Title two</h1>"
    issues = check_headings(soup(html))
    assert any(i.criterion == "2.4.6" and i.severity == "warning" for i in issues)


def test_valid_h1_then_h2():
    issues = check_headings(soup("<h1>Title</h1><h2>Section</h2>"))
    assert issues == []


def test_h1_skips_to_h3():
    issues = check_headings(soup("<h1>Title</h1><h3>Subsection</h3>"))
    assert any(i.criterion == "1.3.1" and i.severity == "error" for i in issues)


def test_h2_skips_to_h4():
    html = "<h1>Title</h1><h2>Section</h2><h4>Deep</h4>"
    issues = check_headings(soup(html))
    assert any(i.criterion == "1.3.1" for i in issues)


def test_first_heading_is_h2_no_skip_error():
    # Missing h1 should be flagged, but no skip error since there's no prior heading
    issues = check_headings(soup("<h2>Section</h2>"))
    criteria = [i.criterion for i in issues]
    assert "2.4.6" in criteria  # missing h1
    skip_errors = [i for i in issues if i.criterion == "1.3.1"]
    assert skip_errors == []


def test_heading_goes_back_up_no_error():
    # Descending back to a higher level (lower number) is fine
    html = "<h1>Title</h1><h2>Section</h2><h3>Sub</h3><h2>Another section</h2>"
    issues = check_headings(soup(html))
    assert issues == []
