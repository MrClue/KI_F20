import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        [None, 3, 1, 3],
        # only calculating 3,1,3 in our exercise...
        #[None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        #[None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    # transitions[start, end]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .6, .3, .1],  # Hot state
                            [.0, .4, .5, .1],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state, observation]
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .2, .4, .4],  # Hot state
                          [.0, .5, .4, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(
            states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions):
    t = len(observations)
    n = len(states)
    # init matrix
    forward = np.zeros((n, t))

    for s in range(1, n - 1):
        forward[s][1] = transitions[0][s] * emissions[s][observations[1]]

    for t in range(2, t):
        obs = observations[t]
        for s in range(1, n - 1):
            summation = 0
            for s_derivative in range(1, n):
                summation += forward[s_derivative][t-1] * transitions[s_derivative][s] * emissions[s][obs]
                forward[s][t] = summation

    qf = 0
    for s in range(1, n):
        qf += forward[s][t - 1] * transitions[s][n - 1]
    forward[n - 1][t] = qf

    # my probability is always off somehow
    return forward[n -1][t]


def compute_viterbi(states, observations, transitions, emissions):
    # the pseudocode got updated in this pdf?
    # https://web.stanford.edu/~jurafsky/slp3/A.pdf

    t = len(observations)
    n = len(states)

    viterbi = np.zeros((n, t))
    backpointer = np.zeros((n, t), dtype=int)

    for s in range(1, n - 1):
        viterbi[s, 1] = transitions[0, s] * emissions[s, observations[1]]
        backpointer[s, 1] = 0

    for t in range(2, t):
        for s in range(1, n - 1):
            viterbi[s][t] = max(viterbi[s_derivative][t-1] * transitions[s_derivative]
                                [s] * emissions[s][observations[1]] for s_derivative in range(1, n - 1))
            backpointer[s][t] = 1 + argmax(viterbi[s_derivative][t-1] * transitions[s_derivative]
                                           [s] * emissions[s][observations[1]] for s_derivative in range(1, n-1))

    bestpathprob = max(viterbi[s, t] for s in range(1, n - 1))
    bestpathpointer = 1 + argmax(viterbi[s, t] for s in range(1, n - 1))

    path = [states[bestpathpointer]]
    for t in range(t, 1, -1):
        bestpathpointer = backpointer[bestpathpointer, t - 1]
        path.append(states[bestpathpointer])
    path.pop(0)
    return reversed(path)


def argmax(sequence):
    # Note: You could use np.argmax(sequence), but only if sequence is a list.
    # If it is a generator, first convert it: np.argmax(list(sequence))
    return max(enumerate(sequence), key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
