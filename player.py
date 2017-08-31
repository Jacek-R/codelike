from fight import test_for_hit, deal_damage
from game_map import *
from inventory import *
from items import create_item


class Player:
    ZDZISLAW = 'Zdzisław'
    HENRYK = 'Henryk'

    def __init__(self, x, y, type_hero):
        self.type_hero = type_hero
        self.x = x
        self.y = y
        self.inventory = []

        if type_hero == Player.ZDZISLAW:
            self.health = 50
            self.damage = 5
            self.defense = 3
            self.to_hit = 4
        elif type_hero == Player.HENRYK:
            self.health = 55
            self.damage = 4
            self.defense = 2
            self.to_hit = 5

    def attack(self, monsters, monster, messages, game_map):
        if test_for_hit(self.to_hit, monster.to_hit):
            dealt_damage = deal_damage(self.damage, monster.defense)
            messages.append(
                'You attacked {} with {}. You dealt {} damage. The blood is everywhere.'.format(monster.monster_type, 'Chair', dealt_damage))
            monster.health -= dealt_damage
            if monster.health <= 0:
                messages.append('The {} died in agony.'.format(monster.monster_type))
                game_map[monster.x][monster.y].tile = Cell.EMPTY
                loot = create_item(monster.drop_rarity)
                monsters.remove(monster)
        else:
            messages.append('You missed {}.'.format(monster.monster_type))


def search_for_monster(monsters, new_x, new_y):
    for monster in monsters:
        if monster.x == new_x and monster.y == new_y:
            return monster


def check_input(player_input, game_map, player, messages):
    new_x = player.x
    new_y = player.y
    valid_input = False
    if player_input == 'W':
        new_y -= 1
        valid_input = True
    elif player_input == 'S':
        new_y += 1
        valid_input = True
    elif player_input == 'A':
        new_x -= 1
        valid_input = True
    elif player_input == 'D':
        new_x += 1
        valid_input = True
    elif player_input == 'P':
        return True
    elif player_input == 'I':
        print_inventory(player.inventory, messages)

    if valid_input:
        tile = game_map[new_x][new_y].tile
        if tile == Cell.EMPTY or tile == Cell.RAGING_NERD or tile == Cell.SYSOP:
            return True
    return False


def determine_action_type(player, new_x, new_y, game_map, monsters, messages):
    if game_map[new_x][new_y].tile == Cell.EMPTY:
        game_map[player.x][player.y].tile = Cell.EMPTY
        player.x = new_x
        player.y = new_y
        game_map[player.x][player.y].tile = Cell.PLAYER
        return True
    if game_map[new_x][new_y].tile == Cell.RAGING_NERD or game_map[new_x][new_y].tile == Cell.SYSOP:
        monster = search_for_monster(monsters, new_x, new_y)
        player.attack(monsters, monster, messages, game_map)
        return True


def action_of_player(player_input, game_map, player, monsters, messages):
    player_finished_turn = False
    if player_input == 'W':
        player_finished_turn = determine_action_type(player, player.x, player.y - 1, game_map, monsters, messages)
    elif player_input == 'S':
        player_finished_turn = determine_action_type(player, player.x, player.y + 1, game_map, monsters, messages)
    elif player_input == 'A':
        player_finished_turn = determine_action_type(player, player.x - 1, player.y, game_map, monsters, messages)
    elif player_input == 'D':
        player_finished_turn = determine_action_type(player, player.x + 1, player.y, game_map, monsters, messages)
    elif player_input == 'P':
        player_finished_turn = True

    game_map[player.x][player.y].tile = Cell.PLAYER
    return player_finished_turn
