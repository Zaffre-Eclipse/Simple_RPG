class Mp_Potion():
    
    def __init__(self, character, name="MP Potion", description="Restores 20 MP.", restore=20):
        self.name = name
        self.description = description
        self.restore = restore
        self.character = character
    
    def use(self,):
        if self.character.items["MP Potion"][1] > 0:
            healed_mp = min(self.character.max_mp - self.character.mp, self.restore)
            self.character.mp += healed_mp
            # Decrease potion count
            item_name, amount = self.character.items["MP Potion"]
            self.character.items["MP Potion"] = (item_name, amount - 1)
            return healed_mp
        else:
            return 0
