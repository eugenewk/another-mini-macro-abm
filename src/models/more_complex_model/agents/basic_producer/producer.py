"""simple agent file"""
from mini_macro_abm.core.data_collector import AgentDataObject
from mini_macro_abm.core.agent_utils.stock_matrix import StockMatrix
from models.more_complex_model.markets.basic_market import BasicMarket

class BasicProducer:

    def __init__(self, id):
        # core setup params, requires id given by sim engine
        self.id = id
        self.stock_matrix = StockMatrix() # gives stock matrix
        self.agent_data = AgentDataObject(id, self.stock_matrix) # creates data tracking object
        self.item = 'item'
        self.item_price = 1
        self.goods_listing_id = None
        
        # this will call the inits for each mixins
        # call this AFTER initializing the agent params, then the mixins can validate their required params exist
        super().__init__()

    def __repr__(self):
        return f"{self.id}"
    
    def add_cash(self, amount):
        self.stock_matrix.manage_cash(amount)

    def remove_cash(self, amount):
        self.stock_matrix.manage_cash(-amount)

    def add_item(self, item: str, amount: int):
        self.stock_matrix.manage_inventory_item(item, amount)

    def create_goods_listing(self, goods_market: BasicMarket) -> bool:
        self.goods_listing_id = goods_market.add_listing(self.id, self.item, 1, self.item_price)

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
       


    
