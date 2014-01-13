
class Base():
    """
    The base class contains parameters and function which has to be used by all other
    classes. These are some global definitions
    """
    
    def __init__(self):
        
        #=======================================================================
        # Object Types
        # Used for counting the objects
        #=======================================================================
        self.objTypes = [
                           "ags",
                           "fac",
                           "for",
                           "lin",
                           "obj",
                           "pol",
                           "str"]