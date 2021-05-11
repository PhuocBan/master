# import sys
# sys.path.append('/content/drive/My Drive/Colab Notebooks/MaliciousSpellingCorrection - Copy')
# from nltk import word_tokenize
from collections import Counter
import pickle
import numpy as np
# !pip install pyxDamerauLevenshtein
from pyxdameraulevenshtein import damerau_levenshtein_distance as dist
from SpellChecker.vocab import Vocab
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
            # small corpus là những từ có ở miền đích
            for key in self.small_corpus: # smaller corpus
                ##  levenshtein_distance: transposition = 2
                ##        if (editdistance.eval(key, word) <= DIST_LIMIT):
                ##            cand_words.append(key)

                # damerau_levenshtein_distance: transposition = 1
                if (dist(key, word) <= cur_dist):
                    cand_words.append(key)
                    freq_list.append(self.freq_small_corpus[self.small_corpus.index(key)])
            ## trả về danh sách các từ tương tự với dist <=3 
        
        # filter words with low frequency
        if (freq_list != [] and max(freq_list)>0):
            # 2 dòng vô dụng
            cand_words = [cand_words[ind] for ind in range(len(freq_list)) if freq_list[ind] > 0]	
            freq_list = [freq for freq in freq_list if freq > 0]
            # sort words by frequency
            # sort và sắp xếp lại
            sort_inds = np.argsort(freq_list)[::-1]
            sort_words = [cand_words[ind] for ind in sort_inds]
            sort_freq = [freq_list[ind] for ind in sort_inds]
        else:
            # cũng vô dụng nốt
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
        # tìm những từ gần giống từ sai ở trong khi khoảng cách chỉnh sửa nhỏ nhất
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
        sent_list: câu có lỗi chính tả
        raw_corpus: tập corpus gốc (tập này phải đúng chính tả)
        refined_corpus: tập corpus của domain (nhỏ hơn và giới hạn hơn)
        output:
        list câu trong đó mỗi câu là list các word
        list các từ đã sửa và từ gốc trước khi sửa


        enumerate spelling correction candidates based on the edit distance
        """
        sent_token_list = []
        raw_corrections = []
        #sent list là cái list câu sai chính tả đầu vô
        ## duyêt từng câu
        print("stage 1")
        # for sent in tqdm(sent_list):
        for sent in sent_list:
            # tách từng từ ra
            token_list = sent.strip().split()
            # gán bình thường
            corrected_token_list = token_list[:]
            corrections = []
            ## duyệt từng từ
            for ind in range(len(token_list)):
                token = token_list[ind]
                # không xét những từ có độ dài lớn hơn 30
                if (len(token) > 30):
                    continue
                if len(token) <=1:
                    continue
                # spelling error
                #nếu từ không có trong corpus
                if (token not in raw_corpus):
                    # tìm những từ gần nó nhất trong tập corpus của domain
                    cand_list = self.getCandFromDict_regularCheck(token, refined_corpus)
                    # nếu chỉ có  1 từ thì add nó vô mảng corrections luôn
                    if (len(cand_list) == 1):
                        ## Phần này thêm vô để loại những từ sai chính tả đã sửa không thuộc badword
                        if cand_list[0] in self.badwords:                    
                            cand_token = cand_list[0]
                            # lấy phần tử duy nhất thay thế cho phần tử đang xét
                            corrected_token_list[ind] = cand_token
                            # add vô là từ kết quả là (từ đề xuất : từ gốc sai chính tả)
                            corrections.append((cand_token, token))

            # add các câu kết quả vô
            sent_token_list.append(corrected_token_list[:])
            # add các từ đã thế vô
            raw_corrections.append(corrections[:])
        print("done stage 1: raw check on edit distance")
        return sent_token_list, raw_corrections   

    def cosSim(self, array1, array2):
        # tính cosine
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
            # nếu từ không có 2 bên trái phải
            weighted_scores = [0] * len(selected_cand_words)
        else:
            max_dist = np.max(dist_list)
            weighted_scores = [0] * len(selected_cand_words)
            for dist in range(1, max_dist+1):
                # lấy ra các vetor với khoảng cách <= dist
                subset_sent_vecs = [sent_vecs[ind] for ind in range(len(dist_list)) if dist_list[ind]<=dist]
                # sau đó lấy độ relevance
                scores = np.array([self.getRelevance(subset_sent_vecs, word_vec) for word_vec in word_vecs])
                weighted_scores = weighted_scores + (1.0 / dist) * scores
        sort_ind = np.argsort(weighted_scores)[::-1] # largest comes first
        sorted_cand_words = [selected_cand_words[ind] for ind in sort_ind]
        sorted_scores = [weighted_scores[ind] for ind in sort_ind]
        return sorted_cand_words, sorted_scores

    def outputCorrectionSent(self, sent_seq, context_size):
        """
        correct one sentence
        input: 
        sent_seq - a list of words in a sentence
        context_size - là kích thước để lấy ngữ cảnh =4
        output: revised_sent_seq  - a list of words in a sentence
                    corr - a list of tuples (corrected_word, error_word)
            cand_corr - a list of a lis t of candidates
        """
        NUMS = "0123456789"
        word_num = len(sent_seq)
        revised_sent_seq = sent_seq[:]
        cand_corr = []
        corr = []
        # duyệt theo từng từ
        for ind in range(word_num):
            word = sent_seq[ind]
            #nếu câu dài hơn 30 từ thì bỏ qua
            if (len(word) > 30):
                continue
            if len(word) <= 1:
                continue
            # ignore digits
            #nếu bỏ qua nếu kí tự nào có số thì bỏ qua: đây có thể bị lách luật 
            num_flag = False
            for digit in NUMS:
                if (digit in word):
                    num_flag = True
                    break
            if (num_flag):
                continue
            sorted_cand_words = []
            #nếu word không có trong corpus
            if (word not in self.corpus):# !!! big corpus
                # generate candidates
                # lấy danh sách các từ tương tự có khoảng cách chỉnh sửa <=3 trong tập corpus train
                cand_words, sort_freq = self.getCandFromDict(word)
                # lấy 4 ứng viên đầu vì càng gần càng giống 
                if (len(cand_words) > self.CAND_LIMIT):
                    cand_words = cand_words[:4]
                # context-based detection
                left_context_words = []
                right_context_words = []
                # left context
                # lấy hết phần tử cách từ đang xét 4 word
                left_ind = ind - 1
                left_num = 0
                while (left_ind>=0 and left_num<=context_size):
                    if (sent_seq[left_ind] in self.corpus):
                        left_context_words.append(sent_seq[left_ind])
                        left_num += 1
                    left_ind -= 1
                # right context
                # xét từ đang xét về phải 4 từ
                right_ind = ind + 1
                right_num = 0
                while (right_ind<word_num and right_num<=context_size):
                    if (sent_seq[right_ind] in self.corpus):
                        right_context_words.append(sent_seq[right_ind])
                        right_num += 1
                    right_ind += 1
                sorted_cand_words, sorted_scores = self.weightedScoreCandidates(cand_words, left_context_words, right_context_words)
                if (len(sorted_cand_words) > 0):
                    ## chỉ sửa những từ có trong badwords
                    if sorted_cand_words[0] in self.badwords:            
                        revised_sent_seq[ind]  = sorted_cand_words[0]
                        corr.append((sorted_cand_words[0], word))

            cand_corr.append(",".join(sorted_cand_words)+" -> "+word)
        # trả về dánh sách đã sửa, (từ sửa + từ gốc), log
        return revised_sent_seq, corr, cand_corr

    def generateAlgoCandCorrection(self, sent_str_list, context_size=4):
        """
        input: sent_str_list - a list of strings
        output: revised_sent_seq - a list of a list of tokens
                    revised_corrections - a list of a list of tuples
        """
        revised_sent_token = []
        revised_corrections = []
        cand_corrections = []
        # stage 1: context-free check
        # trả về câu dạng list từ và các từ đã sửa
        sent_token_list, corrections = self.rawCheckOnDist(sent_str_list, self.corpus, self.small_corpus)

        # stage 2: context-dependent check
        print('stage 2.')
        corrections2 = []
        sent_num = len(sent_token_list)
        # duyệt từng câu
        # for sent_ind in tqdm(range(sent_num)):
        for sent_ind in range(sent_num):
            sent_seq = sent_token_list[sent_ind]
            revised_sent_seq, corr, cand_corr = self.outputCorrectionSent(sent_seq, context_size)
            revised_sent_token.append(revised_sent_seq[:])
            revised_corrections.append(corrections[sent_ind][:]+corr[:])
        cand_corrections.append(cand_corr[:])
        print("done stage 2: context-dependent check.")
        return revised_sent_token, revised_corrections, cand_corrections, corrections












