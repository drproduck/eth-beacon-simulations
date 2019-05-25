import logging
import random
logtoggle = 1 # set this to zero to turn off logging

class Validator(object):
  def __init__(self, name, faction):
    self.name = name
    self.faction = faction
    # self.view = {}

  def __repr__(self):
    return str(self.name)


class Faction(object):

  def __init__(self, num, name):

    """Construct a Faction of validators that follow a common strategy
  
    Args:
      num: the number of validators in this faction
      name: the name of the faction
      validators: the $(num) Validators

    """
    self.num = num
    self.name = name
    # should return a list of (validator, slot) pairs
    self.validators = {Validator(str("%s_%d") % (name, k), self) for k in range(num)}

  def get_timings(self):
    """timings: function that decides the time to publish attestation"""
    pass


  def get_vote(self):
    """return a vote (of a validator)"""
    pass


  def timing_with_mean(self, error_param, mean):
    """timing with mean:
    attests around 0.5 with error bar uniformly distributed within error_param"""
    timings = []
    for v in self.validators:
      timing = adjusted_random_time(mean - error_param, mean + error_param)
      timings.append((v, timing))
    return timings




class HonestFaction(Faction):

  def __init__(self, num, name, aim, error_param, delay_param):
    """A faction of "honest" validators.
    They are supposed to publish at time = aim with some noise

    """
    super().__init__(num, name)
    self.aim = aim
    self.error_param = error_param
    self.delay_param = delay_param


  def get_timings(self):
    return self.timing_with_mean(self.error_param, self.aim)


  def get_vote(self, time_current, votes, flipped=False):

    """
    Args:
      time_current: the current time. Validators only see votes that come before this time.
      votes: all the votes
      delay_param: the validator receives vote at the published time + some unique delay for each vote
      flipped: 
      
    Returns:
      vote: the vote of this validator after considering all seeable votes

    """
    seen_votes = [0, 0]
    for v, timing, vote in votes:
      time_received = adjusted_random_time(timing, timing + self.delay_param)
      logstr = "  %s voted for %s [t=%.3f; t_received=%.3f]" % (v.name, str(vote), timing, time_received)
      if time_received < time_current:
        logstr += (" (counts)")
        seen_votes[vote] += 1
      logger(logtoggle, logstr)
    if seen_votes[0] >= seen_votes[1]:
      vote = 0
    else:
      vote = 1
    if flipped:
      vote = 1 - vote
    return vote


    
class SmokeFaction(Faction):

  def __init__(self, num, name, aim, error_param, delay_param):

    """A faction of validators that publish votes randomly, at time approximately aim - delay_param,
    so that (honest) validators receive these votes at time approximately aim
    """

    super().__init__(num, name)
    self.aim = aim
    self.error_param = error_param
    self.delay_param = delay_param
    self.timings = self.timing_with_mean(error_param, aim-delay_param)


  def get_timings(self):
    return self.timing_with_mean(self.error_param, self.aim - self.delay_param)
    

  def get_vote(self, time, votes):
    """smoke screen: vote randomly"""
    return random.choice([0,1])


def adjusted_random_time(lower, upper):
  """Uniformly random 

  """
  timing = random.uniform(lower, upper)
  if timing < 0.0:
    timing = 0.0
  if timing > 0.99999:
    timing = 0.99999
  return timing

def logger(toggle, log): #logging helper function
  if (toggle == 0):
    return
  if (toggle == 1):
    return logging.info(log)

    

  
