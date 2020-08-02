# DFA and NFA2DFA

Here are my Formal Languages and Automata course programming assignments.
<br>
 `dfa.py` reads a DFA from `DFA_Input_1.txt` file and gets a string from input. It outputs whether input string was accepted by DFA.
 <br>
`nfa_to_dfa.py` reads a NFA from `NFA_Input_2.txt` and writes equivalent DFA to `DFA_Output_2.txt`.

## Input file format
 
 - First line are alphabet separated by space. <br>
 - Second line are automata states separated by space. <br>
 - Third line is initial state. <br>
 - Fourth line are terminal states separated by space. <br>
 The rest of lines determines transitions. Each line specifies one transition:
 ```text
<current state> <letter> <next state>
```
 
 ## Sample input file
 
 ```text
0 1
q0 q1 q2
q0
q1
q0 λ q1
q0 0 q1
q1 0 q0
q1 1 q1
q1 0 q2
q1 1 q2
q2 0 q2
q2 1 q1
```

## More description
Full description (in Persian) is here.
