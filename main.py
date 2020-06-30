import discord, datetime, time, random, sys, praw, requests, encode
client = discord.Client()
prefixes = []
guilds = []
banned = []
reddit_details = []
f = open("Special_info/reddit", "r")
for i in f:
    reddit_details.append(i[:-1])
    print("("+i[:-1]+")")
f.close()

f = open("Special_info/banned", "r")
for i in f:
    banned.append(int(i))
f.close()

f = open("Special_info/prefixes")
for line in f:
    guilds.append(int(line[0:line.index("\u2839")]))
    prefixes.append(line[line.index("\u2839")+1:len(line)-1])
f.close()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    game = discord.Game("SenecaLearning")
    await client.change_presence(activity=game)
    for guild in client.guilds:
        me = guild.me
        if guild.id in guilds:
            await me.edit(nick="("+prefixes[guilds.index(guild.id)]+") LokkenBot")
        else:
            await me.edit(nick="(^) LokkenBot")
            guilds.append(guild.id)
            prefixes.append("^")
            with open("Special_info/prefixes", "a") as file:
                file.write(str(guild.id)+"\u2839^\n")
                file.close()
    temp = [i.id for i in client.guilds]
    for i in guilds:
        if not i in temp:
            print(i, temp)
            f = open("Special_info/prefixes", "r")
            output = ""
            for j in f:
                k = j[:]
                if int(k[:k.index("\u2839")]) == i:
                    k = ""
                output += ""
            f.close()
            f = open("Special_info/prefixes", "w+")
            f.write(output)
            f.close()
            prefixes.remove(prefixes[guilds.index(i)])
            guilds.remove(i)

@client.event
async def on_guild_join(guild):
    guilds.append(guild.id)
    prefixes.append("^")
    guild.me.edit(nick="(^) LokkenBot")
    with open("Special_info/prefixes", "a") as file:
        file.write(str(guild.id)+"\u2839^\n")
        file.close()

@client.event
async def on_message(message):
    lars = client.get_user(360493765154045952)
    if message.author == client.user:
        return
    if message.guild:
        prefix = prefixes[guilds.index(message.guild.id)]
    else:
        prefix=""

    if message.content.lower() =="lokkenbot is bad":
        await message.channel.send("I agree")

    elif message.content.lower() =="who is the best bot?":
        if message.guild:
            bots = []
            for i in message.guild.members:
                if i.bot and i != client.user:
                    bots.append(i)
            if len(bots)==0:
                await message.channel.send("I'm the only bot...")
            else:
                await message.channel.send("The best bot is... ||{0}||".format(random.choice(bots).display_name))
        else:
            await message.channel.send("This is a dm... its just you and me...")

    #Commands    
    elif message.content.lower().startswith(prefix):
        message.content = message.content[len(prefix):]
        if message.content[0] == " ":
            message.content = message.content[1:]
        if message.content.lower().startswith("help"):
            helptext = open("helptext.txt", "r")
            await message.channel.send(helptext.read())
            helptext.close()
            if message.author == lars:
                await lars.send("print\nban\nunban\nbanned\nsend\nexit")

        elif message.content.lower().startswith("ping"):
            await message.channel.send(str(int(str(datetime.datetime.utcnow()-message.created_at)[8:11]))+"ms")

        elif message.content.lower().startswith("pi"):
            while " " in message.content:
                message.content = message.content[0:message.content.index(" ")]+message.content[message.content.index(" ")+1:]
            if message.content[2:].isdigit():
                if int(message.content[2:len(message.content)]) <=1000 and  int(message.content[2:len(message.content)]) > 0:
                    file = open("Special_info\pi", "r")
                    await message.channel.send("3."+file.read()[0:int(message.content[2:len(message.content)])])
                    file.close()
                else:
                    await message.channel.send("Enter a number between 1 and 1000")
            else:
                await message.channel.send("Sorry, your message was encoded wrong")

        elif message.content.lower().startswith("prefix"):
            if message.guild:
                if message.author == message.guild.owner:
                    if len(message.content) != 6:
                        message.content = message.content[6:]
                        while message.content[0] == " ":
                            message.content = message.content[1:]
                        prefixes[guilds.index(message.guild.id)], me = message.content, message.guild.me
                        await me.edit(nick="("+message.content+") LokkenBot")
                        f = open("Special_info/prefixes", "r")
                        temp = ""
                        for line in f:
                            if message.guild.id == int(line[:line.index("\u2839")]):
                                line = str(message.guild.id)+"\u2839"+message.content+"\n"
                            temp += (line)
                        f.close()
                        f = open("Special_info/prefixes", "w+")
                        f.write(temp)
                        f.close()
                        await message.channel.send("The prefix is now: "+message.content)
                    else:
                        await message.channel.send("You need to specify a prefix")
                else:
                    await message.channel.send("This command is only avaliable to the server owner")
            else:
                await message.channel.send("This command can only be used in a server. No prefix is required in DMs")

        elif message.content.lower().startswith("quote"):
            if message.guild:
                message.content = message.content[6:]
                possible_messages = []
                async for i in message.channel.history():
                    if i.author.display_name.lower() == message.content:
                        possible_messages.append(i)
                if len(possible_messages) == 0:
                    await message.channel.send("Sorry, no messages from that user were found.\nCheck if you spelled their nickname correctly")
                else:
                    await message.channel.send("QUOTE\n> {0.content}\n~ {0.author.display_name} {1}".format(random.choice(possible_messages),str(message.created_at)[:-7]))
            else:
                await message.author.send("This command must be used in a server")

        elif message.content.lower().startswith("password"):
            message.content = message.content[8+int(message.content[8]==" "):]
            if message.content.isdigit():
                message.content = int(message.content)
                if message.content >0 and message.content <= 30:
                    password = ""
                    for i in range(message.content):
                        password += chr(random.randint(33,126))
                    await message.author.send("Your password is:")
                    await message.author.send(password)
                else:
                    await message.author.send("Enter a number between 1 and 30")
            else:
                await message.author.send("Please enter a number")

        elif message.content.lower().startswith("delete"):
            quote=False
            if message.content.lower()[7:] == "quote":
                quote = True
            messages = await message.channel.history().flatten()
            for i in messages:
                if i.author==client.user and (i.content.startswith("QUOTE"))==quote:
                    await i.delete()

        elif message.content.lower().startswith("suggest "):
            if not message.author.id in banned:
                message.content = message.content[8:]
                if len(message.content)!=0:
                    if message.guild:
                        name,server = message.author.display_name,str(message.guild)
                    else:
                        name,server = str(message.author),"DMs"
                    await lars.send("{0.author.id}:\n{1} from {2} has suggested {0.content}".format(message,name,server))
                    await lars.send(message.author.id)
            else:
                await message.author.send("You are banned from using the suggest function. Stop trying")

        elif message.content.startswith("banned") and message.author == lars:
            if message.guild:
                await message.channel.send("Command not found")
                await lars.send("Here Silly")
            else:
                if len(banned)==0:
                    await lars.send("No banned users")
                else:
                    for i in banned:
                        await lars.send(str(i))

        elif message.content.lower().startswith("ban ") and message.author == lars:
            if not message.guild:
                if message.content[4:].isdigit():
                    banned.append(int(message.content[4:]))
                    f = open("Special_info/banned", "a")
                    f.write(message.content[4:]+"\n")
                    f.close()
                    await client.get_user(int(message.content[4:])).send("You have been banned from suggesting to LokkenBot")
                    for i in await message.channel.history().flatten:
                        if i.author == client.user and i.content.startswith(str(message.content[4:])):
                            await i.delete()

            else:
                await message.channel.send("Command not found")
                await lars.send("DMs!")

        elif message.content.lower().startswith("unban ") and message.author == lars:
            if not message.guild:
                if message.content[6:].isdigit():
                    if int(message.content[6:]) in banned:
                        banned.remove(int(message.content[6:]))
                        f = open("Special_info/banned", "r")
                        temp = ""
                        for i in f:
                            j = i[:]
                            if (j)[:-1] == message.content[6:]:
                                j = ""
                            temp += j
                        f.close()
                        f = open("Special_info/banned","w+")
                        f.write(temp)
                        f.close()
                        await client.get_user(int(message.content[6:])).send("You are no longer banned from suggesting to LokkenBot")
                    else:
                        await message.author.write("User not banned")
            else:
                await message.channel.send("Command not found")
                await message.author.send("Here silly")

        elif message.content.lower().startswith("info"):
            await message.channel.send("LokkenBot - made by lokken349#9823\nrunning on discord.py version: {0}\npython version: {1}\ncurrently in {2} different servers".format(discord.__version__, sys.version[:sys.version.index(" ")], len(client.guilds)))

        elif message.content.lower().startswith("mathsmeme"):
            reddit = praw.Reddit(client_id=reddit_details[2],client_secret=reddit_details[3],password=reddit_details[1],username=reddit_details[0],user_agent="PrawTut")
            subreddit = reddit.subreddit("mathmemes")
            memes = list(subreddit.new(limit=10))
            for submission in memes:
                if submission.stickied or submission.is_self or submission.over_18:
                    memes.remove(submission)
            submission = random.choice(memes)
            image = requests.get(submission.url)
            with open("meme.jpg", "wb") as file:
                file.write(image.content)
                image = ""

            meme = discord.File("meme.jpg")
            await message.channel.send((submission.title), file=meme)
            f=open("meme.jpg", "w+")
            f.write('')
            f.close()
        
        elif message.content.lower().startswith("print ")and message.author == lars:
            print(message.content[6:])
        
        elif message.content.lower().startswith("test"):
            await message.author.send("Please join the test server at:\nhttps://discord.gg/pkdNm2C")

        elif message.content.lower().startswith("encode"):
            encoded = encode.encode(message.content[7:])
            i,j = 0,0
            while encoded[i] == " ":
                i += 1
            while encoded[len(encoded)-1-j] == " ":
                j += 1
            if i != 0 or j != 0:
                await message.author.send("{0} space(s) at the start and {1} at the end!".format(i,j))
            await message.author.send(encoded)

        elif message.content.lower().startswith("send ") and message.author == lars:
            message.content = message.content [5:]
            if message.content.lower()[:3] == "dm ":
                message.content = message.content[3:]
                if message.content[:message.content.index(" ")].isdigit():
                    await client.get_user(int(message.content[:message.content.index(" ")])).send(message.content[message.content.index(" "):])
            elif message.content.lower()[:6]=="guild ":
                message.content = message.content[6:]
                if message.content[:message.content.index(" ")].isdigit():
                    guild = int(message.content[:message.content.index(" ")])
                    message.content = message.content[message.content.index(" ")+1:]
                    if message.content[:message.content.index(" ")].isdigit():
                        channel = int(message.content[:message.content.index(" ")])
                        await client.get_guild(guild).get_channel(channel).send(message.content[message.content.index(" "):])


        elif message.content.lower().startswith("exit") and message.author == lars:
            sys.exit()
        
        else:
            await message.channel.send("command not found")
f=open("Special_info/token","r")
token = f.read()
f.close()
client.run(token)
