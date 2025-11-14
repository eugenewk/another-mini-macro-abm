from typing import List, Dict

class StockMatrix:
    def __init__(self):
        self.cash: int = 0
        self.inventory: Dict[str, int] = {}

    def __repr__(self):
        return f'cash: {self.cash}, inventory: {self.inventory}'
    
    def manage_cash(self, amount: int):
        # check if amount is too much
        if amount < 0 and abs(amount) > self.cash:
            print('tried to remove too much cash')
        else:
            self.cash += amount
        return self.cash
        

    def manage_inventory_item(self, item:str, amount: int):
        # create if not already exists
        if item not in self.inventory:
            self.inventory[item] = 0

        # check removal limit
        if amount < 0 and abs(amount) > self.inventory[item]:
            print(f'tried to remove {abs(amount)} from {item}, not enough exist')
            return self.inventory[item]
        
        # if all good then proceed
        self.inventory[item] += amount
        return self.inventory[item]

