from __future__ import annotations

import queue
from itertools import chain, combinations
from typing import Union


class State:
    """
    Represents a vertex in automata's graph representation
    """

    def __init__(self, name: Union[str, set]) -> None:
        self.name = name

        self.adjs = []
        self.delta_s = {}
        for letter in alphabet:
            self.delta_s[letter] = set()

    def add_adj(self, v: State, e: str) -> None:
        """
        Adds a transition for state
        :param v: the next state vertex
        :param e: edge label
        """

        self.adjs.append((v, e))

    def calc_delta(self) -> None:
        """
        Calculates δ*(self, a) for every a in alphabet
        """

        self.__bfs()

    def __bfs(self):
        q = queue.Queue(maxsize=1000)
        q.put(self)
        length = 0
        while (not q.empty()) and length <= 2 * lambda_count + 1:
            length += 1
            state = q.get()
            for neighbor, letter in state.adjs:
                if letter == 'λ':
                    q.put(neighbor)
                else:
                    self.delta_s[letter].add(neighbor)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other

    def __ne__(self, other):
        return not (self == other)

    def __str__(self) -> str:
        return str(self.name).replace(' ', '')

    def __repr__(self) -> str:
        return self.__str__()

    # def state_debug(self) -> str:
    #     ret = str(self.name) + '\nTransitions: '
    #     for adj in self.adjs:
    #         ret += adj[1] + ' ' + str(adj[0]) + ', '
    #     # ret += '\nDelta*: '
    #     # for letter in self.delta_s:
    #     #     ret += f"Letter: {letter}: "
    #     #     for n in self.delta_s[letter]:
    #     #         ret += f"{n.name}, "
    #     ret += '\n'
    #     return ret


def powerset(iterable):
    """
    Returns all subsets of iterable object
    :param iterable: input set
    :return: list of all iterable subsets
    """

    s = list(iterable)
    return list(map(set, chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))))


def states_to_list(states: list) -> list:
    """
    Converts a list of State to list of str (using states' name)
    :param states: list of State
    :return: list of str
    """

    states_list = []
    for state in states:
        states_list.append(str(state))
    return states_list


def convert_to_dfa(nfa: list) -> list:
    """
    Converts and NFA to DFA
    :param nfa: NFA
    :return: converted DFA
    """

    # Generating dfa states (it is nfa states' power set)
    dfa = []
    states_list = states_to_list(nfa)
    for dfa_state in powerset(states_list):
        dfa.append(State(dfa_state))

    # Calculating DFAs' transitions for all states using NFAs' δ* for every state and alphabet
    for dfa_state in dfa:
        states = [st for st in nfa if st.name in dfa_state.name]
        for letter in alphabet:
            dst = set()
            for sub_state in states:
                dst.update(sub_state.delta_s[letter])
            dst = [st for st in dfa if st.name == dst][0]
            dfa_state.add_adj(dst, letter)

    return dfa


def iterable_to_line(iterable):
    """
    A utility function for outputting dfa - converts an iterable object (e.g. list) to one line string
    :param iterable:
    :return: returns one line string
    """

    ret = ''
    for i in iterable:
        ret += str(i) + ' '
    ret += '\n'
    return ret


def write_to_file(dfa: list) -> None:
    """
    Writes dfa to 'DFA_Output_2.txt' file
    :param dfa: DFA to be written to file
    """

    with open('DFA_Output_2.txt', 'w') as f:
        f.write(iterable_to_line(alphabet))
        f.write(iterable_to_line(dfa))
        f.write(f"{{'{int_st_name}'}}\n")
        f.write(iterable_to_line([st for st in dfa if set(states_to_list(st.name)) & set(fnl_st_name)]))

        # Writing transitions
        for st in dfa:
            for adj in st.adjs:
                f.write(str(st) + ' ' + adj[1] + ' ' + str(adj[0]) + '\n')


if __name__ == '__main__':
    # Reading NFA from input file and store it as a list of State objects (nfa variable)
    with open('NFA_Input_2.txt', 'r') as f:
        alphabet = f.readline().split()
        nfa = [State(st_name) for st_name in f.readline().split()]
        int_st_name = f.readline().strip()
        initial_state = [st for st in nfa if st.name == int_st_name][0]
        fnl_st_name = f.readline().split()
        final_states = [st for st in nfa if st.name in fnl_st_name]

        # Reading transitions
        lambda_count = 0  # Counts lambda transitions for bfs termination
        while True:
            line = f.readline()
            if line == '':
                break
            transition = line.split()
            src = [st for st in nfa if st.name == transition[0]][0]
            dst = [st for st in nfa if st.name == transition[-1]][0]
            if transition[1] == 'λ':
                lambda_count += 1
            src.add_adj(dst, transition[1])

    # Some calculations and writing output to file
    for st in nfa:
        st.calc_delta()
    dfa = convert_to_dfa(nfa)
    write_to_file(dfa)
