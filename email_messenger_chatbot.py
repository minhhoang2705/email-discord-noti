import imaplib
import email
import facebook


def receive_emails():
    # Connect to the email account using IMAP protocol
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("hoangminhtr003@gmail.com", "yhuhuhdcdexeymah")
    mail.select("inbox")

    # Fetch and parse new emails
    result, data = mail.search(None, "ALL")
    ids = data[0].split()
    for i in range(len(ids)):
        result, data = mail.fetch(ids[i], "(RFC822)")
        raw_email = data[0][1].decode("utf-8")
        email_message = email.message_from_string(raw_email)

        # Extract the relevant information from the email
        subject = email_message["subject"]
        if email_message.get_payload() is not None:
            body = email_message.get_payload(decode=True)
        else:
            body = "No content"

        # Send the information to Messenger
        if body is not None:
            send_to_messenger(subject, body)
        else:
            send_to_messenger(subject, "No content")


def send_to_messenger(subject, body):
    # Connect to the Facebook Messenger platform using Facebook SDK for Python

    access_token = "EAARxwKTEyHMBAAybuXEGJnZBWZAwb8SZAMcdls3y5CdzDaKtErSZC32L7JPyW8oZBFdETDiRxwnHGzb1bbSNSfeUNs6oAbTMaNTVCZBpDMBaZBgB4f4mAWZCbZC3WZB33GCb0wpY0drjDocRr6FSlhvuAIsO5tvsI6yOmvXqRueS0reZARl7dKGjQ3Nux1iXeQDKsTbSObZCZAFNbuwZDZD"
    graph = facebook.GraphAPI(
        access_token=access_token)

    #Cannot send to Messenger
    # Send the message to Messenger
    graph.put_object("me", message=subject + "\n" +
                     body, connection_name="message")


if __name__ == "__main__":
    receive_emails()
