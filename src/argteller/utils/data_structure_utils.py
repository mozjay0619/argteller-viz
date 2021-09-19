from collections import defaultdict

class nested_defaultdict(defaultdict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
    def __getattr__(self, key):
        return self[key]
    
    def __getstate__(self): 
        return self.__dict__
        
    def __setstate__(self, d): 
        self.__dict__.update(d)
        
    def get_unique_value(self, key):
        
        results = self.get_values(key)
        
        if len(results) > 1:
            raise ValueError('More than one key found')
            
        elif len(results) == 0:
            return None
        
        return results[0]
        
    def get_values(self, key):
        
        results = []
        
        for k, v in self.items():
            
            nested_defaultdict._get_values(self, key, results)
            
        return results
    
    @staticmethod
    def _get_values(node, key, results):

        for k, v in node.items():

            if k==key:
                results.append(v)
            
            if isinstance(v, dict):
                nested_defaultdict._get_values(v, key, results)

        
    def get_value_by_depth(self, depth, key):
        
        cur_depth = 0
        
        return self._get_value(depth, cur_depth, self, key)
        
    def _get_value_by_depth(self, depth, cur_depth, d, key):
        
        if depth < cur_depth:
            return None
        
        for k, v in d.items():
            
            if depth == cur_depth:
                
                if k==key:

                    return v
            
            else:
            
                if isinstance(v, dict):

                    return self._get_value(depth, cur_depth+1, v, key)