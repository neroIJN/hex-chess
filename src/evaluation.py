from constants import PIECE_VALUES

class Evaluator:
    """Simple evaluation for material balance.

    evaluate(board) -> (score, total_material)
    - score: signed centipawn score (positive means white advantage)
    - total_material: sum of absolute piece values present on the board

    The evaluation is a simple sum of piece values; kings use a very large
    value to reflect their importance.
    """
    @staticmethod
    def evaluate(board):
        score = 0
        total = 0
        # Iterate over all tiles and sum material
        for tile in board.tiles.values():
            if tile and tile.has_piece():
                color, name = tile.get_piece()
                val = PIECE_VALUES.get(name, 0)
                total += abs(val)
                if color == 'white':
                    score += val
                else:
                    score -= val

        return score, total
    
class PST:
    """Piece-Square Tables for positional evaluation."""
    PST_VALUES = {
        'pawn': [
        ],
        # Add more piece tables as needed
    }
