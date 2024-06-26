import pytest
from unittest.mock import patch, MagicMock
from sudokumaster import validation, numbers_possible, generate_reason, print_board

@pytest.mark.parametrize("inputs, expected_output, mock_returns", [
    (["1", "1", "5"], "Board updated!", [5]),  # Valid placement
    (["1", "1"], "The cell is already filled. Please choose an empty cell.", []),  # Cell already filled
    (["1", "1", "10"], "Invalid range! Please enter numbers within the correct range.", []),  # Invalid range
])

def test_validation(monkeypatch, capfd, inputs, expected_output, mock_returns):
    board = [[0]*9 for _ in range(9)]
    if "cell is already filled" in expected_output:
        board[0][0] = 1

    inputs_cycle = iter(inputs + ["9"]*5)
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_cycle))

    with patch('sudokumaster.print_board', MagicMock()), \
         patch('sudokumaster.numbers_possible', return_value=mock_returns), \
         patch('sudokumaster.generate_reason', return_value="just a test reason") as mock_reason:
        
        validation(board)
        output = capfd.readouterr().out

        assert expected_output in output
        if "violates the Sudoku rules" in expected_output:
            mock_reason.assert_called_once()

# Test generate_reason
@pytest.mark.parametrize("num, board, row, col, expected_reason", [
    (5, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], 1, 1, "the number 5 is already in the same row."),
    (5, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], 3, 4, "the number 5 is already in the same column."),
    (5, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5]
    ], 7, 7, "the number 5 is already in the same 3x3 grid."),
    (5, [
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5]
    ], 0, 0, "the number 5 is already in the same row. and the number 5 is already in the same column. and the number 5 is already in the same 3x3 grid."),
])
def test_generate_reason(num, board, row, col, expected_reason):
    reason = generate_reason(num, board, row, col)
    assert reason == expected_reason

def print_board(board):
    pass

if __name__ == "__main__":
    pytest.main()
