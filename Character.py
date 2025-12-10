class Character:
    """
    This class represents the player character and interacts with
    MainScreen, BattleScreen and ScreenChnager classes
    Tiffany
    """
    
    def __init__(self):
        """
        This is the setup for this class
        """
        
        # Make sure the player starts in the starting room on the mini map
        self.currentPosition = "Start"
        
        # Status Variables
        self.name = "PAWN"
        self.title = "Red Archon"
        self.hp = 4
        self.mp = 50
        self.max_hp = 50
        self.max_mp = 50
        self.atk = 12
        self.defense = 8
        self.spd = 10
        
        # Equipment
        self.equipment = {"Armor": ("Basic Armor", 0),
                          "Weapon": ("Basic Weapon", 0)
                         }
        
        # Items
        self.items = {"HP Potion": ("HP Potion", 0),
                      "MP Potion": ("MP Potion", 0),
                      "Gold": ("Gold", 0)
                     }
        
        # Special moves
        self.special = {"Overclock": ("Overclock", "Double your damage output for 2 attacks", 10),
                        "Tight Guard": ("Tight Guard", "Halve your damage taken for 2 blocks", 10),
                        "Auto-Repairs": ("Auto-Repairs", "Recover 10 HP every round for 3 rounds", 15),
                        "Exit": "Exit"
                       }
        
        
    def pickup(self, name):
        """
        This method adds an item to the players inventory
        
        Args:
            name: The name of the item being added
        """
        
        item_name, amount = self.items[name]   
        self.items[name] = (item_name, amount+1)
        
    def reset(self):
        """This method resets the character back to defualt"""
        
        self.currentPosition = "Start"
        
        # Status Variables
        self.hp = 50
        self.mp = 50
        self.max_hp = 50
        self.max_mp = 50
        self.atk = 12
        self.defense = 8
        self.spd = 10

        # Reset equipment
        self.equipment = {"Armor": ("Basic Armor", 0),
                          "Weapon": ("Basic Weapon", 0)
                         }

        # Reset items
        self.items = {"HP Potion": ("HP Potion", 0),
                      "MP Potion": ("MP Potion", 0),
                      "Gold":("Gold", 0)
                     }