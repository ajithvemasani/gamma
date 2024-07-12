from sudokumaster import validation, generate_board, get_board, print_board, generate_reason,generate_hint_reason, numbers_possible
import pytest
from unittest.mock import patch,MagicMock

#When user wants to play sudoku then this method will generate a sudoku board based on difficulty level
def test_get_board(monkeypatch):
    inputs = iter([
    "123456789",
    "45.789.23",
    ".8912345.",
    "...567891",
    "567...234",
    "891234...",
    "345678912",
    "678912345",
    "........."
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    board = get_board()
    assert len(board) == 9
    assert all(len(row) == 9 for row in board)
    assert board == [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 0, 7, 8, 9, 0, 2, 3],
        [0, 8, 9, 1, 2, 3, 4, 5, 0],
        [0, 0, 0, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 0, 0, 0, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 0, 0, 0],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


def test_print_board_valid(capfd):
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    expected_output = (
        "+-------+-------+-------+\n"
        "| 5 3 . | . 7 . | . . . |\n"
        "| 6 . . | 1 9 5 | . . . |\n"
        "| . 9 8 | . . . | . 6 . |\n"
        "+-------+-------+-------+\n"
        "| 8 . . | . 6 . | . . 3 |\n"
        "| 4 . . | 8 . 3 | . . 1 |\n"
        "| 7 . . | . 2 . | . . 6 |\n"
        "+-------+-------+-------+\n"
        "| . 6 . | . . . | 2 8 . |\n"
        "| . . . | 4 1 9 | . . 5 |\n"
        "| . . . | . 8 . | . 7 9 |\n"
        "+-------+-------+-------+\n"
        "\n"
    )

    print_board(board)
    captured = capfd.readouterr()
    assert captured.out == expected_output

def test_print_board_invalid(capfd):
    print_board([])
    captured = capfd.readouterr()
    assert captured.out == "The board is empty :(\n\n"

#test validation
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

def validation(board):
    """Function to validate user input and update the board."""
    while True:
        try:
            row = int(input("Enter the row (1-9): ")) - 1
            col = int(input("Enter the column (1-9): ")) - 1
            if not (0 <= row < 9) or not (0 <= col < 9):
                raise ValueError("Invalid range! Please enter numbers within the correct range.")
            if board[row][col] != 0:
                print("The cell is already filled. Please choose an empty cell.")
                return
            break
        except ValueError as e:
            print(e)

    attempts = 0
    while attempts < 3:
        try:
            num = int(input("Enter the number (1-9): "))
            if not (1 <= num <= 9):
                raise ValueError("Invalid range! Please enter numbers within the correct range.")
            possible_numbers = numbers_possible(board, row, col)
            if num not in possible_numbers:
                print(f"Invalid number. It violates the Sudoku rules because: {generate_reason(num, board, row, col)}")
                attempts += 1
                continue
            board[row][col] = num
            print("Board updated!")
            print_board(board)
            return
        except ValueError as e:
            print(e)
            attempts += 1

    if attempts == 3:
        possible_numbers = numbers_possible(board, row, col)
        print("Here is a hint. The possible numbers for this cell are:", possible_numbers)
        print("Reason:", generate_hint_reason(possible_numbers, board, row, col))
        while True:
            try:
                hint_choice = int(input(f"Enter one of the possible numbers {possible_numbers}: "))
                if hint_choice in possible_numbers:
                    board[row][col] = hint_choice
                    print("Board updated with a hint!")
                    print_board(board)
                    return
                else:
                    print("Invalid choice. Please choose one of the hinted numbers.")
            except ValueError:
                print("Invalid input! Please enter a valid number.") 

#test generate_reason
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
    ], 1, 0, "the number 5 is already in the same row. and the number 5 is already in the same 3x3 grid."),
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
    ], 2, 4, "the number 5 is already in the same column."),
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
    ], 0, 1, "the number 5 is already in the same row. and the number 5 is already in the same column. and the number 5 is already in the same 3x3 grid."),
])
def test_generate_reason(num, board, row, col, expected_reason):
    reason = generate_reason(num, board, row, col)
    print(f"Generated reason: {reason}")
    assert reason == expected_reason

if __name__ == "__main__":
    pytest.main()