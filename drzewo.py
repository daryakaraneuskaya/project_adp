import numpy as np

class Node():
    
    def __init__(self, left, right, nr_index, value, matrix):
        self.left = left
        self.right = right
        self.nr_index = nr_index
        self.value = value
        self.matrix = matrix
        self.probability = 0
        self.classification = None

    def insert(self, m):
        """Dodawanie calych macierzy z wartosciami do naszego drzewa,
        macierz ktora wprowadzamy musi miec na pozycji [n][-1] poprana predykcje, gdzie n jest liczba od 0 do len(m).
        Sposob podzialu na podstawie indeksu Giniego"""
        if self.check_last(m):
             self.probality = 1
             self.classification = m[0][-1]
             return
        else:
            index_G = self.index_Giniego(m)
            #if index_G[0] == 1 and index_G[1] == 0 :
                #procent_prawdopodobienstwa = {}
                #for x in m:
                    #if x[-1] in procent_prawdopodobienstwa:
                        #procent_prawdopodobienstwa[x[-1]] += 1
                    #elif x[-1] not in procent_prawdopodobienstwa:
                        #procent_prawdopodobienstwa [ x[-1]] = 1
                #self.probability = procent_prawdopodobienstwa[m[0][-1]]/ len(m)
                #return
            #else:
                #podzial na lewy i prawy i odpalenie insert dla lewego i prawego
            self.value = index_G[2]
            self.nr_index = index_G[1]
            left_branch = [x for x in m if x[index_G[1]] >= index_G[2] ]
            left_branch = [x for x in m if x[index_G[1]] < index_G[2] ]
            self.left = Node(None, None, index_G[1] , index_G [2] , left_branch)
            self.right = Node(None, None, index_G[1] , index_G [2] , right_branch)
            self.left.insert(left_branch)
            self.right.insert(right_branch)

    def check_last(self, m):
        tmp = m[0][-1]
        for x in m:
            if x[-1] != tmp:
                return False
        return True
        
    def index_Giniego(self, matrix): #OUT ( minimalny index Giniego, nr. kolumny dla ktorej parametr jest minimalny, wartosc graniczna)
        """Funkcja ktora ma liczyc index Giniego dla wybranej macierzy, podanej w postaci listy list.
            OUT tuple w postaci ( minimalny index Giniego, nr. kolumny dla ktorej parametr jest minimalny, wartosc graniczna)"""
        j = 0
        mini = (1,0,0)
        while j <= len(matrix[0]) -2:
            tmpl = [ [x[j], x[-1]] for x in matrix]
            tmpl.sort()
            wektor = [x[1] for x in tmpl ]
            mini_tmp = self.index_Giniego_wektor_liczby(wektor)
            if mini[0] > mini_tmp[0]:
                mini = (mini_tmp[0], j, matrix[mini_tmp[1]][j] )
            j += 1
        return mini
            
    def index_Giniego_wektor_liczby(self, wektor):
        """Dostaje wektor klasyfikacji posortowanych po wartosciach,
            tzn. dostaje ostatnia kolumne w ktorej znajduja sie predykcje
            OUT minimalny index wraz z pozycja"""
        dlugosc = len(wektor) -1
        warianty = {}
        for x in wektor:
            if x in warianty:
                warianty[x] += 1
            else:
                warianty[x] = 1
        mini = (1 , None)
        i = 1
        tmpl = {}
        keys = warianty.keys()
        for klucze in keys:
            tmpl[klucze] = 0
        while i <= dlugosc :
            tmpl[wektor[i]] += 1
            j = i +1
            tmp = j * (1/ tmpl[keys[0] ] ) * (1 - 1/tmpl[keys [1] ]) + (dlugosc - j) * (1 / (warianty[keys[0]]- tmpl[keys[0]])) * (1 - 1/(warianty[keys[1]]- tmpl[keys[1]]))
            if mini[0] > tmp:
                mini = (tmp, i)
            i += 1
        return mini
    
    def go_through (self, m):
        """Funkcja dostaje wektor z wartosciami przy pomocy ktorych musi zostac klasyfikowany dojendej z dowch grup"""
        if self.probability != 0:
            return self.classification
        elif m[self.nr_index] >= self.value:
            self.left.go_through(m)
        elif m[self.nr_index] < self.value:
            self.right.go_through(m)
        else:
            return "Nie idzie"

class Tree():

    def __init__(self):
        self.root = Node (self, None, None, None, None)

    def insert (self, matrix):
        self.root.insert(matrix)
    
    def go_through(self, m):
        print self.root.go_through(m)

test = [ [1 , 2, 3, 4, 5, 'TAK'] , [1 , 2, 3, 4, 5, 'TAK'], [ 1 , 2, 6, 4, 5, 'NIE'], [2 , 2, 3, 4, 5, 'NIE'] ]

d =Tree()
d.insert(test)