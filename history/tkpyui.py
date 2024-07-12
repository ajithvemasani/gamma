import tkinter as tk

# Define the initial Sudoku board (0 represents empty cells)
initial_board = [
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

# Define the solution board (for validation)
solution_board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

# Create the main window
root = tk.Tk()
root.title("Sudoku Master")

# Function to validate and update cell color
def validate_and_update(event, i, j):
    entry = entries[i][j]
    value = entry.get()
    
    if value.isdigit() and 1 <= int(value) <= 9:
        if int(value) == solution_board[i][j]:
            entry.config(bg='pale green')
        else:
            entry.config(bg='red')
    else:
        entry.delete(0, tk.END)
        entry.config(bg='white')

# Create a 9x9 grid of entry widgets
entries = []
for i in range(9):
    row = []
    for j in range(9):
        if initial_board[i][j] != 0:
            entry = tk.Entry(root, width=2, font=('Arial', 20, 'bold'), justify='center', readonlybackground='white')
            entry.insert(tk.END, initial_board[i][j])
            entry.config(state=tk.DISABLED)
        else:
            entry = tk.Entry(root, width=2, font=('Arial', 20, 'bold'), justify='center')
            entry.bind('<FocusOut>', lambda event, i=i, j=j: validate_and_update(event, i, j))
        entry.grid(row=i, column=j, padx=1, pady=1)
        row.append(entry)
    entries.append(row)

# Run the main event loop
root.mainloop()
