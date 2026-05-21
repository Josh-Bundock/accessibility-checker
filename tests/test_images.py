import pytest
from bs4 import BeautifulSoup
from checker.rules.images import check_images


def soup(html):
    return BeautifulSoup(html, "lxml")


# --- <img> alt attribute ---

def test_img_missing_alt():
    issues = check_images(soup("<img src='photo.jpg'>"))
    assert len(issues) == 1
    assert issues[0].criterion == "1.1.1"
    assert issues[0].severity == "error"


def test_img_empty_alt_no_decoration():
    issues = check_images(soup("<img src='photo.jpg' alt=''>"))
    assert len(issues) == 1
    assert issues[0].criterion == "1.1.1"
    assert issues[0].severity == "warning"


def test_img_empty_alt_role_presentation():
    issues = check_images(soup("<img src='photo.jpg' alt='' role='presentation'>"))
    assert issues == []


def test_img_empty_alt_role_none():
    issues = check_images(soup("<img src='photo.jpg' alt='' role='none'>"))
    assert issues == []


def test_img_empty_alt_aria_hidden():
    issues = check_images(soup("<img src='photo.jpg' alt='' aria-hidden='true'>"))
    assert issues == []


def test_img_empty_alt_in_figure_with_figcaption():
    html = "<figure><img src='photo.jpg' alt=''><figcaption>A photo</figcaption></figure>"
    issues = check_images(soup(html))
    assert issues == []


def test_img_empty_alt_in_figure_without_figcaption():
    html = "<figure><img src='photo.jpg' alt=''></figure>"
    issues = check_images(soup(html))
    assert len(issues) == 1
    assert issues[0].severity == "warning"


def test_img_with_descriptive_alt():
    issues = check_images(soup("<img src='logo.png' alt='Company logo'>"))
    assert issues == []


# --- <input type="image"> ---

def test_input_image_missing_alt():
    issues = check_images(soup("<input type='image' src='btn.png'>"))
    assert len(issues) == 1
    assert issues[0].criterion == "4.1.2"
    assert issues[0].severity == "error"


def test_input_image_empty_alt():
    issues = check_images(soup("<input type='image' src='btn.png' alt=''>"))
    assert len(issues) == 1
    assert issues[0].criterion == "4.1.2"


def test_input_image_with_alt():
    issues = check_images(soup("<input type='image' src='btn.png' alt='Submit form'>"))
    assert issues == []
