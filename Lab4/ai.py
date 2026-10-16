import random


class AI:
    def choose_column(self, board, me="O", opponent="X"):
        # Find columns that can legally accept a token.
        legal = [
            c for c in range(7)
            if board.grid[0][c] == "."
        ]

        # No legal moves are available.
        if not legal:
            return None

        # 1. Take an immediate winning move.
        for col in legal:
            row = board.drop(col, me)

            if row is not None:
                wins = board.winner(me)
                board.grid[row][col] = "."

                if wins:
                    return col

        # 2. Block an immediate opponent win.
        for col in legal:
            row = board.drop(col, opponent)

            if row is not None:
                wins = board.winner(opponent)
                board.grid[row][col] = "."

                if wins:
                    return col

        # 3. Prefer the centre column, then nearby columns.
        centre = 3
        best_distance = min(abs(c - centre) for c in legal)
        preferred = [
            c for c in legal
            if abs(c - centre) == best_distance
        ]

        # Randomly choose among equally preferred columns.
        return random.choice(preferred)
