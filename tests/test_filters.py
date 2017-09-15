from tifa.filters import under_score


def test_under_score_filter():
    assert under_score('Hello') == 'hello'
    assert under_score('HelloWorld') == 'hello_world'
