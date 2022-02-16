import sys
import firebase_admin
import re
import boto3
import json
from datetime import datetime
from firebase_admin import firestore
from os.path import exists


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


def initalize_connection(cert_path):
    cred_obj = firebase_admin.credentials.Certificate(cert_path)
    # initialize default app for firebase
    firebase_admin.initialize_app(cred_obj)
    db = firestore.client()
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
        .limit(10).stream()


def get_data():
    # descend into the tree of document -> collection -> document and
    # pull out salient text
    conversations = []
    conversation_count = 0
    dupe_list = []
    cert_path = sys.argv[1] if len(sys.argv) > 1 else get_credentials()
    conversation_documents = initalize_connection(cert_path)
    for convo_doc in conversation_documents:
        convo_data = convo_doc.to_dict()
        student_id = convo_data['Submission_Owner']

        all_messages = convo_doc.reference.collection('Messages')\
            .order_by(u'Date_Submitted').get()
        if not all_messages:
            continue

        top_doc = all_messages[0]
        top_doc_text = top_doc._data["Text"]

        # ignore this conversation if top message is not unique
        if top_doc_text in dupe_list:
            continue

        conversation = []

        dupe_list.append(top_doc_text)
        for message_doc in all_messages:
            message_data = message_doc.to_dict()
            sender_is_student = student_id == message_data["Sender_ID"]
            sender_type = "Student" if sender_is_student else "Teacher"
            conversation.append({
                "Text": message_data["Text"],
                "Sender_Type": sender_type
                })
        conversations.append(conversation)
        conversation_count += 1
    return conversations


if __name__ == '__main__':
    data = get_data()

    # upload_s3(json.dumps(conversations))
    with open('floop_data.json', 'w') as f:
        json.dump(data, f)
