import cis_config as conf
import random


class Environment:

    def __init__(self, movement_seed, food_seed):
        random.seed(movement_seed)
        self.mov_state = random.getstate()
        random.seed(food_seed)
        self.food_state = random.getstate()

    def enforce_movement(self, cell):
        random.setstate(self.mov_state)
        old_pos = cell.get_pos()
        new_pos = list([])
        new_pos.append(old_pos[0] + random.uniform(-conf.WORLD_VELOCITY,
                                                   conf.WORLD_VELOCITY))
        new_pos.append(old_pos[1] + random.uniform(-conf.WORLD_VELOCITY,
                                                   conf.WORLD_VELOCITY))
        new_pos.append(old_pos[2] + random.uniform(-conf.WORLD_VELOCITY,
                                                   conf.WORLD_VELOCITY))
        cell.set_pos(new_pos[0], new_pos[1], new_pos[2])
        self.mov_state = random.getstate()

    def reveal_food(self, pos):
        random.setstate(self.food_state)
        f = random.uniform(0, 1)
        self.food_state = random.getstate()
        if f < conf.FOOD_THRESHOLD:
            return conf.FOOD_ENERGY
        else:
            return 0
