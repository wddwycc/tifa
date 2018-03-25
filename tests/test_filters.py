from tifa.filters import underscore


def test_underscore():
    assert underscore('Hello') == 'hello'
    assert underscore('HelloWorld') == 'hello_world'
