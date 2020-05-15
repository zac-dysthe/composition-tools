import random


class ZdMarkov:

    def __init__(self, training_data, order=1):
        self.training_data = training_data
        self.order = order

    def transitions(self):
        def build_table(seq, ord):
            table = dict()
            for i in range(ord, len(seq)):
                transition = (tuple(seq[i - ord:i]), seq[i])
                if transition not in table:
                    table[transition] = 1
                else:
                    table[transition] += 1
            return table

        transitions = []
        for j in range(len(self.training_data)):
            for k in range(self.order):
                transitions.append(build_table(self.training_data[j], k + 1))
        return transitions

    def relevant_transitions(self, initial_state):
        relevant_transitions = []
        all_transitions = self.transitions()
        for i in range(len(all_transitions)):
            local_order = len(next(iter(all_transitions[i]))[0])
            for j in [(t, c) for (t, c) in all_transitions[i].items() if t[0] == initial_state[0 - local_order:]]:
                relevant_transitions.append(j)
        return relevant_transitions

    def markov_choice(self, initial_state, order_prevalence=None):
        if order_prevalence is None:
            order_prevalence = [1 for i in range(self.order)]
        transitions = [t[1] for (t, c) in self.relevant_transitions(initial_state)]
        transition_weights = [c * order_prevalence[len(t[0]) - 1] for (t, c) in
                              self.relevant_transitions(initial_state)]
        normalized_weights = [i / sum(transition_weights) for i in transition_weights]
        return random.choices(transitions, weights=normalized_weights)[0]

    def generate_sequence(self, initial_state, length=1, order_prevalence=None):
        if order_prevalence is None:
            order_prevalence = [1 for i in range(self.order)]
        new_sequence = [i for i in initial_state]
        for i in range(self.order, length):
            previous_state = tuple(new_sequence[i - self.order:i])
            next_state = self.markov_choice(previous_state, order_prevalence)
            new_sequence.append(next_state)
        return new_sequence
