import numpy as np

class Weat:

    def cos_similarity(self, tar, att): 
        '''
        Calculates the cosine similarity of the target variable vs the attribute
        
        Parameters: 
            tar (np.array): target variable vector
            att (np.array): attribute variable vector

        Returns: 
            score (float): cosine similarity score of the two vectors
        '''
        score = np.dot(tar, att) / (np.linalg.norm(tar) * np.linalg.norm(att))
        return score


    def mean_cos_similarity(self, tar, att): 
        '''
        Calculates the mean of the cosine similarity between the target and the range of attributes

        Parameters: 
            tar (np.array): target variable vector
            att (np.array): attrbute variable matrix for the an attribute
        
        Returns: 
            mean_cos (float): float type value of the mean cosine similarity between the target and the range of attributes

        Example: 
            tar (np.array): vector of word embeddings for "Programmer" 
            att (np.array): matrix of word embeddings for males (man, husband, male, etc)
        '''
        mean_cos = np.mean([self.cos_similarity(tar, attribute) for attribute in att])
        return mean_cos


    def association(self, tar, att1, att2):
        '''
        Calculates the mean association between a single target and all of the attributes

        Parameters: 
            tar (np.array): target variable vector
            att1 (np.array): attrbute variable matrix for the first attribute
            att2 (np.array): attrbute variable matrix for the second attribute
        
        Returns: 
            association (float): float type value of the association between the target (single) vs the attributes

        Example: 
            tar (np.array): vector of word embeddings for "Programmer" 
            att1 (np.array): matrix of word embeddings for males (man, husband, male, etc)
            att2 (np.array): matrix of word embeddings for females (woman, wife, female, etc)
        '''
        association = self.mean_cos_similarity(tar, att1) - self.mean_cos_similarity(tar, att2)
        return association


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
        denom = np.std(np.array([self.association(target, att1, att2) for target in combined]))

        effect_size = (num1 - num2) / denom
        return effect_size

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
            denom = np.std(np.array([self.cos_similarity(tar, attribute) for attribute in combined]))

            effect_size = num / denom
            return effect_size
        else: 
            raise ValueError("Passed array is not a vector, but a matrix")