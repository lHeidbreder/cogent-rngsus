import random

def toString(*args):
  rtn = ''
  for a in args:
    rtn += str(a)
  return rtn

class RollRequest:
  #the actual request in one of these forms:
  # '$roll x'     - Rolls x D6 and counts successes
  # '$roll x t'   - Rolls x D6 against a CL of t
  # '$roll x+ t'  - Rolls x D6 against a CL of t, succeeding at 3s
  # '$roll xd'    - Rolls x D6 and adds up
  __form = None 

  def __init__(self, form):
    self.__form = form.lower()
  
  def process(self):
    arr = self.__form.split()
    
    #Don't bother with the rest of the function if it's this simple
    if len(arr) == 1:
      return random.randint(1,6)
    #Alternatively append 1 and use the function as it makes for simpler maintainability:
  #    if len(arr) == 1:
  #        arr.append(' 1')
    
    
    #Random values
    rndvals = []
    if arr[1].isnumeric():
      amount = int(arr[1])
    else:
      amount = int(arr[1][:-1])
    for i in range(amount):
      rndvals.append(random.randint(1,6))
    
    #Successes
    successes = 0
    if arr[1][-1] == '+':
      target = 3
    else:
      target = 4
    for val in rndvals:
      if val >= target:
        successes += 1
    
    #Optional target
    target = 0
    if len(arr) > 2 and arr[2].isnumeric:
      challenge_level = int(arr[2])
    else:
      challenge_level = 1
    
    #Determine pattern
    pattern = '$r x'
    if arr[1][-1] in ('d','~'): #== 'd':
      pattern += arr[1][-1] 
    if len(arr) > 2:
      pattern += ' t'
    
    #Make message
    #TODO: lazier evaluation; currently makes every available answer before picking one
    msg_switcher = {
      '$r x':   toString(amount, 'd6: ', rndvals, '\nSuccesses: ', successes),
      '$r xd':  toString(amount, 'd6: ', rndvals, '\nSum: ', sum(rndvals)),
      '$r x t': self.form_x_t(rndvals, successes, challenge_level),
      '$r x~':  toString(amount, 'd6: ', rndvals, '\nAverage: ', sum(rndvals)/len(rndvals))
    }
    #return message
    return msg_switcher[pattern]
    
  def form_x_t(self, values, successes, challenge_level):
    if successes >= challenge_level:
      return toString(values, '\nSuccess with ', (successes-challenge_level), ' Victory Levels!')
    else:
      return toString(values, '\nFailure with ', (challenge_level-successes), ' Levels of Failure')


class FateRequest:
  def __init__(self, roll=None):
    if not isinstance(roll, int) or roll not in range(1,21):
      try:
        self.__roll = int(roll)
      except TypeError:
        self.__roll = random.randint(1,20)
    else:
      self.__roll = roll

  def result(self):
    msg = 'Alea iacta est: {}\n'.format(self.__roll)
    
    if self.__roll < 4: #1-3 / 3
      rtn = 'It is too late to run...'
    elif self.__roll < 8: #4-7 / 4
      rtn = 'Great perils are ahead. Brace yourselves and may fortune be with you.'
    elif self.__roll < 14: #8-13 / 6
      rtn = 'Things are unclear. Prove yourselves and you will preveil.'
    elif self.__roll < 18: #14-17 / 4
      rtn = 'Things ahead seem to be set in your favor. But do not let your guard down.'
    else: #18-20 / 3
      rtn = 'Fortune favors fools. You are in luck today.'
      
    return msg + rtn