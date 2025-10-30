import math

# Read training data
def read_aspell_data():
    spellings = {}
    with open("aspell.txt", "r") as file:
        for line in file:
            line = line.strip()
            if ":" in line:
                correct, misspelled = line.split(":", 1) 
                values = misspelled.strip().split()
                spellings[correct.strip()] = values
    return spellings


# Emission Probabilities
def calc_emission_prob(spellings):
    emissions = {}
    for correct, typos in spellings.items():
        for typo in typos:
            # Edge case: Misspelled word is of different than the correct word
            length = min(len(correct), len(typo))
            for i in range(length):
                c = correct[i]
                t = typo[i]

                if c not in emissions:
                    emissions[c] = {}
                if t not in emissions[c]:
                    emissions[c][t] = 1
                else:
                    emissions[c][t] += 1

    # now turn counts into probabilities
    for c in emissions:
        total = 0
        for t in emissions[c]:
            total += emissions[c][t]
        for t in emissions[c]:
            emissions[c][t] = emissions[c][t] / total
    return emissions


# Transition Probabilities
def calc_transition_prob(spellings):
    transitions = {}
    # go through every correct word
    for word in spellings:
        if len(word) == 0:
            continue

        # start -> first letter
        first = word[0]
        if "START" not in transitions:
            transitions["START"] = {}
        if first not in transitions["START"]:
            transitions["START"][first] = 1
        else:
            transitions["START"][first] += 1

        # letter -> next letter
        for i in range(len(word) - 1):
            a = word[i]
            b = word[i + 1]

            if a not in transitions:
                transitions[a] = {}
            if b not in transitions[a]:
                transitions[a][b] = 1
            else:
                transitions[a][b] += 1

        # last letter -> END
        last = word[-1]
        if last not in transitions:
            transitions[last] = {}
        if "END" not in transitions[last]:
            transitions[last]["END"] = 1
        else:
            transitions[last]["END"] += 1

    # now make probabilities
    probs = {}
    for a in transitions:
        probs[a] = {}
        total = 0
        for b in transitions[a]:
            total += transitions[a][b]
        for b in transitions[a]:
            probs[a][b] = transitions[a][b] / total

    return probs


# Uses emission and transition probabilities to decode the word
def viterbi(word, emission_probs, transition_probs):
    states = list(emission_probs.keys())
    small_num = 0.0001  
    table = [{}]
    path = {}
    for s in states:
        # Handles the first letter of the input word
        emission = emission_probs.get(s, {}).get(word[0], small_num)
        start_prob = transition_probs.get("START", {}).get(s, small_num) 
        table[0][s] = math.log(start_prob) + math.log(emission)
        path[s] = [s]

    # Recursion across all letters
    for t in range(1, len(word)):
        table.append({})
        new_path = {}
        for s in states:
            emission = emission_probs.get(s, {}).get(word[t], small_num)
            best_prob = float("-inf")
            prev_state = None
            for prev in states:
                transition = transition_probs.get(prev, {}).get(s, small_num)
                prob = table[t-1][prev] + math.log(transition) + math.log(emission)
                if prob > best_prob:
                    best_prob = prob
                    prev_state = prev
            table[t][s] = best_prob
            new_path[s] = path[prev_state] + [s]
        path = new_path

    best_score = float("-inf")
    best_state = None

    # Checks which final letter path makes the most sense? Then adds those letters together into the “corrected” word
    for s in states:
        end_prob = transition_probs.get(s, {}).get("END", small_num)
        prob = table[-1][s] + math.log(end_prob)
        if prob > best_score:
            best_score = prob
            best_state = s
    return "".join(path[best_state])


# Splits user input into individual words and calls viterbi()
def correct_input_spelling(emission_probs, transition_probs):
    user_input = input("Enter text to correct: ")
    words = user_input.strip().split()
    corrected_words = []

    for word in words:
        corrected = viterbi(word, emission_probs, transition_probs)
        corrected_words.append(corrected)

    print("Corrected text:", " ".join(corrected_words))


# Main driver
spellings = read_aspell_data()
emissions = calc_emission_prob(spellings)
transitions = calc_transition_prob(spellings)
correct_input_spelling(emissions, transitions)



