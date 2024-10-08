import time
import random
from Cell import Cell

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ) -> None:
        if seed:
            random.seed(seed)
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        self._cells = []
        for col in range(self.num_cols):
            new_col = []
            for row in range(self.num_rows):
                cell = Cell(window=self.win)
                new_col.append(cell)
            self._cells.append(new_col)

        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, I: int, J: int) -> None:
        start_x = self.x1 + I * self.cell_size_x
        end_x = start_x + self.cell_size_x
        start_y = self.y1 + J * self.cell_size_y
        end_y = start_y + self.cell_size_y
        cell = self._cells[I][J]
        cell._x1 = start_x
        cell._x2 = end_x
        cell._y1 = start_y
        cell._y2 = end_y
        cell.draw()
        if self.win:
            self._animate()

    def _animate(self) -> None:
        if self.win:
            self.win.redraw()
            time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, I: int, J: int) -> None:
        current_cell = self._cells[I][J]
        current_cell.visited = True
        while True:
            possible_moves = []
            if I > 0 and not self._cells[I - 1][J].visited:
                possible_moves.append((I - 1, J))
            if J > 0 and not self._cells[I][J - 1].visited:
                possible_moves.append((I, J - 1))
            if I + 1 < self.num_cols and not self._cells[I + 1][J].visited:
                possible_moves.append((I + 1, J))
            if J + 1 < self.num_rows and not self._cells[I][J + 1].visited:
                possible_moves.append((I, J + 1))

            if len(possible_moves) == 0:
                self._draw_cell(I, J)
                return
            
            random_direction = random.choice(possible_moves)
            random_cell = self._cells[random_direction[0]][random_direction[1]]
            if random_direction[0] > I:
                current_cell.has_right_wall = False
                random_cell.has_left_wall = False
            elif random_direction[0] < I:
                current_cell.has_left_wall = False
                random_cell.has_right_wall = False
            elif random_direction[1] > J:
                current_cell.has_bottom_wall = False
                random_cell.has_top_wall = False
            elif random_direction[1] < J:
                current_cell.has_top_wall = False
                random_cell.has_bottom_wall = False
            
            self._break_walls_r(random_direction[0], random_direction[1])
                

    def _reset_cells_visited(self) -> None:
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                cell = self._cells[col][row]
                cell.visited = False

    def solve(self) -> bool:
        return self._solve_r(0, 0)

    def _solve_r(self, I: int, J: int) -> bool:
        self._animate()
        current_cell = self._cells[I][J]
        current_cell.visited = True
        if I + 1 == self.num_cols and J + 1 == self.num_rows:
            return True
        if current_cell.has_top_wall is False and I != 0 and J != 0 and self._cells[I][J - 1].visited is False:
            current_cell.draw_move(self._cells[I][J - 1])
            if self._solve_r(I, J - 1):
                return True
            current_cell.draw_move(self._cells[I][J - 1], True)
        if current_cell.has_right_wall is False and self._cells[I + 1][J].visited is False:
            current_cell.draw_move(self._cells[I + 1][J])
            if self._solve_r(I + 1, J):
                return True
            current_cell.draw_move(self._cells[I + 1][J], True)
        if current_cell.has_bottom_wall is False and self._cells[I][J + 1].visited is False:
            current_cell.draw_move(self._cells[I][J + 1])
            if self._solve_r(I, J + 1):
                return True
            current_cell.draw_move(self._cells[I][J + 1], True)
        if current_cell.has_left_wall is False and self._cells[I - 1][J]:
            current_cell.draw_move(self._cells[I - 1][J])
            if self._solve_r(I - 1, J):
                return True
            current_cell.draw_move(self._cells[I - 1][J], True)
        return False
