import discord
import main

channel = main.disClient.get_channel(int(main.testCh))
channel.send('Hello World')