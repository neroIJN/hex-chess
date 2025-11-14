from typing import Tuple, List

class MoveGenerator:
    """Encapsulates move-generation and attack detection for a HexBoard.

    Expects a board-like object with:
      - tiles: Dict[(q,r) -> HexTile]
      - get_tile(q,r)
      - current_turn
    """

    def __init__(self, board):
        self.board = board

    def get_legal_moves(self, q: int, r: int) -> List[Tuple[int, int]]:
        tile = self.board.get_tile(q, r)
        if not tile or not tile.has_piece():
            return []

        piece_color, piece_name = tile.get_piece()

        # Only show legal moves if it's this piece's turn
        if piece_color != self.board.current_turn:
            return []

        if piece_name == "pawn":
            return self._get_pawn_moves(q, r, piece_color)
        elif piece_name == "knight":
            return self._get_knight_moves(q, r, piece_color)
        elif piece_name == "bishop":
            return self._get_bishop_moves(q, r, piece_color)
        elif piece_name == "rook":
            return self._get_rook_moves(q, r, piece_color)
        elif piece_name == "queen":
            return self._get_queen_moves(q, r, piece_color)
        elif piece_name == "king":
            return self._get_king_moves(q, r, piece_color)

        return []

    def _get_pawn_moves(self, q: int, r: int, color: str):
        moves = []

        white_pawn_starts = [
            (-4, 5), (-3, 4), (-2, 3), (-1, 2), (0, 1),
            (1, 1), (2, 1), (3, 1), (4, 1)
        ]
        black_pawn_starts = [
            (4, -5), (3, -4), (2, -3), (1, -2), (0, -1),
            (-1, -1), (-2, -1), (-3, -1), (-4, -1)
        ]

        if color == "white":
            forward_dir = (0, -1)
            is_starting_position = (q, r) in white_pawn_starts
            capture_dirs = [(-1, 0), (1, -1)]
        else:
            forward_dir = (0, 1)
            is_starting_position = (q, r) in black_pawn_starts
            capture_dirs = [(1, 0), (-1, 1)]

        nq, nr = q + forward_dir[0], r + forward_dir[1]
        target = self.board.get_tile(nq, nr)
        if target and not target.has_piece():
            moves.append((nq, nr))
            if is_starting_position:
                nq2, nr2 = q + forward_dir[0] * 2, r + forward_dir[1] * 2
                target2 = self.board.get_tile(nq2, nr2)
                if target2 and not target2.has_piece():
                    moves.append((nq2, nr2))

        for dq, dr in capture_dirs:
            nq, nr = q + dq, r + dr
            target = self.board.get_tile(nq, nr)
            if target and target.has_piece():
                enemy_color, _ = target.get_piece()
                if enemy_color != color:
                    moves.append((nq, nr))

        return moves

    def _get_knight_moves(self, q: int, r: int, color: str):
        moves = []
        orthogonal_dirs = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (1, -1), (-1, 1)
        ]
        for dq, dr in orthogonal_dirs:
            mid_q, mid_r = q + 2*dq, r + 2*dr

            if (dq, dr) == (1, 0):
                perpendicular = [(0, 1), (1, -1)]
            elif (dq, dr) == (-1, 0):
                perpendicular = [(0, -1), (-1, 1)]
            elif (dq, dr) == (0, 1):
                perpendicular = [(-1, 1), (1, 0)]
            elif (dq, dr) == (0, -1):
                perpendicular = [(1, -1), (-1, 0)]
            elif (dq, dr) == (1, -1):
                perpendicular = [(1, 0), (0, -1)]
            else:
                perpendicular = [(-1, 0), (0, 1)]

            for pq, pr in perpendicular:
                nq, nr = mid_q + pq, mid_r + pr
                target = self.board.get_tile(nq, nr)
                if target:
                    if not target.has_piece():
                        moves.append((nq, nr))
                    else:
                        enemy_color, _ = target.get_piece()
                        if enemy_color != color:
                            moves.append((nq, nr))
        return moves

    def _get_sliding_moves(self, q: int, r: int, color: str, directions):
        moves = []
        for dq, dr in directions:
            nq, nr = q + dq, r + dr
            while (nq, nr) in self.board.tiles:
                target = self.board.get_tile(nq, nr)
                if not target.has_piece():
                    moves.append((nq, nr))
                else:
                    enemy_color, _ = target.get_piece()
                    if enemy_color != color:
                        moves.append((nq, nr))
                    break
                nq += dq
                nr += dr
        return moves

    def _get_bishop_moves(self, q: int, r: int, color: str):
        moves = []
        current_tile = self.board.get_tile(q, r)
        if not current_tile:
            return moves
        target_color = current_tile.color
        diagonal_dirs = [
            (1, 1), (-1, -1),
            (2, -1), (-2, 1),
            (1, -2), (-1, 2)
        ]
        for dq, dr in diagonal_dirs:
            nq, nr = q + dq, r + dr
            while (nq, nr) in self.board.tiles:
                target = self.board.get_tile(nq, nr)
                if target.color != target_color:
                    break
                if not target.has_piece():
                    moves.append((nq, nr))
                else:
                    enemy_color, _ = target.get_piece()
                    if enemy_color != color:
                        moves.append((nq, nr))
                    break
                nq += dq
                nr += dr
        return moves

    def _get_rook_moves(self, q: int, r: int, color: str):
        orthogonal_dirs = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (1, -1), (-1, 1)
        ]
        return self._get_sliding_moves(q, r, color, orthogonal_dirs)

    def _get_queen_moves(self, q: int, r: int, color: str):
        rook_moves = self._get_rook_moves(q, r, color)
        bishop_moves = self._get_bishop_moves(q, r, color)
        return list(set(rook_moves + bishop_moves))

    def _get_king_moves(self, q: int, r: int, color: str):
        moves = []
        current_tile = self.board.get_tile(q, r)
        if not current_tile:
            return moves
        target_color = current_tile.color
        orthogonal_dirs = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (1, -1), (-1, 1)
        ]
        diagonal_dirs = [
            (1, 1), (-1, -1),
            (2, -1), (-2, 1),
            (1, -2), (-1, 2)
        ]
        for dq, dr in orthogonal_dirs:
            nq, nr = q + dq, r + dr
            target = self.board.get_tile(nq, nr)
            if target:
                if not target.has_piece():
                    moves.append((nq, nr))
                else:
                    enemy_color, _ = target.get_piece()
                    if enemy_color != color:
                        moves.append((nq, nr))
        for dq, dr in diagonal_dirs:
            nq, nr = q + dq, r + dr
            target = self.board.get_tile(nq, nr)
            if target and target.color == target_color:
                if not target.has_piece():
                    moves.append((nq, nr))
                else:
                    enemy_color, _ = target.get_piece()
                    if enemy_color != color:
                        moves.append((nq, nr))
        return moves

    def is_square_attacked(self, q: int, r: int, by_color: str) -> bool:
        for (pq, pr), tile in self.board.tiles.items():
            if not tile.has_piece():
                continue
            piece_color, piece_name = tile.get_piece()
            if piece_color != by_color:
                continue
            if piece_name == "pawn":
                if piece_color == "white":
                    capture_dirs = [(-1, 0), (1, -1)]
                else:
                    capture_dirs = [(1, 0), (-1, 1)]
                for dq, dr in capture_dirs:
                    if (pq + dq, pr + dr) == (q, r):
                        return True
            else:
                if piece_name == "knight":
                    moves = self._get_knight_moves(pq, pr, piece_color)
                elif piece_name == "bishop":
                    moves = self._get_bishop_moves(pq, pr, piece_color)
                elif piece_name == "rook":
                    moves = self._get_rook_moves(pq, pr, piece_color)
                elif piece_name == "queen":
                    moves = self._get_queen_moves(pq, pr, piece_color)
                elif piece_name == "king":
                    moves = self._get_king_moves(pq, pr, piece_color)
                else:
                    moves = []
                if (q, r) in moves:
                    return True
        return False