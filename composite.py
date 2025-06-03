import copy
import logging
#logging.basicConfig(level=logging.DEBUG)
## logging.basicConfig(level=logging.CRITICAL)
#logger = logging.getLogger(__name__)

class ExitException(Exception):
    def __init__(self,*kwargs):
        Exception.__init__(self,*kwargs)

class Component(object):
    def __init__(self, *args, **kw):
        pass
    def draw(self):
        pass
##    def add(self, child):
##        pass
##    def remove(self, child):
##        pass
##    def get_child(self,index) :
##        pass

class Leaf(Component):
    def __init__(self, *args, **kw):
        Component.__init__(self, *args, **kw)
    def draw(self):
        pass

class Composite(Component):
    def __init__(self,children=None):
        if type(children) is dict:
            self.children=copy(children)
        else:
            self.children={}
    def __repr__(self):
        return "<Composite('{}')>".format(self.children)
    def draw(self):
        for child in self.children.values():
            child.draw()
    def add(self,name,child) :
        self.children[name]=child
    def remove(self,name):
        del self.children[name]
    def get_child(self,name) :
        result=None
        if name in self.children.keys() :
            result=self.children[name]
        else :
            for key,child in self.children.items():
                # logger.debug("get_child() : {} ".format(key))
                if hasattr(child,"get_child") :
                    result=child.get_child(name)
                    # logger.debug("get_child() : {} ".format(key))
                    # print("get_child() : {} ".format(result))
                    if result :
                        # logger.debug("get_child() : break ")
                        break
        return result
    
    def get_children_names(self,names=[]) :
        for name,child in self.children.items():
            names.append(name)
            if hasattr(child,"get_child") :
                    child.get_children_names(names)
        return names      

