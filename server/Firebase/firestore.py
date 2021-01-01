from Firebase.init_firebase import *


class DocumentAlreadyExistsError(Exception):
    pass
class DocumentNotFoundError(Exception):
    pass
class FieldsDoesNotExist(Exception):
    pass


class FirestoreClient:
    def __doc_ref(col, doc):
        return db.collection(col).document(doc)

    def __doc_exists(col, doc):
        document = FirestoreClient.__doc_ref(col, doc).get()
        return document.exists

    def __fields_exist(col, doc, fields):
        doc_ref = FirestoreClient.__doc_ref(col, doc)
        fields_doc = doc_ref.get(fields).to_dict()
        return len(fields_doc) == len(fields)


    def create(col, doc, data):
        if FirestoreClient.__doc_exists(col, doc):
            raise DocumentAlreadyExistsError
        doc_ref = FirestoreClient.__doc_ref(col, doc)
        return doc_ref.set(data)
    
    def read(col, doc):
        if not FirestoreClient.__doc_exists(col, doc):
            raise DocumentNotFoundError
        doc_ref = FirestoreClient.__doc_ref(col, doc)
        return doc_ref.get().to_dict()
    
    def readAll(col):
        docs = db.collection(col).stream()
        return [doc.to_dict() for doc in docs]

    def update(col, doc, data):
        if not FirestoreClient.__doc_exists(col, doc):
            raise DocumentNotFoundError
        doc_ref = FirestoreClient.__doc_ref(col, doc)
        return doc_ref.update(data)

    def deleteDocument(col, doc):
        if not FirestoreClient.__doc_exists(col, doc):
            raise DocumentNotFoundError
        doc_ref = FirestoreClient.__doc_ref(col, doc)
        return doc_ref.delete()

    def deleteFields(col, doc, fields):
        if not FirestoreClient.__doc_exists(col, doc):
            raise DocumentNotFoundError
        if not FirestoreClient.__fields_exist(col, doc, fields):
            raise FieldsDoesNotExist
        fields_dict = {field : firestore.DELETE_FIELD for field in fields}
        return FirestoreClient.update(col, doc, fields_dict)
