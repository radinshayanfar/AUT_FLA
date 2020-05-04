import queue
from itertools import chain, combinations


class State:
    def __init__(self, name):
        self.name = name

        self.adjs = []
        self.delta_s = {}
        for letter in alphabet:
            self.delta_s[letter] = set()
        self.final = False

    def add_adj(self, v, e):
        self.adjs.append((v, e))

    def calc_delta(self):
        self.__bfs()
        print(self.delta_s)

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
        return self.name == other.name

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __str__(self) -> str:
        return str(self.name).replace(' ', '')

    def __repr__(self) -> str:
        return self.__str__()

    def state_debug(self) -> str:
        ret = str(self.name) + '\nTransitions: '
        for adj in self.adjs:
            ret += adj[1] + ' ' + str(adj[0]) + ', '
        # ret += '\nDelta*: '
        # for letter in self.delta_s:
        #     ret += f"Letter: {letter}: "
        #     for n in self.delta_s[letter]:
        #         ret += f"{n.name}, "
        ret += '\n'
        return ret


def powerset(iterable):
    s = list(iterable)
    return list(map(set, chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))))


def states_to_list(states):
    states_list = []
    for state in states:
        states_list.append(str(state))
    return states_list


def convert_to_dfa(nfa):
    dfa = []
    states_list = states_to_list(nfa)
    for dfa_state in powerset(states_list):
        dfa.append(State(dfa_state))

    for dfa_state in dfa:
        states = [st for st in nfa if st.name in dfa_state.name]
        for letter in alphabet:
            transition = (set(), letter)
            for sub_state in states:
                transition[0].update(sub_state.delta_s[letter])
            dfa_state.add_adj(*transition)

    for dfa_state in dfa:
        print(dfa_state.state_debug())

    return dfa


def iterable_to_line(iterable):
    ret = ''
    for i in iterable:
        ret += str(i) + ' '
    ret += '\n'
    return ret


def write_to_file(dfa):
    with open('DFA_Output_2.txt', 'w') as f:
        f.write(iterable_to_line(alphabet))
        f.write(iterable_to_line(dfa))
        f.write(int_st_name + '\n')
        f.write(iterable_to_line([st for st in dfa if set(states_to_list(st.name)) & set(fnl_st_name)]))

        for st in dfa:
            for adj in st.adjs:
                f.write(str(st) + ' ' + adj[1] + ' ' + str(adj[0]) + '\n')


if __name__ == '__main__':
    with open('NFA_Input_2.txt', 'r') as f:
        alphabet = f.readline().split()
        nfa = [State(st_name) for st_name in f.readline().split()]
        int_st_name = f.readline().strip()
        initial_state = [st for st in nfa if st.name == int_st_name][0]
        fnl_st_name = f.readline().split()
        final_states = [st for st in nfa if st.name in fnl_st_name]

        lambda_count = 0
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

    for st in nfa:
        st.calc_delta()
    dfa = convert_to_dfa(nfa)
    write_to_file(dfa)
