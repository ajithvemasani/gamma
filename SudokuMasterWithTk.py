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
        for row in range(12):
            for col in range(12):
                if row % 4 == 0 or col % 4 == 0:
                    frame = tk.Frame(self.master, bg='black', width=3 if col % 4 == 0 else 1, height=3 if row % 4 == 0 else 1)
                    frame.grid(row=row, column=col, sticky="nsew")
                else:
                    adj_row = row - (row // 4) - 1
                    adj_col = col - (col // 4) - 1
                    var = tk.StringVar()
                    entry = tk.Entry(self.master, textvariable=var, font=('Arial', 10), width=2, justify='center', bd=1)
                    entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                    entry.bind('<FocusIn>', lambda e, r=adj_row, c=adj_col: self.focus_in_action(r, c))
                    entry.bind('<FocusOut>', lambda e, r=adj_row, c=adj_col: self.focus_out_action(r, c))
                    if puzzle[adj_row][adj_col] != 0:
                        var.set(puzzle[adj_row][adj_col])
                        entry.config(font=('Arial', 40), state='readonly')
                    else:
                        self.display_possible_numbers(entry, adj_row, adj_col)
                    self.cells[(adj_row, adj_col)] = (entry, var)
    
        Single_Value_Rule_button = tk.Button(self.master, text="Single Value Rule", command=self.single_value_rule)
        Single_Value_Rule_button.grid(row=12, column=0, columnspan=3, sticky="nsew")
        
                    
    def focus_in_action(self, row, col):
        entry, var = self.cells[(row, col)]
        if puzzle[row][col] == 0:
            var.set('')
            entry.config(font=('Arial', 40), fg='black')

    def focus_out_action(self, row, col):
        entry, var = self.cells[(row, col)]
        try:
            value = int(var.get())
            if 1 <= value <= 9:
                if self.is_valid(value, row, col):
                    puzzle[row][col] = value
                    entry.config(state='readonly')
                    self.update_related_cells(row, col)
                else:
                    messagebox.showerror("Error", "This number can't go here.")
            else:
                raise ValueError
        except ValueError:
            self.display_possible_numbers(entry, row, col)

    def display_possible_numbers(self, entry, row, col):
        if puzzle[row][col] == 0:
            possible = self.possible_numbers(row, col)
            entry.delete(0, 'end')
            entry.insert(0, ' '.join(map(str, sorted(possible))))
            entry.config(font=('Arial', 12), fg='gray', state='normal')

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

    def single_value_rule(self):
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] == 0:
                    possible = self.possible_numbers(row, col) 
                    if len(possible) == 1:
                        puzzle[row][col] = list(possible)[0]
                        entry = self.cells[(row, col)]
                        entry.config(font=('Arial', 40), fg='black', state='readonly')
                        self.update_related_cells(row, col)
                        alertMessage = "Single Value Rule Applied for Cell: " + str(row+1) + " , " + str(col+1)
                        messagebox.showerror("Alert", alertMessage)
                        return row, col, possible
        return

def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
