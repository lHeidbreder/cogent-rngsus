from math import factorial

def bin_co_prob(n, k, p):
    if (k > n):
      return 0
      
    no_pass = 0
    for i in range(k):
      coefficient = factorial(n) / (factorial(n-i) * factorial(i))
      print(coefficient)
      no_pass += coefficient * p**i * (1-p)**(n-i)
      print(no_pass)
    
    return 1-no_pass
  
  
  
class probability_request:
  __pattern = ""
  
  def __init__(self, form):
    self.__pattern = form.lower()


  ##PATTERNS#################################
   
  def __pattern_x(self, args):
    return 'You will expect an average of {} successes'.format(round(float(args['amount']*args['chance']),2))
  
  def __pattern_xd(self, args):
    return 'You will on average roll between {} and {}'.format(3*args['amount'], 4*args['amount']) 
  
  def __pattern_x_t(self, args):
    probability = bin_co_prob(args['amount'], args['cl'], args['chance'])
    if probability == 0:
      return 'There is no chance'
    else:
      return 'Your success chance is {}%'.format(probability*100)


  ##PROCESS##################################
  def process(self):
    arr = self.__pattern.split()
    
    if len(arr) == 1 or self.__pattern[:-1] == '~':
      return 'Go back to school if you can\'t that one figure out'
    
    pattern = '$p x'
    if arr[1][-1] in ('d','~'):
      pattern += arr[1][-1] 
    if len(arr) > 2:
      pattern += ' t'
    
    #arguments
    args = {}
    #dice amount
    try:
      args['amount'] = int(arr[1])
    except ValueError:
      args['amount'] = int(arr[1][:-1])
    except IndexError:
      args['amount'] = 1
    #success chance
    if arr[1][-1] == '+':
      args['chance'] = 2/3
    else:
      args['chance'] = 1/2
    #challenge level
    try:
      args['cl'] = int(arr[2])
    except:
      args['cl'] = 0
    
    msg_switcher = {
      '$p x':   self.__pattern_x,
      '$p xd':  self.__pattern_xd,
      '$p x t': self.__pattern_x_t
    }
    
    return msg_switcher[pattern](args)
    
    