import sys
import firebase_admin
import re
import boto3
import json
from datetime import datetime
from firebase_admin import firestore
from os.path import exists

BATCH_LIMIT = 10


def get_credentials():
    cert_path = input('enter path to cert file: ')
    while not exists(cert_path):
        cert_path = input(
            'invalid file path. Please enter path to Floop cert file: ')
    return cert_path


def connect_s3():
    key_id = sys.argv[2] if len(sys.argv) > 2 else input(
        "Enter your AWS access key id: ")
    '''
    we know what a secret access key ID should look like but not what
    the key itself should look like.
    https://docs.aws.amazon.com/STS/latest/APIReference/API_Credentials.html
    '''

    while not re.match("\w{16,128}", key_id):
        print("Key in incorrect format, please try again")
        key_id = input("re-enter your key: ")
    secret_key = sys.argv[3] if len(sys.argv) > 3 else input(
        "enter your AWS secret access key: ")
    return boto3.Session(
        aws_access_key_id=key_id, aws_secret_access_key=secret_key)


def upload_s3(json):
    s3_session = connect_s3().resource('s3')
    time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    # add file to bucket with current date and time for posterity
    s3_session_object = s3_session.Object(
        'floop-dataset', 'floopData' + time + '.json')
    result = s3_session_object.put(Body=json)
    extracted_status_code = result["ResponseMetadata"]["HTTPStatusCode"]
    if int(extracted_status_code) >= 400:
        print("Something went wrong. Please make sure that you are using an active key,"
              " and that the bucket 'floop-dataset' exists in your VPC" + str(extracted_status_code))
    else:
        print("Success! Result of put operation was HTTP Status Code " + str(extracted_status_code))


def initalize_connection(cert_path, doc_count=BATCH_LIMIT):
    cred_obj = firebase_admin.credentials.Certificate(cert_path)
    # initialize default app for firebase
    firebase_admin.initialize_app(cred_obj)
    db = firestore.client()

    limit = BATCH_LIMIT if doc_count > BATCH_LIMIT else doc_count
    # exclude certain types of comment, on Floop's suggestion
    return db\
        .collection(u'Databases/Dev_Database/Conversations')\
        .where('Comment_Preview',
               'not-in',
               ['What is your goal for this year?',
                'Audio Comment',
                'Freeform',
                'Freeform Comment',
                '', ' '])\
        .limit(limit)


def get_conversations(query, limit, conversations=[], dupe_list=[], count=0):
    # descend into the tree of document -> collection -> document and
    # pull out salient text
    current_conversations = conversations
    conversation_count = count
    current_dupe_list = dupe_list
    query_results = query.get()
    for convo_doc in query_results:
        if conversation_count == limit:
            break

        convo_data = convo_doc.to_dict()
        student_id = convo_data['Submission_Owner']

        all_messages = convo_doc.reference.collection('Messages')\
            .order_by(u'Date_Submitted').get()
        if not all_messages:
            continue

        top_doc = all_messages[0]
        top_doc_text = top_doc._data["Text"]

        # ignore this conversation if top message is not unique
        if top_doc_text in current_dupe_list:
            continue

        conversation = []

        current_dupe_list.append(top_doc_text)
        for message_doc in all_messages:
            message_data = message_doc.to_dict()
            sender_is_student = student_id == message_data["Sender_ID"]
            sender_type = "Student" if sender_is_student else "Teacher"
            conversation.append({
                "Text": message_data["Text"],
                "Sender_Type": sender_type
                })
        current_conversations.append(conversation)
        conversation_count += 1
    if conversation_count < limit:
        last_doc = query_results[len(query_results) - 1]
        return get_conversations(
            query.start_after(last_doc),
            limit,
            current_conversations,
            current_dupe_list,
            conversation_count
        )
    return current_conversations


if __name__ == '__main__':
    cert_path = sys.argv[1] if len(sys.argv) > 1 else get_credentials()
    doc_limit = 100
    query = initalize_connection(cert_path, doc_limit)
    data = get_conversations(query, doc_limit)
    print('total convos', len(data))

    # upload_s3(json.dumps(conversations))
    with open('floop_data.json', 'w') as f:
        json.dump(data, f)
