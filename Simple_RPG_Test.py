import pytest
import arcade
from Character import Character
from Hp_Potion import Hp_Potion
from Mp_Potion import Mp_Potion
from Necromancer import Necromancer
from NightBorne import NightBorne
from BattleScreen import BattleScreen
from MainScreen import MainScreen

# FIXTURES

@pytest.fixture
def character():
    return Character()

@pytest.fixture
def hp_potion(character):
    return Hp_Potion(character)

@pytest.fixture
def mp_potion(character):
    return Mp_Potion(character)

@pytest.fixture
def necromancer():
    return Necromancer()

@pytest.fixture
def nightborne():
    return NightBorne()

@pytest.fixture(scope="session", autouse=True)
def setup_arcade_window():
    """Create a real Arcade window once for the entire test session."""
    import arcade

    # Create the window only once
    window = arcade.Window(800, 600, "Test Window", visible=False)
    arcade.set_window(window)
    yield
    window.close()

@pytest.fixture
def mainscreen():
    # Mock character
    character = Character()

    # Minimal fake maze so MainScreen doesn't crash
    maze = {
        "Start": ([], False, False),
    }

    # Minimal fake connections
    connections = {
        "A": (False, ("Start", "Start")),
    }

    # Create MainScreen normally (now window exists)
    screen = MainScreen(character, maze, connections)

    # Attach the active arcade window
    screen.window = arcade.get_window()
    return screen

@pytest.fixture
def battle(mainscreen):
    return BattleScreen(mainscreen)

class Test_Simple_RPG:
    """
    This is a test class for our RPG game
    Alexandra
    """
    
    def test_drop_loot(self, necromancer, character):
        """This method tests whether dropped loot items are handled properly"""
        
        initial_amount = character.items["HP Potion"][1]
        loot = necromancer.drop_loot(character)
        
        if loot == "HP Potion":
            assert character.items["HP Potion"][1] == initial_amount + 1
        else:
            assert character.items["HP Potion"][1] == initial_amount
            
        assert loot in ["HP Potion", None]
    
    
    def test_pickup(self, character):
        """
        This method tests whether getting items is handled properly
        
        Args:
            character: The character instance being used
        """
        
        char = character
        
        # Add 4 HP potions
        for i in range(4):
            char.pickup("HP Potion")
        
        # Add 5 MP potions
        for j in range(5):
            char.pickup("MP Potion")

        # Add 43 Gold
        for k in range(43):
            char.pickup("Gold")

        # Make sure the correct amounts were added per item
        assert char.items == {"HP Potion": ("HP Potion", 4),
                              "MP Potion": ("MP Potion", 5),
                              "Gold": ("Gold", 43)
                             }
        
    
    def test_use_hp_potion(self, character, hp_potion):
        """
        This method tests whether HP potions function correctly
        
        Args:
            character: The character instance being used
        
            hp_potion: An instance of HP Potion
        """
        
        char = character
        hPotion = hp_potion

        # Add HP potions
        for i in range(10):
            char.pickup("HP Potion")

        # Use 2 potions
        for j in range(2):
            hPotion.use()

        # Inventory check
        assert char.items["HP Potion"][1] == 8

        # HP should not exceed max
        assert char.hp == 50

        # Should not restore more than 20 HP
        char.hp = 20
        hPotion.use()
        assert char.hp == 40

        # Make sure inventory never goes below 0
        for k in range(10):
            hPotion.use()

        assert char.items["HP Potion"][1] == 0
        
        
    def test_use_mp_potion(self, character, mp_potion):
        """
        This method tests whether MP potions function correctly
        
        Args:
            character: The character instance being used
        
            mp_potion: An instance of MP Potion
        """
        
        char = character
        mPotion = mp_potion

        # Add MP potions
        for i in range(12):
            char.pickup("MP Potion")

        # Use 5 potions
        for j in range(5):
            mPotion.use()

        # Inventory check
        assert char.items["MP Potion"][1] == 7

        # MP should not exceed max
        assert char.mp == 50

        # Should not restore more than 20 MP
        char.mp = 15
        mPotion.use()
        assert char.mp == 35

        # Make sure inventory never goes below 0
        for k in range(10):
            mPotion.use()

        assert char.items["MP Potion"][1] == 0

                
    def test_calc_damage(self, mainscreen, battle, necromancer):
        """
        This method tests whether enemy attack damage is handled properly
        
        Args:
            mainscreen: An instance of MainScreen
        
            battle: An instance of BattleScreen
            
            necromancer: An instance of Necromancer
        """
        
        character = mainscreen.character
        # Normal attack calculation is enemy ATK - player DEF
        # In this case: 10 - 8 = 2
        
        character.hp = 50
        # Call enemy_attack
        battle.enemy_attack(necromancer)
        
        # Skip animation by forcing animation to "completed" state
        battle.enemy_sprite_attack_animation_active = False
        
        # Now apply the actual damage
        battle.apply_pending_enemy_damage()
        assert character.hp == 48
        
        # Make sure HP never goes below 0
        character.hp = 1
        battle.enemy_attack(necromancer)
        battle.enemy_sprite_attack_animation_active = False
        battle.apply_pending_enemy_damage()
        assert character.hp == 0
    
    
    def test_guard(self, necromancer, character):
        """
        This method tests whether the guard buff is handled properly
        
        Args:            
            necromancer: An instance of Necromancer
            
            character: The instance of Character being used
        """
        
        # If the character has their tight guard special active
        # then the damage should be halved and the turn count for
        # the special should be decremented
        guard = 0
        damage, guard  = necromancer.calc_damage(guard, character)
        assert damage == 2
        guard = 1
        damage, guard = necromancer.calc_damage(guard, character)
        assert damage == 1
        assert guard == 0
    
    
    def test_character_reset(self, character):
        """
        This method tests whether resetting the game is being handled properly
        
        Args:                        
            character: The instance of Character being used
        """
        
        char = character
        char.hp = 25
        char.mp = 15
        char.atk = 5
        char.defense = 50
        char.spd = 200
        char.max_hp = -510
        char.max_mp = 0
        
        char.items = {"HP Elixer": ("HP Elixer", 30),
                      "MP Elixer": ("MP Elixer", 40),
                      "Diamonds": ("Diamonds", -450)
                     }
        
        char.equipment = {"Chestplate": ("Titanium Armor", 12),
                          "Sword": ("Golden Greatsword", 15)
                         }
        
        char.reset()
        
        assert char.hp == 50
        assert char.mp == 50
        assert char.max_hp == 50
        assert char.max_mp == 50
        assert char.atk == 12
        assert char.defense == 8
        assert char.spd == 10
        
        assert char.equipment == {"Armor": ("Basic Armor", 0),
                                  "Weapon": ("Basic Weapon", 0)
                                 }
        
        assert char.items == {"HP Potion": ("HP Potion", 0),
                              "MP Potion": ("MP Potion", 0),
                              "Gold":("Gold", 0)
                             }
        
    
    def test_nightborne_heal(self, nightborne):
        """
        This method tests whether the boss healing is handled properly
        
        Args:            
            nightborne: An instance of NightBorne
        """
        
        # Make sure the heal doesn't go over max hp
        nightborne.hp = 100
        assert nightborne.heal() == 0
        assert nightborne.hp == 100
        
        nightborne.hp = 83
        assert nightborne.heal() == 17
        assert nightborne.hp == 100
        
        # Make sure the heal doesn't restore more than 40
        nightborne.hp = 50
        assert nightborne.heal() == 40
        assert nightborne.hp == 90
    
    
    def test_nightBorne_debuff(self, nightborne, battle):
        """
        This method tests whether the boss debuff resets the Player buffs
        
        Args:            
            nightborne: An instance of NightBorne
            
            battle: An instance of BattleScreen
        """
        
        # Make sure all active player buffs are reset
        battle.overclock = 2
        battle.guard = 1
        battle.repair = 3
        nightborne.debuff(battle)
        assert battle.overclock == 0
        assert battle.guard == 0
        assert battle.repair == 0


    def test_nightborne_debuff_does_not_affect_hp_mp(self, nightborne, battle, mainscreen):
        """
        This method makes sure that the boss
        debuff doesn't affect Player HP or MP 
        
        Args:            
            nightborne: An instance of NightBorne
            
            battle: An instance of BattleScreen
            
            mainscreen: An instance of MainScreen
        """
        
        char = mainscreen.character
        char.hp = 35
        char.mp = 20
        nightborne.debuff(battle)
        assert char.hp == 35
        assert char.mp == 20