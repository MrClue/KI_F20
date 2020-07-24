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
state = {}
action = None
model = {A: None, B: None, C: None, D: None}

RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Down',
    4: 'Left',
    5: 'Up',
    6: 'NoOp'
}

rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 3,
    (C, 'Clean'): 4,
    (D, 'Clean'): 5,
    (A, B, C, D, 'Clean'): 6
}

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A
}


def INTERPRET_INPUT(input):
    return input


def RULE_MATCH(state, rules):
    return rules.get(tuple(state))


def UPDATE_STATE(state, action, percept):
    (location, status) = percept
    state = percept
    if model[A] == model[B] == model[C] == model[D] == 'Clean':
        state = (A, B, C, D, 'Clean')
    model[location] = status
    return state


def REFLEX_AGENT_WITH_STATE(percept):  # Determine action
    global state, action
    state = UPDATE_STATE(state, action, percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action


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


def run(n):  # run the agent through n steps
    print('     Current                     New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = sensors()  # before action
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_AGENT_WITH_STATE(sensors())
        actuators(action)
        (location, status) = sensors()  # after action
        print("{:8s}{:12s}{:8s}".format(action, location, status))


run(20)
