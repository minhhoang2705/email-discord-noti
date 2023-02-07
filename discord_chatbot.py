import imaplib
import email
import facebook


def receive_emails():
    # Connect to the email account using IMAP protocol
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("minhthse171070@fpt.edu.vn", "nvftimojjegsjzxn")
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
            # send_to_messenger(subject, body)
            print(body)
        else:
            print(body)


def send_to_messenger(subject, body):
    # Connect to the Facebook Messenger platform using Facebook SDK for Python
    page_access_token = 'EAARxwKTEyHMBAIXNFwVAQ0hew2ggNlv6zoSZBcTtA1CCURDWtJ67lIIrPZBPEVYWSZBg0SZAU8TSiZBddrKOXPiqYmjV7zn7ROWrJvu7Nx4FbcosZA2MrIFLuQ3vhtQxYcrSUZCFIORCJA4CZB5LKS1vj0D10AlZB4A5tj2Dtfi3ZCQ0Qx2n4LV1XbCKz7o2gliSoCwtZBvU0ZAGugZDZD'
    graph = facebook.GraphAPI(access_token=page_access_token)

    # Send the message to Messenger
    graph.put_object(parent_object='me', message=subject + "\n" + body,
                     connection_name="conversations", recipient="744737250350905")


if __name__ == "__main__":
    receive_emails()


# Create Discord bot

import discord
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):

    if (message.content is not None):
        print(message.content)
    elif message.content == '':
        print("Have blank content")
    else:
        print("No content")

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello! How may I help you today?')

    if message.content.startswith('!help'):
        await message.channel.send("I am a chatbot designed to assist you. Here are some of the commands I understand:\n\n"
                                   "!hello - say hello\n"
                                   "!help - display this help message\n"
                                   "!info - display information about the chatbot\n")

    if message.content.startswith('!info'):
        await message.channel.send("I am a chatbot built with Python and the discord.py library. My creators did a great job!")


client.run(
    'MTA3MjAzMDg5OTc5OTA3NjkzNA.GzqJdZ.mLRwrS7TpU-SYw-qMMQ3_Q_Rt2bBslQJ3s67xI')
