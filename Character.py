class Character:
    
    def __init__(self):
        self.currentPosition = "Start"
        
        # --- Status Variables ---
        self.name = "PAWN"
        self.title = "Red Archon"
        self.hp = 4
        self.mp = 40
        self.max_hp = 50
        self.max_mp = 50
        self.atk = 12
        self.defense = 8
        self.spd = 10
        
        self.equipment = {"Armor": ("Basic Armor", 0,),
                          "Weapon": ("Basic Weapon", 0)
                         }
        
        self.items = {"HP Potion": ("HP Potion", 1),
                      "MP Potion": ("MP Potion", 1)
                     }
        
    def pickup(self, name:str):
        '''
        Picks up an item.

        Args:
            name: The name of the item.
        '''
        item_name, amount = self.items[name]   
        self.items[name] = (item_name, amount+1)
        
    def reset(self):
        '''
        Resets the character to the start position and all its attributes.

        '''
        self.currentPosition = "Start"
        
        # --- Status Variables ---
        self.hp = 4
        self.mp = 40
        self.max_hp = 50
        self.max_mp = 50
        self.atk = 12
        self.defense = 8
        self.spd = 10

        # --- Reset equipment ---
        self.equipment = {
            "Armor": ("Basic Armor", 0),
            "Weapon": ("Basic Weapon", 0)
        }

        # --- Reset items ---
        self.items = {
            "HP Potion": ("HP Potion", 1),
            "MP Potion": ("MP Potion", 1)
        }
