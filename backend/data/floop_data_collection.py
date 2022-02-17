import firebase_admin
import re
import boto3
import json
import argparse
import scrubadub

from datetime import datetime
from firebase_admin import firestore
from os.path import exists

BATCH_LIMIT = 500
DEFAULT_DOC_LIMIT = 1000

scrubber = scrubadub.Scrubber()
scrubber.add_detector(scrubadub.detectors.DateOfBirthDetector)


def get_credentials():
    cert_path = input('enter path to cert file: ')
    while not exists(cert_path):
        cert_path = input(
            'invalid file path. Please enter path to Floop cert file: ')
    return cert_path


def connect_s3(key, secret):
    key_id = key if key else input("Enter your AWS access key id: ")
    '''
    we know what a secret access key ID should look like but not what
    the key itself should look like.
    https://docs.aws.amazon.com/STS/latest/APIReference/API_Credentials.html
    '''

    while not re.match("\\w{16,128}", key_id):
        print("Key in incorrect format, please try again")
        key_id = input("re-enter your key: ")
    secret_key = secret if secret else input(
        "enter your AWS secret access key: ")
    return boto3.Session(
        aws_access_key_id=key_id, aws_secret_access_key=secret_key)


def upload_s3(json, key, secret):
    s3_session = connect_s3(key, secret).resource('s3')
    time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    # add file to bucket with current date and time for posterity
    s3_session_object = s3_session.Object(
        'floop-dataset', 'floopData' + time + '.json')
    result = s3_session_object.put(Body=json)
    extracted_status_code = result["ResponseMetadata"]["HTTPStatusCode"]
    if int(extracted_status_code) >= 400:
        print(
            "Something went wrong. Please make sure that you are using an \
                active key,"
            " and that the bucket 'floop-dataset' exists in your VPC" +
            str(extracted_status_code))
    else:
        print(
            "Success! Result of put operation was HTTP Status Code " +
            str(extracted_status_code))


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
        top_doc_text = convo_data["Comment_Preview"].strip()

        # ignore this conversation if top message is not unique
        if top_doc_text in current_dupe_list:
            continue

        current_dupe_list.append(top_doc_text)
        all_messages = convo_doc.reference.collection('Messages')\
            .order_by(u'Date_Submitted').get()
        if not all_messages:
            continue

        conversation = []

        for message_doc in all_messages:
            message_data = message_doc.to_dict()
            sender_is_student = student_id == message_data["Sender_ID"]
            sender_type = "Student" if sender_is_student else "Teacher"
            conversation.append({
                "Text": scrubber.clean(message_data["Text"]),
                "Sender_Type": sender_type
            })
        current_conversations.append(conversation)
        conversation_count += 1
        print('{0}/{1} conversations processed'
              .format(conversation_count, limit), end='\r')

    if conversation_count < limit:
        last_doc = query_results[-1]
        return get_conversations(
            query.start_after(last_doc),
            limit,
            current_conversations,
            current_dupe_list,
            conversation_count
        )
    print()
    return current_conversations


def get_script_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='path to floop cert file')
    parser.add_argument('--limit', '-l', type=int,
                        help='number of conversation docs to query')
    parser.add_argument('--key', '-k', type=str, help='AWS access key')
    parser.add_argument('--secret', '-s', type=str, help='AWS secret key')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_script_args()

    cert_path = args.path if args.path else get_credentials()
    doc_limit = args.limit if args.limit else DEFAULT_DOC_LIMIT
    query = initalize_connection(cert_path, doc_limit)

    data = get_conversations(query, doc_limit)
    upload_s3(json.dumps(data), args.key, args.secret)

    print('Done')
