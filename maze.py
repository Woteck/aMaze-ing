from typing import Iterable, Tuple
import pygame
from queue import PriorityQueue
import interactions
# --- Global constants ---
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

class COLOR:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 255, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)

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
        self.color = COLOR.WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLOR.RED

    def is_open(self):
        return self.color == COLOR.GREEN

    def is_barrier(self):
        return self.color == COLOR.BLACK

    def is_start(self):
        return self.color == COLOR.ORANGE

    def is_end(self):
        return self.color == COLOR.TURQUOISE

    def reset(self):
        self.color = COLOR.WHITE

    def make_start(self):
        self.color = COLOR.ORANGE

    def make_closed(self):
        self.color = COLOR.RED

    def make_open(self):
        self.color = COLOR.GREEN

    def make_barrier(self):
        self.color = COLOR.BLACK

    def make_end(self):
        self.color = COLOR.TURQUOISE

    def make_path(self):
        self.color = COLOR.PURPLE

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
            pygame.draw.line(self.window, COLOR.GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(self.window, COLOR.GREY, (j * gap, 0), (j * gap, self.width))

    def update(self):
        """ Updates the grid. """
        # draw all spots
        for row in self.Grid:
            for spot in row:
                spot.draw(self.window)
        # draw whole grid
        self.draw_grid()

class Algorithms:
    """ This class represents a bunch of algorithms. """

    @staticmethod
    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def reconstruct_path(came_from, current):
        while current in came_from:
            current = came_from[current]
            current.make_path()

    @staticmethod
    def A_star(screen, grid_obj, start, end):
        grid = grid_obj.Grid
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = Algorithms.h(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                Algorithms.reconstruct_path(came_from, end)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + Algorithms.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            if current != start:
                current.make_closed()
            
            screen.fill(COLOR.WHITE)
            grid_obj.update()
            pygame.display.update()

        return False

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
        screen.fill(COLOR.WHITE)
        self.grid.update()
        pygame.display.update()

def main():
    # Initialize Pygame and set up the window
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Testing algorithm for class project.")

    # Create our objects and set the data
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

# Call the main function, start up the window
if __name__ == "__main__":
    main()
