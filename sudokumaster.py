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

def main():
    """Main function."""
    board = get_board()
    print_board(board)

if __name__ == "__main__":
    main()
