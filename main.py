from replit import db
import discord
import os
import datetime
import src

client = discord.Client()
log = logger.Logger()

command_map = {
  'info'  : msghandler.handle_info,
  'r'     : msghandler.handle_roll,
  'roll'  : msghandler.handle_roll,
  'become': msghandler.handle_become,
  'iam'   : msghandler.handle_become,
  'tellme': msghandler.handle_tellme,
  'dmg'   : msghandler.handle_damage,
  'damage': msghandler.handle_damage,
  'heal'  : msghandler.handle_heal,
  'clear' : msghandler.handle_clear,
  'keys'  : msghandler.handle_keys
}

#TODO: Add log on disconnect
@client.event
async def on_disconnect():
  log.write('disconnect at {}\n'.format(datetime.datetime.now()))

@client.event
async def on_ready():
  pr('Bot active as user {0.user}'.format(client))
  pr('The following keys are saved:')
  for k in db.keys():
    pr('-' + k)

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = None
  if len(message.attachments) > 0:
    msg = msghandler.handle_attachments(message)
  #Doesn't handle commands on messages with attachments
  elif message.content.startswith('$'):
    msg = command_map.get(message.content.lower().split()[0][1:])(message)

  if msg != None:
    prm(msg)
    await message.channel.send(msg)

#helper method to make logging easier
def pr(*args):
  for a in args:
    print(a)
    log.write(a)
def prm(*args):
  for a in args:
    print(a)
    log.message(a)

client.run(os.getenv('RNGSUS_TOKEN'))