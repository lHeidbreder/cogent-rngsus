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
  #	if len(arr) == 1:
  #		arr.append('1')
    
    
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
      challenge_level = 3
    else:
      challenge_level = 4
    for val in rndvals:
      if val >= challenge_level:
        successes += 1
    
    #Determine format
    format = '$r x'
    if arr[1][-1] in ('d','~'): #== 'd':
      format += arr[1][-1] 
    if len(arr) > 2:
      format += ' t'
    
    #Make message
    msg_switcher = {
      '$r x': toString(amount, 'd6: ', rndvals, '\nSuccesses: ', successes),
      '$r xd': toString(amount, 'd6: ', rndvals, '\nSum: ', sum(rndvals)),
      '$r x t': self.form_x_t(rndvals, successes, challenge_level),
      '$r x~': toString(amount, 'd6: ', rndvals, '\nAverage: ', sum(rndvals)/len(rndvals))
    }
    #return message
    return msg_switcher[format]
    
  def form_x_t(self, values, successes, target):
    if successes >= target:
      return toString(values, '\nSuccess with ', (successes-target), ' Victory Levels!')
    else:
      return toString(values, '\nFailure with ', (target-successes), ' Levels of Failure')