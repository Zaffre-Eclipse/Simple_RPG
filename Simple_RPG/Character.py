class Character:
    
    def __init__(self):
        self.currentPosition = "Start"
        
        # --- Status Variables ---
        self.name = "PAWN"
        self.title = "Red Archon"
        self.hp = 50
        self.mp = 50
        self.max_hp = 50
        self.max_mp = 50
        self.atk = 12
        self.defense = 9
        self.spd = 10
        
        self.equipment = {"Armor": ("Basic Armor", 0,),
                          "Weapon": ("Basic Weapon", 0)
                         }
        
        self.items = {"HP Potion": ("HP Potion", 0), 
                      "MP Potion": ("MP Potion", 0)
                     }
        
    def pickup(self, name:str):
        item_name, amount = self.items[name]   
        self.items[name] = (item_name, amount+1) 

