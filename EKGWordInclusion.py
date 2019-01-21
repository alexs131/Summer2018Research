from graphviz import Digraph
from collections import defaultdict
from CompositionalModels import Pmodel,PRmodel,QRSmodel,STmodel,Tmodel,blowUpP
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

ecg = WordGraph('p'*50)
#print(len(ecg))
print(word.graph)

class FSA:
    def __init__(self,model,fs,alphabet): #edges as (u,v,letter seen) acceptStates as set of final
        #self.states = numStates
        self.graph = blowUpP(alphabet,fs,([(0,0)]),model)
        #self.addEdges(edges)
        self.accept = self.addAccept()
    '''def addEdges(self,edges):
        for (u,v,letter) in edges:
            self.graph[(u,letter)].add(v)'''
    def addAccept(self):
        acc = set()
        for letter,t,s in self.graph:
            if s != 2:
                acc.add((t,s))
        return acc
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

alphabet = ['p','x','q','r','s','y','t','z','n']
pModel = FSA(Pmodel,1000,alphabet)
prModel = FSA(PRmodel,1000,alphabet)
'''qrsModel = FSA((80,100),QRSmodel,1000,alphabet)
stModel = FSA((80,120),STmodel,1000,alphabet)
tModel= FSA((100,250),Tmodel,1000,alphabet)
restModel = FSA((600,1200),Trestmodel,1000,alphabet)'''
print(pModel.graph)
print(sorted(pModel.accept))

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

trans = Transducer(1,[(0,0,0,('p','p')),(0,0,0,('x','x')),(0,0,0,('q','q')),(0,0,0,('r','r')),(0,0,0,('s','s')),
                       (0,0,0,('t','t')),(0,0,0,('y','y')),(0,0,0,('z','z')),(0,0,1,('p','q'))])


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
        tracker = {(0,0,0)} #maintains states to be visited as tuple of (transducer,fsaTime,fsaState)
        for edge in wordGraph.graph:

            newStates1 = set()
            inp = edge[2]
            for state,t,fsas in tracker:
                #print(tracker)
                #Add here for epsilon transtions actually unneeded

                for ed in transducer.graph[state,inp]:
                    nextPossState = ed[0]
                    #newStates.add(nextPossState)
                    letter = ed[2]
                    cost = ed[1]
                    #Could add in here for epsilon transition
                    for e,v in fsa.graph[letter,t,fsas]:
                        newStates1.add((nextPossState,e,v))
                            #newFSA.add(e)
                        #self.graph[(edge[1],ed[0])].add((edge[0],state,ed[2][1],ed[1]))
                        #print((edge[0],state,fsas,edge[1],nextPossState,e,letter,cost))
                        self.graph[(edge[0],state,t,fsas)].add((edge[1],nextPossState,e,v,letter,cost))
                        #(edge from word state,trans state,fsa state to (nextWord,nextTrans,nextFsa,letter,cost))
            tracker = newStates1
    def getStates(self):
        numStates = set()
        for node in self.graph:
            if node not in numStates:
                numStates.add(node)
            for (u,v,w,x,letter,cost) in self.graph[node]:
                if (u,v,w,x) not in numStates:
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
            for (u,v,w,x,cost,letter) in self.graph[node]:
                newGraph[self.hashed[node]].add((self.hashed[(u,v,w,x)],letter,cost))

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
ekg = WordTransducerProduct(ecg, trans, pModel)





ekgGraph = Digraph(comment='EKG DFA')
for u,v,w,x in ekg.graph:
    for a,b,c,d,let,cost in ekg.graph[(u,v,w,x)]:
        ekgGraph.edge(str((u,v,w,x)),str((a,b,c,d)),label=let+str(cost))

ekgGraph.render('test-output/ekg1.gv', view=True)
'test-output/ekg1.gv.pdf'
