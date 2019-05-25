import random
import matplotlib.pyplot as plt

n = 1000000
#Master list of activators and exits
M = []
#Master list of Bounds
B = []
#Master list of intersections
I = []
for i in range(n):
    ###Partitions initial validator set into four parts
    #L_0 = [A,B,C,D]

    'Can probably rewrite this as a function'
    #Samples four uniform numbers
    Numbers = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
    #Normalizes so they add up to 1 to make them percentages
    L_0 = [i/sum(Numbers) for i in Numbers]
    #L_0 = [A,B,C,D]

    ###The rest of V_L (percentage-wise) is based on information from initial validator set
    #V_L = [B,C,E,F]
    #1 - (B + C) = E + F
    x = 1 - (L_0[1] + L_0[2])

    ##Constructs F explicitly
    'Can probably rewrite this as a function'
    #Samples two uniform numbers within the range of activations of L
    X = [random.uniform(0,x), random.uniform(0,x)]
    #Normalizes this so they add up to x
    Normalized_X = [i*x/sum(X) for i in X]
    ##sum(Normalized_X) - x should be machine 0
    #Normalized_X = [E,F]

    #V_R = [C,D,F,G]
    #1 - (C + D + F) = G, so
    #1 - (C + D) = F + G

    ###Assigns the activators and exits
    #a_L = E + F
    a_L = x
    #e_L = A + D
    e_L = L_0[0]+L_0[3]

    #a_R = F+ G
    a_R = 1 - (L_0[2]+L_0[3])
    #e_R = A + B
    e_R = L_0[0] + L_0[1]

    #lower bound
    bound = 2*a_L/3 + 2*e_R/3 + a_R/3 + e_L/3
    #intersection = C+F
    intersection = L_0[2] + Normalized_X[1]

    #If they're within the bound C + F \ge |V_L|/3 - (2a_L/3 + 2e_R/3 + a_R/3 + e_L/3\right)
    'Problem: Size of V_L is not 1 -- but that might not matter because these are percentages'
    if intersection >= 1/3 - bound:
        #Append to the master list
        M.append([a_L,e_L,a_R,e_R])
        B.append(bound)
        I.append(intersection)
