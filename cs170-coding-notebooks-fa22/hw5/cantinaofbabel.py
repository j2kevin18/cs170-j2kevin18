import typing

def reverse_graph(g: typing.Set[typing.Tuple[str, str]]) -> typing.Set[typing.Tuple[str, str]]:
    res = set(())
    for edge in g:
        res.add((edge[1], edge[0]))
    return res
    
def reverse_graph_dict(g: typing.Dict[str, list]) -> typing.Dict[str, list]:
    dict_res = {}
    g_set = set([(u, v) for u in g.keys() for v in g[u]])
    g_set_reverse = reverse_graph(g_set)
    
    for v in g.keys():
        dict_res[v] = []
    for v, u in g_set_reverse:
        dict_res[v].append(u)
    
    return dict_res

# Given a graph G and a vertex v, return all vertices reachable from v
# Return: a set of integers that contains all vertices reachable from v
def explore(g, v) -> typing.Set[str]:
    # Your code here
    visited = {v : False for v in g.keys()}
    visited_reverse = {v : False for v in g.keys()}
    g_reverse = reverse_graph_dict(g)

    def explore(v, visited, g):
        visited[v] = True
        res = {v}

        for node in g[v]:
            if visited[node] == False:
                res = res.union(explore(node, visited, g))

        return res
    
    res = explore(v, visited, g)
    res_reverse = explore(v, visited_reverse, g_reverse)
    return res.intersection(res_reverse)

# Given a graph, do DFS and return a tuple with all vertices as key and their post number as value
def dfs(g) -> typing.Dict[str, int]:
    # Your code here
    visited = {v : False for v in g.keys()}
    pre = {v : 0 for v in g.keys()}
    post = {v : 0 for v in g.keys()}
    clock = 0

    def previsit(v):
        nonlocal post, clock
        pre[v] = clock
        clock += 1


    def postvisit(v):
        nonlocal post, clock
        post[v] = clock
        clock += 1

    def explore(v):
        nonlocal visited, g
        visited[v] = True

        previsit(v)
        
        for node in g[v]:
            if visited[node] == False:
                explore(node)

        postvisit(v)
    
    for v in g.keys():
        if visited[v] == False:
            explore(v)

    return post
    
def kosaraju(g) -> typing.List[typing.Set]:
    # Your code here
    sccs = []
    gR = reverse_graph_dict(g)
    dict_v_to_post = dfs(gR)
    while dict_v_to_post:
        dict_post_to_v = dict([(post, v) for (v, post) in dict_v_to_post.items()])
        max_post_v = dict_post_to_v[max(dict_post_to_v.keys())]
        scc = explore(gR, max_post_v)
        sccs.append(scc)
        for v in scc:
            del dict_v_to_post[v]
    return sccs
    
def preprocess():
    man_lang = {}
    man = {}
    person = set(())
    person_num = int(input())
    
    for _ in range(person_num):
        str = input()
        str_list = str.split()
        
        person.add(str_list[0])
        man_lang[str_list[0]] = str_list[1:]
        
        for lang in str_list[1:]:
            if lang not in man_lang.keys():
                man_lang[lang] = []
            man_lang[lang].append(str_list[0]) #debug

    for indiv in person:
        lang = man_lang[indiv][0]
        man_list = man_lang[lang].copy()
        man_list.remove(indiv)
        man[indiv] = man_list
        
    return man, person_num

def remain(sccs, num):
    max_len = 0
    for scc in sccs:
        max_len = max(max_len, len(scc))
    return num - max_len
     
g, person_sum = preprocess()
sccs = kosaraju(g)
print(g)
print(sccs)
print(remain(sccs, person_sum))
    