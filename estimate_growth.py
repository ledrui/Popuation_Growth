#--------------------------------------------------------
# Name : estimate_growth.py
#
# Author : Iliass Tiendrebeogo, 2014
#
# Desc : function for estimating growth in simulating model
#       
#
#---------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

MALE = 1;  FEMALE = 2

def get_children(n, male_portion, fertility):
    if n == 0: return []
    n = int(fertility*n)  # not all n couples get a child
    r = np.random.random(n)
    children = np.zeros(n, int)
    children[r <  male_portion] = MALE
    children[r >= male_portion] = FEMALE
    return children
    
def advance_generation(parents, policy='one son',
                       male_portion=0.5, fertility=1.0,
                       law_breakers=0, wanted_children=4):
    """
    Given a generation of parents (random integers with
    values MALE or FEMALE), compute the next generation
    of children.
    Return: array of children (MALE and FEMALE values),
    and the maximum number of children found in a family.
    """
    males = len(parents[parents==MALE])
    females = len(parents) - males
    couples = min(males, females)

    if policy == 'one child':
        # Each couple gets one child.
        children = get_children(couples, male_portion, fertility)
        max_children = 1
    elif policy == 'one son':
        # Each couple can continue with a new child until 
        # they get a son.

        # First try.
        children = get_children(couples, male_portion, fertility)
        max_children = 1
        # Continue with getting a new child for each daughter.
        daughters = children[children == FEMALE]
        while len(daughters) > 0:
            new_children = get_children(len(daughters),
                                        male_portion, fertility)
            children = np.concatenate((children, new_children))
            daughters = new_children[new_children == FEMALE]
            max_children += 1
    # A portion law_breakers breaks the law and gets wanted_children.
    illegals = get_children(int(len(children)*law_breakers)*wanted_children,
                            male_portion, fertility=1.0)
    children = np.concatenate((children, illegals))
    return children, max_children

N = 1000000
male_portion = 0.51
fertility = 0.92
law_breakers = 0.06
wanted_children = 6

generations = 10
law_breaking = []
one_son = []
# Start with a "perfect" generation of parents.
start_parents = get_children(N, male_portion=0.5, fertility=1.0)
parents = start_parents.copy()
print 'Strictly one son policy, start with: %d' % len(parents)
for i in range(generations):
    parents, mc = advance_generation(parents, 'one son',
                                     male_portion, fertility,
                                     law_breakers=0, wanted_children=0)
    print '%3d: %d' % (i+1, len(parents))
    one_son.append(len(parents))

parents = start_parents.copy()
print 'one son policy with law_breaking, start: %d' % len(parents)
for i in range(generations):
    parents, mc = advance_generation(parents, 'one son',
                                     male_portion, fertility,
                                     law_breakers, wanted_children)
    print '%3d: %d (max children in a family: %d)' % \
          (i+1, len(parents), mc)
    law_breaking.append(len(parents))

#-------------------------------plotting------------------------------
law_breaking = np.array(law_breaking)
one_son = np.array(one_son)
growth_factor = []
ln = len(law_breaking)
for i in range(ln):
	r = (law_breaking[i]/law_breaking[i-1]) - 1
	growth_factor.append(r)

print growth_factor

plt.figure()
plt.plot( law_breaking, 'b', label="law_breaking policy")
plt.plot( one_son, 'or', label="Strictly one son policy")
plt.plot( growth_factor, 'bo', label="growth_factor r")

plt.legend()
plt.title("One son birth policy  impact on one generation = 10 y")
plt.savefig("/home/zax/Dropbox/PythonLab/Project03/onechild")
plt.show()
