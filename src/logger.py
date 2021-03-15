import datetime
import pathlib
import os

class Logger:
  __name = None
  __file = None

  def __init__(self):
    self.__name = pathlib.Path("logs/log_{}".format(datetime.date.today()))
    if not(pathlib.Path("./logs").exists()) or not(pathlib.Path("./logs").is_dir()):
      os.mkdir("./logs")

  def __str__(self):
    return str(self.__name)

  def __write_log(self,msg,designator):
    with open(self.__name,'a') as file:
      file.write('{} {} {}\n'.format(datetime.datetime.now().strftime("%H:%M:%S"),designator,msg))
      file.close()

  def message(self,msg):
    self.__write_log(msg,"---")

  def write(self,msg):
    self.__write_log(msg,"-->")
  
  def serious(self,msg):
    self.__write_log(msg,"==>")