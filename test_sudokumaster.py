from sudoku import Sudoku
import pytest

#When user wants to play sudoku then this method will generate a sudoku board based on difficulty level
def generate_board():
    while True:
        try:
            difficulty_level = int(input('\nDifficulty levels \n1. Beginner \n2. Intermediate \n3. Expert \nPlease enter which level you prefer 1 or 2 or 3.\n'))
            assert 0 < difficulty_level < 4
            break
        except ValueError:
            print("\nInvalid input! Please enter a valid number.")
        except AssertionError:
            print("\nThe number should be either 1 or 2 or 3. Please try again.")
    
    difficulty_level = 0.25 * difficulty_level
    puzzle = Sudoku(3).difficulty(difficulty_level)
    board = puzzle.board
    #replace 'None' given by Sudoku library with '.' and return board
    board = [[int(element) if element != None else 0 for element in row] for row in board]
    return board

def get_board():
    # Get user input for Sudoku puzzle ('.' denotes an empty cell). Returns a board
    board = []
    print("Enter the Sudoku puzzle row by row (use '.' for empty cells):")
    for i in range(9):
        row_input = input(f"Row {i + 1}: ").strip()
        if len(row_input) != 9 or not all(c.isdigit() or c == '.' for c in row_input):
            print("Invalid input. Each row must contain exactly 9 characters, either digits or '.'.")
            return
        row = [int(c) if c != '.' else 0 for c in row_input]
        board.append(row)
    return board

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

def print_board(board):
    """Function to print the Sudoku board."""
    if board != []:
        for i in range(9):
            if i % 3 == 0:
                print("+-------+-------+-------+")
            for j in range(9):
                if j % 3 == 0:
                    print("| ", end="")
                print(str(board[i][j]) if board[i][j] != 0 else ".", end=" ")
            print("|")
        print("+-------+-------+-------+")
    else:
        print("The board is empty :(")
    print()

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

#function for possible numbers
def numbers_possible(board,Row,Column):
    if board[Row][Column]!=0:
        return[]
    Values=set(range(1,10))
    #checking row
    Values=Values-set(board[Row])
    #checking for column
    Values=Values-{board[r][Column] for r in range(9)}
    #checking the grid
    s_row,s_col=3*(Row//3),3*(Column//3)
    for r in range(s_row,s_row+3):
        for c in range(s_col,s_col+3):
            Values.discard(board[r][c])
    return list(Values)

#printing possible numbers
def values_print(board):
    print("The possible values for empty cell in each column:")
    for Column in range(9):
        print(f"column {Column+1}:")
        for Row in range(9):
            if board[Row][Column]==0:
                Values=numbers_possible(board,Row,Column)
                print(f"Row {Row+1}: {Values}")
        print()


def main():
    """Main function."""
    while True:
        try:
            userChoice = int(input("\n1.Do you have a sudoku game?\nOR\n2.Do you want to generate one Sudoku game?\nPlease enter your choice as either 1 or 2.\n"))
            assert 0 < userChoice < 3
            break
        except ValueError:
            print("\nInvalid input! Please enter a valid number.")
        except AssertionError:
            print("\nThe number should be either 1 or 2. Please try again.")
            
    if userChoice == 1:
        board = get_board()
    elif userChoice == 2:
        board = generate_board()
    print_board(board)
    if board:
        values_print(board)
        
if __name__ == "__main__":
    main()
