#written in python 3.8
"""
File crawler for dynamic file path
    -aikkai
"""
import os, collections.abc, collections
def __getfiles__(*, fullpath:bool = False, restrict: collections.abc.Iterable = (''), includeOnly: bool = False, **kwargs):
        """finds all files inside of working directory and returns it as a dictionary
        **kwargs
         >fullpath : bool = False | Gets Fullpath
         >restrict : tuple = None | Exclude specific file types
        """
        paths = dict()
        p = '' if fullpath == True else os.getcwd()
        if isinstance(restrict, str): restrict = tuple([restrict if restrict.startswith('.') else f'.{restrict}'])
        elif isinstance(restrict, collections.abc.Iterable): restrict = tuple([ext if ext.startswith('.') else f'.{ext}' for ext in restrict if isinstance(ext, str)])
        else: raise TypeError("'restrict' should be a instance of the tuple class")
        paths['working directory'] = os.getcwd()
        if includeOnly != True: #ugly solution but efficiency >
            for root, _, files in os.walk(os.getcwd()):
                for file in files:
                    if not file.endswith(restrict): paths[file] = os.path.join(root, file).replace(p, '')
        else: #boilerplate
            for root, _, files in os.walk(os.getcwd()):
                for file in files:
                    if file.endswith(restrict): paths[file] = os.path.join(root, file).replace(p, '')
        return paths
if __name__ == '__main__':
    print(__getfiles__())