from copy import deepcopy


def main():
    infile = open('input1.txt', 'r')
    outfile = open('output.txt', 'w')

    global kb_ori
    queries = list()

    lines = tuple(infile)
    nq = int(lines[0])

    # queries list
    for i in range(nq):
        queries.append(lines[i + 1].strip())
    ns = int(lines[nq + 1])

    # kb list
    for i in range(ns):
        kb_ori.append(lines[i + nq + 2].strip())

    for i in range(len(queries)):
        if is_entailed(queries[i]):
            # print('TRUE', file = outfile)
            print('TRUE')
        else:
            # print('FALSE', file = outfile)
            print('FALSE')

    infile.close()
    outfile.close()


def is_entailed(query):
    global terminate
    terminate = False

    kb = deepcopy(kb_ori)

    # negate the query and add it to the kb
    if query[0].isalpha():
        kb.insert(0, '~' + query)
    else:
        kb.insert(0, query[1:])

    # predicate table
    literals = dict()
    for idx, sentence in enumerate(kb):
        literals_sub = sentence.split(' | ')
        update_literals(idx, literals_sub, literals)

    idx_sentence = 0
    while not terminate:

        sentence_unify = kb[idx_sentence]

        if sentence_unify.find('|') != -1:
            idx_sentence += 1
            continue

        # unify the literal with other sentence matched

        if sentence_unify[0].isalpha():
            if unification(sentence_unify, idx_sentence, kb, literals, 1):
                return True
        else:
            if unification(sentence_unify[1:], idx_sentence, kb, literals, 0):
                return True

        if idx_sentence == len(kb) - 1:
            terminate = True

        idx_sentence += 1

    return False


def unification(literal_normalized, idx_sentence, kb, literals, negation):
    global terminate

    predicate = literal_normalized[:literal_normalized.find('(')]
    if len((literals[predicate])[negation]) == 0:
        return
    else:
        for idx in (literals[predicate])[negation]:
            if idx != idx_sentence:

                sentence_pick = kb[idx]

                # get variables in literal used for unifying
                vars_unify = literal_normalized[literal_normalized.find('(') + 1: literal_normalized.find(')')].split(
                    ',')

                # get variables in literal matched
                literals_sub_pick = sentence_pick.split(' | ')
                vars_pick = None
                for literal in literals_sub_pick:
                    if negation == 0:
                        if literal[:literal.find('(')] == predicate:
                            vars_pick = literal[literal.find('(') + 1:literal.find(')')].split(',')
                    else:
                        if literal[1:literal.find('(')] == predicate:
                            vars_pick = literal[literal.find('(') + 1:literal.find(')')].split(',')

                i = 0
                binding = True
                binding_list_unify = dict()
                binding_list_pick = dict()
                for var_pick in vars_pick:

                    if var_pick == vars_unify[i]:
                        pass
                    elif var_pick[0].islower() and vars_unify[i][0].isupper():
                        if var_pick not in binding_list_pick:
                            binding_list_pick[var_pick] = vars_unify[i]
                        else:
                            if binding_list_pick[var_pick] != vars_unify[i]:
                                binding = False
                                break
                    elif vars_unify[i][0].islower():
                        if vars_unify[i] not in binding_list_unify:
                            binding_list_unify[vars_unify[i]] = var_pick
                        else:
                            if binding_list_unify[vars_unify[i]] != var_pick:
                                binding = False
                                break
                    else:
                        binding = False
                        break
                    i += 1

                if not binding:
                    continue

                # resolution
                literals_binding = set()
                for literal in literals_sub_pick:
                    if negation == 0:
                        if literal[:literal.find('(')] != predicate:
                            substitution(literal, binding_list_pick, literals_binding)
                    else:
                        if literal[1:literal.find('(')] != predicate:
                            substitution(literal, binding_list_pick, literals_binding)

                # add the new sentence to kb
                if len(literals_binding) != 0:
                    new_sentence = ' | '.join(literals_binding)
                    if new_sentence not in kb:
                        kb.append(new_sentence)
                        # update literals
                        new_idx = len(kb) - 1
                        update_literals(new_idx, literals_binding, literals)
                else:
                    return True


def update_literals(idx, literals_sub, literals):
    for literal in literals_sub:
        end = literal.find('(')
        if literal[0].isalpha():
            predicate = literal[0:end]
            if literals.get(predicate, None) is None:
                literals[predicate] = ([idx], [])
            else:
                literals[predicate][0].append(idx)
        else:
            predicate = literal[1:end]
            if literals.get(predicate, None) is None:
                literals[predicate] = ([], [idx])
            else:
                literals[predicate][1].append(idx)


def substitution(literal, binding_list, literals_binding):
    variables = literal[literal.find('(') + 1:literal.find(')')].split(',')
    predicate_literal = literal[:literal.find('(')]
    vars_binding = list()
    for var in variables:
        if var[0].islower():
            if var in binding_list:
                vars_binding.append(binding_list[var])
            else:
                flag = True
                for k, v in binding_list.items():
                    if var == v:
                        vars_binding.append(k)
                        flag = False
                if flag:
                    vars_binding.append(var)
        else:
            vars_binding.append(var)
    literals_binding.add(predicate_literal + '(' + ','.join(vars_binding) + ')')


kb_ori = list()
terminate = False
show = False

if __name__ == "__main__": main()


