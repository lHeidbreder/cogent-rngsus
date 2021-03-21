import pathlib
import pickle
import os

class Saved_Dict(dict):
  saves_path = pathlib.Path('./saves/')
  if not saves_path.exists():
    os.mkdir(saves_path)
  
  def __init__(self):
    super(Saved_Dict,self).__init__()
    with open(self.saves_path / 'db.pkl', 'wb') as pickled_dict:
      pickle.dump(self, pickled_dict, pickle.HIGHEST_PROTOCOL)
  
  def __setitem__(self, key, value):
    super(Saved_Dict,self).__setitem__(key, value)
    with open(self.saves_path / 'db.pkl', 'wb') as pickled_dict:
      pickle.dump(self, pickled_dict, pickle.HIGHEST_PROTOCOL)
    
  @staticmethod
  def load_db():
    try:
      with open(Saved_Dict.saves_path / 'db.pkl', 'rb') as pickled_dict:
        return pickle.load(pickled_dict)
    except:
      print('No dict saved')
      return Saved_Dict()