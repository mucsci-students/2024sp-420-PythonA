'''This parser will not be an object because parsing is more of a tool for the controller
#o use than a standalone feature. As a result, it makes more sense to just have this be 
a free function with a set of helpers. '''


#general structure idea: Three phase approach
    #p1: take the first token, parse it 
    #p2: take the second token, parse it
    #p3: take everything after the hyphen and parse them as separate items
