import firebase_admin
from firebase_admin import firestore
import json

#initialize connection, auth
def initialize_connection():
    path_to_cert = input("input path to firebase cert file:")
    cred_obj = firebase_admin.credentials.Certificate(path_to_cert)
    firebase_admin.initialize_app(cred_obj)
    db = firestore.client()
    return db.collection(u'Databases/Dev_Database/Conversations').list_documents()

# descend into the tree of document -> collection -> document and pull out salient text
if __name__ == '__main__':
    s = set()
    for convo_doc in initialize_connection():
        all_messages = convo_doc.collection("Messages").list_documents()
        if len(s) > 1000:
            break
        for message_doc in all_messages:
            s.add(message_doc.get().to_dict()["Text"])
            if len(s) > 1000:
                break
    with open('floop_data.json', 'w') as f:
        json.dump(s, f)

