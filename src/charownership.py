from .db import *
import csv
import os

chars = []

def whois(user):
  try:
    return db[str(user)[:-5]+"_nick"]
  except:
    return str(user)[:-5]

def read_csv(filepath):
  print(filepath)
  with open(filepath) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
      chars[row["Name"]] = Character(row)
    os.remove(filepath)
  for c in chars.keys():
    db[c.get_stat("Name")+'_char'] = chars[c].me()

def loadCharsFromDB():
  for key in db.keys():
    if key[-5:-1] == '_char':
      chars[db[key]["Name"]] = Character(db[key])
      

class Character():
  __stats = {} #An empty dictionary

  def __init__(self,row):
    self.__fill(row)

  def __fill(self, row):
    vocnam = "Vocation Names"
    vocval = "Vocation Values"
    profnam = "Proficiency Names"
    profval = "Proficiency Values"
    self.__stats = row

    if vocnam in row.keys():
      for i in range(len(row[vocnam].split(','))):
        nam = row[vocnam].split(',')[i]
        val = row[vocval].split(',')[i]
        self.__stats[nam] = val
      del self.__stats[vocnam]
      del self.__stats[vocval]

    if profnam in row.keys():
      for i in range(len(row[profnam].split(','))):
        nam = row[profnam].split(',')[i]
        val = row[profval].split(',')[i]
        self.__stats[nam] = val
      del self.__stats[profnam]
      del self.__stats[profval]

    try:
      self.__stats["Wounds"] = row["Wounds"][1:-1].split(',')
    except:
      print('Wounds not in standard format for',self.get_stat('Name'))
        
    
  def get_stat(self,stat_key):
    try: #If list or similar, return copy not pointer
      return self.__stats[stat_key].copy()
    except:
      return self.__stats[stat_key]
  
  #returns the stats dictionary to be saved in the db
  def me(self):
    return self.__stats