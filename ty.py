movies = {
    "Top Gun: Maverick": [['o' for _ in range(10)] for _ in range(10)],
    "Avengers: Endgame": [['o' for _ in range(10)] for _ in range(10)],
    "The Matrix": [['o' for _ in range(10)] for _ in range(10)]
}

# เลือกภาพยนตร์ที่ต้องการพิมพ์
selected_movie = "Top Gun: Maverick"
board = movies[selected_movie]

# พิมพ์สถานะปัจจุบันของบอร์ด
board_str = "- Welcome to EU Ciniplex -" + "\n\n"

# เพิ่มบรรทัดสำหรับหน้าจอหนัง
board_str += "____________________________\n/          screen          \ \n\n"

# พิมพ์แถวที่นั่ง
row_labels = 'abcdefghij'
for i, row in enumerate(board):
    board_str += f"  {row_labels[i]}   " + ' '.join(row) + "\n"

# เพิ่มเลขคอลัมน์ด้านล่างของตาราง
board_str += "\n      " + " ".join(str(i) for i in range(1, 11)) + "\n"
board_str += "\nPlease select the seats you would like."
print(board_str)
