import numpy as np
import itertools
from scipy import stats
from scipy.stats.stats import zscore

class Weat:

    def cos_similarity(self, tar, att): 
        '''
        Calculates the cosine similarity of the target variable vs the attribute
        '''
        score = np.dot(tar, att) / (np.linalg.norm(tar) * np.linalg.norm(att))
        return score


    def mean_cos_similarity(self, tar, att): 
        '''
        Calculates the mean of the cosine similarity between the target and the range of attributes
        '''
        mean_cos = np.mean([self.cos_similarity(tar, attribute) for attribute in att])
        return mean_cos


    def association(self, tar, att1, att2):
        '''
        Calculates the mean association between a single target and all of the attributes
        '''
        association = self.mean_cos_similarity(tar, att1) - self.mean_cos_similarity(tar, att2)
        return association

    def differential_association(self, t1, t2, att1, att2):
        '''
        xyz
        '''
        diff_association = np.sum([self.association(tar1, att1, att2) for tar1 in t1]) - \
                        np.sum([self.association(tar2, att1, att2) for tar2 in t2])
        return diff_association


    def effect_size(self, t1, t2, att1, att2):
        '''
        Calculates the effect size (d) between the two target variables and the attributes
        Parameters: 
            t1 (np.array): first target variable matrix
            t2 (np.array): second target variable matrix
            att1 (np.array): first attribute variable matrix
            att2 (np.array): second attribute variable matrix
        
        Returns: 
            effect_size (float): The effect size, d. 
        
        Example: 
            t1 (np.array): Matrix of word embeddings for professions "Programmer, Scientist, Engineer" 
            t2 (np.array): Matrix of word embeddings for professions "Nurse, Librarian, Teacher" 
            att1 (np.array): matrix of word embeddings for males (man, husband, male, etc)
            att2 (np.array): matrix of word embeddings for females (woman, wife, female, etc)
        '''
        combined = np.concatenate([t1, t2])
        num1 = np.mean([self.association(target, att1, att2) for target in t1]) 
        num2 = np.mean([self.association(target, att1, att2) for target in t2]) 
        combined_association = np.array([self.association(target, att1, att2) for target in combined])
        dof = combined_association.shape[0]
        denom = np.sqrt(((dof-1)*np.std(combined_association, ddof=1) ** 2 ) / (dof-1))
        effect_size = (num1 - num2) / denom
        return effect_size



    def p_value(self, t1, t2, att1, att2): 
        '''
        calculates the p value associated with the weat test
        '''
        diff_association = self.differential_association(t1, t2, att1, att2)
        target_words = np.concatenate([t1, t2])
        np.random.shuffle(target_words)

        # check if join of t1 and t2 have even number of elements, if not, remove last element
        if target_words.shape[0] % 2 != 0:
            target_words = target_words[:-1]

        partition_differentiation = []
        for i in range(10000):
            seq = np.random.permutation(target_words)
            tar1_words = seq[:len(target_words) // 2]
            tar2_words = seq[len(target_words) // 2:]
            partition_differentiation.append(
                self.differential_association(tar1_words, tar2_words, att1, att2)
                )
                
        mean = np.mean(partition_differentiation)
        stdev = np.std(partition_differentiation)
        p_val = 1 - stats.norm(loc=mean, scale=stdev).cdf(diff_association)

        # print("Mean: ", mean, "\n\n", "stdev: ", stdev, "\n\n partition ass: ", partition_differentiation, '\n\n association: ', diff_association, '\n\n p value: ', p_val)
        return p_val, diff_association, partition_differentiation

class Wefat(Weat): 

    def effect_size(self, tar, att1, att2):
        '''
        Calculates the effect size (d) between the target variable vector and the attributes

        Parameters: 
            tar (np.array):  target variable vector
            att1 (np.array): first attribute variable matrix
            att2 (np.array): second attribute variable matrix
        
        Returns: 
            effect_size (float): The effect size, d. 
        
        Example: 
            tar (np.array): Vector of word embeddings for a profession "Programmer" 
            att1 (np.array): matrix of word embeddings for males (man, husband, male, etc)
            att2 (np.array): matrix of word embeddings for females (woman, wife, female, etc)
        '''
        if len(tar)==300: # check to ensure that it is a vector, and not a matrix
            combined = np.concatenate([att1, att2])
            num = self.association(tar, att1, att2)
            cos_similarities = np.array([self.cos_similarity(tar, att) for att in combined])
            dof = cos_similarities.shape[0]
            denom = np.sqrt(((dof-1)*np.std(cos_similarities, ddof=1) **2 ) / (dof-1))
            effect_size = num / denom
            return effect_size
        else: 
            raise ValueError("Passed array is not a vector, but a matrix")

    def p_value(self, tar, att1, att2): 
        '''
        calculates the p-value associated with the wefat test
        '''
        association = self.association(tar, att1, att2)
        attributes = np.concatenate([att1, att2])
        np.random.shuffle(attributes)

        # check if join of t1 and t2 have even number of elements, if not, remove last element
        if attributes.shape[0] % 2 != 0:
            attributes = attributes[:-1]

        partition_association = []
        for i in range(10000):
            seq = np.random.permutation(attributes)
            att1_words = seq[:len(attributes) // 2]
            att2_words = seq[len(attributes) // 2:]
            partition_association.append(
                self.association(tar, att1_words, att2_words)
                )
                
        mean = np.mean(partition_association)
        stdev = np.std(partition_association)
        p_val = 1 - stats.norm(loc=mean, scale=stdev).cdf(association)
        # print("Mean: ", mean, "\n\n", "stdev: ", stdev, "\n\n partition ass: ", partition_association, '\n\n association: ', association, '\n\n p value: ', p_val)
        return p_val, association, partition_association


class Weac(Weat):

    def __init__(self, keyword_emb1, keyword_emb2, emb1_vectors, emb2_vectors):
        if len(keyword_emb1) != 300 & len(keyword_emb2) != 300:
            raise ValueError("The input vectors must have 300 dimensions for this implementation of the weac class")

        self.cos_similarities_emb1 = [self.cos_similarity(keyword_emb1, other_word_vector) for other_word_vector in emb1_vectors]
        self.cos_similarities_emb2 = [self.cos_similarity(keyword_emb2, other_word_vector) for other_word_vector in emb2_vectors]
        self.emb1_vectors = emb1_vectors
        self.emb2_vectors = emb2_vectors
        self.keyword_emb1 = keyword_emb1
        self.keyword_emb2 = keyword_emb2


    def effect_size(self):
        '''weac implementation. Returns the effect size of a single key word between two word embeddings'''
        return self.association() / np.std(self.cos_similarities_emb1 + self.cos_similarities_emb2)



    def association(self):
        return np.mean(self.cos_similarities_emb1) - np.mean(self.cos_similarities_emb2)

    
    def p_value(self):
        '''calculate the p-value through permutation testing and fitting to cdf'''

        partition_association = []

        # perform 10000 permutations
        for i in range(100):
            # concatenate the randomly swapped the embedding vectors
            embeddings_join = np.concatenate([*self._randomize_embeddings()])
            embeddings_split = np.array_split(embeddings_join, 2)

            cos_similarities_emb1 = [self.cos_similarity(self.keyword_emb1, other_word_vector) for other_word_vector in embeddings_split[0]]
            cos_similarities_emb2 = [self.cos_similarity(self.keyword_emb2, other_word_vector) for other_word_vector in embeddings_split[1]]

            partition_association.append(
                np.mean(cos_similarities_emb1) - np.mean(cos_similarities_emb2)
            )
        mean = np.mean(partition_association)
        stdev = np.std(partition_association)
        p_val = 1 - stats.norm(loc=mean, scale=stdev).cdf(self.association())
        return p_val




    def _randomize_embeddings(self):
        emb1_random_vectors = self.emb1_vectors
        emb2_random_vectors = self.emb2_vectors

        for i in range(len(emb1_random_vectors)):
            whether_to_swap = np.random.choice([True, False])
            if whether_to_swap:
                intermittent_store = emb1_random_vectors[i]
                emb1_random_vectors[i] = emb2_random_vectors[i]
                emb2_random_vectors[i] = intermittent_store

        return emb1_random_vectors, emb2_random_vectors


 
        

