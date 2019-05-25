import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')
from scipy.stats import truncnorm
from beacon import *
from main import collect_statistics

a = 0.05
b = 0.95
std = 0.2

aim_h=0.5
num_h=20
num_b=10
error_param=0.1
delay_param=0.2
n_games = 1000
n_samples = 10


def sample_p_win(mu_b):
  """given mu_b, compute p(winning|mu_b)"""

  honestFac = 'honest'
  dishonestFac = 'smoke'

  # factions
  faction1 = HonestFaction(num_h, honestFac, aim_h, error_param, delay_param)
  faction2 = SmokeFaction(num_b, dishonestFac, mu_b + delay_param, error_param, delay_param)

  # number of blocks reaching 2/3 consensus
  # to do: more here
  stats = [collect_statistics(play(faction1, faction2)) for _ in range(n_games)] 
  
  n = 0
  for s in stats:
    if s[0] == 0 and s[1] == 0: raise Exception('sometingwong')
    if s[0] == 0 or s[1] == 0: continue
    if s[0] / s[1] >= 2/3 and s[0] / s[1] <= 3/2:
      n += 1
  return n / len(stats)



def get_gradient(mu_b):
  Td_samples = std * truncnorm.rvs((a - mu_Td) / std, (b - mu_Td) / std, size=n_samples) + mu_Td
  grad_log = (Td_samples - mu_Td) / std**2
  p_win = [sample_p_win(Td) for Td in Td_samples]
  mu_probs = truncnorm.pdf((Td_samples - mu_Td) / std, (a - mu_Td) / std, (b - mu_Td) / std) 
  print(mu_probs)
  print(p_win)

  grad = sum(grad_log * p_win) / n_samples
  cost = sum(mu_probs * p_win) / n_samples

  return grad, cost


class robbins_monro():

  def __init__(self, stepsize_init=1, stepsize_lambda=1e-2):
    self.stepsize_init = stepsize_init
    self.stepsize_lambda = stepsize_lambda
    self.iter = 0

  def __call__(self, X, G):
    self.iter += 1
    learn_rate =  self.stepsize_init / (1 + self.stepsize_init*self.stepsize_lambda*self.iter)
    if G == 0: G = (1 if np.random.rand()<0.5 else -1) * 1e-3
# force it to learn
    return X + learn_rate * G


mu_Td = 0.8
update_op = robbins_monro()
n_iters = 20
cost_hist = []

# training
for i in range(n_iters):
  G, cost = get_gradient(mu_Td)
  mu_Td = update_op(mu_Td, G)
  if mu_Td < 0: mu_Td = 1e-5
  if mu_Td > 1: mu_Td = 1 - 1e-5
  cost_hist.append(cost)
  print(mu_Td, cost)

plt.plot(cost_hist)
plt.show()

# score function estimator derivative of p(winning) = \int p(winning)p(mu_d)
# d(mu_d)
# ~ sum p(winning) derivative log p(mu)  for mu_d ~ truncated normal(mu,a,b) 


