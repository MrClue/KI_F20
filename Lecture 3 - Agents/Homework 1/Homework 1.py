"""
REFLEX-VACUUM-AGENT.

Extend the REFLEX-VACUUM-AGENT program to have 4 locations (4 squares):
 * The agent should only sense and act on the square where it is located.
 * Allow any starting square
 * Use run (20) test and display results.
"""

A = 'A'
B = 'B'
C = 'C'
D = 'D'

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A
}


def REFLEX_VACUUM_AGENT(loc_st):  # Determine action
    if loc_st[1] == 'Dirty':
        return 'Suck'
    if loc_st[0] == A:
        return 'Right'
    if loc_st[0] == B:
        return 'Down'
    if loc_st[0] == C:
        return 'Left'
    if loc_st[0] == D:
        return 'Up'


def sensors():  # Sense environment
    location = Environment['Current']
    return location, Environment[location]


def actuators(action):  # Modify environment
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Down' and location == B:
        Environment['Current'] = C
    elif action == 'Left' and location == C:
        Environment['Current'] = D
    elif action == 'Up' and location == D:
        Environment['Current'] = A


def run(n, make_agent):  # run the agent through n steps
    print('     Current                     New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = sensors()  # before action
        print("{:12s}{:8s}".format(location, status), end='')
        action = make_agent(sensors())
        actuators(action)
        (location, status) = sensors()  # after action
        print("{:8s}{:12s}{:8s}".format(action, location, status))


run(20, REFLEX_VACUUM_AGENT)