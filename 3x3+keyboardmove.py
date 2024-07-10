import tkinter as tk
from tkinter import messagebox
import copy

# Initial Sudoku board setup, where 0 indicates an empty space
initial_puzzle = [
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

# Create a copy of the initial puzzle to reset the board
puzzle = copy.deepcopy(initial_puzzle)

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.cells = {}
        self.create_widgets()

        # Bind arrow keys to navigation functions
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)

    def create_widgets(self):
        # Create canvas for drawing grid lines
        self.canvas = tk.Canvas(self.master, width=720, height=720)
        self.canvas.grid(row=0, column=0, rowspan=9, columnspan=9)
        
        # Draw 3x3 subgrid lines
        for i in range(10):
            if i % 3 == 0:
                thickness = 3
            else:
                thickness = 1
            self.canvas.create_line(0, i * 80, 720, i * 80, width=thickness)
            self.canvas.create_line(i * 80, 0, i * 80, 720, width=thickness)
        
        # Create Sudoku grid entries
        for row in range(9):
            for col in range(9):
                var = tk.StringVar()
                text = tk.Text(self.master, font=('Arial', 20), width=10, height=5, wrap='none', padx=10, pady=10)
                text.place(x=col * 80 + 2, y=row * 80 + 2, width=76, height=76)
                text.bind('<FocusIn>', lambda e, r=row, c=col: self.focus_in_action(r, c))
                text.bind('<FocusOut>', lambda e, r=row, c=col: self.focus_out_action(r, c))
                if puzzle[row][col] != 0:
                    text.insert('1.0', puzzle[row][col])
                    text.config(font=('Arial', 28), state='disabled', padx=20, pady=20)
                else:
                    self.display_possible_numbers(text, row, col)
                self.cells[(row, col)] = (text, var)
        
        # Add control buttons
        solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        solve_button.place(x=100, y=750, width=200, height=40)

        clear_button = tk.Button(self.master, text="Clear", command=self.clear_board)
        clear_button.place(x=400, y=750, width=200, height=40)

    def focus_in_action(self, row, col):
        text, var = self.cells[(row, col)]
        if puzzle[row][col] == 0:
            text.delete('1.0', 'end')
            text.config(font=('Arial', 28), fg='black')

    def focus_out_action(self, row, col):
        text, var = self.cells[(row, col)]
        try:
            value = int(text.get('1.0', 'end').strip())
            if 1 <= value <= 9:
                if self.is_valid(value, row, col):
                    puzzle[row][col] = value
                    text.delete('1.0', 'end')
                    text.insert('1.0', value)
                    text.config(state='disabled')
                    self.update_related_cells(row, col)
                else:
                    messagebox.showerror("Error", "This number can't go here.")
            else:
                raise ValueError
        except ValueError:
            self.display_possible_numbers(text, row, col)

    def display_possible_numbers(self, text, row, col):
        if puzzle[row][col] == 0:
            possible = self.possible_numbers(row, col)
            text.delete('1.0', 'end')
            formatted_possible = self.format_possible_numbers(possible)
            text.insert('1.0', formatted_possible)
            text.config(font=('Arial', 16), fg='gray', state='normal')

    def format_possible_numbers(self, possible):
        possible = sorted(possible)
        formatted = ""
        for i in range(1, 10):
            formatted += str(i) if i in possible else " "
            if i % 3 == 0:
                formatted += "\n"
            else:
                formatted += "  "
        return formatted.strip()

    def possible_numbers(self, row, col):
        if puzzle[row][col] != 0: return []
        possible = set(range(1, 10))
        possible -= set(puzzle[row]) | {puzzle[i][col] for i in range(9)}
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(block_row, block_row + 3):
            for j in range(block_col, block_col + 3):
                possible.discard(puzzle[i][j])
        return possible

    def is_valid(self, val, row, col):
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        if any(puzzle[row][i] == val for i in range(9) if i != col): return False
        if any(puzzle[i][col] == val for i in range(9) if i != row): return False
        for i in range(block_row, block_row + 3):
            for j in range(block_col, block_col + 3):
                if puzzle[i][j] == val and (i != row or j != col): return False
        return True

    def update_related_cells(self, row, col):
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(9):
            if i != col: self.display_possible_numbers(self.cells[(row, i)][0], row, i)
            if i != row: self.display_possible_numbers(self.cells[(i, col)][0], i, col)
        for i in range(block_row, block_row + 3):
            for j in range(block_col, block_col + 3):
                if (i != row or j != col): self.display_possible_numbers(self.cells[(i, j)][0], i, j)

    def move_focus(self, row, col):
        entry, var = self.cells.get((row, col), (None, None))
        if entry:
            entry.focus_set()

    def move_left(self, event):
        focused_widget = self.master.focus_get()
        for (row, col), (entry, var) in self.cells.items():
            if entry == focused_widget:
                if col > 0:
                    self.move_focus(row, col - 1)
                break

    def move_right(self, event):
        focused_widget = self.master.focus_get()
        for (row, col), (entry, var) in self.cells.items():
            if entry == focused_widget:
                if col < 8:
                    self.move_focus(row, col + 1)
                break

    def move_up(self, event):
        focused_widget = self.master.focus_get()
        for (row, col), (entry, var) in self.cells.items():
            if entry == focused_widget:
                if row > 0:
                    self.move_focus(row - 1, col)
                break

    def move_down(self, event):
        focused_widget = self.master.focus_get()
        for (row, col), (entry, var) in self.cells.items():
            if entry == focused_widget:
                if row < 8:
                    self.move_focus(row + 1, col)
                break

    def solve(self):
        if self.solve_sudoku(puzzle):
            self.update_board()
            messagebox.showinfo("Solved", "The Sudoku puzzle has been solved!")
        else:
            messagebox.showerror("Error", "The Sudoku puzzle cannot be solved.")

    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def clear_board(self):
        global puzzle
        puzzle = copy.deepcopy(initial_puzzle)
        self.update_board()

    def update_board(self):
        for row in range(9):
            for col in range(9):
                text, var = self.cells[(row, col)]
                if puzzle[row][col] != 0:
                    text.config(state='normal')
                    text.delete('1.0', 'end')
                    text.insert('1.0', puzzle[row][col])
                    text.config(font=('Arial', 28), fg='black', state='disabled')
                else:
                    var.set('')
                    text.config(font=('Arial', 10), state='normal')
                    self.display_possible_numbers(text, row, col)

def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
