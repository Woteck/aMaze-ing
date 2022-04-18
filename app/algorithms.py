# algorithms.py

import pygame
from queue import PriorityQueue
from app.colors import COLORS

class Algorithms:
    """ This class has a bunch of algorithms. """

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
            
            screen.fill(COLORS.WHITE)
            grid_obj.update()
            pygame.display.update()

        return False