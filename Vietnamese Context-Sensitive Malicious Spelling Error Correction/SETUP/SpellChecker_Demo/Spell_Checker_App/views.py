from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from SpellChecker.spelling_checking import spelling_checking
import re

def processing_sent(sent):
    sent = re.sub(r"(.)\1{2,}", r"\1\1", sent)
    sent = re.sub('\x01', '', sent)
    sent = re.sub('_|\s+', ' ', sent)
    sent = re.sub("""\!|\"|\#|\$|\%|\&|\||\'|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~""", '', sent)
    return sent


# Create spell checker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
small_corpus_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\small_corpus.txt')
badwords_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\hate_offensive_vocab.txt')
vocab_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\vocab.txt')
vec_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\vec.npy')
sp = spelling_checking(r"", vocab_dir, vec_dir, small_corpus_dir, badwords_dir, CAND_LIMIT=8 )
sp.readData()

# Create your views here.
def index(request):
    if request.method == 'POST':
        # print(a)
        if request.POST['Sentence'].strip() != '':
            print(request.POST['Sentence'])
            sent = [processing_sent(request.POST['Sentence'])]
            revised_sent_seq, algo_corrections, cand_corrections, one_stage_corrections = sp.generateAlgoCandCorrection(sent, 3)

            revised_sent_seq = ' '.join(revised_sent_seq[0])
            s = []
            for i in algo_corrections[0]:
                s.append(i[1] + ' -> ' +i[0])
            algo_corrections = s
            cand_corrections = cand_corrections[0]
            for i in range(len(cand_corrections)):
                cand_corrections[i] = cand_corrections[i].replace(',', ', ')
                cand_corrections[i] = cand_corrections[i].replace('->', ' -> ')

            return render(request, 'return.html', {'origin':sent[0], 'correct':revised_sent_seq, 'change':algo_corrections, 'detail':cand_corrections})


    return render(request, 'home.html')