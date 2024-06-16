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
def numbers_possible(board,Row,Column):
    if board[Row][Column]!=0:
        return[]
    Values=set(range(1,10))
    #checking row
    Values=Values-set(board[Row])
    #checking for column
    Values=Values-{board[r][column] for r in range(9)}
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
    board = [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]
    print_board(board)
    if board:
        values_print(board)

if __name__ == "__main__":
    main()
