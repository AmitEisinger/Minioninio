# NOTE: This file has to be in the same path as main.py
from Firebase.firestore import *
from Firebase.firestore import FirestoreClient as fc


col = 'col'
doc = 'doc'
data = {
    'name' : 'TADAM',
    'age' : 42
}
update_data = {
    'name' : 'TARIM'
}
fields = ['age']

doc1 = 'doc1'
data1 = {
    'name' : 'TODO',
    'age' : 21
}
doc2 = 'doc2'
data2 = {
    'name' : 'TODO BOM',
    'age' : 100
}


def check_all():
    try:
        # create doc in col
        fc.create(col, doc, data)
        print(fc.read(col, doc) == data)
        # try to create same doc again
        try:
            fc.create(col, doc, data)
            print('fail 1')
        except DocumentAlreadyExistsError:
            pass

        # update doc
        fc.update(col, doc, update_data)
        print(fc.read(col, doc) == {'name' : 'TARIM', 'age' : 42})

        # delete an existing field in doc
        fc.deleteFields(col, doc, fields)
        print(fc.read(col, doc) == {'name' : 'TARIM'})
        # try to delete non-existing fields in doc
        try:
            fc.deleteFields(col, doc, fields+['a'])
            print('fail 2')
        except FieldsDoesNotExist:
            pass

        # delete doc        
        fc.deleteDocument(col, doc)
        # try to delete non-exisitng doc
        try:
            fc.deleteDocument(col, doc)
            print('fail 3')
        except DocumentNotFoundError:
            pass

        # try to read non-existing doc
        try:
            fc.read(col, doc)
            print('fail 4')
        except DocumentNotFoundError:
            pass

        # try to update non-existing doc
        try:
            fc.update(col, doc, update_data)
            print('fail 5')
        except DocumentNotFoundError:
            pass

        print('success! :)')
    except Exception as e:
        print(type(e))


def test_readAll():
    try:
        # create docs
        fc.create(col, doc, data)
        fc.create(col, doc1, data1)
        fc.create(col, doc2, data2)

        # read all the docs
        print(fc.readAll(col))

        # delete docs
        fc.deleteDocument(col, doc)
        fc.deleteDocument(col, doc1)
        fc.deleteDocument(col, doc2)
    except Exception as e:
        print(type(e))


if __name__ == "__main__":
    check_all()
    test_readAll()
