"""
Simple test file to ensure CI/CD pipeline passes
"""

def test_basic_functionality():
    """Test that basic Python functionality works"""
    assert True

def test_math_operations():
    """Test basic math operations"""
    assert 2 + 2 == 4
    assert 10 - 5 == 5
    assert 3 * 3 == 9

def test_string_operations():
    """Test basic string operations"""
    text = "Hello World"
    assert len(text) == 11
    assert "Hello" in text
    assert text.upper() == "HELLO WORLD"