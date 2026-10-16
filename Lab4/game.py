from board import Board
from ai import AI


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.turn = "X"

    def run(self):
        print("Connect Four — you are X.")

        while True:
            self.board.print()

            # Handle a full board before requesting another move.
            if self.board.full():
                print("Draw! The board is full.")
                return

            if self.turn == "X":
                raw = input("Column (1-7), or q: ").strip().lower()

                if raw == "q":
                    print("Game quit. Thanks for playing!")
                    return

                try:
                    col = int(raw) - 1
                except ValueError:
                    print("Invalid input. Enter a column number from 1 to 7, or q to quit.")
                    continue

                # Check the range before attempting to drop a token.
                if not 0 <= col < 7:
                    print("Invalid column. Choose a number from 1 to 7.")
                    continue

                # Reject full columns without changing the board.
                if self.board.grid[0][col] != ".":
                    print(f"Column {col + 1} is full. Choose another column.")
                    continue

            else:
                col = self.ai.choose_column(self.board)

                # Handle an AI that cannot find a move.
                if col is None:
                    if self.board.full():
                        print("Draw! The board is full.")
                    else:
                        print("AI could not find a move. Game ended.")
                    return

                # Validate the AI's selected column too.
                if not isinstance(col, int) or not 0 <= col < 7:
                    print("AI returned an invalid column. Game ended.")
                    return

                if self.board.grid[0][col] != ".":
                    print(f"AI selected full column {col + 1}. Game ended.")
                    return

            # Only valid moves reach this point.
            row = self.board.drop(col, self.turn)

            # Defensive check in case the move is rejected.
            if row is None:
                print("Move rejected. Please try again.")
                if self.turn == "O":
                    print("AI could not complete its move. Game ended.")
                    return
                continue

            # Task 4 - Report each successful move exactly once.
            if self.turn == "X":
                print(f"You dropped X in column {col + 1}.")
            else:
                print(f"AI dropped O in column {col + 1}.")

            # Check for a win immediately after the move.
            if self.board.winner(self.turn):
                self.board.print()
                if self.turn == "X":
                    print("You win!")
                else:
                    print("AI wins!")
                return

            # Check for a draw after checking for a win.
            if self.board.full():
                self.board.print()
                print("Draw! The board is full.")
                return

            # Switch turns only when the game is still active.
            self.turn = "O" if self.turn == "X" else "X"
