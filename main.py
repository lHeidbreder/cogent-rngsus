import discord
import os
import datetime
#import src
from src import logger
from src import msghandler
from src import charownership
from src import db as saved_dictionary

client = discord.Client()
log = logger.Logger()
db = saved_dictionary.Saved_Dict.load_db()
VERSION = "20210322.2116"
msghandler.VERSION = VERSION
msghandler.db = db  
charownership.db = db
charownership.load_chars()

command_map = {
  'info'  : msghandler.handle_info,
  'r'     : msghandler.handle_roll,
  'roll'  : msghandler.handle_roll,
  'p'     : msghandler.handle_probability,
  'prob'  : msghandler.handle_probability,
  'become': msghandler.handle_become,
  'iam'   : msghandler.handle_become,
  'tellme': msghandler.handle_tellme,
  'dmg'   : msghandler.handle_damage,
  'damage': msghandler.handle_damage,
  'heal'  : msghandler.handle_heal,
  'save'  : msghandler.handle_save,
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
  if len(db.keys()) > 0:
    pr('The following keys are saved:')
    for k in db.keys():
      pr('-' + k)
  else:
    pr('No keys are currently saved')

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

def get_token():
  TOKEN = ""
  TOKEN = os.getenv('RNGSUS_TOKEN')
  if TOKEN in ("",None):
    print("RNGSUS_TOKEN was not set in the environment")
    TOKEN = input("Enter your token: ")
  return TOKEN

try:
	client.run(get_token())
except Exception:
	print('Couldn\'t establish connection; is variable RNGSUS_TOKEN valid?')