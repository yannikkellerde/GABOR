## Winpatterns
In games like Qango or tic tac toe the players take alternating turs, filling squares with their respective symbol (X or O's for tic tac toe). A player wins, if he placed his symbol on all squares of a winpattern of a game. For tic tac toe, these winpatterns would be all horizontal, vertical or diagonal lines each consisting of 3 squares. For quango, we have 5 square lines, 2x2 squares, and winpatterns indicated by colors on the board.

## Game description as a graph
The games we want to solve can be described by an undirected graph. The graph consists of vericies each with one of 3 potential colors (one for each player, one for empty). There will be 2 types of edges, let's call the first one blue edges and the second one green edges. Each winpattern will be represented by as many vertices, as the number of squares in the winpattern. These vertices will be fully connected by blue edges. When 2 winpatterns overlap (there are squares that correspond to both winpatterns), the respective vertices of the winpatterns will be connected via a green edge.

### Playing on a graph
Players now take alternating turns, coloring all vertices of a subgraph that is separated from the rest of the graph with respect to green edges. When a player has colored all verticies of a subgraph separated with respect to blue edges, he wins the game.

### Pruning the graph while playing
We can remove any, with respect to blue edges, separated subgraph, if it contains verticies in both players colors. We can also remove all fully separated subgraphs (with respect to blue and green edges) that contain more than one vertex in "empty square color".

## Taking advantage of graph representation
### Move sorting
The proof number search is much more efficient at finding a solution, if it looks at moves that are likely to be good first. In the graph, we can quickly obtain the simple and efficient heuristic of picking the subgraph separated with respect to green edges, that contains the most verticies. We could even go further and look at the amount of "empty colored" verticies in each subgraph separated with respect to blue edges adjacent to the each potentially picked subgraph.

## Exploiting symetry and transposition
### Why do we need it?
The most important and hardest part of using the graphs for our proof number search is exploiting symetry and transpositions. The basic version of proof number search just works with a game tree, looking at all possible moves at each stage of the game and does not recognize any transpositions. This is terrible for games like qango, as this would lead to isomorphic positions being analyzed potentially hundreds of times. This means, that we need to use transposition tables to store previous results. There are versions of PN search for directed acyclic graphs out there like [this](https://pdfs.semanticscholar.org/86f5/1429a19cfc76e9d42f28b93c62e978c816a0.pdf). When using our graph representations, we need to be careful though, as the pruning of subgraphs can potentially lead to game graphs that contain cycles.

### Graph isormorphism and hashing
Now for the hard part. To recognize that we are in a game state, that we have been in before, we need to solve the graph isomorphism problem. The graph isomorphism problem is of NP-intermediate complexity, so runtime and scalability will be a concern. Actually, our problem is even harder, as we can't store that many whole graphs in our memory, so we will need to solve the graph hashing problem. Related to that problem, we will need to find a unique ordering for the vericies that is the same for isomorphic graphs, because otherwise, we won't know which verticies we need to color to get from one node of the game graph to another after exploiting an isomorphism.

For the hashing/vertex ordering, we will have a time budget of 10 milliseconds at most, for the code to still be efficient. Luckily we won't have to create an ordering from scratch in that time. For the proof number search, we will only need to change the ordering of the last game-state based on a move a player made. From a unique ordering, calculating a hash value should be trivial, as for uniquely ordered graphs, the graph isomorphism problem is trivially solvable.