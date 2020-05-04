from __future__ import annotations
from sys import exit


class State:
    """
    Represents a vertex in automata's graph representation
    """

    def __init__(self, name: str) -> None:
        self.name = name

        self.delta = {}

    def add_adj(self, v: State, e: str) -> None:
        """
        Adds a transition for state
        :param v: the next state vertex
        :param e: edge label
        """

        self.delta[e] = v

    def next_state(self, letter: str) -> State:
        """
        Returns δ(self, letter)
        :param letter:
        :return:
        """
        return self.delta.get(letter)

    def __eq__(self, other):
        return self.name == other.name


if __name__ == '__main__':
    # Reading DFA from input file and store it as a list of State objects (dfa variable)
    with open('DFA_Input_1.txt', 'r') as f:
        alphabet = f.readline().split()
        dfa = [State(st_name) for st_name in f.readline().split()]
        int_st_name = f.readline().strip()
        initial_state = [st for st in dfa if st.name == int_st_name][0]
        fnl_st_name = f.readline().split()
        final_states = [st for st in dfa if st.name in fnl_st_name]

        # Reading transitions
        while True:
            line = f.readline()
            if line == '':
                break
            transition = line.split()
            src = [st for st in dfa if st.name == transition[0]][0]
            dst = [st for st in dfa if st.name == transition[-1]][0]
            src.add_adj(dst, transition[1])

    text = list(input("Enter input string: "))

    # Calculating δ*(initial_state, text)
    current_state = initial_state
    for letter in text:
        current_state = current_state.next_state(letter)
        # Rejecting input if no transitions is possible from current state
        if current_state is None:
            print("Rejected")
            exit(0)

    print("Accepted" if current_state in final_states else "Rejected")
