# LittleMouseAdventure
A Practice Adventure RPG Game

This is a simple RPG game developed with Pygame, featuring combat, character progression, gacha, save system and other functionalities. All code is written as Python scripts with a clear structure, making it suitable for learning or further expansion.
File Description
```bash
main.py         The main entry point of the game, containing the main loop, event handling, state switching and rendering scheduling.
constants.py    Defines all constants, such as screen dimensions, colors, fonts, game states, button sizes, gacha probabilities, etc.
ui.py           Contains all rendering functions, including drawing for menus, combat, progression, gacha and other interfaces.
handlers.py     Input processing functions, handling mouse click events and calling corresponding logic functions based on the current game state.
battle.py       Combat logic, including functions for player attacks, player skills (healing), enemy attacks, etc.
levels.py       Level data, generating corresponding enemy data based on the level number.
upgrade.py      Character progression logic, including functions for using experience books and skill books.
gacha.py        Gacha logic, including character pool definitions and gacha functions (consumes gold coins).
save.py         Save and load functionality, saving game progress using JSON files.
```

Run Instructions
Install Python 3.12+ and the Pygame library:
```bash
pip install pygame
```

Run main.py:
```bash
python main.py
```

Game Controls
Click buttons with the mouse to make selections
Press the ESC key to return to the previous menu
Game Features
Combat System: Attack, Heal, Enemy AI
Character Progression: Level Up, Learn Skills
Gacha System: Consume gold coins to randomly obtain new characters
Save System: Auto-save and manual save
