# Assignment 3.1

- Everything mentioned in the assignment has been implemented.
- **Bonus** :
    - King’s Leviathan Axe has also been implemented.
    - Dragon Character has been added, it can fly over walls.
    - Queen's Eagle Arrow has been added.
    - Movement avoiding walls has also been implemented.

- To run the game : `python3 game.py`
- To view replays : `python3 replay.py`  and select the replay you want to watch according to mentioned date and time.
- For Victory : All buildings apart from walls get destroyed from the map in all three levels.
- For Defeat : If all troops and King die before destroying all buildings apart from walls.

## Controls :

### Hero :

- w : move up
- a : move left
- d : move right
- s : move down
- 1 : Special Attack
- space : Normal Attack

### Barbarian :

- z : spawn at point 1
- x : spawn at point 2
- c : spawn at point 3

### Dragon :

- v : spawn at point 1
- b : spawn at point 2
- n : spawn at point 3

### Archer :

- i : spawn at point 1
- o : spawn at point 2
- p : spawn at point 3

### Balloon :

- j : spawn at point 1
- k : spawn at point 2
- l : spawn at point 3

### Stealth Archer :

- t : spawn at point 1
- y : spawn at point 2
- u : spawn at point 3

### Healer :

- e : spawn at point 1
- f : spawn at point 2
- g : spawn at point 3

q : Quit Game

## Assumptions :

- Rage and Heal Spell can be applied multiple times.
- The limit for troops in each level is as follows :
    - Barbarians : 10
    - Archers : 7
    - Balloon : 5
    - Dragon : 3
- You have to choose the type of troop movement at start of the game.
- You have to choose the hero after each level.


### Assignment 3: 
- Level of Cannon Hardcoded in village.py(Line No. 88) to 3. 
- Level of Wizard Tower Hardcoded in village.py(Line No. 98) to 1. 
- Level of Walls Hardcoded in village.py(Line No. 56, 60, 64, 68, 72, 76, 80, 84) to 3(to show Explosion).
- Healer Heals all it's Troops in a Square of 1*1 Tile Dimensions (i.e 4 tiles Area).
- Healer moves to the Nearest Wounded Troop to Heal it first. In case there are no Wounded Troops, Healer aproaches the Nearest Troop
to Heal it.
- Stealth Archer, even if it is Invisible, can be Damaged by Explosion by the Wall.
- Stealth Archer, is Invisible for the First 10 Seconds, here it Means that it can't be Targeted by Defenses in those 10 Seconds.