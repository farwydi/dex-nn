"""
Manager utils
"""
import box
import config
import controller
import player


class Manager:
    """
    Manager utils
    """

    def __init__(self, gm):
        self.iterator = 0
        self.gmu = gm
        self.objects = []
        self.text_offset = 25

    def create_player(self, size, name='Player'):
        """
        Create new Player
        """
        obj = player.Player(self.gmu, self, name + str(self.iterator),
                            size, self.text_offset)
        self.objects.append(obj)
        self.iterator += 1
        self.text_offset += 30
        return obj

    def create_food(self, size, name='Food'):
        """
        Create new Food
        """
        obj = box.Food(self.gmu, self, name + str(self.iterator), size)
        self.objects.append(obj)
        self.iterator += 1
        return obj

    def create_poison(self, size, name='Poison'):
        """
        Create new Poison
        """
        obj = box.Poison(self.gmu, self, name + str(self.iterator), size)
        self.objects.append(obj)
        self.iterator += 1
        return obj

    def draw_all(self):
        """
        Draw All Object
        """
        for obj in self.objects:
            obj.draw()

    def are_live(self):
        """
        return True if all players is not death
        """
        for plr in self.objects:
            if isinstance(plr, player.Player):
                if plr.death:
                    return False
        return True

    def re_init_death_player(self):
        """
        Create new Player
        """
        for plr in self.objects:
            if isinstance(plr, player.Player):
                if plr.death:
                    plr.re_init()

    def if_all_player_death(self):
        """
        if_all_player_death
        """
        for plr in self.objects:
            if isinstance(plr, player.Player):
                if not plr.death:
                    return False

        return True

    def re_init_world(self):
        """
        re_init_world
        """
        for obj in self.objects:
            obj.re_init()
            if isinstance(obj, box.Food):
                if obj.type == 0:
                    self.objects.remove(obj)
                    self.create_poison(config.BOX_SIZE)

    @classmethod
    def __in_vision(cls, position1, position2):
        """
        __in_vision
        """
        dis = pow(position1[0] - position2[0], 2) + \
            pow(position1[1] - position2[1], 2)
        return dis <= pow(config.PLAYER_VISION * 1.3, 2)

    def get_vision(self, obj):
        """
        get_vision
        """
        wall = 0
        posion = None
        food = None
        for v_box in self.objects:
            b_position = list(v_box.position)
            b_position[0] += int(v_box.size / 2)
            b_position[1] += int(v_box.size / 2)
            if isinstance(v_box, box.Poison):
                if self.__in_vision(b_position, obj.position):
                    posion = v_box
            if isinstance(v_box, box.Food):
                if self.__in_vision(b_position, obj.position):
                    food = v_box

        to_move = controller.Object.get_move(
            obj.position, obj.rotation, config.PLAYER_VISION)

        if to_move[0] > config.WORLD_SIZE[0] or to_move[1] > config.WORLD_SIZE[1]:
            wall = 1

        if to_move[0] < 0 or to_move[1] < 0:
            wall = 1

        return (wall, posion, food)

    def poison_2_food(self, poison):
        """
        poison_2_food
        """
        position = poison.position
        self.objects.remove(poison)
        food = self.create_food(config.BOX_SIZE)
        food.type = 0
        food.position = position

    def life_cycle(self):
        """
        life_cycle
        """
        for plr in self.objects:
            plr.life()

    def action(self):
        """
        action
        """
        for plr in self.objects:
            if isinstance(plr, player.Player):
                if not plr.death:
                    plr.think()
                    
    def score_all(self):
        for plr in self.objects:
            if isinstance(plr, player.Player):
                if not plr.death:
                    plr.score += 1

    def all_payer_damage(self):
        for plr in self.objects:
            if isinstance(plr, player.Player):
                if not plr.death:
                    plr.health -= 25
                    plr.life()