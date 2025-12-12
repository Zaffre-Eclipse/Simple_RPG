# CRYPTID: Red Archon

*Welcome to your first day of training...*

A turn-based RPG game built with Python and the Arcade library. Navigate through a maze-like testing facility, battle enemies, collect items, and prepare for the final boss encounter.

## Overview

**CRYPTID: Red Archon** is an object-oriented RPG game where you play as PAWN, a warrior in the Red Archon Army. Explore rooms, engage in strategic turn-based combat, manage your inventory, and reach the end of the testing facility.

## Features

- **Maze Exploration**: Navigate through interconnected rooms with a minimap system
- **Turn-Based Combat**: Strategic battles with Quick Time Event (QTE) mechanics for attacks and dodges
- **Character Progression**: Manage HP, MP, attack, defense, and speed stats
- **Equipment System**: Upgrade your armor and weapons to increase combat effectiveness
- **Item Management**: Collect and use HP/MP potions, and accumulate gold
- **Shop System**: Purchase equipment and consumables with gold
- **Special Abilities**: Use powerful special moves like Overclock, Tight Guard, and Auto-Repairs
- **Multiple Enemy Types**: Face different enemies including Necromancers and the final boss NightBorne
- **Audio Experience**: Background music and sound effects that change based on context
- **Tutorial System**: In-game tutorials for combat, shops, and boss battles

## Project Structure

```
Group Project/
├── Simple_RPG/              # Main game version (most complete)
│   ├── Art/                 # Game assets (sprites, backgrounds)
│   │   ├── Attack/          # Attack animation assets
│   │   ├── Dodge/           # Dodge QTE assets
│   │   ├── Enemies/         # Enemy sprites
│   │   └── Room_Backgrounds/# Room background images
│   ├── Music/               # Background music files
│   ├── SFX/                 # Sound effect files
│   ├── Intro.py             # Game entry point and intro screen
│   ├── MainScreen.py        # Main game view and overworld logic
│   ├── BattleScreen.py      # Battle system and combat logic
│   ├── Character.py         # Player character class
│   ├── Necromancer.py       # Regular enemy class
│   ├── NightBorne.py        # Boss enemy class
│   ├── Hp_Potion.py         # HP potion item class
│   ├── Mp_Potion.py         # MP potion item class
│   ├── Potions.py           # Potion base class
│   ├── ScreenChanger.py     # UI rendering and popup management
│   └── Simple_RPG_Test.py  # Test file
│
├── Simple_And_Clean_RPG/    # Simplified version of the game
│   └── README.md            # Version-specific documentation
│
└── Simple_RPG_old/          # Legacy version
    └── README.md            # Version-specific documentation
```

## Prerequisites

- **Python 3.x** (Python 3.7 or higher recommended)
- **Arcade Library 3.3** - Python game development library
- **PIL (Pillow)** - Image processing library (for sprite animations)

## Installation

1. **Clone or download this repository**

2. **Install required dependencies:**

   Open Command Prompt and run:
   ```
   pip install arcade pillow
   ```

   Or if you prefer using a requirements file, create one with:
   ```
   arcade
   pillow
   ```

   Then install with:
   ```
   pip install -r requirements.txt
   ```

## How to Run

1. Open Command Prompt and navigate to the project directory
2. Run the main game file:

   ```
   python Simple_RPG\Intro.py
   ```

   Or from within the Simple_RPG directory:

   ```
   cd Simple_RPG
   python Intro.py
   ```

## Gameplay Instructions

### Controls

- **Arrow Keys (↑↓←→)**: Move between rooms
- **Z**: Investigate room (search for items) or use shop
- **X**: Open/close status menu
- **ENTER**: Confirm selection in menus
- **LEFT/RIGHT**: Navigate menu options
- **UP/DOWN**: Navigate menu options (in some menus)

### Combat System

- **Attack**: Press Z during the attack QTE to deal damage
- **Dodge**: Press the indicated arrow key during boss attacks to reduce damage
- **Items**: Use HP/MP potions to restore health and mana
- **Special Moves**: 
  - **Overclock**: Double damage for 2 attacks (10 MP)
  - **Tight Guard**: Halve damage taken for 2 blocks (10 MP)
  - **Auto-Repairs**: Recover 10 HP every round for 3 rounds (15 MP)

### Game Mechanics

- **Room Exploration**: Each room can be investigated once for loot
- **Minimap**: Track your progress and visited rooms in the upper-right corner
- **Shop**: Purchase equipment upgrades and consumables with gold
- **Equipment**: Armor increases defense, weapons increase attack
- **Gold**: Earned by investigating rooms, used to buy items in the shop

## Game Flow

1. **Intro Screen**: Watch the introduction and press Z to begin
2. **Exploration**: Navigate through rooms using arrow keys
3. **Combat**: Random encounters trigger turn-based battles
4. **Loot Collection**: Investigate rooms (Z key) to find items and gold
5. **Shopping**: Visit the shop to upgrade equipment
6. **Boss Battle**: Reach the End room to face the final boss
7. **Victory**: Defeat the boss to complete the game

## Development

This project was developed as a group project for an Introduction to Object Oriented Programming course. The codebase demonstrates:

- Object-oriented design principles
- Class inheritance and composition
- Game state management
- Event-driven programming
- Animation and sprite handling
- Audio integration

### Key Classes

- **Character**: Player character with stats, equipment, and inventory
- **MainScreen**: Main game view managing overworld, combat, and UI
- **BattleScreen**: Combat system with turn management and QTE mechanics
- **Necromancer/NightBorne**: Enemy classes with unique behaviors
- **ScreenChanger**: UI rendering and popup management
- **MiniMap**: Minimap visualization system

## Credits

Developed by: Anner, Isaac, Tiffany, Alexandra


## License

This project was created for educational purposes as part of a university course.

