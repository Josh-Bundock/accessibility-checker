import pytest
from bs4 import BeautifulSoup
from checker.rules.links import check_links


def soup(html):
    return BeautifulSoup(html, "lxml")


# --- <a> links ---

def test_link_no_text():
    issues = check_links(soup("<a href='#'></a>"))
    assert any(i.criterion == "4.1.2" and i.severity == "error" for i in issues)


def test_link_with_text():
    issues = check_links(soup("<a href='#'>Click here</a>"))
    assert issues == []


def test_link_with_aria_label():
    issues = check_links(soup("<a href='#' aria-label='Go home'></a>"))
    assert issues == []


def test_link_aria_hidden_skipped():
    issues = check_links(soup("<a href='#' aria-hidden='true'></a>"))
    assert issues == []


def test_link_no_href_skipped():
    # <a> without href is a placeholder, not a link
    issues = check_links(soup("<a>Not a link</a>"))
    assert issues == []


def test_link_with_title():
    issues = check_links(soup("<a href='#' title='Home'></a>"))
    assert issues == []


def test_link_with_img_alt():
    issues = check_links(soup("<a href='#'><img src='icon.png' alt='Home'></a>"))
    assert issues == []


def test_link_with_img_no_alt():
    issues = check_links(soup("<a href='#'><img src='icon.png' alt=''></a>"))
    assert any(i.criterion == "4.1.2" for i in issues)


def test_link_with_aria_labelledby():
    html = "<span id='lbl'>Home</span><a href='#' aria-labelledby='lbl'></a>"
    issues = check_links(soup(html))
    assert issues == []


# --- <button> elements ---

def test_button_no_text():
    issues = check_links(soup("<button></button>"))
    assert any(i.criterion == "4.1.2" and i.severity == "error" for i in issues)


def test_button_with_text():
    issues = check_links(soup("<button>Submit</button>"))
    assert issues == []


def test_button_with_aria_label():
    issues = check_links(soup("<button aria-label='Close dialog'></button>"))
    assert issues == []


def test_button_aria_hidden_skipped():
    issues = check_links(soup("<button aria-hidden='true'></button>"))
    assert issues == []
