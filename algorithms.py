"""
.. module:: algorithms
    :synopsis: Covers algorithms for:
        * specification
        * generalization
        * elimination of candidates
"""
import yaml


def load_yaml(filename):
    with open(filename) as yaml_file:
        return yaml.load(yaml_file.read())


class SymbolicLearningSystem(object):
    def __init__(self, possibilities, learning_set):
        """
        :param possibilities: dict with name and possibilities
        :param learning_set: list of tuples with learning set (dict, bool)
        """
        self.possibilities = possibilities
        self.learning_set = learning_set
        self.general = [dict.fromkeys(self.possibilities, True)]
        self.specific = [dict.fromkeys(self.possibilities, False)]

    @classmethod
    def from_yamls(cls, possibilities, learning, *args, **kwargs):
        return cls(load_yaml(possibilities), load_yaml(learning))

    @classmethod
    def from_yaml(cls, yaml_filename, *args, **kwargs):
        return cls(**load_yaml(yaml_filename))

    @staticmethod
    def check_classification(item, example, test):
        """
        check if example (not)classifies with item by given
        """
        for key in example:
            if example[key] != item[key] and item[key] is not True:
                return not test
        return test

    def classificates_negative(self, item, example):
        return self.check_classification(item, example, False)

    def classificates_positive(self, item, example):
        return self.check_classification(item, example, True)

    def minimal_generalizations(self, items, example):
        minimal = []
        for item in items:
            hypothesis = {}
            for key in example:
                if item[key] is False or item[key] == example[key]:
                    hypothesis[key] = example[key]
                else:
                    hypothesis[key] = True
            minimal.append(hypothesis)
        return minimal if minimal else [example]

    def minimal_specializations(self, items, example):
        minimal = []
        for item in items:
            for key in example:
                for elem in [poss for poss in self.possibilities[key]
                             if poss != example[key]]:
                    hypothesis = item.copy()
                    if hypothesis[key] is True:
                        hypothesis[key] = elem
                        minimal.append(hypothesis)
        return minimal

    def is_more_general(self, hypothesis):
        for g_hypo in self.general:
            for key in hypothesis:
                if hypothesis[key] is not True and g_hypo[key] is True:
                    return True
        return False

    def is_more_specific(self, hypothesis):
        for s_hypo in self.specific:
            for key in hypothesis:
                if hypothesis[key] is not True and s_hypo[key] != hypothesis[key]:
                    return False
        return True

    @staticmethod
    def find_by_true(fun, iterable):
        counted = [hypo.values().count(True) for hypo in iterable]
        if not counted:
            return []

        search = fun(counted)
        return [elem for elem in iterable if elem.values().count(True) == search]

    def find_minimal_general(self):
        return self.find_by_true(min, self.general)

    def maximal_specific(self):
        return self.find_by_true(max, self.specific)

    def generalize(self, example):
        #Elements of G that classify example as negative are removed from G
        self.general = [
            elem for elem in self.general
            if not self.classificates_negative(elem, example)
        ]
        #Each element s of S that classifies example as negative is removed and
        #replaced by the minimal generalizations of s that classify e as positive and
        #are less general than some member of G;
        incompatible = []
        for elem in self.specific[:]:
            if self.classificates_negative(elem, example):
                self.specific.remove(elem)
                incompatible.append(elem)

        for hypothesis in self.minimal_generalizations(incompatible, example):
            if self.is_more_general(hypothesis):
                self.specific.append(hypothesis)

        # Remove more general hypotheses than others from S;
        self.specific = self.maximal_specific()
        print "Hipoteza specyficzna: ", self.specific
        print "Hipoteza ogolna: ", self.general

    def specialize(self, example):
        #Elements of S that classify example as positive are removed from S;
        self.specific = [
            elem for elem in self.specific
            if not self.classificates_positive(elem, example)
        ]

        #Each element g of G that classifies example as positive is removed and
        #replaced by the minimal specializations of g that classifies example
        #as negative and are more general than some member of S.
        incompatible = []
        for elem in self.general[:]:
            if self.classificates_positive(elem, example):
                self.general.remove(elem)
                incompatible.append(elem)

        for hypothesis in self.minimal_specializations(incompatible, example):
            if self.is_more_specific(hypothesis):
                self.general.append(hypothesis)

        # Remove less general hypotheses than others from S;
        self.general = self.find_minimal_general()

        print "Hipoteza specyficzna: ", self.specific
        print "Hipoteza ogolna: ", self.general

    def learn(self):
        """
        eliminate candidates algorithm
        """
        print "Hipoteza specyficzna: ", self.specific
        print "Hipoteza ogolna: ", self.general
        for example, right in self.learning_set:
            if right:
                print "Przyklad prawidzwy: generalizuje"
                self.generalize(example)
            else:
                print "Przyklad negatywny: specjalizuje"
                self.specialize(example)

        if not self.specific:
            return self.general
        else:
            return self.specific





if __name__ == '__main__':
    possibilities = {
        'kolor': ['czerwony', 'niebieski'],
        'rozmiar': ['maly', 'sredni', 'duzy'],
        'ksztalt': ['kolo', 'kwadrat'],
    }
    learning_set = [
        ({
            'kolor': 'czerwony',
            'rozmiar': 'duzy',
            'ksztalt': 'kolo',

        }, True),
        ({
            'kolor': 'czerwony',
            'rozmiar': 'maly',
            'ksztalt': 'kwadrat',

        }, False),
        ({
            'kolor': 'czerwony',
            'rozmiar': 'maly',
            'ksztalt': 'kolo',

        }, True),
        ({
            'kolor': 'niebieski',
            'rozmiar': 'duzy',
            'ksztalt': 'kolo',

        }, False),
        # ({
        #     'kolor': 'czerwony',
        #     'rozmiar': 'maly',
        #     'ksztalt': 'kolo',

        # }, True),
        # ({
        #     'kolor': 'czerwony',
        #     'rozmiar': 'sredni',
        #     'ksztalt': 'kolo',

        # }, False),
    ]

    # sls = SymbolicLearningSystem(possibilities, learning_set)
    # sls = SymbolicLearningSystem.from_yamls("learning_sets/possibilities.yaml",
    #                                         "learning_sets/learning_set.yaml")
    sls = SymbolicLearningSystem.from_yaml("learning_sets/place/all.yaml")
    sls.learn()
    # print "General: ", sls.general
    # print "Specific: ", sls.specific
