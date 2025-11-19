"""simple agent file"""
from mini_macro_abm.core.data_collector import AgentDataObject
from mini_macro_abm.core.agent_utils.stock_matrix import StockMatrix
from models.more_complex_model.markets.basic_market import BasicMarket
from typing import List, Dict
import copy

class BasicProducer:

    def __init__(self, id):
        # core setup params, requires id given by sim engine
        self.id = id
        self.stock_matrix = StockMatrix() # gives stock matrix
        self.agent_data = AgentDataObject(id, self.stock_matrix) # creates data tracking object
        self.item = 'item'
        self.item_price = 1
        self.goods_listing_id = None

        # track purchase orders for each step
        self.purchase_orders: List[Dict] = []

        # note for this step: daily_purchase_orders clears self.purchase_orders list after recording and so must be evaluated last here
        self.agent_data.add_data_attributes(['item_price', 'count_of_daily_transactions', 'daily_purchase_orders'])
        
        # this will call the inits for each mixin
        # call this AFTER initializing the agent params, then the mixins can validate their required params exist
        super().__init__()
    
    # use @property tag to define custom properties
    # add them to the tracking using self.agent_data.add_data_attributes(['property1', 'property2']) in the init
    @property
    def count_of_daily_transactions(self):
        daily_transactions = len(self.purchase_orders)
        return daily_transactions

    @property
    def daily_purchase_orders(self):
        daily_purchase_orders = copy.deepcopy(self.purchase_orders)
        self.purchase_orders = [] # clear list for next step, this param must be placed last in the attributes tracking
        return daily_purchase_orders
    



    def __repr__(self):
        return f"{self.id}"
    
    def add_cash(self, amount):
        self.stock_matrix.manage_cash(amount)

    def remove_cash(self, amount):
        self.stock_matrix.manage_cash(-amount)

    def add_item(self, item: str, amount: int):
        self.stock_matrix.manage_inventory_item(item, amount)

    def create_goods_listing(self, goods_market: BasicMarket) -> bool:
        self.goods_listing_id = goods_market.add_listing(self, self.id, self.item, 1, self.item_price)

    def update_listing_price(self, goods_market: BasicMarket, new_price: int) -> bool:
        if not self.goods_listing_id: 
            raise ValueError(f"listing does not exist for {self.id}, tried to update")
        
        # if listing exists, allow update
        goods_market.update_listing_price(self.goods_listing_id, new_price)

    def update_listing_qty(self, goods_market: BasicMarket) -> bool:
        # note: right now this will just set listing qty equal to inventory
        if not self.goods_listing_id:
            raise ValueError(f"listing does not exist for {self.id}, tried to update")
        
        goods_market.update_listing_qty(self.goods_listing_id, self.stock_matrix.inventory[self.item])

    def receive_purchase_order(self, market: BasicMarket, buyer_id: str, good: str, qty_requested: int, payment_amt: int) -> bool:
        # needs to receive a purchase order from a household agent for a particular good
        # first check quantity is available
        qty_available = self.stock_matrix.inventory.get(good, 0) # default to 0 if item doesn't exist
        
        if qty_available >= qty_requested:
            # create purchase order, append to list
            purchase_order = {
                'buyer': buyer_id,
                'good': good,
                'amt': qty_requested,
                'total_paid': payment_amt
            }
            print("purchase successful:")
            print({str(purchase_order)})
            self.purchase_orders.append(purchase_order)
            # reduce inventory by amount and credit cash by payment amt
            self.stock_matrix.manage_inventory_item(good, -qty_requested)
            self.stock_matrix.manage_cash(payment_amt)
            self.update_listing_qty(market)
            return True
        else:
            print("purchase failed")
            print(f"{qty_requested} by {buyer_id}, only {qty_available} available")
            return False




        

    
       


    
