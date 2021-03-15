from replit import db
import os

import discord
import random
from rollrequest import RollRequest
import charownership as co
import requests

def handle_attachments(message):
  for a in message.attachments:
    if a.filename.lower().endswith('characters.csv'):
      designator = 'chars.csv'
      __save_file(a,designator)
      co.read_csv(designator)

def __save_file(attachment,designator):
  #TODO: restrict by file size
  req = requests.get(attachment.url)
  open(designator,'wb').write(req.content)


def handle_info(message):
  return (
  "Cogent Bot for Discord\nVersion:" + os.getenv('VERSION')
+ "\n" + "-"*10 + "\n"
+ "Rolling syntax as follows:\n"
+ '$roll / $r - Rolls a single d6\n'
+ '$roll x - Rolls x d6 and counts successes\n'
+ '$roll x+ - Rolls x d6 against a target of 3, counts successes\n'
+ '$roll x t - Rolls x d6 against a CL of t, counts Victory Levels\n'
+ '$roll x+ t - Same as above but counts 3s as well\n'
+ '$roll xd - Rolls x d6 and sums them up\n'
+ '$roll x~ - Rolls x d6 and gives the average\n\n'
+ '$become / $iam nickname - Allows you to change your nickname\n'
+ '$become myself - Removes your nickname\n\n'
+ '$tellme x - If you are associated with a character, you are told your bonus for stat x\n'
+ '$damage / $dmg x - Adds a wound of severity x to your character\n'
+ '$heal x - Removes a wound of severity x'
)

def save(self,message):
  for c in co.chars:
    db[c.get_stat('Name')] = c.me()

def handle_roll(message):
  request = RollRequest(message.content)
  rnd = request.process()
  return 'Roll as requested by {}:\n{}'.format(co.whois(message.author),rnd)

def handle_become(message):
  if len(message.content.split(' ',1)) > 1:
    arg = message.content.split(' ',1)[1]
    key = str(message.author)[:-5]+"_nick"
    if arg.lower() == "myself":
      del db[key]
      msg = "{} is theirself again.".format(str(message.author))
    else:
      db[key] = arg

      #check if arg is character name
      if (arg+'_char') in db.keys():
        append = '\nCharacter found; it\'s now controlled by you'
      else:
        append = '\nNo character found'

      msg = "{} is now {}.{}".format(str(message.author),(db[key]),append)
  else:
    msg = 'No nickname given. How should I call you from now, {}?'.format(co.whois(message.author))
  return msg

def handle_tellme(message):
  #safety first
  if len(message.content.split()) == 1:
    return 'What do you want to know, {}?'.format(co.whois(message.author))

  msg = ''
  key = message.content[message.content.index('me ')+3:]
  if (co.whois(message.author)) not in co.chars or not isinstance(co.chars[co.whois(message.author)],dict):
    msg = 'You don\'t own a character, {}'.format(co.whois(message.author))
  elif co.whois(message.author) != str(message.author):
    val = co.chars[co.whois(message.author)].get_stat(key)
    try:
      int(val)
      prefix = ''
      if val >= 0:
        prefix = '+'
      msg = '{}\'s {} gets {}{} dice'.format(co.whois(message.author),key,prefix,val)
    except:
      msg = '{}\'s {}: {}'.format(co.whois(message.author),key,val)
  else:
    msg = 'You don\'t have an alterego, {}'.format(co.whois(message.author))
  
  return msg

def handle_damage(message):
  try:
    severity = int(message.content.split()[1])-1
    co.chars[co.whois(message.author)].get_stat("Wounds")[severity] += 1
    return 'Wound of Level {} added. {} in total'.format(severity+1,co.chars[co.whois(message.author)].get_stat("Wounds")[severity])
  except:
    return 'Needs a number'

def handle_heal(message):
  try:
    severity = int(message.content.split()[1])-1
    co.chars[co.whois(message.author)].get_stat("Wounds")[severity] = max(co.chars[co.whois(message.author)].get_stat("Wounds")[severity]-1,0)
    return 'A wound of Level {} healed. {} remain'.format(severity+1,co.chars[co.whois(message.author)].get_stat("Wounds")[severity])
  except:
    return 'Needs a number'

def handle_clear(message):
  if message.content.lower().startswith('$clear db now'):
    try:
      db.clear()
    except:
      return 'Clearing failed'
    return 'Database was completely and irrevocably cleared'

def handle_keys(message):
  return str(db.keys())