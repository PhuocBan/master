from SpellChecker.spelling_checking import spelling_checking
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(BASE_DIR)

small_corpus_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\small_corpus.txt')
badwords_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\hate_offensive_vocab.txt')
vocab_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\vocab.txt')
vec_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\vec.npy')
sp = spelling_checking(r"", vocab_dir, vec_dir, small_corpus_dir, badwords_dir, CAND_LIMIT=8 )

sp.readData()

error_sent_list = ['Tụi m chết với taooo']
revised_sent_seq, algo_corrections, cand_corrections = sp.generateAlgoCandCorrection(error_sent_list, 3)

print(revised_sent_seq)
print(algo_corrections)
print(cand_corrections)