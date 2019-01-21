from collections import defaultdict
import sys
class Graph: #data structure for finding strongly connected components

    def __init__(self,vertices,connections):
        self.V= vertices #No. of vertices
        self.graph = defaultdict(list) # default dictionary to store graph
        self.addEdges(connections)
    def addEdges(self,connections):
        for (u,v,w) in connections:
            self.addEdge(u,v)
    # function to add an edge to graph
    def addEdge(self,u,v):
        self.graph[u].append(v)

    # A function used by DFS
    def DFSUtil(self,v,visited,component):
        # Mark the current node as visited and print it
        visited[v]= True
        #print v,
        component.append(v)
        #print component
        #Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i]==False:
                self.DFSUtil(i,visited,component)
        return component


    def fillOrder(self,v,visited, stack):
        # Mark the current node as visited
        visited[v]= True
        #Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i]==False:
                self.fillOrder(i, visited, stack)
        stack = stack.append(v)


    # Function that returns reverse (or transpose) of this graph
    def getTranspose(self):
        g = Graph(self.V,[])

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j,i)
        return g
    # The main function that finds and prints all strongly
    # connected components
    def printSCCs(self):
        components = []
        stack = []
        # Mark all the vertices as not visited (For first DFS)
        visited =[False]*(self.V)
        # Fill vertices in stack according to their finishing
        # times
        for i in range(self.V):
            if visited[i]==False:
                self.fillOrder(i, visited, stack)

        # Create a reversed graph
        gr = self.getTranspose()

        # Mark all the vertices as not visited (For second DFS)
        visited =[False]*(self.V)

        # Now process all vertices in order defined by Stack
        while stack:
            i = stack.pop()
            if visited[i]==False:
                comp = gr.DFSUtil(i, visited,[])
                components.append(comp)
                #print""

        return components

connections = [(0,1,1), (0,2,10), (1,2,3),
                   (2,3,2), (3,1,0), (3,0,8)] # edge list of form u,v,w representing edge from u to v with weight w
g = Graph(4,connections)
print(g.printSCCs())
g1 = Graph(5, [(1,0,0),(0,2,0),(2,1,0),(0,3,0),(3,4,0)])
print(g1.printSCCs())

def splitComponents(graph,edgelist): #function to take edges from connected components
    components = graph.printSCCs()
    edgesComponents = []
    for comp in components:
        edgeComp = []
        for u,v,w in edgelist:
            if u in comp and v in comp:
                edgeComp.append((u,v,w))
        edgesComponents.append(edgeComp)
    return edgesComponents

print splitComponents(g1,[(1,0,0),(0,2,0),(2,1,0),(0,3,0),(3,4,0)])


class Edges: #class for Karp's algorithm, edges stored differently
    def __init__(self,numVert,edges):
        self.V = numVert
        self.edges = defaultdict(set)
        self.addEdges(edges)
    def addEdges(self,connections):
        for u,v,w in connections:
            self.edges[v].add((u,w))
    def generate_edges(self):
        edlist = []
        for node in self.edges:
            for neighbour in self.edges[node]:
                edlist.append((node, neighbour))
        return edlist

def initTable(numVert): #initialize dp table to all -1s (representing infinity)
    dp = [[-1]*numVert for _ in range(numVert+1)]
    return dp

def shortestpath(edges): #fills in dp table for shortest path from start vertex to all others of diff path lens
    dp = initTable(edges.V)
    dp[0][0] = 0
    for i in range(1,edges.V+1):
        for j in range(edges.V):
            for edge in edges.edges[j]:
                #print edge
                #print i
                if (dp[i-1][edge[0]] != -1):
                    curr_wt = dp[i-1][edge[0]] + edge[1]
                    if (dp[i][j] == -1):
                        dp[i][j] = curr_wt
                    else:
                       dp[i][j] = min(dp[i][j], curr_wt)
                #print dp
    return dp


def minAvgWeight(edges): #computes min avg weight using alg from Karp's paper
    dp = shortestpath(edges)
    avg = [-1]*edges.V
    for i in range(edges.V):
        if dp[edges.V][i] != -1:
            for j in range(edges.V):
                if dp[j][i] != -1:
                    avg[i] = max(avg[i],float(dp[edges.V][i]-dp[j][i])/float((edges.V-j)))
    print avg
    res = avg[0]
    for i in range(edges.V):
        if avg[i] != -1 and (avg[i] < res or res == -1):
            res = avg[i]
    return res

#print(minAvgWeight(4))

def minOfComponents(graph,connections): #runs the above on all the strongly connected components in a graph and returns smallest
    sccs = graph.printSCCs()
    components = splitComponents(graph,connections)
    result = sys.maxint
    i = 0
    for comp in components:
        e = Edges(len(sccs[i]),comp)
        temp = minAvgWeight(e)
        if temp < result and temp != -1:
            result = temp
        i += 1
    return result
e = Edges(5,[(1,0,1),(0,2,2),(2,1,3),(0,3,4),(3,4,5)])
print(shortestpath(e))
print(minAvgWeight(e))
print minOfComponents(g,connections)
print(minOfComponents(g1,[(1,0,1),(0,2,2),(2,1,3),(0,3,4),(3,4,5)]))
