import random
import time
import grpc
import multiprocessing as mp
from multiprocessing.managers import BaseManager

import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto
import cis_config as conf
from cell import Cell
from cis_worker import CIS_Worker
from environment import Environment

cell_id_counter = 0


class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
    """

    def ComputeCellInteractions(self, incoming_batch, context):
        global cell_id_counter
        environment = Environment(1233411049932, 129495899654)
        # BaseManager.register('Cell', Cell)
        # cis_manager = BaseManager()
        # cis_manager.start()
        manager = mp.Manager()
        new_cells = manager.list([])
        new_cell_lock = mp.Lock()

        movement_queue = mp.Queue()
        interaction_queue = mp.Queue()
        energy_queue = mp.Queue()
        division_queue = mp.Queue()

        for cell_proto in incoming_batch.cells_to_compute:
            cell_obj = Cell(cell_proto)
            movement_queue.put(cell_obj)
            # interaction_queue.put(cell_obj)
            # energy_queue.put(cell_obj)
            # division_queue.put(cell_obj)

        workers = []
        for i in range(self.thread_number):
            workers.append(CIS_Worker(
                environment,
                movement_queue,
                interaction_queue,
                energy_queue,
                division_queue,
                new_cells,
                new_cell_lock,
                self.cell_id_counter
            ))
            workers[i].start()

        for wrk in workers:
            wrk.join()

        new_batch = proto.CellComputeBatch(
            time_step=incoming_batch.time_step,
            cells_to_compute=new_cells,
            cells_in_proximity=incoming_batch.cells_in_proximity)

        return new_batch

    def BigBang(self, request, context):
        for i in range(conf.INITIAL_NUMBER_CELLS):
            initial_position = []
            for j in conf.WORLD_DIMENSION:
                initial_position.append(random.uniform(0, j))
            initial_position = proto.Vector(
                x=initial_position[0],
                y=initial_position[1],
                z=initial_position[2])
            cell = proto.Cell(
                id=i,
                energy_level=conf.INITIAL_ENERGY_LEVEL,
                pos=initial_position,
                vel=proto.Vector(
                    x=0,
                    y=0,
                    z=0),
                dna=bytes(),
                connections=[])
            yield cell
