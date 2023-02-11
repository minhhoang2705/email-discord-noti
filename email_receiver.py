import os
import imaplib
import email
import json
import chardet


EMAIL = '' 
PASSWORD = ''
SERVER = 'imap.gmail.com'
MODE = 'UNSEEN'
REVERSED = True 
GMAIL_FOLDERS = 'INBOX'

def detect_and_decode(text, default_encoding='utf-8'):
    encoding = None
    if isinstance(text, str):
        text = text.encode()
        encoding = default_encoding
    else:
        encoding = chardet.detect(text)['encoding']
    if encoding is None: encoding = default_encoding
    return text.decode(encoding, 'ignore')

def get_email_info(email_id, save_directory='.'):
    result, data = mail.fetch(email_id, "(RFC822)")
    email_message = email.message_from_bytes(data[0][1])
    email_info = {
        'from': detect_and_decode(email_message['From']),
        'subject': detect_and_decode(email_message['Subject'].encode()),
        'content': '',
        'attachments': []
    }
    
    if email_message.is_multipart():
        for part in email_message.get_payload():
            if part.get_content_type() == 'text/plain':
                email_info['content'] += detect_and_decode(part.get_payload(decode=True))
    else:
        email_info['content'] = detect_and_decode(email_message.get_payload())

    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart': continue
        if part.get('Content-Disposition') is None: continue
        file_name = part.get_filename()
        if bool(file_name):
            email_info['attachments'].append(detect_and_decode(file_name.encode()))
            download_attachment(mail, part, os.path.join(save_directory, file_name))
    print(email_info)
    return email_info


def download_attachment(mail, part, save_path):
    content = part.get_payload(decode=True)
    with open(save_path, 'wb') as f:
        f.write(content)


mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")
result, data = mail.search(None, "ALL")
email_ids = data[0].split()

if REVERSED: email_ids = email_ids[::-1]

email_info_list = []
for email_id in email_ids:
    email_info = get_email_info(email_id)
    email_info_list.append(email_info)
    break

with open('email_info.json', 'w') as outfile:
    json.dump(email_info_list, outfile)