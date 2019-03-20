from networkx.utils import open_file

class Data:
    ''' Read the data and return the results in a dictionary
    
    name of nodes:
        In the raw data, the name of nodes is represented by an integer, 
        but this confuse us when do calculation and bring some same nodeId 
        with different in graph. So, I plan to modify the nodeId to:
            {
                movieId: 1 --> movie_1
                tagId  : 1 --> tag_1
                userId : 1 --> user_1
            }


    inputs
    --------
    path : relative directory path for files 
        i.e. '/ml-latest'

    returns
    ---------
    a graph with  data in specific file

    '''
    def __init__(self, path=None):
        import os
        if path == None:
            self._path = os.getcwd() + '/ml-latest'
        else:
            self._path = os.getcwd() + str(path)
    
    def movie_tag_relevance(self, file='/genome-scores.csv', thresh = float(0)):

        ''' read data from genome-scores.csv

            return 
            -------
            a dict : {movieId:{tagId:{relevance: val},...},...}
        '''
        path = self._path + str(file)
        return self._read_edgelist(path,comments='movieId',delimiter=',',nodetype_A = 'movie', nodetype_B = 'tag', data = (('relevance', float),),thresh=thresh)

    def user_movie_rating_timestamp(self, file='/ratings.csv', thresh = float(0)):
        '''
        return
        ------
        a dict : {userId:{movieId:{rating:val, timestamp:val},...},...}
        '''
        path = self._path + str(file)
        return self._read_edgelist(path,comments='movieIduserId',delimiter=',',nodetype_A = 'user', nodetype_B = 'movie', data = (('rating', float),('timestamp',int)),thresh=thresh)

    def movie_title_genres(self, file='/movies.csv'):
        '''
        return
        ------
        {movieId:{title:[string], genres:[strings]}, ...}
        '''
        path = self._path + str(file)
        return self._read_maplist(path,comments='movieId',delimiter=',',nodetype='movie', data=(('title', str),('genres',str)))
    
    def tag_tagdef(self,file='/genome-tags.csv'):
        path = self._path + str(file)
        return self._read_maplist(path,comments='movieId',delimiter=',',nodetype='tag',data=(('tag',str)))




    @open_file(1, mode='rb')
    def _read_edgelist(self, path, comments="#", delimiter=None, nodetype_A=None, nodetype_B=None, data=True,thresh=float(0),encoding='utf-8'):
        """

        Parameters
        ----------
        path : file or string
        File or filename to read. If a file is provided, it must be
        opened in 'rb' mode.
        Filenames ending in .gz or .bz2 will be uncompressed.
        comments : string, optional
        The character used to indicate the start of a comment.
        delimiter : string, optional
        The string used to separate values.  The default is whitespace.
        create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
        nodetype : int, float, str, Python type, optional
        Convert node data from strings to specified type
        data : bool or list of (label,type) tuples
        Tuples specifying dictionary key names and types for edge data
        edgetype : int, float, str, Python type, optional OBSOLETE
        Convert edge data from strings to specified type and use as 'weight'
        encoding: string, optional
        Specify which encoding to use when reading file.

        
        """
        lines = (line.decode(encoding) for line in path)
        return self._parse_edgelist(lines, comments=comments, delimiter=delimiter,nodetype_A=nodetype_A,nodetype_B=nodetype_B,data=data,thresh=thresh)




    def _parse_edgelist(self, lines, comments='#', delimiter=None, nodetype_A=None, nodetype_B=None,data=True,thresh=float(0)):
        """

        Returns
        -------
        #G: NetworkX Graph
            #The graph corresponding to lines
        edgelist : dict

        """

        from ast import literal_eval
        #G = nx.empty_graph(0, create_using)
        adjlist = {}
        for line in lines:
            p = line.find(comments)
            if p >= 0:
                line = line[:p]
            if not len(line):
                continue
            # split line, should have 2 or more
            s = line.strip().split(delimiter)
            if len(s) < 2:
                continue
            u = s.pop(0)
            v = s.pop(0)
            d = s
            # if nodetype is not None:
            #     try:
            #         u = nodetype(u)
            #         v = nodetype(v)
            #     except:
            #         raise TypeError("Failed to convert nodes %s,%s to type %s."
            #                         % (u, v, nodetype))
            u = nodetype_A + '_' + str(u)
            v = nodetype_B + '_' + str(v)

            if len(d) == 0 or data is False:
                # no data or data type specified
                edgedata = {}
            elif data is True:
                # no edge types specified
                try:  # try to evaluate as dictionary
                    edgedata = dict(literal_eval(' '.join(d)))
                except:
                    raise TypeError(
                        "Failed to convert edge data (%s) to dictionary." % (d))
            else:
                # convert edge data to dictionary with specified keys and type
                if len(d) != len(data):
                    raise IndexError(
                        "Edge data %s and data_keys %s are not the same length" %
                        (d, data))
                edgedata = {}
                for (edge_key, edge_type), edge_value in zip(data, d):
                    try:
                        edge_value = edge_type(edge_value)
                        if(edge_value<thresh):
                            continue
                    except:
                        raise TypeError(
                            "Failed to convert %s data %s to type %s."
                            % (edge_key, edge_value, edge_type))
                    edgedata.update({edge_key: edge_value})
            #G.add_edge(u, v, **edgedata)
        #return G
            if u in adjlist:
                adjlist[u].update({v:edgedata})
            else:
                adjlist.update({u:{v:edgedata}})
        return adjlist


    @open_file(1, mode='rb')
    def _read_maplist(self, path, comments="#", delimiter=None, nodetype=None, data=True,encoding='utf-8'):
        """
        Returns
        -------
        G : graph
        A networkx Graph or other type specified with create_using


        See Also
        --------
        parse_edgelist

        Notes
        -----
        Since nodes must be hashable, the function nodetype must return hashable
        types (e.g. int, float, str, frozenset - or tuples of those, etc.)
        """
        lines = (line.decode(encoding) for line in path)
        return self._parse_maplist(lines, comments=comments, delimiter=delimiter,nodetype=nodetype,data=data)


    def _parse_maplist(self,lines, comments='#', delimiter=None, nodetype=None,data=True):
        """Parse lines of an edge list representation of a graph.

        Parameters
        ----------
        lines : list or iterator of strings
            Input data in edgelist format
        comments : string, optional
        Marker for comment lines
        delimiter : string, optional
        Separator for node labels
        create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
        nodetype : Python type, optional
        Convert nodes to this type.
        data : bool or list of (label,type) tuples
        If False generate no edge data or if True use a dictionary
        representation of edge data or a list tuples specifying dictionary
        key names and types for edge data.

        Returns
        -------
        #G: NetworkX Graph
            #The graph corresponding to lines
        mapping : dict
        {movieId:{title:'title', genres:[genres1, genres2,...]},...}

        """

        from ast import literal_eval
        #G = nx.empty_graph(0, create_using)
        maplist = {}
        for line in lines:
            p = line.find(comments)
            if p >= 0:
                line = line[:p]
            if not len(line):
                continue
            # split line, should have 2 or more
            s = line.strip().split(delimiter)
            if len(s) < 1:
                continue
            u = s.pop(0)
            d = s
            # if nodetype is not None:
            #     try:
            #         u = nodetype(u)
            #         v = nodetype(v)
            #     except:
            #         raise TypeError("Failed to convert nodes %s,%s to type %s."
            #                         % (u, v, nodetype))
            u = nodetype + '_' + str(u)

            if len(d) == 0 or data is False:
                # no data or data type specified
                mapdata = {}
            elif data is True:
                # no edge types specified
                try:  # try to evaluate as dictionary
                    mapdata = dict(literal_eval(' '.join(d)))
                except:
                    raise TypeError(
                        "Failed to convert edge data (%s) to dictionary." % (d))
            else:
                # convert edge data to dictionary with specified keys and type
                if len(d) != len(data):
                    raise IndexError(
                        "Edge data %s and data_keys %s are not the same length" %
                        (d, data))
                mapdata = {}
                for (edge_key, edge_type), edge_value in zip(data, d):
                    try:
                        edge_value = edge_type(edge_value).split('|')
                    except:
                        raise TypeError(
                            "Failed to convert %s data %s to type %s."
                            % (edge_key, edge_value, edge_type))
                    mapdata.update({edge_key: edge_value})
            #G.add_edge(u, v, **edgedata)
        #return G
            maplist.update({u:mapdata})
        return maplist