from constants import PIECE_VALUES, MG_PST_VALUES, EG_PST_VALUES, MAX_PHASE, PHASE_VALUES

class PST:
    """Piece-Square Tables for positional evaluation."""
    
    @staticmethod
    def get_pst_value(piece_name: str, q: int, r: int, color: str, phase: int) -> int:
        """
        Get the piece-square table value for a piece at (q, r).
        Uses tapered evaluation based on game phase.
        
        Args:
            piece_name: Name of the piece ('pawn', 'knight', etc.)
            q, r: Axial coordinates
            color: 'white' or 'black'
            phase: Current game phase (0 to MAX_PHASE)
            
        Returns:
            Centipawn value for this piece's position
        """
        # Get MG and EG values
        mg_table = MG_PST_VALUES.get(piece_name, {})
        eg_table = EG_PST_VALUES.get(piece_name, {})
        
        # For black pieces, flip the board coordinates
        if color == 'black':
            q_lookup, r_lookup = -q, -r
        else:
            q_lookup, r_lookup = q, r
        
        # Get values from tables (default to 0 if position not in table)
        mg_value = mg_table.get((q_lookup, r_lookup), 0)
        eg_value = eg_table.get((q_lookup, r_lookup), 0)
        
        # Tapered evaluation: blend MG and EG based on phase
        # Phase goes from MAX_PHASE (opening) to 0 (endgame)
        tapered_value = (mg_value * phase + eg_value * (MAX_PHASE - phase)) // MAX_PHASE
        
        return tapered_value


class Evaluator:
    """Evaluation calculation based on material balance and positional advantage.
    
    evaluate(board) -> (score, total_material, phase)
    - score: signed centipawn score (positive means white advantage)
    - total_material: sum of absolute piece values present on the board
    - phase: current game phase (0 to MAX_PHASE)
    """
    
    @staticmethod
    def calculate_phase(board) -> int:
        """
        Calculate the current game phase based on remaining material.
        
        Returns:
            Phase value (0 = endgame, MAX_PHASE = opening)
        """
        phase = 0
        
        for tile in board.tiles.values():
            if tile and tile.has_piece():
                color, name = tile.get_piece()
                phase += PHASE_VALUES.get(name, 0)
        
        # Clamp phase to MAX_PHASE
        return min(phase, MAX_PHASE)
    
    @staticmethod
    def evaluate(board):
        """
        Evaluate the board position.
        
        Returns:
            Tuple of (score, total_material, phase)
            - score: positive favors white, negative favors black
            - total_material: sum of all piece values on board
            - phase: current game phase
        """
        score = 0
        total_material = 0
        
        # Calculate game phase first
        phase = Evaluator.calculate_phase(board)
        
        # Iterate over all tiles
        for tile in board.tiles.values():
            if tile and tile.has_piece():
                color, name = tile.get_piece()
                q, r = tile.q, tile.r
                
                # Material value
                material_value = PIECE_VALUES.get(name, 0)
                total_material += abs(material_value)
                
                # Positional value from PST
                pst_value = PST.get_pst_value(name, q, r, color, phase)
                
                # Total piece value (material + position)
                piece_value = material_value + pst_value
                
                # Add to score (positive for white, negative for black)
                if color == 'white':
                    score += piece_value
                else:
                    score -= piece_value
        
        return score, total_material, phase