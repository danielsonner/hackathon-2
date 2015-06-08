#quadtree space partitioning libTrueQuadSpacerary, by Jacob Roth
# in this software we will be representing all points as two-element tuples (x,y)


class BuiltQuadSpace():
    # a quadtree region that is built up from the pixel level.

    def __init__(self,x,y,size,topleft,topright,bottomleft,bottomright):
        '''construct a BuiltQuadSpace by explictily defining its subspaces'''
        self.topleft = topleft
        self.topright = topright
        self.bottomleft = bottomleft
        self.bottomright = bottomright
        
        self.x = x
        self.y = y
        self.size = size

    def query(self,x,y):
        '''returns true or false at the point'''
        
        if x > self.x+self.size or x < self.x-self.size or y > self.y+self.size or y < self.y-self.size:
            raise ValueError("Queried outside of bounds")

        if x<= self.x and y>self.y:
            return self.topleft.query(x,y)
        elif x> self.x and y>self.y:
            return self.topright.query(x,y)

        elif x<= self.x and y<=self.y:
            return self.bottomleft.query(x,y)
        elif x> self.x and y<=self.y:
            return self.bottomright.query(x,y)


    @classmethod # make a constructor that works by returning 
    def constructRecursively(cls,x,y,size,constructionFunc,resolution=1):
        '''iterate over the entire square space defined by x,y, and size
        to construct a BuiltQuadSpace that defines where in that space
        constructionFunc is true. it's recommended that size be a power of
        two so we have integer sizes all the way down to 1.'''
        if size<=resolution: # we won't be recursing any further. Make a decision and return true or false
            if constructionFunc(x,y):
                return TrueQuadSpace(x,y,size)
            else:
                return FalseQuadSpace(x,y,size)
                

        halfsize = size/2
        topleft = BuiltQuadSpace.constructRecursively(x-halfsize,y+halfsize,halfsize,constructionFunc,resolution)
        topright = BuiltQuadSpace.constructRecursively(x+halfsize,y+halfsize,halfsize,constructionFunc,resolution)
        bottomleft = BuiltQuadSpace.constructRecursively(x-halfsize,y-halfsize,halfsize,constructionFunc,resolution)
        bottomright = BuiltQuadSpace.constructRecursively(x+halfsize,y-halfsize,halfsize,constructionFunc,resolution)

        if all(map(lambda quadspace: isinstance(quadspace,TrueQuadSpace),[topleft,topright,bottomleft,bottomright])): #if all four quadrants are contiguous true, we are contiguous true
            return TrueQuadSpace(x,y,size) 
        elif all(map(lambda quadspace: isinstance(quadspace,TrueQuadSpace),[topleft,topright,bottomleft,bottomright])): #if all four quadrants are contiguous false, we are contiguous false 
            return FalseQuadSpace(x,y,size)
        else: # mixed subspace
            return cls(x,y,size,topleft,topright,bottomleft,bottomright)



class TrueQuadSpace(BuiltQuadSpace):
    ''' represents a block on which the construction function is true'''
    def __init__(self,x,y,size):
        self.x =x
        self.y=y
        self.size=size
    def query(self,x,y):
        return True

class FalseQuadSpace(BuiltQuadSpace):
    ''' represents a block on which the construction function is false'''
    def __init__(self,x,y,size):
        self.x =x
        self.y=y
    def query(self,x,y):
        return False
        self.size=size

