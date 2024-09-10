import tkinter as tk
from tkinter import messagebox
import math

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.symbols = ['X', 'O']
        self.current_symbol = 'O'  # Player starts
        self.level = 1
        self.max_level = 10
        self.frames = []
        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root, bg="#282c34")
        self.login_frame.pack(padx=20, pady=20)

        self.password_label = tk.Label(self.login_frame, text="Enter password:", fg="white", bg="#282c34", font=('Arial', 14))
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.login_frame, show='*', font=('Arial', 14))
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.authenticate, bg="#61afef", fg="white", font=('Arial', 14))
        self.login_button.pack(pady=10)

    def authenticate(self):
        password = "1234"
        attempt = self.password_entry.get()
        if attempt == password:
            self.login_frame.destroy()
            self.create_board_size_screen()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def create_board_size_screen(self):
        self.size_frame = tk.Frame(self.root, bg="#282c34")
        self.size_frame.pack(padx=20, pady=20)

        self.size_label = tk.Label(self.size_frame, text="Enter board size (e.g., 3 for 3x3):", fg="white", bg="#282c34", font=('Arial', 14))
        self.size_label.pack(pady=5)

        self.size_entry = tk.Entry(self.size_frame, font=('Arial', 14))
        self.size_entry.pack(pady=5)

        self.size_button = tk.Button(self.size_frame, text="Set Size", command=self.set_board_size, bg="#61afef", fg="white", font=('Arial', 14))
        self.size_button.pack(pady=10)

    def set_board_size(self):
        size = self.size_entry.get()
        try:
            self.size = int(size)
            if self.size < 3:
                raise ValueError("Board size must be at least 3.")
            self.size_frame.destroy()
            self.create_game_boards()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid board size: {e}")

    def create_game_boards(self):
        for level in range(1, self.max_level + 1):
            frame = tk.Frame(self.root, bg="#282c34", padx=20, pady=20)
            frame.pack_forget()
            self.frames.append(frame)
            board = [['' for _ in range(self.size)] for _ in range(self.size)]
            buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
            for i in range(self.size):
                for j in range(self.size):
                    buttons[i][j] = tk.Button(frame, text='', font=('Arial', 24), width=5, height=2,
                                              command=lambda row=i, col=j, level=level: self.on_button_click(row, col, level),
                                              bg="#98c379", fg="#282c34", activebackground="#61afef")
                    buttons[i][j].grid(row=i, column=j, padx=5, pady=5)
            setattr(self, f'board_{level}', board)
            setattr(self, f'buttons_{level}', buttons)
        self.show_board(self.level)

    def show_board(self, level):
        self.current_symbol = 'O'
        self.frames[level-1].pack(padx=20, pady=20)

    def hide_board(self, level):
        self.frames[level-1].pack_forget()

    def on_button_click(self, row, col, level):
        board = getattr(self, f'board_{level}')
        buttons = getattr(self, f'buttons_{level}')
        if board[row][col] == '':
            board[row][col] = self.current_symbol
            buttons[row][col].config(text=self.current_symbol)
            if self.check_win(board, self.current_symbol):
                messagebox.showinfo("Game Over", f"{self.current_symbol} wins!")
                self.reset_game(level)
            elif not any('' in row for row in board):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game(level)
            else:
                self.current_symbol = 'X' if self.current_symbol == 'O' else 'O'
                if self.current_symbol == 'X':
                    self.root.after(1000, lambda: self.ai_move(level))

    def ai_move(self, level):
        best_move = self.find_best_move(level)
        if best_move:
            row, col = best_move
            board = getattr(self, f'board_{level}')
            buttons = getattr(self, f'buttons_{level}')
            board[row][col] = 'X'
            buttons[row][col].config(text='X')
            if self.check_win(board, 'X'):
                messagebox.showinfo("Game Over", "AI wins!")
                self.reset_game(level)
            elif not any('' in row for row in board):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game(level)
            else:
                self.current_symbol = 'O'

    def find_best_move(self, level):
        best_val = -math.inf
        best_move = None
        board = getattr(self, f'board_{level}')
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    move_val = self.minimax(board, 0, False)
                    board[i][j] = ''
                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val
        return best_move

    def minimax(self, board, depth, is_max):
        score = self.evaluate(board)
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any('' in row for row in board):
            return 0
        if is_max:
            best = -math.inf
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        best = max(best, self.minimax(board, depth + 1, not is_max))
                        board[i][j] = ''
            return best
        else:
            best = math.inf
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        best = min(best, self.minimax(board, depth + 1, not is_max))
                        board[i][j] = ''
            return best

    def evaluate(self, board):
        for symbol in ['X', 'O']:
            for row in board:
                if all(cell == symbol for cell in row):
                    return 10 if symbol == 'X' else -10
            for col in range(self.size):
                if all(board[row][col] == symbol for row in range(self.size)):
                    return 10 if symbol == 'X' else -10
        if all(board[i][i] == 'X' for i in range(self.size)) or \
           all(board[i][self.size - i - 1] == 'X' for i in range(self.size)):
            return 10
        if all(board[i][i] == 'O' for i in range(self.size)) or \
           all(board[i][self.size - i - 1] == 'O' for i in range(self.size)):
            return -10
        return 0

    def check_win(self, board, symbol):
        for row in board:
            if all(cell == symbol for cell in row):
                return True
        for col in range(self.size):
            if all(board[row][col] == symbol for row in range(self.size)):
                return True
        if all(board[i][i] == symbol for i in range(self.size)) or \
           all(board[i][self.size - i - 1] == symbol for i in range(self.size)):
            return True
        return False

    def reset_game(self, level):
        board = getattr(self, f'board_{level}')
        buttons = getattr(self, f'buttons_{level}')
        for i in range(self.size):
            for j in range(self.size):
                board[i][j] = ''
                buttons[i][j].config(text='')
        self.current_symbol = 'O'
        if level < self.max_level:
            self.hide_board(level)
            self.level += 1
            self.show_board(self.level)
        else:
            messagebox.showinfo("Game Over", "You have completed all levels!")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
