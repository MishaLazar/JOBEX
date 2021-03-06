from math import*
from decimal import Decimal


class Similarity():

    """ Five similarity measures function """

    def euclidean_distance(self,x,y):

        """ return euclidean distance between two lists """

        return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

    def manhattan_distance(self,x,y):

        """ return manhattan distance between two lists """

        return sum(abs(a-b) for a,b in zip(x,y))

    def minkowski_distance(self,x,y,p_value):

        """ return minkowski distance between two lists """

        return self.nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)),
           p_value)

    def nth_root(self,value, n_root):

        """ returns the n_root of an value """

        root_value = 1/float(n_root)
        return round (Decimal(value) ** Decimal(root_value),3)

    def cosine_similarity(self,x,y):

        """ return cosine similarity between two lists """

        numerator = sum(a*b for a,b in zip(x,y))
        denominator = self.square_rooted(x)*self.square_rooted(y)
        return round(numerator/float(denominator),3)

    def square_rooted(self,x):

        """ return 3 rounded square rooted value """

        return round(sqrt(sum([a*a for a in x])),3)

    @staticmethod
    def jaccard_similarity_original(x , y):

        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))

        union_cardinality = len(set.union(*[set(x), set(y)]))

        return intersection_cardinality/float(union_cardinality)

    @staticmethod
    def jaccard_similarity(set1, set2):
        set1 = list(map(int,set1))
        set2 = list(map(int, set2))

        matched = []
        for s in set1:
            if s in set2:
                matched.append(s)

        intersection_cardinality = len(set.intersection(*[set(set1), set(matched)]))

        union_cardinality = len(set.union(*[set(set1), set(matched)]))

        return intersection_cardinality / float(union_cardinality)