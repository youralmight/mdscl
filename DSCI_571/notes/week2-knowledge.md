# DSCI 571 第二周：相似性模型、预处理与无泄漏 Pipeline

## 范围与来源状态

覆盖当前 README 的 Lecture 3 **k-NNs, SVM RBF** 与 Lecture 4 **Preprocessing, pipelines, column transformer**。主依据是课程书当前同步版本 Chapter 3–4、当前 in-class demos 与 Lab 2 应用范围。README 的 Lecture 4 第二个旧链接名仍含 `05_column-transformer-text-feats`，但当前课程书已把 column transformer 合并进 Chapter 4；当前 Chapter 5 是下一讲的 “More Preprocessing: Categorical Features and Text”，不作为本周主线。**这是第二周知识笔记，不是已确认的 Quiz 1 范围，也不是 Lab 答案。**

## 1. “相似”必须由 representation 定义

一个样本用 feature vector 表示：

$$x=(x_1,\ldots,x_d).$$

所有样本位于 $d$ 维 feature space。Euclidean distance 为

$$d(u,v)=\sqrt{\sum_{j=1}^{d}(u_j-v_j)^2}.$$

距离非负，相同 feature values 时为 0。但公式可计算不等于语义合理。选择哪些 features、怎样编码、用什么单位和 scale，共同决定谁与谁“近”。

### 1.1 Scale 会改变邻居

若 age 以 years、income 以 dollars，income 差值可能比 age 大几千倍，从而主导 Euclidean distance。把 dollars 改成 thousands 即可改变 nearest neighbour，虽然现实对象没变。这说明 raw units 在替我们做 model choice。

`StandardScaler` 用 training mean 与 SD 做

$$z=\frac{x-\mu_{train}}{\sigma_{train}}.$$

training data 的每列变为约 mean 0、SD 1；validation/test 只用同一组 training statistics 做 transform。Standardization 不会把值限制到 [0,1]，也不保证每个 feature 同等有用。

Distance-based models（k-NN、RBF SVM）通常需要 scale；decision tree 的 threshold split 一般对单调 rescaling 不敏感。

## 2. k-nearest neighbours（k-NN）

### 2.1 Classification

对 query：

1. 计算它到 training examples 的距离；
2. 找最近的 $k$ 个；
3. `weights="uniform"` 时多数投票；`weights="distance"` 时近邻影响更大。

```python
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5, weights="uniform")
knn.fit(X_train, y_train)
y_pred = knn.predict(X_valid)
```

查询只能与 training examples 比，不与 test examples 的 labels 比。`n_neighbors` 和 `weights` 都是 hyperparameters，应在 training/CV 中选择。

### 2.2 Regression

`KNeighborsRegressor` 取 $k$ 个邻居 target 的 mean；distance weighting 时做加权平均。$k=1$ 的 prediction function 很不平滑，对单点敏感；较大 $k$ 更平滑，但可能抹掉局部规律。

### 2.3 $k$ 与 model complexity

- 小 $k$：very local、boundary 灵活，training score 高，可能 overfit。
- 大 $k$：更平滑，可能 underfit。
- 在 `weights="uniform"` 时，$k$ 接近整个 training set 会让 classifier 接近总猜 majority class、regressor 接近总猜 global mean。`weights="distance"` 即使包含全部 training examples，prediction 仍可随 query 改变。

不能按最好看的 boundary 或 test score 选 $k$。应保留 test，比较 CV train/validation scores，再 refit 选中的 configuration。

### 2.4 成本与限制

k-NN fitting 主要保存 training data，通常便宜；prediction 要与许多 training examples 比，storage 和 prediction 在大数据上昂贵。

它对以下因素敏感：

- feature scale；
- irrelevant features；
- arbitrary IDs / bad encodings；
- distance metric；
- high dimensionality。

**Curse of dimensionality：**维度增加而样本数固定时，点在空间中变稀，nearest/farthest distances 变得不易区分；许多 irrelevant dimensions 会把有用距离信号淹没。更多 features 不必然更好。

## 3. RBF support vector machine

RBF SVM 也由距离构造 similarity，但不是近邻投票。拟合时识别直接决定 decision function 的 training examples——support vectors——并学习它们的贡献。

RBF kernel：

$$K(x_i,x)=\exp\left(-\gamma\lVert x_i-x\rVert^2\right).$$

相同点 similarity 为 1；距离增大后趋近 0。Kernel 是由 distance 构造的 similarity，不是 distance metric。

### 3.1 Support vectors

support vectors 常靠近 decision boundary，因为它们影响边界位置；困难或 misclassified points 也可能成为 support vectors。它们不是人工预先选择，也不保证数量少。`SVC.support_vectors_` 在 fit 后给出对应 feature vectors。

### 3.2 `gamma`：影响有多局部

- 小 `gamma`：宽 influence region，boundary 较 smooth，可能 underfit。
- 大 `gamma`：窄而 local 的 influence，可形成复杂 boundary，可能 overfit。

scale 改变 squared distances，也会改变固定 `gamma` 的实际含义。

### 3.3 `C`：training mistakes 的惩罚

- 小 `C`：容忍更多 training errors，boundary 通常 smoother，可能 underfit。
- 大 `C`：更强迫 fit 困难 training points，boundary 通常更细，可能 overfit。

这些是趋势，不保证 validation score 单调变化。

### 3.4 `C` 与 `gamma` 必须联合选择

`gamma` 决定 influence radius，`C` 决定错误代价；二者效果交互。不能可靠地先单独定一个再只调另一个。Week 2 先理解联合 tuning 原因，具体 `GridSearchCV` / optimization bias 属后续课程内容。

```python
from sklearn.svm import SVC

svc = SVC(kernel="rbf", C=10, gamma=0.1)
```

| 维度 | k-NN | RBF SVM |
|---|---|---|
| distance 的作用 | 选邻居 | 转为 RBF similarity |
| fit | 主要保存 training set | 选择 support vectors、学习权重/边界 |
| prediction | 邻居投票/平均 | 合并 learned similarities |
| 主要 hyperparameters | `n_neighbors`, `weights` | `C`, `gamma` |
| 常见成本 | prediction/storage | fitting，尤其样本大时 |

## 4. Transformer API：学习怎样改变 X

Predictive estimator 学 `X → y`，提供 `fit(X,y)`、`predict(X)`、`score(X,y)`。Transformer 学 feature representation：

- `fit(X)`：从 training data 学参数；
- `transform(X)`：用已学参数转换；
- `fit_transform(X)`：对同一 training input 连续 fit + transform。

validation/test/deployment 只能调用已 fitted transformer 的 `transform`，不能重新 fit。任何从 data 学东西的 preprocessing 都受 Golden Rule 约束，不只是“模型”。

## 5. 常见 feature types 与 transformations

### 5.1 Numeric：scaling

`StandardScaler` 学每列 mean/SD。适合 distance/kernel models；对 outliers 敏感，且“每列相同 variance importance”本身是 modeling choice。

### 5.2 Missing values：imputation

```python
from sklearn.impute import SimpleImputer
SimpleImputer(strategy="median")
```

- mean/median imputer 在 fit 时学 replacement value；只能从 fold training data 学。
- categorical 常用 `strategy="most_frequent"` 或有理由的 constant。
- imputation 让 estimator 可运行，但不会找回真实缺失值，也不会修复 missingness mechanism；missing indicator 有时有信息，需要另作判断。

### 5.3 Nominal categories：one-hot encoding

```python
from sklearn.preprocessing import OneHotEncoder
OneHotEncoder(handle_unknown="ignore")
```

每个已知类别生成 indicator，避免制造顺序。fit 学 categories 和 output columns。

- `handle_unknown="ignore"`：新类别在该 feature 的已知 indicator 上全为 0；避免错误，但所有 unseen categories 无法区分。
- 默认 sparse output 适合 high-cardinality；小例子可 `sparse_output=False`。
- binary feature 可 `drop="if_binary"` 只留一列，但 all-zero representation 可能同时表示 dropped category 与 unknown category；要确认这种 ambiguity 可接受。

### 5.4 Ordinal categories：显式顺序

```python
from sklearn.preprocessing import OrdinalEncoder
OrdinalEncoder(categories=[["low", "medium", "high"]])
```

只在 categories 真有 order 时使用。编码 0/1/2 还假设相邻间距相同；这不是 labels 自动保证的事实。对 nominal categories 用 arbitrary integers 会让 distance model 误认为有顺序与距离。

### 5.5 Passthrough 与 drop

- 已是合适表示的 0/1 feature 可 passthrough。
- pure identifier 通常应 drop；scaling ID 不会使其有测量意义。
- sensitive attribute 是否使用是应用、法规、公平目标与 proxy 结构的问题。删除一列不保证 fairness，因为其他 features 可能携带相同信息。
- target 或 prediction 时才产生的信息绝不能进入 X。

## 6. Data leakage：split 之后，每个 fold 还要再守一次边界

错误流程：

```python
X_scaled = StandardScaler().fit_transform(X_train)
cross_validate(knn, X_scaled, y_train)
```

虽然 held-out test 没参与，但 scaler 已看过所有 `X_train`，包括每一折临时 validation rows。validation information 进入 training representation，CV score 可能 optimistic。

正确做法：把 transformer 与 estimator 放进同一个 pipeline，再把 **raw X_train** 交给 CV。

```python
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_validate

pipe = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    KNeighborsClassifier()
)
cv = cross_validate(pipe, X_train_numeric, y_train, return_train_score=True)
```

每个 fold 都 clone 并 fit 一条新 pipeline：imputer 只学 fold training median，scaler 只学 fold training mean/SD，model 只学 fold training transformed data；validation 只 transform + score。

Pipeline 不能防止 analyst 反复查看 held-out test 并据此改选择。它保护已定义 procedure 的内部边界，不替代工作纪律。

## 7. 不同 columns 需要不同 transformations

普通 pipeline 的每一步作用于全部输入 columns。Mixed-type DataFrame 需要 `ColumnTransformer` 将 columns 分支处理，再水平拼接 outputs。

```python
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

numeric_pipe = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
)

preprocessor = make_column_transformer(
    (numeric_pipe, numeric_features),
    (OneHotEncoder(handle_unknown="ignore"), nominal_features),
    (OrdinalEncoder(categories=[level_order]), ordinal_features),
    ("passthrough", passthrough_features),
    ("drop", drop_features),
)

model_pipe = make_pipeline(preprocessor, SVC(kernel="rbf"))
```

### 7.1 运行语义

`model_pipe.fit(X,y)`：

1. 每个 branch 在各自 raw columns 上 fit/transform；
2. outputs 按 branch 顺序拼起来；
3. final estimator 在拼接矩阵上 fit。

`predict(new_X)`：每个 branch 只 transform，新 columns 结构保持与 training 一致，再交给 fitted estimator。

未列 columns 默认 drop。遗漏可能是 bug，必须核对每个 input feature 恰好属于一个 branch 或明确 drop。

### 7.2 Dense / sparse output

one-hot 可产生很多 0，sparse output 节省内存。ColumnTransformer 会根据各 branch 输出与 sparse threshold 决定 combined output。不要为了查看而对大型 sparse output 盲目 `.toarray()`。

`get_feature_names_out()` 可检查 transformed columns；检查时可在 training data 上 fit 一个副本，但用于 CV 的完整 pipeline 仍要接 raw data，让每折独立 fit。

## 8. 完整无泄漏工作流

1. 明确一行、target 与 prediction time。
2. 尽早 split held-out test；只在 training data 做影响选择的 EDA。
3. 按 feature semantics 分 numeric / nominal / ordinal / binary / drop。
4. 为每组建立 transformer；所有 learned steps 放 pipeline 内。
5. 用 CV 比 baseline、tree、k-NN、RBF SVM 等 candidates；同一 folds 与 metric。
6. 联合比较相关 hyperparameters；本周至少理解 `k`、`C`、`gamma` 的方向。
7. 选择 complete workflow 后，在全部 training data refit。
8. 对 test evaluate 一次；报告相对 baseline 的结果、split、preprocessing 与 random seeds。

## 9. 常见错误与判断

| 错误 | 为什么错 | 修正 |
|---|---|---|
| full data fit scaler 后 split | test 影响 representation | split first |
| X_train 先 fit_transform 再 CV | fold validation 泄漏 | pipeline 交给 CV |
| training/test 各 fit encoder | 相同 column position 可表示不同类别 | test 只 transform |
| nominal categories 编 0,1,2 | 制造 order/distance | one-hot |
| scaling ID | 数值接近无语义 | drop/re-engineer |
| target one-hot 后当 feature | 直接泄漏答案 | target 独立于 X |
| test score 反复比较 | test 变成 validation | 只在最终选择后一次使用 |
| tree 与 k-NN 一律同样 scale | 忽略 estimator properties | 按模型解释 preprocessing |

## 10. 独立微型例子：为什么 pipeline 改变 nearest neighbours

假设 training data 有 `age`、`income`，其中 income 以 dollars 计。raw k-NN 几乎只看 income。把 `StandardScaler` 放入 pipeline 后，两个 features 都以各自 training SD 为单位进入 distance。

在一次 CV fold 中，validation row 不参与 mean/SD；若它的 income 极端，仍只用 fold training statistics transform。这个细节正是 pipeline 必须进入 CV 的原因。

同理，若某 category 只出现在 validation fold：该 fold 的 `OneHotEncoder(handle_unknown="ignore")` 没见过它，会将其表示为全 0，而不会偷偷用 validation data 新建 column。不同 folds 可以学到不同 categories；CV 的目标就是模拟这种 unseen-data 流程。

## 11. 复习自检

1. Euclidean distance 的每一维是否真是可比较的 measurement？
2. 改 units 会不会改变 model？若会，是否需要 scaling？
3. 小/大 $k$、`gamma`、`C` 分别怎样影响 flexibility？
4. support vector 与 nearest neighbour 有什么不同？
5. 每个 transformer 在 fit 时学什么？
6. missing category、unknown category 与 dropped category 的 representation 是否混淆？
7. preprocessing 是否在 pipeline 内，并把 raw X 交给 CV？
8. ColumnTransformer 是否覆盖所有 columns 且没有 target？
9. test 是否只在最终 evaluate 一次？
10. score 是否相对 baseline 解读，而不是单独宣称“好”？

## 来源、版本差异与边界

### 当前课程来源

- [当前课程 README](/Users/youralmight/workspaces/reps/mdscl/DSCI_571/official/current/DSCI_571_sup-learn-1_students/README.md)
- [Chapter 3：Similarity-Based Models](/Users/youralmight/workspaces/reps/mdscl/DSCI_571/official/public/DSCI_571_sup-learn-1_book/book/03_kNNs-SVM-RBF.ipynb)
- [Chapter 4：Preprocessing, Pipelines, and Column Transformers](/Users/youralmight/workspaces/reps/mdscl/DSCI_571/official/public/DSCI_571_sup-learn-1_book/book/04_preprocessing-pipelines-column-transformers.ipynb)
- [Lecture 3 current demo](/Users/youralmight/workspaces/reps/mdscl/DSCI_571/official/current/DSCI_571_sup-learn-1_students/class-demos/demo-03-decision-boundaries-knn-SVC-demo.ipynb)
- [Lecture 4–5 current preprocessing demo](/Users/youralmight/workspaces/reps/mdscl/DSCI_571/official/current/DSCI_571_sup-learn-1_students/class-demos/demo-04-05-preprocessing.ipynb)
- [Lab 2 题面，仅用于识别应用范围](/Users/youralmight/workspaces/reps/mdscl/DSCI_571/assignments/lab2/DSCI_571_lab2_yz2000/lab2.ipynb)

### 版本差异

- 当前 demo README 仍列旧文件名 `demo-03-decision-boundaries-KNN-demo.ipynb` 与 `demo-04-05-preprocessing-demo.ipynb`，实际同步文件名分别含 `knn-SVC` 与 `preprocessing`；本文按实际当前文件。
- 当前 course README 的 Lecture 4 links 仍用旧在线 chapter filenames，而同步课程书已重组为 Chapter 4（含 ColumnTransformer）与 Chapter 5（More preprocessing/text）。本文只覆盖 Lecture 4 对应的 Chapter 4，不提前把 bag-of-words 当本周必学。
- 登录后的 PrairieLearn exit questions、Friday model answers 与推荐视频逐字稿未读取，不推断其内容。
- 本文没有填写 Lab 2 的 feature lists、reasoning、pipeline、CV 数值或最终 test 结果。