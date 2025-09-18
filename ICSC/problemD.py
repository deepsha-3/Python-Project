import sys
import random
from typing import List

# All 8 possible directions a word can go:
# right, left, down, up, and the 4 diagonals

DIRECTIONS = [
    (0, 1),   # →
    (0, -1),  # ←
    (1, 0),   # ↓
    (-1, 0),  # ↑
    (1, 1),   # ↘
    (1, -1),  # ↙
    (-1, 1),  # ↗
    (-1, -1)  # ↖
]

def inside_grid(row: int, col: int) -> bool:
    """Check if a position is inside the 10x10 grid."""
    return 0 <= row < 10 and 0 <= col < 10

def word_fits(grid: List[List[str]], word: str, row: int, col: int, drow: int, dcol: int) -> bool:
    """
    Check if a word can be placed starting from (row, col) in the given direction.
    It must stay inside the grid and not conflict with other letters.
    """
    for i, letter in enumerate(word):
        r, c = row + i * drow, col + i * dcol
        if not inside_grid(r, c):
            return False
        if grid[r][c] != '.' and grid[r][c] != letter:
            return False
    return True

def place_word(grid: List[List[str]], word: str, row: int, col: int, drow: int, dcol: int):

    """Place the word into the grid at (row, col) going in (drow, dcol) direction."""
    for i, letter in enumerate(word):
        r, c = row + i * drow, col + i * dcol
        grid[r][c] = letter

def create_crossword(words: list) -> list:
    """
    Generate a 10x10 word search puzzle containing the given words.
    
    Args:
        words: A list of words to include in the puzzle.
        
    Returns:
        A 2D array (list of lists) representing the word search puzzle.
    """
    # Step 1: Start with a 10x10 empty grid
    grid = [['.' for _ in range(10)] for _ in range(10)]
    
    # Step 2: Convert words to uppercase (standard in word searches)
    words = [w.upper() for w in words if 1 <= len(w) <= 10]

    # Step 3: Place each word
    for word in words:
        placed = False

        # Try random positions up to 1000 times
        for _ in range(1000):
            row, col = random.randint(0, 9), random.randint(0, 9)
            drow, dcol = random.choice(DIRECTIONS)
            
            if word_fits(grid, word, row, col, drow, dcol):
                place_word(grid, word, row, col, drow, dcol)
                placed = True
                break

        # If random placement fails, scan systematically
        if not placed:
            for row in range(10):
                for col in range(10):
                    for drow, dcol in DIRECTIONS:
                        if word_fits(grid, word, row, col, drow, dcol):
                            place_word(grid, word, row, col, drow, dcol)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break

        if not placed:
            raise ValueError(f"Could not place the word: {word}")

    # Step 4: Fill remaining cells with random letters
    for row in range(10):
        for col in range(10):
            if grid[row][col] == '.':
                grid[row][col] = chr(ord('A') + random.randint(0, 25))

    return grid


# --- Main execution block. DO NOT MODIFY.  ---
if __name__ == "__main__":
    try:
        # Read words from first line (comma-separated)
        words_input = input().strip()
        words = [word.strip() for word in words_input.split(',')]
        
        # Generate the word search puzzle
        puzzle = create_crossword(words)
        
        # Print the result as a 2D grid
        for row in puzzle:
            print(''.join(row))
            
    except ValueError as e:
        print(f"Input Error: {e}", file=sys.stderr)
        sys.exit(1)
    except EOFError:
        print("Error: Not enough input lines provided.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
