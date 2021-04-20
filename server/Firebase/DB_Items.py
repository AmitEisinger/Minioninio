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
                continue
            amounts_diff = item[ClientMessageFields.AMOUNT] - doc[DocumentFields.AMOUNT]    # desirable - available
            if amounts_diff > 0:
                item[ClientMessageFields.AMOUNT] = amounts_diff
                not_available_items.append(item)
        return not_available_items

    def get_available_items(items):
        available_items = []
        for item in items:
            doc = fc.read(COL, item[DocumentFields.ID])
            if doc:
                amounts_diff = item[ClientMessageFields.AMOUNT] - doc[DocumentFields.AMOUNT]    # desirable - available
                if amounts_diff > 0:
                    item[ClientMessageFields.AMOUNT] = doc[DocumentFields.AMOUNT]
                available_items.append(item)
        return available_items
    
    def update_items_amount(items):
        for item in items:
            doc = fc.read(COL, item[DocumentFields.ID])
            if not doc:
                continue
            new_amount = doc[DocumentFields.AMOUNT] - item[ClientMessageFields.AMOUNT]
            if new_amount > 0:
                to_update = {DocumentFields.AMOUNT : item[ClientMessageFields.AMOUNT]}
                fc.update(COL, item[DocumentFields.ID], {DocumentFields.AMOUNT : new_amount})
            else:
                fc.deleteDocument(COL, item[DocumentFields.ID])
