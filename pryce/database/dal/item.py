from pryce import *
from database import models

def get_items():
    items = Item.query.all()
    return items
   
def add_store(store):
     
    db.session.add(store);
