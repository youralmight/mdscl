# DSCI 512 CL 第二周：图、稀疏矩阵、BFS 与 DFS

## 范围与阅读状态

依据当前 CL 课程 README，本周是 Lecture 3（2026-10-12，Graphs and Sparse Matrices）与 Lecture 4（2026-10-14，Graph Searches and Trees）。本文覆盖两讲 learning objectives、课堂正文与 Lab 2 所需的概念，但不解答 Lab 题目，也不提供可提交实现。**这是第二周知识笔记，不是教师确认的 Quiz 1 范围。**PageRank、图着色和 NP-complete 问题在讲义中标为 optional，不进入主线。

## 1. 先把现实问题写成图

图（graph）表示“实体及实体之间的关系”。形式上

$$G=(V,E),$$

其中 $V$ 是顶点（vertices / nodes）集合，$E$ 是边（edges）集合。一条边 $(u,v)$ 表示 $u,v\in V$ 之间存在所定义的关系。

建模前必须先说明：

1. **一个顶点是什么？**例如机场、用户、网页、课程。
2. **一条边是什么？**例如直飞、好友、链接、先修关系。
3. **关系有方向吗？**A 关注 B 不代表 B 关注 A；好友关系通常对称。
4. **边上有数量吗？**距离、价格、容量或时间可作为权重。
5. **问题关心存在性、最少边数还是最小总权重？**“最少转机”与“最低票价”不是同一个最短路问题。

### 1.1 核心术语

| 术语 | 可操作定义 | 易错点 |
|---|---|---|
| neighbour | 与某顶点直接相连的顶点 | directed graph 中要区分出邻居与入邻居 |
| degree | 与顶点关联的边数 | directed graph 需区分 in-degree / out-degree |
| walk | 相邻边连接成的顶点序列；顶点和边可以重复 | 只要求“能沿边走”，不等于 path |
| path | 不重复顶点的 walk | 路径长度通常是边数，不是顶点数 |
| cycle | 起点与终点相同、其他顶点不重复且不重复边的闭合 walk | 简单无向图中的 cycle 至少含 3 条边；沿一条边往返不是 cycle |
| connected | 无向图中任意两顶点之间都有 path | directed graph 需另分 weakly / strongly connected |
| complete | 每对不同顶点都直接相连 | 简单无向 complete graph 有 $V(V-1)/2$ 条边 |

### 1.2 四类基本图

- **Undirected：**边无方向，$(u,v)$ 与 $(v,u)$ 是同一关系。
- **Directed：**边有方向；两个方向都存在时必须分别保存两条边。
- **Unweighted：**只记录关系是否存在；每条边在“最少边数”意义下成本相同。
- **Weighted：**边带数值。权重含义必须明确；负权、距离和容量需要不同算法，不能只看到 `weight` 就一概称“距离”。

方向与权重是两条独立维度：图可以 directed + weighted，也可以 undirected + unweighted。

## 2. NetworkX：图对象与可观察接口

```python
import networkx as nx

G = nx.Graph()                 # undirected
G.add_nodes_from(["A", "B", "C", "D"])
G.add_edge("A", "B", weight=4)
G.add_edges_from([("A", "C"), ("C", "D")])

list(G.nodes())
list(G.edges())
list(G.neighbors("A"))
G.degree("A")
```

- `nx.Graph()` 建无向图；`nx.DiGraph()` 建有向图。
- `add_node` / `add_nodes_from` 加顶点；加边时若端点还不存在，NetworkX 会创建端点。
- `add_edge(u, v, weight=...)` 的额外命名参数成为 edge attributes。
- `G.neighbors(u)` 返回迭代器，不是固定列表；若要多次使用可显式 `list(...)`。
- 绘图 layout 的坐标可随机变化；图画法改变不表示图结构改变。
- `nx.bfs_edges(G, source)` 与 `nx.dfs_edges(G, source)` 返回各自 search tree 中发现边的顺序；邻居迭代顺序变化时，遍历顺序也可能变化，但 reachability 不变。

`defaultdict` 很适合手工建立 adjacency list：

```python
from collections import defaultdict

adj = defaultdict(list)
for u, v in [("A", "B"), ("A", "C"), ("C", "D")]:
    adj[u].append(v)
    adj[v].append(u)            # undirected 才加反向
```

`defaultdict(list)` 传入的是可调用的 factory；不能写 `defaultdict(list())`，因为后者已经创建了一个具体列表。

## 3. 图的两种基本表示

令 $|V|$ 为顶点数，$|E|$ 为边数。

### 3.1 Adjacency list

每个顶点保存它的邻居集合。空间为

$$O(|V|+|E|).$$

无向边通常在两个端点的邻接表各出现一次，但常数 2 不改变 Big-O。

- 遍历某顶点所有邻居：$O(\deg(u))$。
- 若邻居存为普通 list，检查特定边 $(u,v)$ 最坏为 $O(\deg(u))$，因此上界可写 $O(|V|)$。
- 若邻居存为 hash set/dict，成员检查平均可近似 $O(1)$，但仍有 hashing 条件与最坏情形。
- 稀疏图、动态增删边、BFS/DFS 通常适合 adjacency list。

### 3.2 Adjacency matrix

给顶点固定索引，建立 $|V|\times|V|$ 矩阵 $A$：

$$
A_{ij}=\begin{cases}
1,&(i,j)\in E,\\
0,&(i,j)\notin E.
\end{cases}
$$

weighted graph 可把非零项换成权重；“没有边”如何编码必须与合法零权边区分。

- dense matrix 空间：$O(|V|^2)$，与实际边数无关。
- 检查指定边：直接读 `A[i, j]`，为 $O(1)$。
- 无向图矩阵对称；有向图一般不对称。
- 从矩阵列出某顶点所有邻居，要扫描一整行，通常为 $O(|V|)$。

简单无向 complete graph 的边数是 $|V|(|V|-1)/2$；简单 directed complete graph（不含 self-loop）才有 $|V|(|V|-1)$ 条有向边。讲义把无向 complete graph 的边数写成后一个值时，多算了一个方向；复杂度仍为 $O(|V|^2)$。

### 3.3 怎样选

| 需求 | 常见选择 | 原因 |
|---|---|---|
| 很稀疏，主要遍历邻居 | adjacency list | 只存实际边 |
| 频繁询问固定两点是否直接相连 | dense/sparse matrix 或 set-based adjacency | 指定位置/成员检查快 |
| 静态图，做矩阵乘法、PageRank、谱方法 | sparse matrix | 保留线性代数接口，又避免存大量零 |
| 图很小且可读性优先 | dense matrix | 简单直接 |

不存在只凭“图”就唯一正确的表示；必须看稀疏度、操作模式和内存。

## 4. Sparse matrix：数学性质与存储结构要分开

- 数学上，**sparse matrix** 是绝大多数元素为 0 的矩阵。
- 编程中，**sparse matrix data structure** 主要保存非零项及其位置；某些实现也允许显式存储数值为 0 的条目。

两者相关但不等同：稀疏数学矩阵可以错误地存成 dense array；非稀疏矩阵也能硬存成 sparse structure，只是开销可能更大。

```python
from scipy import sparse

A = sparse.csr_matrix([
    [0, 4, 0, 0],
    [4, 0, 1, 0],
    [0, 1, 0, 2],
    [0, 0, 2, 0],
])

A.shape        # (4, 4)
A.nnz          # number of stored entries, including explicit zeros
A[1, 2]        # scalar lookup
A[1, :]        # sparse row, shape remains two-dimensional
```

### 4.1 CSR 的三个数组

Compressed Sparse Row（CSR）按行压缩：

- `data`：依次保存所有 stored values，可能包含显式存入的 0；
- `indices`：每个 stored value 所在的列号；
- `indptr`：每一行在 `data` / `indices` 中的起止边界。

第 `r` 行的 stored entries 位于切片 `indptr[r]:indptr[r+1]`。空行会令相邻两个 pointer 相等。

SciPy 的 `nnz` 是 **stored entries 的数量**，包括 explicit zeros；要数数学意义上的非零值应使用 `count_nonzero()`。存储量与 `nnz` 近似成正比，还需 row pointers，因此概念上可写 $O(\text{nnz}+m)$（$m$ 为行数），而不是 dense 的 $O(mn)$。

### 4.2 CSR 与 CSC

| 格式 | 组织方式 | 快的访问模式 | 慢的访问模式 |
|---|---|---|---|
| CSR | row pointers + column indices | row slicing、row-wise 运算 | 反复 column slicing |
| CSC | column pointers + row indices | column slicing、column-wise 运算 | 反复 row slicing |

`csr.tocsc()` 可转换，但转换本身花时间和内存。先根据重复操作方向选格式，不要在循环中来回转换。

`A.toarray()` 会真正分配完整 dense matrix。若形状巨大，即使 `nnz` 很小，也可能立即耗尽内存。只为了看形状、`nnz`、某行或某个标量，不应先 dense 化。

稀疏矩阵用 `A[i, j]` 明确索引；`A[i][j]` 的第一步仍返回二维 sparse row，语义和 NumPy 的一维 row 不同。

## 5. Tree 是特殊的 graph

图论中的 tree 是**连通且无环的无向图**。因此任意两个顶点之间恰有一条简单路径。层次结构通常指定一个 root，由此产生 parent/child 语言。

| 术语 | 定义 |
|---|---|
| root | 层次起点，没有 parent |
| parent / child | 相邻层的直接前驱 / 后继 |
| leaf | 没有 child 的节点 |
| subtree | 某节点及其全部 descendants |
| depth | root 到该节点的边数 |
| height of node | 该节点到最深 leaf 的最大边数 |
| tree height | root 的 height |

实际 hierarchy 可直接映射成 tree。例如文件系统中，根目录是 root，子目录/文件是 child，没有下级项目的文件或空目录是 leaf；某个目录及其全部下级项目构成 subtree。Tree 让“列出某目录的全部 descendants”“沿 parent 找完整路径”等操作与层级关系一致。Organization chart 和嵌套 HTML/XML 也可作同类映射。

“balanced”不是所有 tree 的共同性质；不同树结构有不同的正式平衡条件。本周只需理解高度相差过大会影响后续树算法，不把 BST/AVL 的具体规则提前加入。

## 6. BFS：按离起点的边数逐层扩展

Breadth-first search 使用 FIFO queue。对起点 $s$：

1. 把 $s$ 标为 visited 并入队。
2. 取出队首 `v`。
3. 处理 `v`；若是目标可停止。
4. 对每个未 visited 的邻居：**先标记，再入队**。
5. 队列空仍未找到时，目标不可达。

```python
from collections import deque

def bfs_distance(adj, start):
    distance = {start: 0}
    q = deque([start])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in distance:
                distance[w] = distance[v] + 1
                q.append(w)
    return distance
```

用 dictionary 同时充当 visited 与 distance，避免重复状态。若等到 dequeue 才标记，同一顶点可能被多个邻居重复入队。

### 6.1 BFS 能保证什么

在**unweighted graph**（或每条边成本相同）中，BFS 首次发现顶点时得到从起点到它的最少边数；要重建路径，再保存 `parent[w] = v`。

BFS 不会自动求 weighted graph 的最小总权重路径。即使一条路径边更少，它的权重总和也可能更大；需要适合权重条件的算法。

### 6.2 复杂度

用 adjacency list 且每个 reachable vertex 只处理一次：

- 时间：$O(|V|+|E|)$；无向边会从两端看到两次，仍是 $O(|E|)$。
- 额外空间：visited、distance/parent 与 queue 合计 $O(|V|)$。

若 queue 用 Python list 的 `pop(0)`，每次会移动剩余元素，可能引入额外线性成本；实现 FIFO 应优先 `collections.deque.popleft()`。算法的图论复杂度假设 queue 操作是 $O(1)$。

## 7. DFS：沿一条路走深，再回退

Depth-first search 可用递归调用栈，也可像下面这样显式保存 `(vertex, neighbor_iterator)` frames。发现一个未访问 child 后立即下降；只有 child 完成后，才继续 parent 尚未检查的 neighbors。

```python
def dfs_order(adj, start):
    visited = {start}
    order = [start]
    # 每个 frame 保存当前顶点及尚未检查完的邻居 iterator。
    stack = [(start, iter(adj[start]))]

    while stack:
        _, neighbors = stack[-1]
        for w in neighbors:
            if w not in visited:
                visited.add(w)
                order.append(w)
                stack.append((w, iter(adj[w])))
                break
        else:
            stack.pop()

    return order
```

每个 stack frame 保留 parent 尚未检查完的邻居；发现一个新 child 后先下降，child 完成后才回到 parent 继续 siblings，因此保持 depth-first。邻居迭代顺序仍会影响合法 DFS order；若要固定顺序，需要明确排序，并计入排序成本。

| 维度 | BFS | DFS |
|---|---|---|
| frontier | FIFO queue | LIFO stack / recursion |
| 探索形状 | 逐层 | 尽量走深再回退 |
| unweighted shortest-edge path | 保证 | 不保证 |
| 时间（adjacency list） | $O(V+E)$ | $O(V+E)$ |
| 最坏额外空间 | $O(V)$ | $O(V)$ |
| 常见风险 | 宽图 frontier 很大 | 深图 stack / recursion 很深 |

二者都会遍历从起点沿允许的边方向**可达**的顶点；在 undirected graph 中，这正好是起点所在 connected component。要遍历整个 undirected disconnected graph，需要对每个尚未 visited 的顶点重新启动一次 search。Directed graph 的 weak/strong components 不能由这一步骤直接替代。

## 8. 复习时的判定顺序

1. 顶点和边各代表什么？边有方向或权重吗？
2. `V`、`E`、`nnz` 分别是多少？图是否稀疏？
3. 当前操作是查指定边、枚举邻居、矩阵运算，还是 graph traversal？
4. dense matrix、adjacency list、CSR/CSC 哪个匹配访问模式？
5. 问的是可达性、最少边数还是最小权重？
6. BFS 是否在 enqueue 时立即记录 visited？DFS 是否保存尚未检查完的邻居状态，真正先走深再回退？
7. 说的是 source reachability，还是 undirected connected component / directed weak or strong component？
8. 复杂度是否把底层结构算进去，例如 `list.pop(0)` 不是常数时间？

## 来源、边界与讲义勘误

### 当前课程主来源

- [当前 CL README](/Users/youralmight/workspaces/reps/mdscl/DSCI_512/official/current/DSCI_512_alg-data-struct_students/README.md)
- [Lecture 3：Graphs and Sparse Matrices](/Users/youralmight/workspaces/reps/mdscl/DSCI_512/official/current/DSCI_512_alg-data-struct_students/lectures/03_graphs-sparse-matrices.ipynb)
- [Lecture 4：Graph Searches and Trees](/Users/youralmight/workspaces/reps/mdscl/DSCI_512/official/current/DSCI_512_alg-data-struct_students/lectures/04_graph-search-tree.ipynb)
- [Lab 2 题面，仅用于识别应用知识](/Users/youralmight/workspaces/reps/mdscl/DSCI_512/assignments/lab2/DSCI_512_lab2_yz2000/lab2.ipynb)

### 指定预习与边界

- Lecture 3 指定 Runestone graph objectives/vocabulary；核心术语已与当前讲义核对。
- Lecture 4 指定 BFS storage/analysis 与 BFS/DFS introduction；本文按当前 lecture objectives 整理。
- 指定 DFS/BFS 视频未依赖画面内容；PageRank 明确作为 optional，不扩展为本周主线。
- 讲义的无向 complete graph 边数少了除以 2；本文已按简单无向图定义修正。讲义给 BFS/DFS 的空间复杂度缺右侧 `$` 只是排版错误，结论为 $O(V)$。
- 本文不包含 Lab 2 的函数答案、测试结果或针对原题数据的求解。