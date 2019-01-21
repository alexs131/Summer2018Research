from collections import defaultdict
from graphviz import Digraph
class inputLang:
    def __init__(self,numStates,edges,acceptStates): #edges as (u,v,letter seen) acceptStates as set of final
        self.states = numStates
        self.graph = defaultdict(set)
        self.addEdges(edges)
        self.accept = acceptStates
    def addEdges(self,edges):
        for (u,v,letter) in edges:
            self.graph[u].add((v,letter))

n = inputLang(2,[(0,0,'b'),(0,1,'a'),(1,1,'b'),(1,0,'a')],{0})
nfa = inputLang(2,[(0,0,'a'),(0,0,'b'),(0,1,'a')],{1})
n1 = inputLang(3,[(0,0,'b'),(0,0,'c'),(0,1,'a'),(1,0,'a'),(1,0,'c'),(1,2,'b'),(2,2,'a'),(2,2,'b'),(2,2,'c')],{2})
print(n.graph)

class FSA:
    def __init__(self,numStates,edges,acceptStates): #edges as (u,v,letter seen) acceptStates as set of final
        self.states = numStates
        self.graph = defaultdict(set)
        self.addEdges(edges)
        self.accept = acceptStates
    def addEdges(self,edges):
        for (u,v,letter) in edges:
            self.graph[(u,letter)].add(v)

ekg = FSA(43,[(0,1,'b'),(0,1,'c'),(0,1,'d'),(1,2,'c'),(1,2,'d'),(2,3,'d'),(2,3,'e'),
            (3,4,'c'),(3,4,'d'),(4,5,'c'),(4,5,'d'),(5,6,'c'),(5,6,'d'),(6,7,'c'),(6,7,'d'),(6,7,'b'),
            (7,8,'b'),(7,8,'c'),(7,8,'d'),(8,9,'f'),(8,9,'g'),(8,9,'h'),(9,10,'j'),(9,10,'k'),
            (10,11,'f'),(10,11,'g'),(10,11,'h'),(11,12,'a'),(11,12,'b'),(11,12,'c'),
            (12,13,'c'),(12,13,'d'),(13,14,'c'),(13,14,'d'),(14,15,'c'),(14,15,'d'),(15,16,'c'),
            (15,16,'d'),(16,17,'c'),(16,17,'d'),(17,18,'c'),(17,18,'d'),(18,19,'e'),(19,20,'e'),(19,20,'f'),
            (20,21,'e'),(20,21,'f'),(21,22,'e'),(21,22,'f'),(21,22,'g'),(22,23,'e'),(22,23,'e'),(23,24,'e'),
            (23,24,'f'),(24,25,'e'),(25,26,'c'),(25,26,'d'),(26,27,'c'),(26,27,'d'),(27,28,'c'),(27,28,'d'),
            (28,29,'c'),(28,29,'d'),(29,30,'c'),(29,30,'d'),(30,31,'c'),(30,31,'d'),(31,32,'c'),(31,32,'d'),
            (32,33,'c'),(32,33,'d'),(33,34,'c'),(33,34,'d'),(34,35,'c'),(34,35,'d'),(35,36,'c'),(35,36,'d'),
            (36,37,'c'),(36,37,'d'),(37,38,'c'),(37,38,'d'),(38,39,'c'),(38,39,'d'),(39,40,'c'),(39,40,'d'),
            (40,41,'c'),(40,41,'d'),(41,42,'c'),(41,42,'d'),(42,0,'c'),(42,0,'d')
            ],0)

fsa = FSA(2,[(0,1,'a'),(0,0,'b'),(1,0,'a'),(1,1,'b')],{1})
print(fsa.graph)
'''fsa1 = FSA(3,[(0,0,'a'),(0,1,'b'),(1,0,'b'),(1,2,'a'),(2,2,'b'),(2,1,'a')],{0}) '''
fsa2 = FSA(3,[(0,0,'a'),(0,0,'c'),(0,1,'b'),(1,0,'c'),(1,2,'a'),(1,2,'b'),(2,2,'a'),(2,2,'b'),(2,2,'c')],{0})

class Transducer:
    def __init__(self,numStates,edges): #edges as (u,v,weight,input,output)
        self.states = numStates
        self.graph = defaultdict(set)
        self.addEdges(edges)
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

trans = Transducer(1,[(0,0,1,('a','b')),(0,0,1,('b','a',))])
trans1 = Transducer(1,[(0,0,1,('a','b')),(0,0,1,('b','c')),(0,0,0,('a','a')),(0,0,2,('c','a')),(0,0,2,('a','c'))])
trans2 = Transducer(2,[(0,0,1,('a','b')),(0,0,0,('a','a')),(0,1,2,('b','a')),(0,1,3,('a','b')),
                      (1,1,1,('a','b')),(1,1,0,('a','a')),(1,0,2,('b','a')),(1,0,3,('a','b'))])
print(trans.graph)


class LanguageTransducerProduct:
    def __init__(self,n,transducer,l):
        self.graph = defaultdict(set)
        self.addEdges(n,transducer,l)
        self.nfinal = n.accept
        self.fsafinal = l.accept
        self.getStates = self.getStates()
        self.numStates = self.numStates()
        self.hashed = self.hashTuple()

    def addEdges(self,n,transducer,fsa): #(edge from word state,trans state to (nextWord,nextTrans,letter,cost))
        tracker = [(0,0,0)] #maintains states to be visited as tuple of (transducer,fsa)
        visited = set()
        while tracker:
            orig,state,fsas = tracker.pop(0)
            #newStates1 = set()
            #for orig,state,fsas in tracker:
            visited.add((orig,state,fsas))
            for edge in n.graph[orig]:
                nextState = edge[0]
                inp = edge[1]
                    #print(tracker)
                    #Add epsilon transitions
                for ed in transducer.graph[state,inp]:
                    nextPossState = ed[0]
                        #newStates.add(nextPossState)
                    letter = ed[2]
                    cost = ed[1]
                        #add epsilon transtions
                    for e in fsa.graph[fsas,letter]:
                        if((nextState,nextPossState,e) not in visited):
                            tracker.append((nextState,nextPossState,e))
                                #newFSA.add(e)
                                #self.graph[(edge[1],ed[0])].add((edge[0],state,ed[2][1],ed[1]))
                                #print((edge[0],state,fsas,edge[1],nextPossState,e,letter,cost))
                            self.graph[(orig,state,fsas)].add((nextState,nextPossState,e,inp,letter,cost))
                            #(edge from word state,trans state,fsa state to (nextWord,nextTrans,nextFsa,letter,cost))
            #tracker = newStates1
            print(tracker)
    def getStates(self):
        numStates = set()
        for node in self.graph:
            if node not in numStates:
                numStates.add(node)
            for (u,v,w,inp,letter,cost) in self.graph[node]:
                if (u,v,w) not in numStates:
                    numStates.add((u,v,w))
        return numStates
    def numStates(self):
        return len(self.getStates)
    def hashTuple(self):
        vertices = dict()
        vertices[(0,0,0)] = 0
        count = 1
        for state in (self.getStates):
            if state != (0,0,0):
                vertices[state] = count
                count += 1
        return vertices

    def generate_edges(self):
        edlist = []
        for state in self.graph:
            for edge in self.graph[state]:
                edlist.append((state, edge))
        return edlist
    def initTable(self,numVert):
        dp = [[float("Inf")]*numVert for _ in range(numVert+1)]
        return dp

    def shortestpath(self): #fills in dp table for shortest path from start vertex to all others of diff path lens
        dp = self.initTable(self.numStates)
        dp[0][0] = 0
        for i in range(1,self.numStates+1):
            for j in range(self.numStates):
                for edge in self.convertGraph1()[j]:
                    #print edge
                    #print i
                    if (dp[i-1][edge[0]] != float("Inf")):
                        curr_wt = dp[i-1][edge[0]] + edge[3]
                        if (dp[i][j] == float("Inf")):
                            dp[i][j] = curr_wt
                        else:
                           dp[i][j] = min(dp[i][j], curr_wt)
                    #print dp
        return dp

    def convertGraph(self):
        newGraph = defaultdict(set)
        for node in self.graph:
            for (u,v,w,inp,letter,cost) in self.graph[node]:
                newGraph[self.hashed[node]].add((self.hashed[(u,v,w)],inp,letter,cost))

        return newGraph
    def convertGraph1(self):
        newGraph = defaultdict(set)
        for node in self.graph:
            for (u,v,w,inp,letter,cost) in self.graph[node]:
                newGraph[self.hashed[(u,v,w)]].add((self.hashed[node],inp,letter,cost))

        return newGraph

    def getEndStates(self):
        acceptStates = []
        for w,t,f in self.getStates:
            if w in self.nfinal and f in self.fsafinal:
                acceptStates.append((w,t,f)) #self.hashed[(w,t,f)])
        return acceptStates
    def BellmanFord(self,src,graph):
        dist = [float("Inf")]*self.numStates
        dist[src] = 0
        for i in range(self.numStates-1):
            for u in graph:
                for v,inp,out,cost in graph[u]:
                    if dist[u] != float("Inf") and dist[u] + cost < dist[v]:
                        dist[v] = dist[u] + cost

        for u in graph:
            for (v,inp,out,cost) in graph[u]:
                if dist[u] != float("Inf") and dist[u] + cost < dist[v]:
                    print("Graph has negative cycle")
                    return
        return dist

    def makeNegative(self):
        graph = self.convertGraph()
        newGraph = defaultdict(set)
        for node in graph:
            for v,inp,out,cost in graph[node]:
                newGraph[node].add((v,inp,out,cost*-1))
        return newGraph

    def languageInclusion(self,boundary):
        graph = self.convertGraph()
        newGraph = defaultdict(set)
        accept = self.getEndStates()
        for node in graph:
            for v,inp,out,cost in graph[node]:
                newGraph[node].add((v,inp,out,cost-boundary))

        print(newGraph)
        dist = self.BellmanFord(0,newGraph)
        print(dist)
        if dist == None: #Negative weight cycle exists
            return False

        for state in accept:
            if dist[self.hashed[state]] <= 0: #there is a path to a final state <= 0
                return False
        return True


        '''distances = self.shortestpath()
        for state in self.getEndStates():
            index = self.hashed[state]
            for i in range(self.numStates+1):
                if distances[i][index] != -1 and float(distances[i][index] / index)'''




fsa3 = FSA(6,[(0,3,'a'),(3,0,'a'),(0,1,'b'),(3,4,'b'),(1,2,'a'),(1,5,'b'),(4,5,'b'),(4,2,'a'),(2,2,'a'),
               (2,5,'b'),(5,5,'a'),(5,5,'b')],{1,2,4})
#product = LanguageTransducerProduct(n1,trans1,fsa2)
product = LanguageTransducerProduct(nfa,trans2,fsa)
print (product.graph)
print(product.getStates)
print(product.hashed)
print(product.getEndStates())
print(product.shortestpath())
'''product = WordTransducerProduct(word2,trans,fsa2)
#product = WordTransducerProduct(word1,trans1,fsa3) '''
product1 = LanguageTransducerProduct(n1,trans1,fsa2)
print(product1.fsafinal)
print(fsa2.accept)
print (product1.graph)
print(product1.getStates)
print(product1.convertGraph1())
print(product1.getEndStates())
print(product1.shortestpath())
#print(product1.BellmanFord(0))
print(product1.hashed)
print(product1.languageInclusion(0))

ekgGraph = Digraph(comment='EKG DFA')
for node,letter in ekg.graph:
    for edge in ekg.graph[node,letter]:
        ekgGraph.edge(str(node),str(edge),label=letter)

ekgGraph.render('test-output/ekg-graph.gv', view=True)
'test-output/ekg-graph.gv.pdf'
'''
dot = Digraph(comment='The Round Table')
dot1 = Digraph(comment='NFA')

for node in product.graph:
    for (u,v,w,i,l,c) in product.graph[node]:
        dot.edge(str(node),str((u,v,w)),label=i + '->' + l + str(c))

for node in product1.graph:
    for (u,v,w,i,l,c) in product1.graph[node]:
        dot1.edge(str(node),str((u,v,w)),label=i + '->' + l + str(c))


dot.render('test-output/trial1-graph.gv', view=True)
'test-output/trial1-graph.gv.pdf'

dot1.render('test-output/lang1-graph.gv', view=True)
'test-output/lang1-graph.gv.pdf' '''
