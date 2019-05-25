#!/usr/env/bin python

import matplotlib.pyplot as plt
from collections import Counter
import logging
from beacon import *

# logging = 0 # uncomment to turn off logging



def collect_statistics(votes):
  vote_count = []
  for vote in votes:
      vote_count += [vote[2]]

  vote_count = Counter(vote_count)

  return (vote_count[0], vote_count[1])


    
if __name__ == "__main__": # log with the following format
  num = 20
  honestFac = 'honest'
  dishonestFac = 'smoke'
  aim = 0.5
  error_param = 0.1
  delay_param = 0.2
  n_simulations = 100
  logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                  format="%(asctime)-15s %(levelname)-8s %(message)s")

  # factions
  faction1 = HonestFaction(num, honestFac, aim, error_param, delay_param)
  faction2 = SmokeFaction(num, dishonestFac, aim, error_param, delay_param)

  # number of blocks reaching 2/3 consensus
  # to do: more here
  stats = [collect_statistics(play(faction1, faction2)) for _ in range(n_simulations) ] 
  
  print(stats)
  n = 0
  for s in stats:
    if s[0] == 0 and s[1] == 0: raise Exception("Somethingwong")
    if s[0] == 0 or s[1] == 0: n += 1
    if s[0] / s[1] >= 3/2 or s[0] / s[1] <= 2/3:
      n += 1

  print('win/lose ration: %d\n' % n)

  
