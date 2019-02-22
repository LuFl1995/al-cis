import numpy as np
import grpc
import protocol_pb2 as proto
import protocol_pb2_grpc as grpc_proto
import cis_config as conf
import random
import time
import uuid

import cis_env
import cis_cell


class CellComputeServicer(grpc_proto.CellInteractionServiceServicer):
    """
    """

    def ComputeCellInteractions(self, incoming_batch, context):
        # Movement
        for c in incoming_batch.cells_to_compute:
            cis_env.enforce_movement(c)

        # Interaction

        # Energy
        for c in incoming_batch.cells_to_compute:
            cis_env.feed_cell(c)

        # Survival
        living_cells = []
        for c in incoming_batch.cells_to_compute:
            if cis_cell.is_alive(c):
                living_cells.append(c)

        # Division
        for c in living_cells:
            new_cell = cis_cell.divide(c)
            if new_cell is not None:
                living_cells.append(new_cell)

        new_batch = proto.CellComputeBatch(
            time_step=incoming_batch.time_step,
            cells_to_compute=living_cells,
            cells_in_proximity=incoming_batch.cells_in_proximity,
        )
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
                id=str(uuid.uuid1()),
                energy_level=conf.INITIAL_ENERGY_LEVEL,
                pos=initial_position,
                vel=proto.Vector(
                    x=0,
                    y=0,
                    z=0),
                dna=bytes(),
                connections=[])
            yield cell
