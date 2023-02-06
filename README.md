# NovaNotifier-2
New Version Of NovaNotifier 
  
[NovaRO Forum](https://www.novaragnarok.com/forum/topic/11837-nova-market-notifier) 

## Build Instructions
    1. Create your MongoDB Database. (Name: nova / Collections: Items, Users)  
        1.1 Items: Items icons.
        1.2 Users: User information.  
    1. Add your MongoDB SRV to Files/Database.env (E.g: mongo_token = mongodb+srv://...)
    1. Run main.exe
  
## MongoDB User Fields  
    channel[int]: Discord Channel.  
    discord[str]: Discord Name.  
    token[str]: Auth Token.  
    cookie_key[BinData]: Key for decrypt cookies.  
    date[Date]: Last time using NovaNotifier. 
    price_alert[Array]: items found that bot need to notify.  
    price_alert[Array]: items sold that bot need to notify. 
    price_flag[Bool]: Mark if there is price items to notify.
    sold_flag[Bool]: Mark if there is sold items to notify.
    search[Array]: Items you are searching.
    table[Array]: !search command. 
    
 ## Discord Bot
  Create your own, for reference my **!start** code:

  ```python  
  async def on_message(message):
    if message.content.lower() == '!start':
      channel = message.author.id
      message_channel = client.get_user(channel)
      discord = f"{message.author.display_name}#{message.author.discriminator}"
      token = token_hex(3)
      while db.nova.users.find_one({'token': token}):
        token = token_hex(3)
      await message_channel.send(f"Token: {token}")
      db.nova.users.replace_one({'channel': channel}, {
        'channel': channel,
        'discord': discord,
        'token': token,
        'cookie_key': Fernet.generate_key(),
        'date': datetime.utcnow(),
        'price_alert': [],
        'sold_alert': [],
        'table': [],
        'price_flag': False,
        'sold_flag': False,
        'search': {},
        'accounts': False
        }, upsert=True)
  ```  
    
  
