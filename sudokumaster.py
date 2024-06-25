from sudoku import Sudoku

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

#function for possible numbers
def numbers_possible(board, Row, Column):
    if board[Row][Column] != 0:
        return []
    Values = set(range(1, 10))
    #checking row
    Values = Values - set(board[Row])
    #checking for column
    Values = Values - {board[r][Column] for r in range(9)}
    #checking the grid
    s_row, s_col = 3 * (Row // 3), 3 * (Column // 3)
    for r in range(s_row, s_row + 3):
        for c in range(s_col, s_col + 3):
            Values.discard(board[r][c])
    return list(Values)

#printing possible numbers
def values_print(board):
    print("The possible values for empty cell in each column:")
    for Column in range(9):
        print(f"column {Column+1}:")
        for Row in range(9):
            if board[Row][Column] == 0:
                Values = numbers_possible(board, Row, Column)
                print(f"Row {Row+1}: {Values}")
        print()

def validation(board):
    """Function to validate user input and update the board."""
    while True:
        try:
            row = int(input("Enter the row (1-9): ")) - 1
            col = int(input("Enter the column (1-9): ")) - 1
            assert 0 <= row < 9 and 0 <= col < 9
            if board[row][col] != 0:
                print("The cell is already filled. Please choose an empty cell.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter valid numbers.")
        except AssertionError:
            print("Invalid range! Please enter numbers within the correct range.")

    attempts = 0
    while attempts < 3:
        try:
            num = int(input("Enter the number (1-9): "))
            assert 1 <= num <= 9
            possible_numbers = numbers_possible(board, row, col)
            if num not in possible_numbers:
                print(f"Invalid number. It violates the Sudoku rules because: {generate_reason(num, board, row, col)}. Try another number.")
                attempts += 1
                continue
            board[row][col] = num
            print_board(board)
            return
        except ValueError:
            print("Invalid input! Please enter valid numbers.")
        except AssertionError:
            print("Invalid range! Please enter numbers within the correct range.")
        attempts += 1

    if attempts == 3:
        possible_numbers = numbers_possible(board, row, col)
        print("Here is a hint. The possible numbers for this cell are: ", possible_numbers)
        print("Reason: ", generate_hint_reason(possible_numbers, board, row, col))
        while True:
            try:
                hint_choice = int(input(f"Enter one of the possible numbers {possible_numbers}: "))
                if hint_choice in possible_numbers:
                    board[row][col] = hint_choice
                    print_board(board)
                    return
                else:
                    print("Invalid choice. Please choose one of the hinted numbers.")
            except ValueError:
                print("Invalid input! Please enter a valid number.")

def generate_reason(num, board, row, col):
    reasons = []
    if num in board[row]:
        reasons.append(f"the number {num} is already in the same row.")
    if num in [board[r][col] for r in range(9)]:
        reasons.append(f"the number {num} is already in the same column.")
    s_row, s_col = 3 * (row // 3), 3 * (col // 3)
    if num in [board[r][c] for r in range(s_row, s_row + 3) for c in range(s_col, s_col + 3)]:
        reasons.append(f"the number {num} is already in the same 3x3 grid.")
    return " and ".join(reasons)

def generate_hint_reason(possible_numbers, board, row, col):
    return f"The possible numbers are valid because they do not repeat in the same row, column, or 3x3 grid."
    print("The possible values for each cell:")
    for Row in range(9):
        for Column in range(9):
            if board[Row][Column] == 0:
                Values=numbers_possible(board,Row,Column)
                print(f"Cell({Row+1},{Column+1}): {Values}")

def main():
    """Main function."""
    while True:
        try:
            userChoice = int(input("\n1. Do you have a sudoku game?\nOR\n2. Do you want to generate one Sudoku game?\nPlease enter your choice as either 1 or 2.\n"))
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
        while True:
            try:
                playChoice = int(input("Do you want to input a number? 1 for Yes, 2 for No: "))
                assert 0 < playChoice < 3
                if playChoice == 1:
                    validation(board)
                else:
                    break
            except ValueError:
                print("\nInvalid input! Please enter a valid number.")
            except AssertionError:
                print("\nThe number should be either 1 or 2. Please try again.")

if __name__ == "__main__":
    main()
