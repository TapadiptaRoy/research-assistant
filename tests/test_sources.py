from sources.pubmed_source import _stringify


def test_stringify_plain_string():
    assert _stringify("hello") == "hello"


def test_stringify_dict_with_text():
    assert _stringify({"#text": "hello", "i": "N"}) == "hello"


def test_stringify_none():
    assert _stringify(None) == ""


def test_stringify_nested_dict():
    # a dict whose #text value is itself a dict (deeper nesting)
    assert _stringify({"#text": {"#text": "deep hello"}}) == "deep hello"


def test_stringify_list():
    assert _stringify(["a", "b", "c"]) == "a b c"