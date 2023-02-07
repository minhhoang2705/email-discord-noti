import discord
intents = discord.Intents.default()
intents.members = True


class DiscordChatbot:
    def __init__(self, token):
        self.client = discord.Client(intents=intents)
        self.token = token

    async def on_ready(self):
        print(f'Logged in as {self.client.user}')

        """
        The function is called when a message is sent in the Discord server. If the message starts with
        a certain string, the bot will respond with a certain message.
        
        :param message: The message object that triggered the event
        :return: The bot is returning the message that the user typed in.
        """
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello! How may I help you today?')

        if message.content.startswith("!help"):
            await message.channel.send("I am a chatbot designed to assist you. Here are some of the commands I understand:\n\n"
                                       "!hello - say hello\n"
                                       "!help - display this help message\n"
                                       "!info - display information about the chatbot\n")

        if message.content.startswith('!info'):
            await message.channel.send("I am a chatbot built with Python and the discord.py library. My creators did a great job!")

    def start(self):
        @self.client.event
        async def on_ready():
            await self.on_ready()

        @self.client.event
        async def on_message(message):
            await self.on_message(message)

        self.client.run(self.token)
