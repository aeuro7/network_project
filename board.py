# def print_board(board):
#     """Print the current state of the board."""
#     board_str = "- Welcome to EU Ciniplex -"+"\n\n    " + " ".join(str(i) for i in range(1, 11)) + "\n"  # Column numbers from 1 to 10
#     row_labels = 'abcdefghij'
#     for i, row in enumerate(board):
#         board_str += f"{row_labels[i]}   " + ' '.join(row) + "\n"
#     print(board_str)
#     return board_str


def print_board(board):
    board_str = "- Welcome to EU Ciniplex -" + "\n\n"

    # เพิ่มบรรทัดสำหรับหน้าจอหนัง
    board_str += "____________________________\n/          screen          \\ \n\n"

    # พิมพ์แถวที่นั่ง
    row_labels = 'abcdefghij'
    for i, row in enumerate(board):
        board_str += f"  {row_labels[i]}   " + ' '.join(row) + "\n"

    # เพิ่มเลขคอลัมน์ด้านล่างของตาราง
    board_str += "\n      " + " ".join(str(i) for i in range(1, 11)) + "\n"
    board_str += "\nPlease select the seats you would like."
    print(board_str)
    return board_str

