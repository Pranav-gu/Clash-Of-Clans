import points as pt
import collections
from graph import moveWithoutBreakingWalls
import time

barbarians = []
dragons = []
balloons = []
archers = []
stealth_archers = []            # added
healers = []            # added
king = []

troops_spawned = {
    'barbarian': 0,
    'archer': 0,
    'dragon': 0,
    'balloon': 0,
    'stealth_archers': 0,        # added
    'healers': 0        # added
}


def clearTroops():
    barbarians.clear()
    dragons.clear()
    balloons.clear()
    archers.clear()
    stealth_archers.clear()
    healers.clear()
    king.clear()
    troops_spawned['barbarian'] = 0
    troops_spawned['dragon'] = 0
    troops_spawned['balloon'] = 0
    troops_spawned['archer'] = 0
    troops_spawned['stealth_archers'] = 0           # added
    troops_spawned['healers'] = 0           # added


def king_transfer(King):
    king.append(King)
    print(king)

class Barbarian:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.position = position
        self.alive = True
        self.target = None

    def move(self, pos, V, type):
        if (self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if (r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if (info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if (coords == None):
                    flag = 1
                    break
                info = vmap[pos[0]][pos[1]]
                x = 0
                y = 0
                if (info != pt.TOWNHALL):
                    x = int(info.split(':')[1])
                    y = int(info.split(':')[2])
                else:
                    x = pos[0]
                    y = pos[1]
                if (x == coords[0] and y == coords[1]):
                    flag = 1
                    break
                self.position = coords
            if (flag == 0):
                return
        if (r == 0):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if (abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if (abs(pos[1] - self.position[1]) == 1):
                        break
        elif (r > 1):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if (self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if (self.position[0] == pos[0]):
                        return
        elif (c > 1):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if (self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if (self.position[1] == pos[1]):
                        return
        elif (r+c == 2):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1

    def check_for_walls(self, x, y, vmap):
        if (vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V):
        target = V.wall_objs[(x, y)]
        self.attack_target(target)

    def break_building(self, x, y, V):
        target = None
        if (V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if (self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        barbarians.remove(self)

    def deal_damage(self, hit):
        if (self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


class Archer:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.attack_radius = 3
        self.position = position
        self.alive = True
        self.target = None

    def isInAttackradius(self, pos):
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if (r**2 + c**2 <= self.attack_radius**2):
            return True
        return False

    def move(self, pos, V, type):
        if (self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if (self.isInAttackradius(pos)):
            info = vmap[pos[0]][pos[1]]
            if (info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if (coords == None):
                    flag = 1
                    break
                self.position = coords
            if (flag == 0):
                return
        if (r == 0):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if (self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if (self.isInAttackradius(pos)):
                        break
        elif (r > 1):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if (self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if (self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
        elif (c > 1):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if (self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if (self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
        elif (r+c == 2):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if (self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if (self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if (self.isInAttackradius(pos)):
                        break

    def check_for_walls(self, x, y, vmap):
        if (vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V):
        target = V.wall_objs[(x, y)]
        self.attack_target(target)

    def break_building(self, x, y, V):
        target = None
        if (V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if (self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        archers.remove(self)

    def deal_damage(self, hit):
        if (self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


# -------------------------code added up-------------------------------------------
class Stealth_Archer(Archer):
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.attack_radius = 3
        self.position = position
        self.alive = True
        self.target = None
        self.creation_time = time.time()
        self.invisibility_time = 10

    def kill(self):
        self.alive = False
        stealth_archers.remove(self)

    def deal_damage(self, hit):
        if (self.alive == False):
            return
        self.health -= hit
        if (self.invisibility_time > 0):
            self.health += hit
        if self.health <= 0:
            self.health = 0
            self.kill()

# -------------------------code added down-------------------------------------------


# -------------------------code added up-------------------------------------------

class Healer:
    def __init__(self, position):
        self.speed = 2
        self.health = 250
        self.max_health = 250
        self.heal_radius = 7
        self.heal_strength = 20
        self.position = position
        self.alive = True
        
    def move(self, pos, V, King):
        if (self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if (r + c <= 7):
            # info = vmap[pos[0]][pos[1]]
            x = pos[0]
            y = pos[1]
            self.break_building(x, y, V, King)
            return
        elif (r == 0):
            if (pos[1] > self.position[1]+7):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if (abs(pos[1] - self.position[1]) <= 7):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if (abs(pos[1] - self.position[1]) <= 7):
                        break
        elif (r > 1):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if (self.position[0] > pos[0]):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if (self.position[0] > pos[0]):
                        break
        elif (c > 1):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if (self.position[1] > pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if (self.position[1] > pos[1]):
                        return
        elif (r+c == 8):
            if (pos[0] > self.position[0]):
                self.position[0] += 7
            else:
                self.position[0] -= 7

    def break_building(self, x, y, V, King):
        list = []
        vmap = V.map
        for i in range(x-self.heal_radius, x+1+self.heal_radius):
            for j in range(y-self.heal_radius, y+1+self.heal_radius):
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if (k >= 0 and k <= 17 and l >= 0 and l <= 35):
                            for barb in barbarians:
                                if barb.position[0] == k and barb.position[1] == l:
                                    list.append(barb)
                            for arch in archers:
                                if arch.position[0] == k and arch.position[1] == l:
                                    list.append(arch)
                            for bal in balloons:
                                if bal.position[0] == k and bal.position[1] == l:
                                    list.append(bal)
                            for arch in stealth_archers:
                                if arch.position[0] == k and arch.position[1] == l:
                                    list.append(arch)
                            for drag in dragons:
                                if drag.position[0] == k and drag.position[1] == l:
                                    list.append(drag)
                            for he in healers:
                                if he.position[0] == k and he.position[1] == l and he.position[0] != x and he.position[1] != y:
                                    list.append(he)
                            if King.position[0] == k and King.position[1] == l:
                                list.append(King)
        for target in list:
            self.attack_target(target)

    def attack_target(self, target):
        if (self.alive == False):
            return
        target.health += self.heal_strength
        if (target.health > target.max_health):
            target.health = target.max_health
        

    def kill(self):
        self.alive = False
        healers.remove(self)

    def deal_damage(self, hit):
        if (self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.heal_strength = self.heal_strength*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health




# -------------------------code added down-------------------------------------------


class Dragon:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 5
        self.position = position
        self.alive = True

    def move(self, pos, V):
        if (self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if (r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if (info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif (r == 0):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if (abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if (abs(pos[1] - self.position[1]) == 1):
                        break
        elif (r > 1):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if (self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if (self.position[0] == pos[0]):
                        return
        elif (c > 1):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if (self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if (self.position[1] == pos[1]):
                        return
        elif (r+c == 2):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1

    def break_building(self, x, y, V):
        target = None
        if (V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if (self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        dragons.remove(self)

    def deal_damage(self, hit):
        if (self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


class Balloon:
    def __init__(self, position):
        self.speed = 2
        self.health = 100
        self.max_health = 100
        self.attack = 2
        self.position = position
        self.alive = True

    def move(self, pos, V):
        if (self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if (r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if (info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif (r == 0):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if (abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if (abs(pos[1] - self.position[1]) == 1):
                        break
        elif (r > 1):
            if (pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if (self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if (self.position[0] == pos[0]):
                        return
        elif (c > 1):
            if (pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if (self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if (self.position[1] == pos[1]):
                        return
        elif (r+c == 2):
            if (pos[0] > self.position[0]):
                self.position[0] += 1
            else:
                self.position[0] -= 1

    def break_building(self, x, y, V):
        target = None
        if (V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if (self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        balloons.remove(self)

    def deal_damage(self, hit):
        if (self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


def spawnBarbarian(pos):
    if (pt.troop_limit['barbarian'] <= troops_spawned['barbarian']):
        return

    # convert tuple to list
    pos = list(pos)
    barb = Barbarian(pos)
    troops_spawned['barbarian'] += 1
    barbarians.append(barb)


def spawnArcher(pos):
    if (pt.troop_limit['archer'] <= troops_spawned['archer']):
        return

    # convert tuple to list
    pos = list(pos)
    archer = Archer(pos)
    troops_spawned['archer'] += 1
    archers.append(archer)


# ------------------------code added up ----------------
def spawnStealthArcher(pos):
    if (pt.troop_limit['stealth_archers'] <= troops_spawned['stealth_archers']):
        return
    # convert tuple to list
    pos = list(pos)
    stealth_archer = Stealth_Archer(pos)
    troops_spawned['stealth_archers'] += 1
    stealth_archers.append(stealth_archer)

# ------------------------code added down ----------------


def spawnDragon(pos):
    if (pt.troop_limit['dragon'] <= troops_spawned['dragon']):
        return

    # convert tuple to list
    pos = list(pos)
    dr = Dragon(pos)
    troops_spawned['dragon'] += 1
    dragons.append(dr)


def spawnBalloon(pos):
    if (pt.troop_limit['balloon'] <= troops_spawned['balloon']):
        return

    # convert tuple to list
    pos = list(pos)
    bal = Balloon(pos)
    troops_spawned['balloon'] += 1
    balloons.append(bal)


# ------------------------code added up ----------------
def spawnHealers(pos):
    if (pt.troop_limit['healers'] <= troops_spawned['healers']):
        return

    # convert tuple to list
    pos = list(pos)
    bal = Healer(pos)
    troops_spawned['healers'] += 1
    healers.append(bal)
# ------------------------code added down ----------------


def move_barbarians(V, type):
    if (type == 1):
        for barb in barbarians:
            if (barb.alive == False):
                continue
            if barb.target != None:
                if (V.map[barb.target[0]][barb.target[1]] == pt.BLANK):
                    barb.target = None

            if (barb.target == None):
                barb.target = search_for_closest_building(
                    barb.position, V.map, 0)
            if (barb.target == None):
                continue
            barb.move(barb.target, V, type)
    elif (type == 2):
        for barb in barbarians:
            if (barb.alive == False):
                continue
            closest_building = search_for_closest_building(
                barb.position, V.map, 0)
            if (closest_building == None):
                continue
            barb.move(closest_building, V, type)


def move_archers(V, type):
    if (type == 1):
        for archer in archers:
            if (archer.alive == False):
                continue
            if archer.target != None:
                if (V.map[archer.target[0]][archer.target[1]] == pt.BLANK):
                    archer.target = None
            if (archer.target == None):
                archer.target = search_for_closest_building(
                    archer.position, V.map, 0)
            if (archer.target == None):
                continue
            archer.move(archer.target, V, type)
    elif (type == 2):
        for archer in archers:
            if (archer.alive == False):
                continue
            closest_building = search_for_closest_building(
                archer.position, V.map, 0)
            if (closest_building == None):
                continue
            archer.move(closest_building, V, type)


# --------------------------------------------code added up ------------------------------------------
def move_stealth_archers(V, type):
    if (type == 1):
        for stealth_archer in stealth_archers:
            if (stealth_archer.alive == False):
                continue
            if stealth_archer.target != None:
                if (V.map[stealth_archer.target[0]][stealth_archer.target[1]] == pt.BLANK):
                    stealth_archer.target = None
            if (stealth_archer.target == None):
                stealth_archer.target = search_for_closest_building(
                    stealth_archer.position, V.map, 0)
            if (stealth_archer.target == None):
                continue
            stealth_archer.move(stealth_archer.target, V, type)
    elif (type == 2):
        for stealth_archer in stealth_archers:
            if (stealth_archer.alive == False):
                continue
            closest_building = search_for_closest_building(
                stealth_archer.position, V.map, 0)
            if (closest_building == None):
                continue
            stealth_archer.move(closest_building, V, type)

# --------------------------------------------code added down ------------------------------------------


def move_dragons(V):
    for dr in dragons:
        if (dr.alive == False):
            continue
        closest_building = search_for_closest_building(dr.position, V.map, 0)
        if (closest_building == None):
            continue
        dr.move(closest_building, V)


# --------------------------------------------code added up ------------------------------------------
def move_healers(V, King):
    for he in healers:
        if (he.alive == False):
            continue
        closest_troop = search_for_closest_troop(he.position, V.map, King)
        if (closest_troop == None):
            continue
        he.move(closest_troop.position, V, King)
# --------------------------------------------code added down ------------------------------------------


def move_balloons(V):
    for bal in balloons:
        if (bal.alive == False):
            continue
        closest_building = search_for_closest_building(bal.position, V.map, 1)
        if (closest_building == None):
            continue
        bal.move(closest_building, V)


def search_for_closest_building(pos, vmap, prioritized):
    closest_building = None
    closest_dist = 10000
    flag = 0
    for i in range(len(vmap)):
        for j in range(len(vmap[i])):
            item = vmap[i][j].split(':')[0]
            if (prioritized == 0):
                if (item == pt.HUT or item == pt.CANNON or item == pt.TOWNHALL or item == pt.WIZARD_TOWER):
                    dist = abs(i - pos[0]) + abs(j - pos[1])
                    if (dist < closest_dist):
                        flag = 1
                        closest_dist = dist
                        closest_building = (i, j)
            else:
                if (item == pt.CANNON or item == pt.WIZARD_TOWER):
                    dist = abs(i - pos[0]) + abs(j - pos[1])
                    if (dist < closest_dist):
                        flag = 1
                        closest_dist = dist
                        closest_building = (i, j)
    if (flag == 0 and prioritized == 0):
        return None
    elif (flag == 0 and prioritized == 1):
        return search_for_closest_building(pos, vmap, 0)
    else:
        return closest_building


# --------------------------------------------code added up ------------------------------------------
def search_for_closest_troop(pos, vmap, King):
    closest_troop = None
    closest_dist = 10000
    closest_wounded_troop = None
    closest__wounded_dist = 10000
    for barb in barbarians:
        dist = abs(barb.position[0]-pos[0]) + abs(barb.position[1]-pos[1])
        if (dist < closest_dist):
            closest_dist = dist
            closest_troop = barb
        if (barb.health < barb.max_health and dist < closest__wounded_dist):
            closest__wounded_dist = dist
            closest_wounded_troop = barb

    for arch in archers:
        dist = abs(arch.position[0]-pos[0]) + abs(arch.position[1]-pos[1])
        if (dist < closest_dist):
            closest_dist = dist
            closest_troop = arch
        
        if (arch.health < arch.max_health and dist < closest__wounded_dist):
            closest__wounded_dist = dist
            closest_wounded_troop = arch


    for arch in stealth_archers:
        dist = abs(arch.position[0]-pos[0]) + abs(arch.position[1]-pos[1])
        if (dist < closest_dist):
            closest_dist = dist
            closest_troop = arch
        
        if (arch.health < arch.max_health and dist < closest__wounded_dist):
            closest__wounded_dist = dist
            closest_wounded_troop = arch


    for bal in balloons:
        dist = abs(bal.position[0]-pos[0]) + abs(bal.position[1]-pos[1])
        if (dist < closest_dist):
            closest_dist = dist
            closest_troop = bal
        
        if (bal.health < bal.max_health and dist < closest__wounded_dist):
            closest__wounded_dist = dist
            closest_wounded_troop = bal


    for drags in dragons:
        dist = abs(drags.position[0]-pos[0]) + abs(drags.position[1]-pos[1])
        if (dist < closest_dist):
            closest_dist = dist
            closest_troop = drags
        
        if (drags.health < drags.max_health and dist < closest__wounded_dist):
            closest__wounded_dist = dist
            closest_wounded_troop = drags


    for heal in healers:
        dist = abs(heal.position[0]-pos[0]) + abs(heal.position[1]-pos[1])
        if (dist < closest_dist and dist != 0):
            closest_dist = dist
            closest_troop = heal
        
        if (heal.health < heal.max_health and dist < closest__wounded_dist and dist != 0):
            closest__wounded_dist = dist
            closest_wounded_troop = heal

    
    if (King.alive and closest_dist > abs(pt.HERO_POS[0]-pos[0]) + abs(pt.HERO_POS[1]-pos[1])):
        closest_dist = abs(pt.HERO_POS[0]-pos[0]) + abs(pt.HERO_POS[1]-pos[1])
        closest_troop = King
    
    if (King.alive and King.health < King.max_health and abs(pt.HERO_POS[0]-pos[0]) + abs(pt.HERO_POS[1]-pos[1]) < closest__wounded_dist):
            closest__wounded_dist = abs(pt.HERO_POS[0]-pos[0]) + abs(pt.HERO_POS[1]-pos[1])
            closest_wounded_troop = King

    if (closest_wounded_troop is None):
        return closest_troop
    return closest_wounded_troop


# --------------------------------------------code added down------------------------------------------


def findPathWithoutWall(grid, start, end):
    graph = []
    for row in grid:
        row2 = []
        for col in row:
            if (col == pt.BLANK):
                row2.append(0)  # 0 means walkable
            else:
                row2.append(1)  # 1 means not walkable
        graph.append(row2)
    graph[start[0]][start[1]] = 2  # mark start as 2
    graph[end[0]][end[1]] = 3  # mark end as 3

    coords = moveWithoutBreakingWalls(graph, start)
    if coords == None:
        return None
    else:
        return list(coords)
