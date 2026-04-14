import pytest
from src.parser import validate_course_data, is_open

def test_valid_open_course():
    data = {"code": "36000", "enrolled": "100/150", "status": "OPEN", "waitlist": "0/0"}
    assert validate_course_data(data) == True
    assert is_open(data) == True

def test_full_course():
    data = {"code": "36000", "enrolled": "150/150", "status": "FULL", "waitlist": "20/20"}
    assert validate_course_data(data) == True
    assert is_open(data) == False

def test_missing_field():
    data = {"code": "36000", "status": "OPEN"}
    assert validate_course_data(data) == False

def test_none_data():
    assert validate_course_data(None) == False
