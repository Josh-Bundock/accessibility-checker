import pytest
from bs4 import BeautifulSoup
from checker.rules.structure import check_structure, check_js_rendering


def soup(html):
    return BeautifulSoup(html, "lxml")


# --- Page title (2.4.2) ---

def test_missing_title():
    issues = check_structure(soup("<html><head></head><body></body></html>"))
    assert any(i.criterion == "2.4.2" for i in issues)


def test_empty_title():
    issues = check_structure(soup("<html><head><title></title></head><body></body></html>"))
    assert any(i.criterion == "2.4.2" for i in issues)


def test_valid_title():
    issues = check_structure(soup("<html><head><title>My Page</title></head><body></body></html>"))
    assert not any(i.criterion == "2.4.2" for i in issues)


# --- HTML lang (3.1.1) ---

def test_missing_lang():
    issues = check_structure(soup("<html><head></head><body></body></html>"))
    assert any(i.criterion == "3.1.1" for i in issues)


def test_empty_lang():
    issues = check_structure(soup("<html lang=''><head></head><body></body></html>"))
    assert any(i.criterion == "3.1.1" for i in issues)


def test_valid_lang():
    issues = check_structure(soup("<html lang='en'><head></head><body></body></html>"))
    assert not any(i.criterion == "3.1.1" for i in issues)


# --- Duplicate IDs (4.1.1) ---

def test_duplicate_id():
    html = "<div id='nav'>A</div><div id='nav'>B</div>"
    issues = check_structure(soup(html))
    assert any(i.criterion == "4.1.1" for i in issues)


def test_unique_ids():
    html = "<div id='header'>A</div><div id='main'>B</div>"
    issues = check_structure(soup(html))
    assert not any(i.criterion == "4.1.1" for i in issues)


# --- Table headers (1.3.1) ---

def test_table_no_th_no_scope():
    html = "<table><tr><td>Cell</td></tr></table>"
    issues = check_structure(soup(html))
    assert any(i.criterion == "1.3.1" for i in issues)


def test_table_with_th():
    html = "<table><tr><th>Header</th></tr><tr><td>Cell</td></tr></table>"
    issues = check_structure(soup(html))
    assert not any(i.criterion == "1.3.1" for i in issues)


def test_table_with_scope():
    html = "<table><tr><td scope='col'>Header</td></tr></table>"
    issues = check_structure(soup(html))
    assert not any(i.criterion == "1.3.1" for i in issues)


# --- JS rendering detection ---

def test_js_rendered_react_root():
    html = "<html><body><div id='root'></div><script></script><script></script><script></script></body></html>"
    assert check_js_rendering(soup(html)) is True


def test_js_rendered_next():
    html = "<html><body><div id='__next'></div><script></script><script></script><script></script></body></html>"
    assert check_js_rendering(soup(html)) is True


def test_js_rendered_custom_elements():
    html = "<html><body><my-component></my-component></body></html>"
    assert check_js_rendering(soup(html)) is True


def test_not_js_rendered():
    html = """<html><head><title>Page</title></head><body>
    <h1>Title</h1><p>Para</p><p>Para</p><p>Para</p><p>Para</p><p>Para</p>
    </body></html>"""
    assert check_js_rendering(soup(html)) is False
