import tkinter as tk
from tkinter import messagebox

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
        self.master.title("Sudoku")
        self.cells = {}
        self.create_widgets()

    def create_widgets(self):
        for row in range(9):
            for col in range(9):
                var = tk.StringVar()
                entry = tk.Entry(self.master, width=2, font=('Arial', 45), justify='center', textvariable=var)
                entry.grid(row=row, column=col, sticky="nsew")
                if puzzle[row][col] != 0:
                    entry.insert(tk.END, puzzle[row][col])
                    entry.config(state='disabled')
                else:
                    possible_vals = self.possible_numbers(row, col)
                    entry.insert(tk.END, ' '.join(map(str, possible_vals)))
                    entry.config(font=('Arial', 15))
                self.cells[(row, col)] = entry

        button_frame = tk.Frame(self.master)
        button_frame.grid(row=9, column=0, columnspan=9, sticky="ew")
        tk.Button(button_frame, text="Clear", command=self.clear).grid(row=0, column=0)

    def possible_numbers(self, row, col):
        if puzzle[row][col] != 0:
            return []

        possible = set(range(1, 10))
        possible -= set(puzzle[row]) | {puzzle[i][col] for i in range(9)}
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(block_row, block_row + 3):
            for j in range(block_col, block_col + 3):
                possible.discard(puzzle[i][j])
        return list(possible)

    
    def clear(self):
        for (row, col), entry in self.cells.items():
            if puzzle[row][col] == 0:
                entry.delete(0, tk.END)
                possible_vals = self.possible_numbers(row, col)
                entry.insert(tk.END, ' '.join(map(str, possible_vals)))
                entry.config(font=('Arial', 12))  
                
def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
