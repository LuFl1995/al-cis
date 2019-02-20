import cis_config as conf
import protocol_pb2 as proto


class Cell():

    def __init__(self, proto_cell):
        self.cell_proto = proto_cell

    def is_alive(self):
        return self.cell_proto.energy_level > conf.ENERGY_THRESHOLD

    def get_pos(self):
        return (self.cell_proto.pos.x,
                self.cell_proto.pos.y,
                self.cell_proto.pos.z)

    def set_pos(self, x, y, z):
        self.cell_proto.pos.x = x
        self.cell_proto.pos.y = y
        self.cell_proto.pos.z = z

    def move(self):
        pass

    def eat(self, found_energy):
        new_energy = self.cell_proto.energy_level + found_energy
        new_energy -= conf.GENERAL_ENERGY_CONSUMPTION
        self.cell_proto.energy_level = new_energy

    def interact(self, other_cell):
        pass

    def divide(self, latest_cell_id):
        if self.cell_proto.energy_level > conf.DIVISION_THRESHOLD:
            self.cell_proto.energy_level -= conf.DIVISION_ENERGY_COST

            with latest_cell_id.get_lock():
                new_id = latest_cell_id.value = latest_cell_id.value + 1

            new_cell = proto.Cell(
                id=new_id,
                energy_level=conf.INITIAL_ENERGY_LEVEL,
                pos=self.cell_proto.pos,
                vel=proto.Vector(
                    x=0,
                    y=0,
                    z=0),
                dna=bytes(),
                connections=[])
            new_cell = Cell(new_cell)
            return new_cell
        else:
            return None
