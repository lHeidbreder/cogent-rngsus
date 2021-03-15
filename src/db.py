import pathlib
import pickle

class Saved_Dict(dict):
  path = pathlib.Path('../saves/db')
  def __setitem__(self, key, value, /):
    super(db,self).__setitem__(key, value)
    with open(self.path + '.pkl', 'wb'):
      pickle.dump(self, self.Path, pickle.HIGHEST_PROTOCOL)
    
  @staticmethod
  def load_db():
    try:
      with open(Saved_Dict.path + '.pkl', 'rb') as pickled_dict:
        return pickle.load(pickled_dict)
    except:
      print('No dict saved')
      return None