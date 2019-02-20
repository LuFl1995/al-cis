from multiprocessing import Process, Queue, Value
import time
from copy import deepcopy
import queue


class CIS_Worker(Process):

    def __init__(self, environment, mov_queue, act_queue, eng_queue,
                 div_queue, new_cells, new_cell_lock, cell_id_counter):
        Process.__init__(self)
        self.env = environment
        self.mov_queue = mov_queue
        self.act_queue = act_queue
        self.eng_queue = eng_queue
        self.div_queue = div_queue
        self.new_cells = new_cells
        self.new_cell_lock = new_cell_lock
        self.cell_id_counter = cell_id_counter

    def run(self):
        stuff_todo = True
        while stuff_todo:
            if not self.mov_queue.empty():
                # Query cell for movement
                cell = self.mov_queue.get()
                self.env.enforce_movement(cell)
                cell.move()
                self.act_queue.put(cell)
            elif not self.act_queue.empty():
                # Query cell for interaction
                # cell = self.act_queue.get()
                # for p_cell in get_approx(cell):
                    # cell.interact(p_cell)
                cell = self.act_queue.get()
                self.eng_queue.put(cell)
                pass
            elif not self.eng_queue.empty():
                # Query cell for Energy
                cell = self.eng_queue.get()
                food = self.env.reveal_food(cell.get_pos())
                cell.eat(food)
                self.div_queue.put(cell)
            elif not self.div_queue.empty():
                # Query cell for  Division
                cell = self.div_queue.get()
                new_cell = cell.divide(self.cell_id_counter)
                if new_cell is not None:
                    with self.new_cell_lock:
                        self.new_cells.append(new_cell.cell_proto)
                if cell.is_alive():
                    with self.new_cell_lock:
                        self.new_cells.append(cell.cell_proto)
            else:
                stuff_todo = False
