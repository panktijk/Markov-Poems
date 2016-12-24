import markovify
import pronouncing
import random
from nltk.corpus import wordnet as wn

def generate_poem():
    poem = ['']*4
    while True:
        candidates = generate_candidates()
        line2, line4, new_candidates = generate_rhyming_lines(candidates)
        if new_candidates:
            poem[1] = line2
            poem[3] = line4
            poem[0] = random.choice(new_candidates)
            new_candidates.remove(poem[0])
            poem[2] = random.choice(new_candidates)
            return poem
            
def generate_candidates():
    with open("poems.txt") as f:
        text = f.read()
        # Build the model.
        text_model = markovify.NewlineText(text)   
    candidates = []
    for i in range(20):
        line = text_model.make_short_sentence(60).lower()
        phones = []
        print line
        for word in line.split():
            word = ''.join(e for e in word if e.isalnum())
            print word
            print pronouncing.phones_for_word(word)
            if pronouncing.phones_for_word(word): 
                phones.append(pronouncing.phones_for_word(word)[0])
                #phones = [pronouncing.phones_for_word(p)[0] for p in line.split()]
                if sum([pronouncing.syllable_count(p) for p in phones]) == 10:
                    print line
                    candidates.append(line)  
    return candidates

def generate_rhyming_lines(candidates):
    curr_candidates = candidates
    line_num = 0
    while line_num < len(candidates):
        print 'curr_candidates: ', curr_candidates
        print 'line_num: ', line_num        
        line2, line4 = find_rhyming_lines(curr_candidates)
        if line2 or line4:
            curr_candidates.remove(line2)
            curr_candidates.remove(line4)
            return line2, line4, curr_candidates
        curr_candidates = get_synonyms(candidates, line_num)
        line_num += 1
    return None, None, None
    
def find_rhyming_lines(candidates):
    for candidate in candidates:
        line4_candidates = [c4 for c4 in candidates if (c4 != candidate) & (check_if_line_rhymes(candidate, c4))]
        if line4_candidates:
            return candidate, random.choice(line4_candidates)
    return None, None
    
def get_synonyms(candidates, line_num):
    line = candidates[line_num]
    words = line.split()
    last_word = ''.join(e for e in words[-1] if e.isalnum())
    word_synsets = wn.synsets(last_word)
    if word_synsets:
        word_syns = wn.synsets(last_word)[0].lemma_names()
        for syn in word_syns:
            if ('_' not in syn ) & (syn != words[-1]):
                words[-1] = syn
                candidates[line_num-1] = ' '.join(words)
                break
    return candidates
    
def check_if_line_rhymes(line1, line2):
    word1 = line1.split()[-1]
    word1 = ''.join(e for e in word1 if e.isalnum())
    word2 = line2.split()[-1]
    word2 = ''.join(e for e in word2 if e.isalnum())
    return (word2 in pronouncing.rhymes(word1))
    
poem = generate_poem()
for line in poem:
    print line
    

