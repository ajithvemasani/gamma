import tkinter as tk
from tkinter import messagebox

# Initial Sudoku board setup, where 0 indicates an empty space
puzzle = [
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

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.cells = {}
        self.create_widgets()

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

def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
