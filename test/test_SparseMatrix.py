import pytest

def test_SparseMatrix_is_importable():
    from Scrabble.src.SparseMatrix import SparseMatrix

@pytest.mark.xfail(reason='expected string does not account for width formatting.')
def test_toString():
    from Scrabble.src.SparseMatrix import SparseMatrix
    x = SparseMatrix()
    x[(1,1)] = 1
    expected_string = ' .  . \n .  1 \n'
    assert x.toString() == expected_string
    assert x.toString(default=',') == expected_string.replace('.',',')

def test_init_parameters():
    from Scrabble.src.SparseMatrix import SparseMatrix
    x = SparseMatrix({'test': 'test'})
    assert x['test'] == 'test'
