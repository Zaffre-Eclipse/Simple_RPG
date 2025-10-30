class Hp_Potion():
    
    def __init__(self, character, name="HP Potion", description="Restores 20 HP.", restore=25):
        self.name = name
        self.description = description
        self.restore = restore
        self.character = character
    
    
    def use(self,):
        if self.character.items["HP Potion"][1] > 0:
            healed_hp = min(self.character.max_hp - self.character.hp, self.restore)
            self.character.hp += healed_hp
            # Decrease potion count
            item_name, amount = self.character.items["HP Potion"]
            self.character.items["HP Potion"] = (item_name, amount - 1)
            return healed_hp
        else:
            return 0
