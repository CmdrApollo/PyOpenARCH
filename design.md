# Gameplay Plan

As of right now, there is no gameplay implemented in PyOpenARCH. Therefore, any talk of gameplay is purely hypothetical. That being said, there are many ideas for the gameplay of PyOpenARCH, as detailed below. Needless to say, this is all open to change.

## General Gameplay Ideas

1. PyOpenARCH is a turn-based grand strategy game. Each turn occurs over the course of the equivalent 1 season in the northern hemisphere. That meaning that there are 4 seasons in a year, and therefore 4 in-game turns in an in-game year.
2. Each turn, a player has 3 "Action Points" with which to perform actions, each action costing 1 point. Actions are split into different categories (as of now undecided) such as agriculture, commerce, research, emmigration, etc.
3. Certain actions are more effective during certain seasons. For example, a "plant crops" action would be most successful during spring and least successful during winter and a "harvest crops" action would be best played during autumn.

## Expansion and Governors

1. Since you only have so many actions to spend per turn, you can hire "Governors", people who fill specific roles and perform specific actions for a given city on a yearly cycle. Governors come with different predetermined schedules/actions that they perform year in and year out. For example, an "Agricultural" Governor would focus on the city performing agricultural actions. When hiring a governor, the player is presented with a few (perhaps 3) options and must pick one. Once hired, a Governor must be in place for a year (4 turns) before being able to be replaced.
2. Expansion actions are limited to the player. Governors cannot expand into further territories by themselves.

## Resources

1. The four main resources in PyOpenARCH are Gold, Food, Morale, and Research.
2. In PyOpenARCH, resources are global, meaning that once they are collected they are shared among all cities in your nation (this is in order to lessen micromanagement).

## Biomes

1. Each of the 4 biomes has 4 stats, as determined by the chart below (they are abstracted as either high, medium, or low), which it then passes on to any city/colony within its borders. The stats are Attractiveness (At), Defense/Defendability (Df), Fertility (Ft), and Resources (Rc).
2. Upon world generation, every tile's stats are determined by its biome and then nudged randomly in order to give some variation.

```
  |Bch|Pln|Frs|Mnt|
--+---+---+---+---+
At| H | H | L | M |
--+---+---+---+---+
Df| L | M | H | H |
--+---+---+---+---+
Ft| H | H | M | L |
--+---+---+---+---+
Rc| M | L | H | H |
--+---+---+---+---+
```

### Landmarks

1. Sometimes, a tile will generate a "landmark", a natural formation or process that gives a passive bonus that can be thought of similarly to a perk in certain other games. An example of this would be an "ancient ruin" landmark that gives a passive boost to research or a "bay" landmark on a beach tile that increases how many people passively come to that tile.
2. As a late-game "treat", players should be able to build man-made landmarks for large sums of gold that perform the same tasks as naturally occuring landmarks with a slight debuff compared to the naturally occuring ones. For example, a player could spend lots of money to have their population dig a man-made bay on a beach tile in order to have (close to) the same effect as a naturally occuring bay.