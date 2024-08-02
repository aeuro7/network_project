

def print_board(board):
    board_str = "- Welcome to EU Ciniplex -" + "\n\n"

    board_str += "____________________________\n/          screen          \\ \n\n"

    row_labels = 'abcdefghij'
    for i, row in enumerate(board):
        board_str += f"  {row_labels[i]}   " + ' '.join(row) + "\n"

    board_str += "\n      " + " ".join(str(i) for i in range(1, 11)) + "\n"
    board_str += "\nPlease select the seats you would like."
    # print(board_str)
    return board_str

