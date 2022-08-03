
import copy
 

# Biblioteca para a fila de prioridade
from heapq import heappush, heappop
 
# Esta variável pode ser alterada para mudar o programa de 8 puzzle(n=3) para 15 puzzle(n=4) para 24 puzzle(n=5)...
n = 3
 
# bottom, left, top, right
row = [ 1, 0, -1, 0 ]
col = [ 0, -1, 0, 1 ]
 
# Classe da fila de prioridade
class priorityQueue:
     
    # Aqui é o construtor da fila de prioridade
    def __init__(self):
        self.heap = []
 
    # Aqui insere uma varíavel nova 'k'
    def push(self, k):
        heappush(self.heap, k)
 
    # Método que remove o mínimo elemento da fila de prioridade
    def pop(self):
        return heappop(self.heap)
 
    # Método para saber se a fila está vazia
    def empty(self):
        if not self.heap:
            return True
        else:
            return False
 
# Estrutura do nó
class node:
     
    def __init__(self, parent, mat, empty_tile_pos,
                 cost, level):
                      
        # Aqui armazena o nó pai do nó atual ajuda a traçar o caminho quando a resposta for encontrada
        self.parent = parent
 
        # Aqui armazena a matriz
        self.mat = mat
 
        # Aqui armazena a posição na qual o bloco de espaço vazio existe na matriz
        self.empty_tile_pos = empty_tile_pos
 
        # Aqui armazena o número de peças mal colocadas
        self.cost = cost
 
        # Aqui armazena o número de movimentos até agora
        self.level = level
 
    # Este método é definido para que a fila de prioridade seja formada com base na variável de custo dos objetos
    def __lt__(self, nxt):
        return self.cost < nxt.cost
 
# Função para calcular o número de quadrados mal colocadas, ou seja. número de peças não vazias fora de sua posição de meta
def calculateCost(mat, final) -> int:
     
    count = 0
    for i in range(n):
        for j in range(n):
            if ((mat[i][j]) and
                (mat[i][j] != final[i][j])):
                count += 1
                 
    return count
 
def newNode(mat, empty_tile_pos, new_empty_tile_pos,
            level, parent, final) -> node:
                 
    # Copiar dados da matriz pai para a matriz atual

    new_mat = copy.deepcopy(mat)
 
    # Move um azulejo/quadrado para uma posição
    x1 = empty_tile_pos[0]
    y1 = empty_tile_pos[1]
    x2 = new_empty_tile_pos[0]
    y2 = new_empty_tile_pos[1]
    new_mat[x1][y1], new_mat[x2][y2] = new_mat[x2][y2], new_mat[x1][y1]
 
    # Definir o número de peças mal colocadas
    cost = calculateCost(new_mat, final)
 
    new_node = node(parent, new_mat, new_empty_tile_pos,
                    cost, level)
    return new_node
 
# Função para printar a matriz N x N
def printMatrix(mat):
     
    for i in range(n):
        for j in range(n):
            print("%d " % (mat[i][j]), end = " ")
             
        print()
 
# Função que checa o if para ver se valida a matriz coordenada
def isSafe(x, y):
     
    return x >= 0 and x < n and y >= 0 and y < n
 
# Imprimir caminho do nó raiz para o nó de destino
def printPath(root):
     
    if root == None:
        return
     
    printPath(root.parent)
    printMatrix(root.mat)
    print()
 
# Função para resolver N x N - 1 algoritmo de quebra-cabeça usando Branch and Bound. empty_tile_pos é a posição do bloco em branco no estado inicial.
def solve(initial, empty_tile_pos, final):
     
    # Cria uma fila de prioridade para armazenar nós ativos da árvore de pesquisa
    pq = priorityQueue()
 
    # Aqui cria um nó raiz
    cost = calculateCost(initial, final)
    root = node(None, initial,
                empty_tile_pos, cost, 0)
 
    # Adicionar raiz à lista de nós ativos
    pq.push(root)
 
    # Encontra um nó ativo com menor custo, adiciona seus filhos à lista de nós ativos e finalmente o exclui da lista.
    while not pq.empty():
 
        # Encontre um nó ativo com menor custo estimado e exclua-o da lista de nós ativos
        minimum = pq.pop()
 
        # Se mínimo é o nó de resposta
        if minimum.cost == 0:
             
            # Imprima o caminho da raiz ao destino;
            printPath(minimum)
            return
 
        # Aqui gera todos os filhos possíveis
        for i in range(n):
            new_tile_pos = [
                minimum.empty_tile_pos[0] + row[i],
                minimum.empty_tile_pos[1] + col[i], ]
                 
            if isSafe(new_tile_pos[0], new_tile_pos[1]):
                 
                # Aqui cria um nó filho
                child = newNode(minimum.mat,
                                minimum.empty_tile_pos,
                                new_tile_pos,
                                minimum.level + 1,
                                minimum, final,)
 
                # Adicionar filho à lista de nós ativos
                pq.push(child)
 
# Driver Code
 
# Inicia a configuração. O valor 0 é usado para espaço vazio
initial = [ [ 1, 2, 3 ],
            [ 8, 0, 4 ],
            [ 7, 6, 5 ] ]
 
# Configuração final solucionável. O valor 0 é usado para espaço vazio
final = [ [ 1, 2, 3 ],
          [ 4, 5, 6 ],
          [ 7, 8, 0 ] ]
 
# Coordenadas do bloco em branco na configuração inicial
empty_tile_pos = [ 1, 2 ]
 
# Chamada de função para resolver o quebra-cabeça
solve(initial, empty_tile_pos, final)