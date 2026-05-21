from bs4 import BeautifulSoup
from checker.runner import run_checks


def soup(html):
    return BeautifulSoup(html, "lxml")


CLEAN_HTML = """
<html lang="en">
<head><title>Test Page</title></head>
<body>
  <h1>Main heading</h1>
  <h2>Section</h2>
  <p>Some content</p>
  <img src="photo.jpg" alt="A photo">
  <a href="/about">About us</a>
  <label for="email">Email</label>
  <input type="email" id="email" name="email" autocomplete="email">
</body>
</html>
"""

BROKEN_HTML = """
<html>
<head></head>
<body>
  <h1>Title</h1>
  <h3>Skipped heading</h3>
  <img src="photo.jpg">
  <a href="#"></a>
  <input type="text">
  <table><tr><td>Cell</td></tr></table>
</body>
</html>
"""

SPA_HTML = """
<html>
<head></head>
<body>
  <div id="root"></div>
  <script src="main.js"></script>
  <script src="vendor.js"></script>
  <script src="runtime.js"></script>
</body>
</html>
"""


def test_clean_page_no_issues():
    issues, manual_checks, js_rendered = run_checks(soup(CLEAN_HTML))
    assert issues == []
    assert js_rendered is False
    assert len(manual_checks) > 0


def test_broken_page_has_issues():
    issues, manual_checks, js_rendered = run_checks(soup(BROKEN_HTML))
    criteria = {i["criterion"] for i in issues}
    assert "1.1.1" in criteria   # missing alt
    assert "4.1.2" in criteria   # empty link
    assert "1.3.1" in criteria   # missing label + heading skip + table


def test_spa_detected():
    issues, manual_checks, js_rendered = run_checks(soup(SPA_HTML))
    assert js_rendered is True


def test_manual_checks_always_returned():
    issues, manual_checks, js_rendered = run_checks(soup(CLEAN_HTML))
    assert isinstance(manual_checks, list)
    assert len(manual_checks) >= 5
