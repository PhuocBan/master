# import sys
# sys.path.append('/content/drive/My Drive/Colab Notebooks/MaliciousSpellingCorrection - Copy')
# from nltk import word_tokenize
from collections import Counter
import pickle
import numpy as np
# !pip install pyxDamerauLevenshtein
from pyxdameraulevenshtein import damerau_levenshtein_distance as dist
from vocab import Vocab
import os
# from tqdm import tqdm
# from unidecode import unidecode
# import re

# def dist(w1, w2):
#   w1 = unidecode(w1)
#   w2 = unidecode(w2)
#   return(damerau_levenshtein_distance(w1, w2))

# def loaikitudau(word):
#   return word[0] + re.sub('w|s|f|r|x|j', '', word[1:])


class spelling_checking(Vocab):

    def __init__(self, embedding_directory, vocabInputFile, vectorInputFile, small_corpusFile_directory, badwordsFile_directory, vecDim=300, CAND_LIMIT=4, DIST_LIMIT=2, isFunctional=False):

        self.vecDim = vecDim
        self.embedding_directory = embedding_directory
        self.vocabInputFile = vocabInputFile
        self.vectorInputFile = vectorInputFile
        self.small_corpusFile_directory = small_corpusFile_directory
        self.badwordsFile_directory = badwordsFile_directory
        self.isFunctional = isFunctional
        # self.vocab = Vocab(vecDim, embedding_directory, vocabInputFile, vectorInputFile, isFunctional) # !!
        self.CAND_LIMIT = CAND_LIMIT # 8 - if more candiates are generated, this word might be a non-sense word
        self.DIST_LIMIT = DIST_LIMIT
        # print(self.vocab)
        # self.corpus = self.vocab.vocabList[:]
        # readSmallCorpus(self.small_corpusFile_directory)
        # readBadwords(self.badwordsFile_directory)

    def readData(self):
        def readSmallCorpus(small_corpusFile_directory):
            small_corpus = []
            freq_small_corpus = []
            lines = open(small_corpusFile_directory, encoding='utf8').readlines()
            for i in lines:
                key, freq = i.split()
                small_corpus.append(key)
                freq_small_corpus.append(int(freq))
            return small_corpus, freq_small_corpus

        def readBadwords(badwordsFile_directory):
            return open(badwordsFile_directory, encoding='utf8').read().split('\n')

        def info():
            print("Corpus length         ", len(self.corpus))
            print("Small corpus length   ", len(self.small_corpus))
            print("Badwords length       ", len(self.badwords))

        self.vocab                                  = Vocab(self.vecDim, self.embedding_directory, self.vocabInputFile, self.vectorInputFile, self.isFunctional)  
        self.corpus                                 = self.vocab.vocabList[:]
        self.small_corpus, self.freq_small_corpus   = readSmallCorpus(self.small_corpusFile_directory)
        self.badwords                               = readBadwords(self.badwordsFile_directory)
        info()

    # def readBadwords(self, badwordsFile_directory):
    #     self.badwords = open(badwordsFile_directory).read().split('\n')

    # def readSmallCorpus(self, small_corpusFile_directory):
    #     small_corpus = []
    #     freq_small_corpus = []
    #     lines = open(small_corpusFile_directory).readlines()
    #     for i in lines:
    #         key, freq = i.split()
    #         small_corpus.append(key)
    #         freq_small_corpus.append(int(freq))
    #     self.small_corpus = small_corpus

    # def info():
    #     print("Corpus length         ", len(self.corpus))
    #     print("Small corpus length   ", len(self.small_corpus))
    #     print("Badwords length       ", len(self.badwords))

    def getCandFromDict(self, word):
        """
        use edit distance to generate candidates
        input: word
        output: sort_words - words sorted in frequency order with edit distance no larger than 3
                    sort_freq - sorted frequency
        """
        # word = loaikitudau(word)
        cand_words = []
        freq_list = []
        cur_dist = 0
        # print(word)
        # for i in self.small_corpus:
        #     if dist(i, word) <= self.DIST_LIMIT:
        #         cand_words.append(i)
        #         freq_list.append(self.freq_small_corpus[self.small_corpus.index(i)])

        while (cand_words == [] and cur_dist <=3):
            cur_dist += 1
            # small corpus l?? nh???ng t??? c?? ??? mi???n ????ch
            for key in self.small_corpus: # smaller corpus
                ##  levenshtein_distance: transposition = 2
                ##        if (editdistance.eval(key, word) <= DIST_LIMIT):
                ##            cand_words.append(key)

                # damerau_levenshtein_distance: transposition = 1
                if (dist(key, word) <= cur_dist):
                    cand_words.append(key)
                    freq_list.append(self.freq_small_corpus[self.small_corpus.index(key)])
            ## tr??? v??? danh s??ch c??c t??? t????ng t??? v???i dist <=3 
        
        # filter words with low frequency
        if (freq_list != [] and max(freq_list)>0):
            # 2 d??ng v?? d???ng
            cand_words = [cand_words[ind] for ind in range(len(freq_list)) if freq_list[ind] > 0]	
            freq_list = [freq for freq in freq_list if freq > 0]
            # sort words by frequency
            # sort v?? s???p x???p l???i
            sort_inds = np.argsort(freq_list)[::-1]
            sort_words = [cand_words[ind] for ind in sort_inds]
            sort_freq = [freq_list[ind] for ind in sort_inds]
        else:
            # c??ng v?? d???ng n???t
            sort_words = cand_words[:]
            sort_freq = [0] * len(cand_words)
        #print "cand_words", cand_words
        return sort_words, sort_freq

    def getCandFromDict_regularCheck(self, word, refined_corpus):
        """
        use edit distance to generate candidates
        input: word
        output: a list of candidate words
        """
        # word = loaikitudau(word)
        # t??m nh???ng t??? g???n gi???ng t??? sai ??? trong khi kho???ng c??ch ch???nh s???a nh??? nh???t
        cand_words = []
        cur_dist = 0
        while (cand_words == []):
            cur_dist += 1
            for key in refined_corpus: # smaller corpus
                if (dist(key, word) <= cur_dist):
                    cand_words.append(key)
        return cand_words

    def rawCheckOnDist(self, sent_list, raw_corpus, refined_corpus):
        """
        input: 
        sent_list: c??u c?? l???i ch??nh t???
        raw_corpus: t???p corpus g???c (t???p n??y ph???i ????ng ch??nh t???)
        refined_corpus: t???p corpus c???a domain (nh??? h??n v?? gi???i h???n h??n)
        output:
        list c??u trong ???? m???i c??u l?? list c??c word
        list c??c t??? ???? s???a v?? t??? g???c tr?????c khi s???a


        enumerate spelling correction candidates based on the edit distance
        """
        sent_token_list = []
        raw_corrections = []
        #sent list l?? c??i list c??u sai ch??nh t??? ?????u v??
        ## duy??t t???ng c??u
        print("stage 1")
        # for sent in tqdm(sent_list):
        for sent in sent_list:
            # t??ch t???ng t??? ra
            token_list = sent.strip().split()
            # g??n b??nh th?????ng
            corrected_token_list = token_list[:]
            corrections = []
            ## duy???t t???ng t???
            for ind in range(len(token_list)):
                token = token_list[ind]
                # kh??ng x??t nh???ng t??? c?? ????? d??i l???n h??n 30
                if (len(token) > 6):
                    continue
                if len(token) <=1:
                    continue
                # spelling error
                #n???u t??? kh??ng c?? trong corpus
                if (token not in raw_corpus):
                    # t??m nh???ng t??? g???n n?? nh???t trong t???p corpus c???a domain
                    cand_list = self.getCandFromDict_regularCheck(token, refined_corpus)
                    # n???u ch??? c??  1 t??? th?? add n?? v?? m???ng corrections lu??n
                    if (len(cand_list) == 1):
                        ## Ph???n n??y th??m v?? ????? lo???i nh???ng t??? sai ch??nh t??? ???? s???a kh??ng thu???c badword
                        if cand_list[0] in self.badwords:                    
                            cand_token = cand_list[0]
                            # l???y ph???n t??? duy nh???t thay th??? cho ph???n t??? ??ang x??t
                            corrected_token_list[ind] = cand_token
                            # add v?? l?? t??? k???t qu??? l?? (t??? ????? xu???t : t??? g???c sai ch??nh t???)
                            corrections.append((cand_token, token))

            # add c??c c??u k???t qu??? v??
            sent_token_list.append(corrected_token_list[:])
            # add c??c t??? ???? th??? v??
            raw_corrections.append(corrections[:])
        print("done stage 1: raw check on edit distance")
        return sent_token_list, raw_corrections   

    def cosSim(self, array1, array2):
        # t??nh cosine
        if (np.linalg.norm(array1) * np.linalg.norm(array2)) == 0:
                return 0
        return np.dot(array1, array2) / (np.linalg.norm(array1) * np.linalg.norm(array2))

    def getRelevance(self, X, w):
        X = np.nan_to_num(X)
        w = np.nan_to_num(w)
        X = np.array(X)
        X_transpose = np.transpose(X)
        coef = np.dot(np.linalg.pinv(X_transpose), w)
        w_appro = np.dot(X_transpose, coef)
        relevance = self.cosSim(w, w_appro)
        return relevance

    def weightedScoreCandidates(self, cand_words, left_context_words, right_context_words):
        """
        input: a list of words, context sequence
        output: sorted cand words, scores (both in decreasing order)
        """
        selected_cand_words, word_vecs = self.vocab.getVectors(cand_words)
        _, left_sent_vecs = self.vocab.getVectors(left_context_words)
        dist_list = range(len(left_sent_vecs))
        _, right_sent_vecs = self.vocab.getVectors(right_context_words)
        dist_list = list(dist_list) + list(range(len(right_sent_vecs)))
        sent_vecs = np.array(list(left_sent_vecs) + list(right_sent_vecs))
        if (len(sent_vecs)==0):
            # n???u t??? kh??ng c?? 2 b??n tr??i ph???i
            weighted_scores = [0] * len(selected_cand_words)
        else:
            max_dist = np.max(dist_list)
            weighted_scores = [0] * len(selected_cand_words)
            for dist in range(1, max_dist+1):
                # l???y ra c??c vetor v???i kho???ng c??ch <= dist
                subset_sent_vecs = [sent_vecs[ind] for ind in range(len(dist_list)) if dist_list[ind]<=dist]
                # sau ???? l???y ????? relevance
                scores = np.array([self.getRelevance(subset_sent_vecs, word_vec) for word_vec in word_vecs])
                weighted_scores = weighted_scores + (1.0 / dist) * scores
        sort_ind = np.argsort(weighted_scores)[::-1] # largest comes first
        sorted_cand_words = [selected_cand_words[ind] for ind in sort_ind]
        sorted_scores = [weighted_scores[ind] for ind in sort_ind]
        return sorted_cand_words, sorted_scores

    def outputCorrectionSent(self, sent_seq, context_size, correct_word, wrong_word):
        """
        correct one sentence
        input: 
        sent_seq - a list of words in a sentence
        context_size - l?? k??ch th?????c ????? l???y ng??? c???nh =4
        output: revised_sent_seq  - a list of words in a sentence
                    corr - a list of tuples (corrected_word, error_word)
            cand_corr - a list of a lis t of candidates
        """
        sent_seq = sent_seq.split()
        NUMS = "0123456789"
        word_num = len(sent_seq)
        revised_sent_seq = sent_seq[:]
        cand_corr = []
        corr = []
        recall = 0
        pre = 0
        # duy???t theo t???ng t???
        for ind in range(word_num):
            word = sent_seq[ind]
            #n???u c??u d??i h??n 30 t??? th?? b??? qua
            if (len(word) > 6):
                continue
            if len(word) <= 1:
                continue
            # ignore digits
            #n???u b??? qua n???u k?? t??? n??o c?? s??? th?? b??? qua: ????y c?? th??? b??? l??ch lu???t 
            num_flag = False
            for digit in NUMS:
                if (digit in word):
                    num_flag = True
                    break
            if (num_flag):
                continue
            sorted_cand_words = []
            #n???u word kh??ng c?? trong corpus
            if (word not in self.corpus):# !!! big corpus
                # generate candidates
                # l???y danh s??ch c??c t??? t????ng t??? c?? kho???ng c??ch ch???nh s???a <=3 trong t???p corpus train
                cand_words, sort_freq = self.getCandFromDict(word)

                # l???y 4 ???ng vi??n ?????u v?? c??ng g???n c??ng gi???ng 
                if (len(cand_words) > self.CAND_LIMIT):
                    cand_words = cand_words[:4]

                # ki???m tra
                # if word == wrong_word:
                #     # print(cand_words)
                #     if len(set(cand_words) & set(self.badwords)) >0:
                #         recall = 1
                #     # print(correct_word)
                #     # print(cand_words)
                #     if correct_word in cand_words:
                #         pre = 1
                #     return recall, pre
                # else:
                #     if len(set(cand_words) & set(self.badwords)) >0:
                #         print("T???: ", word, '\t', ' '.join(sent_seq))
                
                if word == wrong_word:
                    # print(cand_words)
                    if len(set(cand_words)) >0:
                        recall = 1
                    # print(correct_word)
                    # print(cand_words)
                    # if correct_word in cand_words:
                    #     pre = 1
                    return recall, pre
                else:
                    if len(set(cand_words)) >0:
                        print("T???: ", word, '\t', ' '.join(sent_seq))
                    
        return recall, pre
        #         # context-based detection
        #         left_context_words = []
        #         right_context_words = []
        #         # left context
        #         # l???y h???t ph???n t??? c??ch t??? ??ang x??t 4 word
        #         left_ind = ind - 1
        #         left_num = 0
        #         while (left_ind>=0 and left_num<=context_size):
        #             if (sent_seq[left_ind] in self.corpus):
        #                 left_context_words.append(sent_seq[left_ind])
        #                 left_num += 1
        #             left_ind -= 1
        #         # right context
        #         # x??t t??? ??ang x??t v??? ph???i 4 t???
        #         right_ind = ind + 1
        #         right_num = 0
        #         while (right_ind<word_num and right_num<=context_size):
        #             if (sent_seq[right_ind] in self.corpus):
        #                 right_context_words.append(sent_seq[right_ind])
        #                 right_num += 1
        #             right_ind += 1
        #         sorted_cand_words, sorted_scores = self.weightedScoreCandidates(cand_words, left_context_words, right_context_words)
        #         if (len(sorted_cand_words) > 0):
        #             ## ch??? s???a nh???ng t??? c?? trong badwords
        #             if sorted_cand_words[0] in self.badwords:            
        #                 revised_sent_seq[ind]  = sorted_cand_words[0]
        #                 corr.append((sorted_cand_words[0], word))

        #     cand_corr.append(",".join(sorted_cand_words)+" -> "+word)
        # # tr??? v??? d??nh s??ch ???? s???a, (t??? s???a + t??? g???c), log
        # return revised_sent_seq, corr, cand_corr

    def generateAlgoCandCorrection(self, sent_str_list, correct_words, wrong_words , context_size=4):
        """
        input: sent_str_list - a list of strings
        output: revised_sent_seq - a list of a list of tokens
                    revised_corrections - a list of a list of tuples
        """
        revised_sent_token = []
        revised_corrections = []
        cand_corrections = []
        # stage 1: context-free check
        # tr??? v??? c??u d???ng list t??? v?? c??c t??? ???? s???a
        # sent_token_list, corrections = self.rawCheckOnDist(sent_str_list, self.corpus, self.small_corpus)

        # stage 2: context-dependent check
        print('stage 2.')
        corrections2 = []
        sent_num = len(sent_str_list)
        # duy???t t???ng c??u
        # for sent_ind in tqdm(range(sent_num)):
        recall = 0
        pre = 0
        for sent_ind in range(sent_num):
            sent_seq = sent_str_list[sent_ind]
            r, p = self.outputCorrectionSent(sent_seq, context_size, correct_words[sent_ind], wrong_words[sent_ind])
            recall += r
            pre +=p
            # revised_sent_token.append(revised_sent_seq[:])
            # revised_corrections.append(corrections[sent_ind][:]+corr[:])
        # cand_corrections.append(cand_corr[:])
        # print("done stage 2: context-dependent check.")
        # return revised_sent_token, revised_corrections, cand_corrections, corrections
        print("Recall: ", recall*100/sent_num)
        print("Pre:    ", pre*100/recall)


BASE_DIR = os.path.dirname(r'C:\Users\Phuoc Ban\Desktop\demo\SpellChecker_Demo\Spell_Checker_App')
small_corpus_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\small_corpus.txt')
badwords_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\hate_offensive_vocab.txt')
vocab_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\vocab.txt')
vec_dir = os.path.join(BASE_DIR, r'Spell_Checker_App\SpellChecker\vec.npy')
sp = spelling_checking(r"", vocab_dir, vec_dir, small_corpus_dir, badwords_dir, CAND_LIMIT=8 )
sp.readData()

import pandas as pd  
data = pd.read_csv(r'C:\Users\Phuoc Ban\Desktop\demo\SpellChecker_Demo\Spell_Checker_App\SpellChecker\sai_chinh_ta_khong_dong_nghia.csv')
correct_words = data['correct_words']
wrong_words   = data['wrong_words']
hate_offensive_cmts = data['hate_offensive_cmts']
wrong_hate_offensive_cmts = data['wrong_hate_offensive_cmts']

correct_words = list(correct_words)
for i in range(len(correct_words)):
  correct_words[i] = correct_words[i]

# print(correct_words)


print(sp.generateAlgoCandCorrection(wrong_hate_offensive_cmts, correct_words, list(wrong_words)))











