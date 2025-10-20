words = {}
invalid_lines = 0
with open('data//words.txt', 'r', encoding = 'utf-8-sig') as file:
    for line in file:
        thing = line.strip('\n')
        if line.count(';') == 2:
            thing = thing.split(';')
            if len(thing[0]) < 1 and len(thing[1]) < 1 and len(thing[2]) < 1:
                print('\nEmpty member(s)!!!\n')
                invalid_lines += 1
                continue
            if len(thing[1]) == len(thing[2]):
                words[thing[2].lower()] = thing[1].lower().replace('*', '_')
        else:
            print('\nLine formatted wrongly!!!\n')
            invalid_lines += 1

wordlist = list(words.keys())
answer = ''
bugged = []
hidden = []
answer_len = 0
est_vwl_left = 0
win = False

chars = {chr(ch):0 for ch in range(97, 123)}
for ch in 'ăâîșț':
    chars[ch] = 0
guessed_chars = []
len_guessed = 0
tries = 0
total_tries = 0
fail_combo = 0

consonants = 'rntlscmbpdgfvșțhzjkxywq'
len_cns = len(consonants)
vowels = 'aieuoăâî'
len_vwl = len(vowels)
diphtong = ('ea', 'oa', 'ia')
hiatus = ('ou', 'uu', 'ii', 'ao')
found_diph = set()

cns_idx = 0
vwl_idx = 0
turn = 'V'
forced = ''


def choose_turn():
    global est_vwl_left, vowels, answer_len, forced, fail_combo
    global vwl_idx, len_vwl, cns_idx, len_cns, turn

    hide = ''.join(hidden)

    for i in range(0, answer_len-1):
        v1, v2 = hide[i], hide[i+1]
        if (i, i+1) in found_diph:
            continue
        elif v1+v2 not in hiatus and v1 in vowels and v2 in vowels:
            if v1 == v2:
                continue
            elif v1+v2 in diphtong:
                est_vwl_left += 1
                found_diph.add((i, i+1))
            elif v1 not in 'ăâî' and v2 in 'iu':
                est_vwl_left += 1
                found_diph.add((i, i+1))
    
    if fail_combo >= 3:
        fail_combo = 0
        if turn == 'C' and vwl_idx < len_vwl:
            turn = 'V'
        elif turn == 'V' and cns_idx < len_cns:
            turn = 'C'
        return
    
    if est_vwl_left < 1:
        turn = 'C'

    for i in range(1, answer_len-1):
        l1, l2 = hide[i-1], hide[i+1]
        if hide[i] == '_' and '_' not in l1+l2:
            if l1 in 'cg' and l2 in 'ei':
                forced = 'h'
            elif l1 in vowels and l2 in vowels:
                turn = 'C'
            elif l1 in consonants and l2 in consonants:
                turn = 'V'
            else:
                turn = 'V'
        
    if hidden[-1] == '_' and hidden[-2] in consonants:
        turn = 'V'
    if vwl_idx >= len_vwl:
        turn = 'C'
    if cns_idx >= len_cns:
        turn = 'V'

def bot():
    global chars, vowels, vwl_idx, len_vwl, cns_idx, len_cns, turn

    if vwl_idx >= len_vwl and cns_idx >= len_cns:
        return None

    if turn == 'V':
        if vwl_idx < len_vwl:
            while vwl_idx < len_vwl and chars[vowels[vwl_idx]] != 0:
                vwl_idx += 1
            if vwl_idx < len_vwl:
                return vowels[vwl_idx]
            else:
                turn = 'C'
                return bot()
    elif turn == 'C':
        if cns_idx < len_cns:
            while cns_idx < len_cns and chars[consonants[cns_idx]] != 0:
                cns_idx += 1
            if cns_idx < len_cns:
                return consonants[cns_idx]
            else:
                turn = 'V'
                return bot()

def play():
    global win, guessed_chars, answer_len, answer, hidden, est_vwl_left, correct, fail_combo
    global turn, tries, total_tries, chars, vowels, forced, len_guessed

    while not win:
        if len_guessed == answer_len:
            print(f"The answer is: {answer}")
            print('You won!\n')
            win = True
            break
        if win:
            break
    
        for char in hidden:
            print(char, end = ' ')
        
        if forced and chars[forced] == 0:
            att = forced
            forced = ''
        else:
            att = bot()
        print(f"\nAttempt #{tries+1}\nGuess a letter: {att}")
        
        if att == None:
            print('Error!  All letters have been tried or something else went wrong...\n')
            with open('results//errors.txt', 'a', encoding = 'utf-8-sig') as file:
                file.write(answer+'\n')
            break

        matches = False
        dcrt_a = False
        for i in range(answer_len):
            if att == answer[i]:
                len_guessed += 1
                if att in vowels:
                    est_vwl_left -= 1
                hidden[i] = att
                matches = True
            if i > 0 and i < answer_len-1:
                if hidden[i] == '_':
                    dcrt_a = True

        if matches:
            print(f"\n{att.upper()} fits!\n\n")
            guessed_chars.append(att)
            chars[att] = 2
            fail_combo = 0
            if att == 'â':
                chars['î'] = 1
            elif att == 'î':
                chars['â'] = 1
        else:
            chars[att] = 1
            fail_combo += 1
            print('\nWrong!\n\n')

        if not dcrt_a and chars['â'] == 0:
            chars['â'] = 1
        if chars['î'] == 0:
            if hidden[0] != '_' or hidden[1] in vowels:
                chars['î'] = 1
            elif cns_idx >= len_cns//2:
                forced = 'î'

        tries += 1
        total_tries += 1
        choose_turn()

def reset(n):
    global vwl_idx, len_vwl, cns_idx, len_cns, turn, fail_combo, found_diph
    global win, hidden, tries, total_tries, guessed_chars, len_guessed
    global correct, est_vwl_left, chars, vowels, answer, answer_len

    answer = wordlist[n]
    hidden = list(words[answer])
    answer_len = len(answer)
    est_vwl_left = answer_len//3 + 1

    chars = {chr(ch):0 for ch in range(97, 123)}
    for ch in 'ăâîșț':
        chars[ch] = 0
       
    found_diph = set()
    guessed_chars = []
    len_guessed = 0
    tries = 0
    win = False
    vwl_idx = 0
    cns_idx = 0
    fail_combo = 0
    turn = 'V'
    for ch in hidden:
        if ch.isalpha() and chars[ch] != 2:
            chars[ch] = 2
            len_guessed += answer.count(ch)
            guessed_chars.append(ch)
            if ch in vowels:
                est_vwl_left -= answer.count(ch)

lim = len(wordlist)
game_id = 1
with open('results//results.txt', 'w', encoding = 'utf-8-sig') as file:
    file.write('game_id, tries, solution, status, guess_sequence\n\n')
with open('results//errors.txt', 'w', encoding = 'utf-8-sig') as file:
    file.write('')
for n in range(lim):
    reset(n)
    play()
    with open('results//results.txt', 'a', encoding = 'utf-8-sig') as file:
        file.write(f"{game_id}, {tries}, {''.join(hidden)}, {'OK' if win else 'FAIL'}, {''.join(guessed_chars)}\n")
    game_id += 1
with open('results//results.txt', 'a', encoding = 'utf-8-sig') as file:
    file.write(f"\nTotal tries: {total_tries}")

print(f"\n\n\n\n\nTotal attempts: {total_tries}\nAverage attempts: {total_tries//lim}\n\n")