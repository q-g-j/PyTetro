PyTetro
=======
### A Tetris clone written in Python using pygame


Latest release:
---------------
|Filename|Platform|
|:---|:---|
|[PyTetro.exe](https://github.com/q-g-j/PyTetro/releases/download/latest/PyTetro.exe)|Windows - 32 bit||

Controls:
---------

### Menu navigation:
|Key|Action|
|-|-|
|UP or "I"|navigate up|
|DOWN or "K"|navigate down|
|ENTER|apply selection|

### Ingame control:
|Key|Action|
|-|-|
|LEFT or "J"|move tetromino left|
|RIGHT or "L"|move tetromino right|
|SPACE|move tetromino down|
|DOWN or "K"|rotate tetromino counterclockwise|
|UP or "I"|rotate tetromino clockwise|
|PAUSE or "P"|pause / resume the game|

### Scoring:
|Cleared Lines|Awarded Points|
|-|-|
|1|10|
|2|40|
|3|90|
|4|160|

### Levelling up:
A level up is achieved as soon as you have managed to remove a certain number of lines.<br/><br/>
**Formula:** ```current level - 1 + 10 lines``` to reach the next level<br/><br/>
The maximum is 20 levels.
