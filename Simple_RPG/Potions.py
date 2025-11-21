# Potions parent class
class Potion:
    def __init__(self, character, name, description, restore):
        self.character = character
        self.name = name
        self.description = description
        self.restore = restore

# Healing Potion 
class Hp_Potion(Potion):
    def __init__(self, character, name="HP Potion", description="Restores 20 HP.", restore=20):
        super().__init__(character, name, description, restore)
    
    def use(self):
        # Check if the potion is in the inventory
        if self.character.items["HP Potion"][1] > 0:
            healed_hp = min(self.character.max_hp - self.character.hp, self.restore)
            self.character.hp += healed_hp
            # Decrease potion count
            item_name, amount = self.character.items["HP Potion"]
            self.character.items["HP Potion"] = (item_name, amount - 1)
            return healed_hp
        else:
            return 0

# Mana Potion
class Mp_Potion(Potion):
    def __init__(self, character, name="MP Potion", description="Restores 20 MP.", restore=20):
        super().__init__(character, name, description, restore)
    
    def use(self):
        # Check if the potion is in the inventory
        if self.character.items["MP Potion"][1] > 0:
            healed_mp = min(self.character.max_mp - self.character.mp, self.restore)
            self.character.mp += healed_mp
            # Decrease potion count
            item_name, amount = self.character.items["MP Potion"]
            self.character.items["MP Potion"] = (item_name, amount - 1)
            return healed_mp