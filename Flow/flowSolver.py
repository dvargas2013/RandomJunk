#!/usr/bin/env python
_range = xrange

class State():
    def setTips(self):
        self.tips = dict()
        for i,lis in enumerate(self.data):
            for j,val in enumerate(lis):
                if val: self.tips[(i,j)] = val
        self.N = max(self.tips.values())
    def __init__(self, source):
        if type(source) == type(self):
            self.data = [[cv for cv in lis] for lis in source.data] # Stores the original data representation basically
            self.tips = source.tips.copy() # Stores where beginning of every color is (there are 2 or 0 of each color)
            self.moves = source.moves # Moves[][] you can make grouped by the keys() in tips. Basically the moves from each neighbothood around the tip
            self.score = source.score # Save the score so you don't have to recompute every time. Just in case
            self.N = source.N # The maximum color number index thing. For __str__ purposes
        elif type(source) == list:
            self.data = source
            self.setTips() # tips and N
            self.setstate() # moves and score
    def neighbors(self, i, j):
        for ii,jj in [(0,1),(1,0),(-1,0),(0,-1)]:
            if 0 <= i+ii and i+ii < len(self.data):
                if 0 <= j+jj and j+jj < len(self.data[i+ii]):
                    yield self.data[i+ii][j+jj],i+ii,j+jj
    def getMoves(self):
        if not self.moves:
            self.moves = []
            for ij,c in self.tips.items():
                cneigh = []
                for cv,ii,jj in self.neighbors(*ij):
                    if cv == 0 or ( cv == c and (ii,jj) in self.tips.keys() ):
                        cneigh.append( (c,ij,ii,jj) )
                        yield (c,ij,ii,jj)
                if cneigh: self.moves.append( cneigh )
                else:
                    self.score = -1
                    return
        else:
            for cneigh in self.moves:
                for cijij in cneigh: yield cijij
    def forcestate(self):
        if not self.moves: list(self.getMoves())
        for cneigh in list(self.moves):
            if len(cneigh) == 1: # If there is only 1 move for that color neighborhood
                self.rawmove(cneigh[0])
                self.moves = False
    def rawmove(self,cijij):
        color,ij,i,j = cijij
        self.tips.pop(ij)
        if self.data[i][j] == color:
            self.tips.pop((i,j))
        else:
            self.data[i][j] = color
            self.tips[(i,j)] = color
    def setstate(self):
        self.moves = False
        self.score = 0
        try:
            while self.score != -1 and not self.moves:
                if len(self.tips) == 0: return # Bruh you just won the game
                self.forcestate()
        except KeyError: self.score = -1
    def makeMove(self,cijij):
        self.rawmove(cijij)
        self.setstate()
        return self
    def copy(self): return State(self)
    def floodfill(self,ij):
        queue = set([ij]) 
        flooded = set([ij])
        while queue:
            ij = queue.pop()
            for cv,ii,jj in self.neighbors(*ij):
                if cv == 0 and (ii,jj) not in flooded:
                    flooded.add((ii,jj))
                    queue.add((ii,jj))
        return flooded
    def connectivityCheck(self):
        regions = []
        c2ijs = dict()
        ij2sec = dict()
        for ij,c in self.tips.items():
            for cv,ii,jj in self.neighbors(*ij):
                if cv == 0:
                    # Regions are sets with 4-connected 0-colored points
                    region = next( ((i,r) for i,r in enumerate(regions) if (ii,jj) in r) ,False)
                    if not region: # Not in any previous regions
                        region = self.floodfill((ii,jj)) 
                        regions.append( region ) # New region yay
                        region = (len(regions)-1, region)
                    sec,reg = region
                    c2ijs[c] = c2ijs.get(c,set()).union(set([ij]))
                    ij2sec[ij] = ij2sec.get(ij,set()).union(set([sec]))
        for c,ijs in c2ijs.items():
            if len(ijs) != 2: return False
            ij1, ij2 = ijs
            if len( ij2sec[ij1].intersection(ij2sec[ij2]) ) == 0:
                # Make sure that each pair of tips are capable of connecting
                return False
        reg = regions.pop(0)
        for region in regions: reg = reg.union(region)
        
        if any(any( cv == 0 and (i,j) not in reg for j,cv in enumerate(lis) ) for i,lis in enumerate(self.data)):
            return False # If there is any 0-point that isn't part of the filled regions
        return True
    def getScore(self):
        if self.score: return self.score
        if not self.moves: list(self.getMoves())
        sc1 = sum(len(cneigh) for cneigh in self.moves)
        sc2 = sum(sum(cv==0 for cv in lis) for lis in self.data)
        if sc1 == 0 and sc2 == 0: return 0
        if sc1>0 and sc2>0 and self.connectivityCheck():
            self.score = sc1+sc2
            return self.score
        else: self.score = -1
        return self.score
    def __str__(self):
        stk = set(self.tips.keys())
        l = len(str(self.N))+1
        form = "{0:^%s}"%l
        return '\n'.join( ' '.join(form.format(str(cv)+("*" if (i,j) in stk else "")) for j,cv in enumerate(lis)) for i,lis in enumerate(self.data) )

'''
As Long as State Can:
    getMoves() - generate all moves from state
    getScore() - score itself as a function of how far away it is from finishing
    makeMove() - make a move generated from getMoves()
    copy() - create or duplicate itself

Note:
    getScore() is called at least 3 times on the same state. You should probably save it somewhere
    getMoves() is technically only called once but the move status is a good way to generate score usually
    copy() could easily be implemented inside the __init__ by passing itself
    getScore() should only return negatives if it is an invalid state and 0 when it is a final/goal state
'''

def solve(state):
    states = [] # Make a list of all states so far
    state = State(state)
    while state.getScore() != 0:
        yield state.copy().data
        for move in state.getMoves():
            scopy = state.copy()
            scopy.makeMove(move)
            if scopy.getScore() >= 0: states.append(scopy)
        states = sorted( states, key = lambda x: x.getScore() ) # Sort so that lowest score is first
        state = states.pop(0) # Grab closest state to end
    yield state.data

if __name__ == '__main__':
    ar = [[1, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 3, 0], [1, 2, 0, 0, 0, 0, 0, 0]]
    # for state in solve(ar):
    #     print(state)
    #     print("")
    s = State(ar)
    print(s.connectivityCheck())