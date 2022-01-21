import firebase_admin
from firebase_admin import firestore
import json
from os.path import exists

def get_credentials():
    cert_path = input('enter path to cert file: ')
    while not exists(cert_path):
        cert_path = input('invalid file path. Please enter path to Floop cert file: ')
    return cert_path

def initalize_connection(cert_path):
    cred_obj = firebase_admin.credentials.Certificate(cert_path)
    # initialize default app for firebase
    firebase_admin.initialize_app(cred_obj)
    db = firestore.client()
    # exclude certain types of comment, on Floop's suggestion
    return db.collection(u'Databases/Dev_Database/Conversations').where('Comment_Preview', 'not-in', [
        'What is your goal for this year?', 'Audio Comment', 'Freeform', 'Freeform Comment', '', ' ']).limit(
        1000).stream()

# descend into the tree of document -> collection -> document and pull out salient text
if __name__ == '__main__':
    arr = []
    cert_path = get_credentials()
    conversation_documents = initalize_connection(cert_path)
    for convo_doc in conversation_documents:
        all_messages = convo_doc.reference.collection('Messages').order_by(u'Date_Submitted').limit(1).get()
        message_doc = all_messages[0]
        arr.append(message_doc._data["Text"])
        # leaving this print statement in because the operation is so long running, it's helpful to
        # prove that the script isn't stuck
        print(arr)
    with open('floop_data.json', 'w') as f:
        json.dump(list(set(arr)), f)
