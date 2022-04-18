import pygame
from app.colors import COLORS
from app.algorithms import Algorithms
from typing import Iterable, Tuple

# --- Global constants ---
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# --- Classes ---

class Spot:
    """
    A class object representing the Spot.

    :ivar int row: Row position of the Spot in the Grid.
    :ivar int col: Column position of the Spot in the Grid.
    :ivar int width: The width number of the pixel (from the window).
    :ivar int total_rows: The total number of rows in the Grid.
    """

    def __init__(self, row_pos: int, col_pos: int, width: int, total_rows: int):
        super().__init__()
        self.row = row_pos
        self.col = col_pos
        self.x = row_pos * width
        self.y = col_pos * width
        self.color = COLORS.WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLORS.RED

    def is_open(self):
        return self.color == COLORS.GREEN

    def is_barrier(self):
        return self.color == COLORS.BLACK

    def is_start(self):
        return self.color == COLORS.ORANGE

    def is_end(self):
        return self.color == COLORS.TURQUOISE

    def reset(self):
        self.color = COLORS.WHITE

    def make_start(self):
        self.color = COLORS.ORANGE

    def make_closed(self):
        self.color = COLORS.RED

    def make_open(self):
        self.color = COLORS.GREEN

    def make_barrier(self):
        self.color = COLORS.BLACK

    def make_end(self):
        self.color = COLORS.TURQUOISE

    def make_path(self):
        self.color = COLORS.PURPLE

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid: Iterable[Iterable[int]]):
        """ Updates Spot neighbors (up, down, right, left). """
    
        self.neighbors = []

        # LOWER NEIGHBOR SPOT
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # UPPER NEIGHBOR SPOT
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT NEIGHBOR SPOT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # LEFT NEIGHBOR SPOT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
    # TODO : wtf is this older me ? new me fix it pls  
    """
    def update_neighbors(self, grid):
        self.neighbors = []

        # DOWN
        lower_spot = grid.get_spot(self.row + 1, self.col)
        if self.row < self.total_rows - 1 and not lower_spot.is_barrier():
            self.neighbors.append(lower_spot)
        
        # UP
        upper_spot = grid.get_spot(self.row - 1, self.col)
        if self.row > 0 and not upper_spot.is_barrier():
            self.neighbors.append(upper_spot)

        # RIGHT
        right_spot = grid.get_spot(self.row, self.col + 1)
        if self.col < self.total_rows - 1 and not right_spot.is_barrier():
            self.neighbors.append(right_spot)
        
        # LEFT
        left_spot = grid.get_spot(self.row, self.col - 1)
        if self.col > 0 and not left_spot.is_barrier():
            self.neighbors.append(left_spot)
    """
    def __lt__(self, other):
        return False

class Grid:
    """
    A class object representing the Grid.

    :ivar pygame.Surface window: The pygame.Surface instance used as the window.
    :ivar int rows: The rows number of the Grid.
    :ivar int width: The width number of the pixel (from the window).
    """

    def __init__(self, window: pygame.Surface, rows: int, width: int):
        self.window = window
        self.rows = rows
        self.width = width
        self.Grid = self.make_grid(self.rows, self.width)

    def make_grid(self, rows: int, width: int) -> Iterable[Iterable[int]]:
        """
            Returns a grid list according to rows and width.

            :param rows: Number of rows.
            :type  rows: int
            :param width: Width number of pixel.
            :type  width: int
        """
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(row_pos=i, col_pos=j, width=gap, total_rows=rows)
                grid[i].append(spot)

        return grid

    def get_spot(self, row: int, col: int) -> Spot:
        """
            Returns grid's row and column position from pixel position.

            :param row: Row spot position in the grid.
            :type  row: int
            :param col: Col spot position in the grid.
            :type  col: int
        """
        return self.Grid[row][col]

    def get_all_spot(self) -> Iterable[Spot]:
        """ Returns all grid's spot. """
        all_spot = []
        for row in self.Grid:
            for spot in row:
                all_spot.append(spot)
        return all_spot

    def pos_to_grid(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
            Returns grid's row and column position from pixel position.

            :param pos: Position of the pixel.
            :type  pos: Tuple[int, int]
        """
        gap = self.width // self.rows # column // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    def get_spot_from_pos(self, pos: Tuple[int, int]) -> Spot:
        """
            Returns grid's row and column numbers from pixel position.

            :param pos: Position of the pixel.
            :type  pos: Tuple[int, int]
        """
        # getting (row, col) coordinates from pos.
        row, col = self.pos_to_grid(pos)
        # returning spot from the grid row & col pos.
        return self.get_spot(row, col)

    def draw_grid(self):
        """ Draws the grid. """
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.window, COLORS.GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(self.window, COLORS.GREY, (j * gap, 0), (j * gap, self.width))

    def update(self):
        """ Updates the grid. """
        # draw all spots
        for row in self.Grid:
            for spot in row:
                spot.draw(self.window)
        # draw whole grid
        self.draw_grid()

class Interface:
    """
    A class object representing the Spot.

    :ivar pygame.Surface window: The pygame.Surface instance used as the window.
    :ivar int height: The window height.
    :ivar int width: The window width.
    """

    def __init__(self, window: pygame.Surface, height: int, width: int):
        self.WINDOW = window

        self.GRID_HEIGHT = height
        self.GRID_WIDTH = width

        self.GRID_ROWS = 20

        self.grid = Grid(window=self.WINDOW, rows=self.GRID_ROWS, width=self.GRID_WIDTH)
        self.start = None
        self.end   = None

    def process_events(self):
        """ 
            Process all pygame events. 
            Returns "False" if we need to close the window.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # LEFT MOUSE BUTTON (LMB)  -> set spot
            if pygame.mouse.get_pressed()[0]:
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                spot: Spot = self.grid.get_spot_from_pos(pos=pos)

                # checking if "start" already exists AND if spot from (row, col) is not the "end".
                if not self.start and spot != self.end:
                    self.start = spot
                    self.start.make_start()

                # checking if "end" already exists AND if spot from (row, col) is not the "start".
                elif not self.end and spot != self.start:
                    self.end = spot
                    self.end.make_end()

                # checking whether spot is not "end" nor "start".
                elif spot != self.end and spot != self.start:
                    spot.make_barrier()

            # RIGHT MOUSE BUTTON (RMB) -> reset spot
            elif pygame.mouse.get_pressed()[2]:
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                spot: Spot = self.grid.get_spot_from_pos(pos=pos)

                spot.reset()
                if spot == self.start:
                    self.start = None
                elif spot == self.end:
                    self.end = None

            if event.type == pygame.KEYDOWN:
                # SPACE KEY DOWN  -> apply A* path finding algorithm
                if event.key == pygame.K_SPACE and self.start and self.end:
                    for spot in self.grid.get_all_spot():
                        spot.update_neighbors(self.grid.Grid) # TODO change this fcking pls dad

                    Algorithms.A_star(screen=self.WINDOW, grid_obj=self.grid, start=self.start, end=self.end)

                # C KEY DOWN  -> reset the grid
                if event.key == pygame.K_c:
                    self.start = None
                    self.end = None
                    self.grid = Grid(window=self.WINDOW, rows=self.GRID_ROWS, width=self.GRID_WIDTH)

        return True

    def display_frame(self, screen):
        """ Displays everything to the screen. """
        screen.fill(COLORS.WHITE)
        self.grid.update()
        pygame.display.update()

def main():
    # Initialize Pygame.
    pygame.init()

    # Set up the window.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Testing algorithm for class project.")

    # Create our objects and set the datas.
    run = True
    fps = 60
    clock = pygame.time.Clock()

    # Create an instance of the Window class
    interface = Interface(window=screen, height=SCREEN_HEIGHT, width=SCREEN_WIDTH)

    # Main game loop
    while run:

        # Process events (keystrokes, mouse clicks, etc)
        run = interface.process_events()

        # Draw the current frame
        interface.display_frame(screen)

        # Pause for the next frame
        clock.tick(fps)

    # Close window and exit
    pygame.quit()

if __name__ == "__main__":
    main()
