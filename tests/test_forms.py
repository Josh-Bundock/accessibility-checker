import pytest
from bs4 import BeautifulSoup
from checker.rules.forms import check_forms


def soup(html):
    return BeautifulSoup(html, "lxml")


# --- Label detection ---

def test_input_no_label():
    issues = check_forms(soup("<input type='text'>"))
    assert any(i.criterion == "1.3.1" and i.severity == "error" for i in issues)


def test_input_with_aria_label():
    issues = check_forms(soup("<input type='text' aria-label='Full name'>"))
    assert not any(i.criterion == "1.3.1" for i in issues)


def test_input_with_label_for():
    html = "<label for='name'>Name</label><input type='text' id='name'>"
    issues = check_forms(soup(html))
    assert not any(i.criterion == "1.3.1" for i in issues)


def test_input_wrapped_in_label():
    html = "<label>Name <input type='text'></label>"
    issues = check_forms(soup(html))
    assert not any(i.criterion == "1.3.1" for i in issues)


def test_input_with_title():
    issues = check_forms(soup("<input type='text' title='Search'>"))
    assert not any(i.criterion == "1.3.1" for i in issues)


def test_input_with_aria_labelledby():
    html = "<span id='lbl'>Email</span><input type='text' aria-labelledby='lbl'>"
    issues = check_forms(soup(html))
    assert not any(i.criterion == "1.3.1" for i in issues)


# --- Unlabellable types should be skipped ---

def test_hidden_input_no_label():
    issues = check_forms(soup("<input type='hidden'>"))
    assert not any(i.criterion == "1.3.1" for i in issues)


def test_submit_input_no_label():
    issues = check_forms(soup("<input type='submit' value='Go'>"))
    assert not any(i.criterion == "1.3.1" for i in issues)


def test_button_input_no_label():
    issues = check_forms(soup("<input type='button' value='Click'>"))
    assert not any(i.criterion == "1.3.1" for i in issues)


# --- select and textarea ---

def test_select_no_label():
    issues = check_forms(soup("<select><option>One</option></select>"))
    assert any(i.criterion == "1.3.1" for i in issues)


def test_textarea_no_label():
    issues = check_forms(soup("<textarea></textarea>"))
    assert any(i.criterion == "1.3.1" for i in issues)


def test_select_with_label():
    html = "<label for='s'>Pick one</label><select id='s'><option>One</option></select>"
    issues = check_forms(soup(html))
    assert not any(i.criterion == "1.3.1" for i in issues)


# --- Autocomplete ---

def test_email_field_missing_autocomplete():
    issues = check_forms(soup("<input type='email' name='email'>"))
    assert any(i.criterion == "1.3.5" for i in issues)


def test_email_field_autocomplete_on():
    issues = check_forms(soup("<input type='email' name='email' autocomplete='on'>"))
    assert any(i.criterion == "1.3.5" for i in issues)


def test_email_field_correct_autocomplete():
    issues = check_forms(soup("<input type='email' name='email' autocomplete='email'>"))
    assert not any(i.criterion == "1.3.5" for i in issues)


def test_name_field_missing_autocomplete():
    issues = check_forms(soup("<input type='text' name='fname'>"))
    assert any(i.criterion == "1.3.5" for i in issues)


def test_phone_field_missing_autocomplete():
    issues = check_forms(soup("<input type='tel' name='phone'>"))
    assert any(i.criterion == "1.3.5" for i in issues)
