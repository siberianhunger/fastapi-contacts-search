import pytest
from txt_to_db_data_parser import parse_separate_line, filter_name


@pytest.fixture
def valid_txt_lines():
    return [
        "123; John Peterson",
        "456;Doe",
        "555; 12345"
    ]


@pytest.fixture
def invalid_txt_lines():
    return [
        "John 123",
        "789",
        "Hello World",
        "",
        "123; John; ",
        "  456   Doe  "
    ]


@pytest.fixture
def sample_names_for_regexp_check():
    return [
        "Pepega (the boy)",
        "some ",
        "S.T.A.L.K.E.R.",
        "Who’s there?",
    ]


def test_parse_separate_line_valid(valid_txt_lines):
    expected_results = [
        (123, "John Peterson"),
        (456, "Doe"),
        (555, "12345")
    ]

    for line, expected in zip(valid_txt_lines, expected_results):
        assert parse_separate_line(line) == expected


def test_parse_separate_line_invalid(invalid_txt_lines):
    for line in invalid_txt_lines:
        assert parse_separate_line(line) is None


def test_filter_name(sample_names_for_regexp_check):
    expected_names = [
        "Pepega (the boy)",
        "some",
        "STALKER",
        "Who’s there",
    ]

    for line, expected in zip(sample_names_for_regexp_check, expected_names):
        assert filter_name(line) == expected


if __name__ == '__main__':
    pytest.main()
