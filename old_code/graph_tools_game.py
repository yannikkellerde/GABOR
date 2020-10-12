def track_vertices(self,del_inds):
        ind_list = list(range(self.graph.num_vertices()))
        for ind in sorted(del_inds):
            if ind==len(ind_list):
                ind_list.append(None)
            else:
                ind_list.append(ind_list[ind])
                ind_list[ind] = None
        return ind_list
    
    def track_forward(self,del_inds,ind_list):
        for ind in reversed(sorted(del_inds)):
            if ind != len(ind_list)-1:
                ind_list[ind] = ind_list.pop()
            else:
                ind_list.pop()

    def make_move(self,move,hashme=True):
        square_node = list(find_vertex(self.graph,self.graph.vp.h,move))[0]
        self.make_move_vertex(square_node)
        if hashme:
            self.hashme()


    def forced_move_search(self):
        vert_inds = dict()
        double_threat = set()
        force_me_to = None
        loss = False
        for vert in self.graph.vertices():
            deg = vert.out_degree()
            owner = self.owner_map[self.graph.vp.o[vert]]
            if owner != None:
                if owner == self.onturn or owner=="f":
                    if deg == 1:
                        return True
                    elif deg == 2:
                        nod1,nod2 = vert.all_neighbors()
                        ind1,ind2 = int(nod1),int(nod2)
                        if ind1 in vert_inds:
                            double_threat.add(ind1)
                        if ind2 in vert_inds:
                            double_threat.add(ind2)
                        vert_inds[ind1] = ind2
                        vert_inds[ind2] = ind1
                else:
                    if deg == 1:
                        sq, = vert.all_neighbors()
                        ind = self.graph.vertex_index[sq]
                        if force_me_to is None:
                            force_me_to = ind
                        else:
                            if ind != force_me_to:
                                loss = True
        if loss:
            return False
        if force_me_to is not None:
            if force_me_to in vert_inds:
                vert_inds = {force_me_to:vert_inds[force_me_to]}
            else:
                return None
        if len(set(vert_inds).intersection(double_threat))>0:
            return True
        if len(vert_inds) > 1:
            orig_graph = Graph(self.graph)
        for i,ind in enumerate(vert_inds.keys()):
            if i!=0:
                if i==len(vert_inds)-1:
                    self.graph = orig_graph
                else:
                    self.graph = Graph(orig_graph)
            vert = self.graph.vertex(ind)
            del_inds = self.make_move_vertex(vert)
            reply_ind = self.track_vertices(del_inds)[vert_inds[ind]]
            reply_vert = self.graph.vertex(reply_ind)
            self.make_move_vertex(reply_vert)
            if self.forced_move_search():
                return True
        return None

    def create_node_hash_map(self):
        self.node_hash_map = dict()
        for vertex in self.game.graph.vertices():
            if self.game.graph.vp.o[vertex] == 0:
                self.node_hash_map[self.game.graph.vp.h[vertex]] = self.node_map[int(vertex)]