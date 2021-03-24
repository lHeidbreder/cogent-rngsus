from src import db as saved_dictionary
import csv
from pathlib import Path
import pickle
import os

chars = []
saves_path = Path('./saves/')
db = {}

##Static methods##
def whois(user):
  try:
    return db[str(user)[:-5]+"_nick"]
  except Exception:
    print('key not found: ', str(user)[:-5]+"_nick")
    return str(user)[:-5]

def write_to_db():
  global chars, db
  for c in chars:
    db[c.get_name()+'_char'] = c

def save_chars():
  global chars
  for entry in db.values():
    if isinstance(entry,RPGCharacter) and entry not in chars:
      chars.append(entry)
  
  with open(saves_path / 'chars.pkl', 'wb') as pickled_chars:
    pickle.dump(chars, pickled_chars) #, pickle.HIGHEST_PROTOCOL)
    
def load_chars():
  global chars
  try:
    with open(saves_path / 'chars.pkl', 'rb') as pickled_chars:
      chars = pickle.load(pickled_chars)
      write_to_db()
  except Exception as e:
    print('Failed to import chars:',e)
    chars = []

def read_csv(filepath):
  with open(Path(filepath)) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
      c = RPGCharacter(row)
      chars.append(RPGCharacter(row))
    try:
      os.remove(filepath)
    except PermissionError:
      print('Failed to delete file')
  save_chars()
  
#Character class
class RPGCharacter:
  def __init__(self, row):
    #initialize all attributes
    self.__attributes = {
      'str': 0,
      'ref': 0,
      'int': 0
    }
    self.__core_skills = {
      'perception': 0
    }
    self.__str_skills = {
      'athletics': 0,
      'grapple': 0,
      'swim': 0,
      'aim/throw': 0
    }
    self.__ref_skills = {
      'acrobatics': 0,
      'ride/pilot': 0,
      'sleight of hand': 0,
      'stealth': 0
    }
    self.__int_skills = {
      'deception': 0,
      'persuasion': 0,
      'infiltration': 0,
      'survival': 0
    }
    self.__vocations = {}
    self.__proficiencies = {}
    self.__commerce_points = 0
    self.__destiny_points = 0
    self.__wounds = [0,0,0,0]
    self.__disabling_characteristics = []

    #fill in
    #attributes & skills
    for k in self.__attributes.keys():
      self.__attributes[k] = int(row[k])
    for k in self.__core_skills.keys():
      self.__core_skills[k] = int(row[k])
    for k in self.__str_skills.keys():
      self.__str_skills[k] = int(row[k])
    for k in self.__ref_skills.keys():
      self.__ref_skills[k] = int(row[k])
    for k in self.__int_skills.keys():
      self.__int_skills[k] = int(row[k])
    
    #vocations
    vocnam = row['vocation names'].split(',')
    vocval = str(row['vocation values']).split(',')
    for i in range(len(vocnam)):
      self.__vocations[vocnam[i]] = vocval[i]
    
    #proficiencies
    profnam = row['proficiency names'].split(',')
    profval = str(row['proficiency values']).split(',')
    for i in range(len(profnam)):
      self.__proficiencies[profnam[i]] = profval[i]
    
    #points
    self.__commerce_points = row['cp']
    self.__destiny_points = row['dp']
    
    #misc
    if row['wounds'] != "":
      wounds = str(row['wounds']).split(',')
      for i in range(len(wounds)):
        self.__wounds[i] = int(wounds[i])
    self.__disabling_characteristics = row['disabling characteristics'].split(',')
    self.__name = row['name']
  
  def __wound_penalty(self):
    pen = 0
    for i in range(4):
      pen += self.__wounds[i]*(i+1)
    return pen
  
  def get_name(self):
    return self.__name
  
  def get(self,stat):
    stat = stat.lower()
    if stat == 'name':
      return self.get_name()
      
    if stat in self.__attributes.keys():
      return self.__attributes[stat]
    if stat in self.__core_skills.keys():
      return self.__core_skills[stat]
    if stat in self.__str_skills.keys():
      return self.__str_skills[stat]
    if stat in self.__ref_skills.keys():
      return self.__ref_skills[stat]
    if stat in self.__int_skills.keys():
      return self.__int_skills[stat]
    
    if stat in ['vocations','vocation names']:
      return self.__vocations.keys()
    if stat in self.__vocations.keys():
      return self.__vocations[stat]
    if stat in ['proficiencies','proficiency names']:
      return self.__proficiencies.keys()
    if stat in self.__proficiencies.keys():
      return self.__proficiencies[stat]
    
    if stat in ['commerce','commerce points','cp']:
      return self.__commerce_points
    if stat in ['destiny','destiny points','dp']:
      return self.__destiny_points
    if stat.startswith('wound'):
      return self.__wounds
    if stat in ['disabling characteristics','disable','disab']:
      return self.__disabling_characteristics
    
    return None
    
    
  def get_roll(self, stat):
    base = 3 - self.__wound_penalty()
    if stat in self.__attributes.keys():
      return self.__attributes[stat] + base
    if stat in self.__core_skills.keys():
      return self.__core_skills[stat] + sum(self.__attributes.values()) + base
    if stat in self.__str_skills.keys():
      return self.__str_skills[stat] + self.__attributes['str'] + base
    if stat in self.__ref_skills.keys():
      return self.__ref_skills[stat] + self.__attributes['ref'] + base
    if stat in self.__int_skills.keys():
      return self.__int_skills[stat] + self.__attributes['int'] + base
    if stat in self.__vocations.keys():
      return int(self.__vocations[stat]) + sum(self.__attributes.values()) + base
    if stat in self.__proficiencies.keys():
      return int(self.__proficiencies[stat]) + sum(self.__attributes.values()) + base
    
    return None