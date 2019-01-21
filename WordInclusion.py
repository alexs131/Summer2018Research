from graphviz import Digraph
from collections import defaultdict

class WordGraph:
    def __init__(self, word): # word as string
        self.states = len(word) + 1
        self.graph = []
        self.addWord(word)
    def addWord(self,word):
        for i in range(len(word)):
            self.graph.append((i,i+1,word[i]))

word = WordGraph('aaba')
word1 = WordGraph('aaabbab')
word2 = WordGraph('aaabcaa')

ecg = WordGraph('cdedcccbgjgbcccccceefgfeecccccccccccccccccc')
#print(len(ecg))
print(word.graph)

class FSA:
    def __init__(self,numStates,edges,acceptStates): #edges as (u,v,letter seen) acceptStates as set of final
        self.states = numStates
        self.graph = defaultdict(set)
        self.addEdges(edges)
        self.accept = acceptStates
    def addEdges(self,edges):
        for (u,v,letter) in edges:
            self.graph[(u,letter)].add(v)
    def epsilonClosure(self,s):
        stack = [s]
        visited = [s]
        while stack:
            state = stack.pop()
            for v in self.graph[s,'epsilon']:
                if v not in visited:
                    stack.append(v)
                    visited.append(v)
        return visited
ekg = FSA(44,[(0,1,'b'),(0,1,'c'),(0,1,'d'),(1,2,'c'),(1,2,'d'),(2,3,'d'),(2,3,'e'),
            (3,4,'c'),(3,4,'d'),(4,5,'c'),(4,5,'d'),(5,6,'c'),(5,6,'d'),(6,7,'c'),(6,7,'d'),(6,7,'b'),
            (7,8,'b'),(7,8,'c'),(7,8,'d'),(8,9,'f'),(8,9,'g'),(8,9,'h'),(9,10,'j'),(9,10,'k'),
            (10,11,'f'),(10,11,'g'),(10,11,'h'),(11,12,'a'),(11,12,'b'),(11,12,'c'),
            (12,13,'c'),(12,13,'d'),(13,14,'c'),(13,14,'d'),(14,15,'c'),(14,15,'d'),(15,16,'c'),
            (15,16,'d'),(16,17,'c'),(16,17,'d'),(17,18,'c'),(17,18,'d'),(18,19,'e'),(19,20,'e'),(19,20,'f'),
            (20,21,'e'),(20,21,'f'),(21,22,'e'),(21,22,'f'),(21,22,'g'),(22,23,'e'),(22,23,'f'),(23,24,'e'),
            (23,24,'f'),(24,25,'e'),(25,26,'c'),(25,26,'d'),(26,27,'c'),(26,27,'d'),(27,28,'c'),(27,28,'d'),
            (28,29,'c'),(28,29,'d'),(29,30,'c'),(29,30,'d'),(30,31,'c'),(30,31,'d'),(31,32,'c'),(31,32,'d'),
            (32,33,'c'),(32,33,'d'),(33,34,'c'),(33,34,'d'),(34,35,'c'),(34,35,'d'),(35,36,'c'),(35,36,'d'),
            (36,37,'c'),(36,37,'d'),(37,38,'c'),(37,38,'d'),(38,39,'c'),(38,39,'d'),(39,40,'c'),(39,40,'d'),
            (40,41,'c'),(40,41,'d'),(41,42,'c'),(41,42,'d'),(42,0,'c'),(42,0,'d')
            ],{0})
alphabet = ['a','b','c','d','e','f','g','h','i','j','k']
for i in range(ekg.states):
    print(i)
    for char in alphabet:
        print(char)
        if len(ekg.graph[(i,char)]) == 0:
            ekg.graph[(i,char)].add(43)

''' ekgGraph = Digraph(comment='EKG DFA')
for node,letter in ekg.graph:
    for edge in ekg.graph[node,letter]:
        ekgGraph.edge(str(node),str(edge),label=letter)

ekgGraph.render('test-output/ekg-graph.gv', view=True)
'test-output/ekg-graph.gv.pdf' '''

fsa = FSA(2,[(0,1,'a'),(1,0,'a'),(0,0,'b'),(1,1,'b')],{0})
fsa1 = FSA(3,[(0,0,'a'),(0,1,'b'),(1,0,'b'),(1,2,'a'),(2,2,'b'),(2,1,'a')],{0})
fsa2 = FSA(3,[(0,0,'a'),(0,0,'c'),(0,1,'b'),(1,0,'c'),(1,2,'a'),(1,2,'b'),(2,2,'a'),(2,2,'b'),(2,2,'c')],{0})
class Transducer:
    def __init__(self,numStates,edges): #edges as (u,v,weight,input,output)
        self.states = numStates
        self.graph = defaultdict(set)
        self.addEdges(edges)
    def epsilonClosure(self,s):
        stack = [s]
        visited = set((s,0))
        while stack:
            state = stack.pop()
            for v,w,o in self.graph[state,'epsilon']:
                if (v,w) not in visited:
                    stack.append(v)
                    visited.add((v,w))
        return visited

    def addEdges(self,edges):
        for (u,v,weight,(inp,output)) in edges:
            self.graph[(u,inp)].add((v,weight,output))
    #def getOutputChar(self,edges,)
    def generate_edges(self):
        edlist = []
        for state in self.graph:
            for edge in self.graph[state]:
                edlist.append((state, edge))
        return edlist

trans3 = Transducer(1,[(0,0,0,('a','a')),(0,0,0,('b','b')),(0,0,0,('c','c')),(0,0,0,('d','d')),
         (0,0,0,('e','e')),(0,0,0,('f','f')),(0,0,0,('g','g')),(0,0,0,('h','h')),(0,0,0,('i','i')),
         (0,0,0,('j','j')),(0,0,0,('k','k')),(0,0,1,('a','b')),(0,0,1,('b','a')),(0,0,1,('b','c')),
         (0,0,1,('c','b')),(0,0,1,('c','d')),(0,0,1,('d','c')),(0,0,1,('d','e')),(0,0,1,('e','d')),
         (0,0,1,('e','f')),(0,0,1,('f','e')),(0,0,1,('f','g')),(0,0,1,('g','f')),(0,0,1,('g','h')),
         (0,0,1,('h','g')),(0,0,1,('h','i')),(0,0,1,('i','h')),(0,0,1,('i','j')),(0,0,1,('j','i')),
         (0,0,1,('j','k')),(0,0,1,('k','j'))])


trans = Transducer(1,[(0,0,1,('a','b')),(0,0,1,('b','c')),(0,0,0,('a','a')),(0,0,2,('c','a')),(0,0,2,('a','c')),
                       (0,0,0,('b','b')),(0,0,0,('c','c'))])
trans1 = Transducer(2,[(0,0,1,('a','b')),(0,0,0,('a','a')),(0,1,2,('b','a')),(0,1,3,('a','b')),
                      (1,1,1,('a','b')),(1,1,0,('a','a')),(1,0,2,('b','a')),(1,0,3,('a','b'))])
print(trans.generate_edges())


class WordTransducerProduct:
    def __init__(self,wordGraph,transducer,fsa):
        self.graph = defaultdict(set)
        self.addEdges(wordGraph,transducer,fsa)
        self.final = fsa.accept
        self.getStates = self.getStates()
        self.numStates = self.numStates()
        self.hashed = self.hashTuple()
        self.wordlen = wordGraph.states
    def addEdges(self,wordGraph,transducer,fsa): #(edge from word state,trans state to (nextWord,nextTrans,letter,cost))
        tracker = {(0,0)} #maintains states to be visited as tuple of (transducer,fsa)
        for edge in wordGraph.graph:
            '''newStates1 = set()
            for state,fsas in tracker:
                visit = transducer.epsilonClosure(state)
                visit1 = fsa.epsilonClosure(fsas)
                for s,cost in visit:
                    for f in visit1:
                        newStates1.add((s,f))
                        self.graph[(edge[0],state,fsas)].add((edge[0],s,f,'epsilon',cost))

            tracker = newStates1'''
            newStates1 = set()
            inp = edge[2]
            for state,fsas in tracker:
                #print(tracker)
                #Add here for epsilon transtions actually unneeded

                for ed in transducer.graph[state,inp]:
                    nextPossState = ed[0]
                    #newStates.add(nextPossState)
                    letter = ed[2]
                    cost = ed[1]
                    #Could add in here for epsilon transition
                    for e in fsa.graph[fsas,letter]:
                        newStates1.add((nextPossState,e))
                            #newFSA.add(e)
                        #self.graph[(edge[1],ed[0])].add((edge[0],state,ed[2][1],ed[1]))
                        #print((edge[0],state,fsas,edge[1],nextPossState,e,letter,cost))
                        self.graph[(edge[0],state,fsas)].add((edge[1],nextPossState,e,letter,cost))
                        #(edge from word state,trans state,fsa state to (nextWord,nextTrans,nextFsa,letter,cost))
            tracker = newStates1
    def getStates(self):
        numStates = set()
        for node in self.graph:
            if node not in numStates:
                numStates.add(node)
            for (u,v,w,letter,cost) in self.graph[node]:
                if (u,v,w) not in numStates:
                    numStates.add((u,v,w))
        return numStates
    def numStates(self):
        return len(self.getStates)
    def hashTuple(self):
        vertices = dict()
        count = 0
        for state in self.getStates:
            vertices[state] = count
            count += 1
        return vertices

    def generate_edges(self):
        edlist = []
        for state in self.graph:
            for edge in self.graph[state]:
                edlist.append((state, edge))
        return edlist
    def topologicalSort(self,v,visited,stack,convertedGraph):
        visited[v] = True
        if v in convertedGraph.keys():
            for node,letter,cost in convertedGraph[v]:
                if visited[node] == False:
                    self.topologicalSort(node,visited,stack,convertedGraph)
        stack.append(v)

    def shortest(self,s,convertedGraph):
        visited = [False]*self.numStates
        stack = []
        for i in range(self.numStates):
            if visited[i] == False:
                self.topologicalSort(s,visited,stack,convertedGraph)

        dist = [float("Inf")]*self.numStates
        dist[s] = 0

        while stack:
            i = stack.pop()
            for node,cost,letter in convertedGraph[i]:
                if dist[node] > dist[i] + cost:
                    dist[node] = dist[i] + cost
        return dist
        '''for i in range(self.numStates):
            print ("%d" %dist[i]) if dist[i] != float("Inf") else  "Inf" ,'''
    def convertGraph(self):
        newGraph = defaultdict(set)
        for node in self.graph:
            for (u,v,w,cost,letter) in self.graph[node]:
                newGraph[self.hashed[node]].add((self.hashed[(u,v,w)],letter,cost))

        return newGraph
    def getEndStates(self):
        acceptStates = []
        for (w,t,f) in self.getStates:
            #print(w,t,f)
            if (w == self.wordlen-1) and f in self.final:
                acceptStates.append((w,t,f)) #self.hashed[(w,t,f)])
        return acceptStates
    def wordInclusion(self,boundary):
        distances = self.shortest(self.hashed[(0,0,0)],self.convertGraph())
        acceptStates = self.getEndStates()
        if acceptStates == []:
            return False
        for (w,t,f) in acceptStates:
            if ((float(distances[self.hashed[(w,t,f)]] / (self.wordlen-1)) <= boundary)):
                print(float(distances[self.hashed[(w,t,f)]] / (self.wordlen-1)))
                return False
        return True



nfa = FSA(2,[(0,0,'a'),(0,0,'b'),(0,1,'a')],{1})
fsa3 = FSA(6,[(0,3,'a'),(3,0,'a'),(0,1,'b'),(3,4,'b'),(1,2,'a'),(1,5,'b'),(4,5,'b'),(4,2,'a'),(2,2,'a'),
               (2,5,'b'),(5,5,'a'),(5,5,'b')],{1,2,4})
'''product = WordTransducerProduct(ecg,trans3,ekg)
print(product.graph)
ekgGr = Digraph(comment='Attempt 1')


for node in product.graph:
    for (u,v,w,l,c) in product.graph[node]:
        ekgGr.edge(str(node),str((u,v,w)))#label=word2.graph[u-1][2] + '->' + l + str(c))
ekgGr.render('test-output/ekgGr-graph.gv', view=True)
'test-output/ekgGr-graph.gv.pdf' '''
product = WordTransducerProduct(word2,trans,fsa2)
#product = WordTransducerProduct(word1,trans1,fsa3)
product1 = WordTransducerProduct(word,trans1,nfa)
print(sorted(product.generate_edges()))
print(product.hashTuple())
print(product.convertGraph())
print(product.shortest(product.hashed[(0,0,0)],product.convertGraph()))
print(product.getStates)
print(product.final)
print(product.getEndStates())
print(product.wordInclusion(0))
print(product.wordInclusion(0.25))
print(product.wordInclusion(1))
print(product.wordInclusion(1.25))
print(product.wordInclusion(2))

print(sorted(product1.generate_edges()))
print(product1.hashed)
print(product1.shortest(product1.hashed[(0,0,0)],product1.convertGraph()))
print(product1.getEndStates())
print(product1.wordInclusion(1.25))



dot = Digraph(comment='The Round Table')
dot1 = Digraph(comment='NFA')
count = 0

for node in product1.graph:
    for (u,v,w,l,c) in product1.graph[node]:
        dot1.edge(str(node),str((u,v,w)),label=l + str(c))
    #for edge in product.graph[node]:'''

'''dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')


dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')'''

'''dot.render('test-output/test-graph.gv', view=True)
'test-output/test-graph.gv.pdf' '''

dot1.render('test-output/nfa-graph.gv', view=True)
'test-output/nfa-graph.gv.pdf'
