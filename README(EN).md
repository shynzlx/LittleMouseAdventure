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


## Update logs ##
**Update TEST_0.3_alpha -2026.3.10**
✨ Optimizations

Combat animation optimization. Combat logic changed. 

Enemy positions changed from hardcoded → level.py now designs each level's enemy positions individually.

**Update TEST_0.2_alpha -2026.3.9**

⚙️ Combat Logic Adjustments

Added speed-based combat logic.

✨ Optimizations

Optimized main menu UI and combat UI.

Major character file update: Characters are now defined in individual files within the character package.

**Update TEST 0.1.2 alpha -2026.3.8**

✨ New Features
Deployment System: You can now manage up to 5 characters in your active party. Only deployed characters participate in combat.

Development Interface Scrolling: When there are more than 6 characters, you can scroll through the list using the mouse wheel.

Deployment Status Indicator: In the development interface, the button border for deployed characters is displayed in gold, while standby characters have a white border.

Deployment Toggle Button: In the development interface, a new "Set Deployed/Standby" button has been added to the detailed information area on the right. Click it to toggle a character's deployment status, automatically checking the deployment limit (max 5 characters).

Development Interface Scrollbar: When there are more than 6 characters, use the mouse wheel to scroll and view all characters.

⚙️ Combat Logic Adjustments
The combat interface now only displays and allows actions for deployed characters. Undeployed characters do not appear in combat.

Enemy attacks only target deployed and alive characters.

🔧 Functionality Adjustments
Combat Mechanic Optimization:

Attacks and healing only affect alive characters. Deceased characters are no longer considered in damage calculation or receive healing.

Enemy attacks automatically skip deceased characters to avoid ineffective actions.

Interface Simplification: Removed the redundant "ESC Return to Level Select" text hint from the bottom of the combat interface (as there is already a "Flee" button and the global ESC return function), reducing clutter.

Enhanced Global ESC Return: Pressing ESC in confirmation screens also returns to the level select interface, consistent with clicking the "Return" button.

🐛 Bug Fixes
Fixed an issue where buttons for experience books, skill books, the gacha interface, and the deployment toggle were unresponsive (due to inconsistencies between button coordinates and detection areas).

Fixed an issue where scrolling the mouse wheel in the combat interface inadvertently triggered attack buttons (by filtering wheel button events).

Fixed an issue where there were two "Return to Main Menu" elements simultaneously in the bottom left corner of the level select mode (removed redundant ESC prompt text).

Fixed an issue where the "Return to Main Menu" button in the development interface was unusable (improved event handling logic).

Fixed an issue where the game would end prematurely upon the death of a single player character, and enemies would continue attacking deceased characters.

📦 Data Compatibility

Added an active field (boolean) in save files to record each character's deployment status. When loading old save files, the first 5 characters are automatically set as deployed, and the rest are set as standby.
