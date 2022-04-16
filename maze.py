from typing import Tuple
import pygame
from queue import PriorityQueue

# --- Global constants ---
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

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


class Spot():
    """ This class represents the spot. """
    def __init__(self, row, col, width, total_rows):
        super().__init__()
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
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

class Grid():
    """ This class represents the grid. """

    def __init__(self, window, rows, width):
        self.window = window
        self.rows = rows
        self.width = width
        self.Grid = self.make_grid(self.rows, self.width)

    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(row=i, col=j, width=gap, total_rows=rows)
                grid[i].append(spot)

        return grid

    def draw_grid(self, window, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

    def get_spot(self, row, col):
        return self.Grid[row][col]

    def get_all_spot(self):
        all_spot = []
        for row in self.Grid:
            for spot in row:
                all_spot.append(spot)
        return all_spot

    def update(self):
        """ Update the grid. """
        # draw all spots
        for row in self.Grid:
            for spot in row:
                spot.draw(self.window)
        # draw whole grid
        self.draw_grid(self.window, self.rows, self.width)

class Algorithms():
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
    def A_star(grid, start, end):
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

        return False

class Interface():
    """
        This class represents an instance of the interface. 
        If we need to reset the interface ame we'd just need to create a new instance of this class.
    """

    def __init__(self, window, screen_size):
        self.WINDOW = window

        self.GRID_WIDTH = screen_size[0]
        self.GRID_HEIGHT = screen_size[1]

        self.GRID_ROWS = 20

        self.grid = Grid(window=self.WINDOW, rows=self.GRID_ROWS, width=self.GRID_WIDTH)
        self.start = None
        self.end   = None

    def pos_to_grid(self, pos, rows, column):
        """
            Return grid's row and column numbers from pixel position.

            :param pos: Position of the pixel.
            :type pos: Tuple[int, int]
            :param rows: Grid's number of row.
            :type rows: int
            :param column: Grid's number of column.
            :type column: int
        """
        gap = column // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    def get_spot_from_mouse_pos(self) -> Spot:
        # getting mouse pos.
        pos: Tuple[int, int] = pygame.mouse.get_pos()
        # getting (x, y) = (row, col) coordinates.
        row, col = self.pos_to_grid(pos, self.GRID_ROWS, self.GRID_WIDTH)
        # getting spot object from the window grid.
        spot = self.grid.get_spot(row, col)
        return spot

    def process_events(self):
        """ 
            Process all pygame events. 
            Return "False" if we need to close the window.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # LEFT MOUSE BUTTON (LMB)  -> set spot
            if pygame.mouse.get_pressed()[0]:
                spot: Spot = self.get_spot_from_mouse_pos()

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
                spot: Spot = self.get_spot_from_mouse_pos()

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

                    Algorithms.A_star(grid=self.grid.Grid, start=self.start, end=self.end)

                # C KEY DOWN  -> reset the grid
                if event.key == pygame.K_c:
                    self.start = None
                    self.end = None
                    self.grid = Grid(window=self.WINDOW, rows=self.GRID_ROWS, width=self.GRID_WIDTH)

        return True

    def display_frame(self, screen):
        """ Display everything to the screen. """
        screen.fill(WHITE)
        self.grid.update()
        pygame.display.update()

def main():
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Testing algorithm for class project.")

    # Create our objects and set the data
    run = True
    fps = 60
    clock = pygame.time.Clock()

    # Create an instance of the Window class
    interface = Interface(window=screen, screen_size=size)

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
