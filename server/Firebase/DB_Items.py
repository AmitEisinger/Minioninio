from Firebase.firestore import FirestoreClient as fc
from Definitions.DatabaseStructure import *
from Definitions.Protocol import ClientMessageFields


COL = Collections.ITEMS

class DB_Items:
    def get_all_items():
        return fc.readAll(COL)
    
    def get_not_available_items(items):
        not_available_items = []
        for item in items:
            doc = fc.read(COL, item[DocumentFields.ID])
            if not doc:
                not_available_items.append(item)
            amounts_diff = item[ClientMessageFields.AMOUNT] - doc[DocumentFields.AMOUNT]    # desirable - available
            elif amounts_diff > 0:
                not_available_items[ClientMessageFields.AMOUNT] = amounts_diff
        return not_available_items

    def get_available_items(items):
        available_items = items
        for i,item in enumerate(available_items):
            doc = fc.read(COL, item[DocumentFields.ID])
            if not doc:
                del available_items[i]
            elif doc[DocumentFields.AMOUNT] < item[ClientMessageFields.AMOUNT]:
                available_items[ClientMessageFields.AMOUNT] = doc[DocumentFields.AMOUNT]
        return available_items
