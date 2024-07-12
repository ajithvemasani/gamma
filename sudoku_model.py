import copy

def load_puzzle(data):
    puzzle = copy.deepcopy(data)
    for row in range(0,len(puzzle)):
        for col in range(0, len(puzzle[row])):
            value = str(data[row][col])
            if value == "0":
                possibilities = "123456789"
            else:
                possibilities = value
            puzzle[row][col] = {
                "value": value,
                "possibilities":possibilities
            }
    return puzzle   

def single_value_rule(puzzle):
    puzzle = copy.deepcopy(puzzle)
    for row in range(0,9):
        for col in range(0,9):
            possibilities = puzzle[row][col]["possibilities"]
            # if we have constrained the possibility, remove it for everything else
            if len(possibilities) == 1:
                # save the value
                puzzle[row][col]["value"] = possibilities
                # remove possibility from row and column
                for k in range(0, 9):
                    puzzle[row][k]["possibilities"] = puzzle[row][k]["possibilities"].replace(possibilities,"")
                    puzzle[k][col]["possibilities"] = puzzle[k][col]["possibilities"].replace(possibilities,"")
                # remove possibility from group
                g_row_0 = int(row / 3) * 3
                g_col_0 = int(col / 3) * 3
                for g_row in range(g_row_0, g_row_0 + 3):
                    for g_col in range(g_col_0, g_col_0 + 3):
                        puzzle[g_row][g_col]["possibilities"] = puzzle[g_row][g_col]["possibilities"].replace(possibilities,"")
                puzzle[row][col]["possibilities"] = ""
                return puzzle, f"Set {row},{col} to {possibilities} using single value rule."
    return puzzle, "No single value rule opportunities found."

def draw_puzzle(puzzle):
    for row in puzzle:
        for cell in row:
            print((cell["value"]+"          ")[0:10],end="")
        print()
        for cell in row:
            print((cell["possibilities"]+"          ")[0:10],end="")
        print()
        print()

def test_load_puzzle():
    data = [
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
    puzzle=load_puzzle(data)
    assert len(puzzle) == len(data)
    for row in puzzle:
        assert len(row) == len(data[0])
    for irow in range(0, len(data)):
        for icol in range(0, len(data[irow])):
            assert puzzle[irow][icol]["value"] == str(data[irow][icol])
            if puzzle[irow][icol]["value"] != "0":
                assert puzzle[irow][icol]["possibilities"] == puzzle[irow][icol]["value"]
            else:
                assert puzzle[irow][icol]["possibilities"] == "123456789"

def test_single_value_rule():
    data = [
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
    puzzle = load_puzzle(data)
    puzzle, message = single_value_rule(puzzle)
    print(message)
    draw_puzzle(puzzle)

def test_complete_solution():
    data = [
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
    puzzle = load_puzzle(data)
    for i in range(0,100):
        puzzle, message = single_value_rule(puzzle)
        print(message)
    draw_puzzle(puzzle)

if __name__ == "__main__":
    test_load_puzzle()
    #test_single_value_rule()
    test_complete_solution()