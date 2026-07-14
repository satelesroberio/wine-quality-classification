"""Geração programática dos notebooks do Tech Challenge Fase 2.

Cada notebook é montado célula a célula (nbformat) e executado (nbclient),
materializando outputs e figuras diretamente no .ipynb e em results/.
"""

from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks"


def md(text: str):
    return new_markdown_cell(text.strip())


def code(text: str):
    return new_code_cell(text.strip())


def build_eda_notebook():
    cells = [
        md("""
# 01 - Compreensão do Problema e Análise Exploratória (EDA)

**Tech Challenge Fase 2 - POSTECH Data Analytics**

Objetivo: prever a qualidade de um vinho a partir de suas características
físico-químicas, tratando o problema como uma **classificação binária**:

- **Alta Qualidade**: nota (`quality`) >= 7
- **Baixa/Média Qualidade**: nota < 7

Dataset: [Wine Quality Dataset](https://archive.ics.uci.edu/dataset/186/wine+quality)
(UCI/Kaggle), combinando as amostras de vinho tinto e branco em uma única base,
com uma coluna adicional `wine_type` indicando a origem.
"""),
        code("""
import sys
sys.path.insert(0, "../src")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from data_loader import load_dataset

sns.set_theme(style="whitegrid")
RESULTS = "../results"

df = load_dataset()
df.head()
"""),
        md("""
## Estrutura do dataset

6.497 amostras (1.599 tintos + 4.898 brancos), 11 variáveis físico-químicas
preditoras, mais `wine_type` (engenharia de feature), `quality` (nota original)
e `high_quality` (target binário).
"""),
        code("""
df.info()
"""),
        code("""
df.describe().T
"""),
        md("""
## Qualidade da entrada: nulos e duplicatas

Não há valores faltantes no dataset. Há, no entanto, **1.177 linhas duplicadas
(18,1% da base)** - um efeito conhecido deste dataset: como as variáveis são
medidas físico-químicas arredondadas em poucas casas decimais, diferentes
amostras acabam colidindo no mesmo perfil de valores. Essas duplicatas serão
removidas **antes do split treino/teste** na etapa de pré-processamento
(notebook 02), para evitar vazamento de dados (a mesma amostra aparecendo em
treino e teste simultaneamente).
"""),
        code("""
print("Valores nulos:", df.isnull().sum().sum())
print("Linhas duplicadas:", df.duplicated().sum(),
      f"({df.duplicated().mean()*100:.1f}%)")
"""),
        md("""
## Da nota original à classificação binária

A nota de qualidade concentra-se fortemente entre 5 e 7 (formato aproximadamente
normal, com poucas amostras nos extremos 3, 4, 8 e 9). Ao aplicar o corte em
`quality >= 7`, obtemos:

- **19,7%** das amostras como Alta Qualidade
- **80,3%** como Baixa/Média Qualidade

Ou seja, um desbalanceamento de aproximadamente **1 para 4**. Isso tem duas
implicações diretas para as próximas etapas:

1. **Métricas**: acurácia isoladamente é enganosa (um modelo trivial que sempre
   prevê "Baixa/Média" já acertaria ~80%). Serão priorizadas recall, precisão,
   F1 e AUC (ROC e Precision-Recall) para a classe minoritária.
2. **Modelagem**: será usado `class_weight="balanced"` (e equivalente via
   `scale_pos_weight` no XGBoost) para compensar o desbalanceamento durante o
   treino.

O desbalanceamento também varia por tipo de vinho: **13,6%** dos tintos são
Alta Qualidade contra **21,6%** dos brancos - um indício de que `wine_type`
pode carregar sinal relevante.
"""),
        code("""
fig, axes = plt.subplots(1, 3, figsize=(16, 4))

sns.countplot(data=df, x="quality", ax=axes[0], color="#4C72B0")
axes[0].set_title("Distribuição da nota original (quality)")

df["high_quality"].map({0: "Baixa/Média (<7)", 1: "Alta (>=7)"}).value_counts().plot(
    kind="bar", ax=axes[1], color=["#4C72B0", "#DD8452"]
)
axes[1].set_title("Distribuição do target binário")
axes[1].tick_params(axis="x", rotation=0)

df.groupby("wine_type")["high_quality"].mean().mul(100).plot(
    kind="bar", ax=axes[2], color=["#C44E52", "#55A868"]
)
axes[2].set_title("% Alta Qualidade por tipo de vinho")
axes[2].set_ylabel("%")
axes[2].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig(f"{RESULTS}/01_target_distribution.png", dpi=150)
plt.show()
"""),
        md("""
## Distribuição das variáveis físico-químicas por classe

Comparando a distribuição de cada variável entre as duas classes, é possível
identificar visualmente quais parecem separar melhor Alta Qualidade de
Baixa/Média Qualidade.
"""),
        code("""
features = [c for c in df.columns if c not in ("quality", "high_quality", "wine_type")]

fig, axes = plt.subplots(4, 3, figsize=(15, 16))
for ax, col in zip(axes.flat, features):
    sns.kdeplot(data=df, x=col, hue="high_quality", ax=ax, common_norm=False, legend=False)
    ax.set_title(col)
axes.flat[-1].axis("off")
fig.legend(["Baixa/Média", "Alta"], loc="lower right", bbox_to_anchor=(0.95, 0.05))
plt.tight_layout()
plt.savefig(f"{RESULTS}/02_feature_distributions.png", dpi=150)
plt.show()
"""),
        md("""
## Correlações com a qualidade

A tabela abaixo mostra a correlação de Pearson de cada variável com a nota
original (`quality`) e com o target binário (`high_quality`). A leitura é
consistente entre as duas versões da variável alvo, o que reforça que a
binarização não distorce o sinal presente nos dados.
"""),
        code("""
numeric_cols = [c for c in df.columns if c != "wine_type"]
corr = df[numeric_cols].corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
ax.set_title("Matriz de correlação")
plt.tight_layout()
plt.savefig(f"{RESULTS}/03_correlation_heatmap.png", dpi=150)
plt.show()

corr["high_quality"].drop(["high_quality", "quality"]).sort_values(key=abs, ascending=False)
"""),
        md("""
### Leitura das correlações (justificativa variável a variável)

- **Álcool (+0,39 com quality / +0,39 com high_quality)**: a correlação mais
  forte da base. Vinhos com maior teor alcoólico tendem a vir de uvas mais
  maduras (mais açúcar convertido em álcool na fermentação), associadas a
  perfis sensoriais mais encorpados e melhor avaliados por especialistas.
- **Densidade (-0,31 / -0,28)**: correlação negativa esperada, pois densidade
  e álcool são inversamente relacionados fisicamente (etanol é menos denso que
  água) - a densidade funciona quase como um proxy invertido do teor alcoólico
  e do açúcar residual.
- **Acidez volátil (-0,27 / -0,15)**: mede principalmente ácido acético,
  associado a defeitos de fermentação (contaminação bacteriana). Quanto maior,
  mais o vinho tende a apresentar aroma de vinagre, reduzindo a nota.
- **Cloretos (-0,20 / -0,16)**: proxy de salinidade/teor mineral da uva;
  concentrações altas geram gosto salgado indesejado, penalizando a avaliação.
- **Ácido cítrico (+0,09 / +0,05)**: correlação positiva fraca; em pequenas
  doses contribui para frescor e equilíbrio ácido, mas o efeito é discreto
  frente às demais variáveis.
- **Dióxido de enxofre livre (+0,06 / +0,01)**: correlação praticamente nula
  isoladamente; seu papel (antioxidante/antimicrobiano) só faz sentido em
  conjunto com o SO2 total, o que motiva a feature de proporção livre/total
  criada no pré-processamento (notebook 02).
- **Sulfatos (+0,04 / +0,03)** e **pH (+0,02 / +0,03)**: correlações lineares
  fracas com o target; podem ainda contribuir em interações não-lineares
  capturadas por modelos baseados em árvore.
- **Acidez fixa (-0,08 / -0,05)**, **SO2 total (-0,04 / -0,05)** e **açúcar
  residual (-0,04 / -0,06)**: correlações lineares desprezíveis com a
  qualidade nesta base - não devem ser descartadas do modelo, mas não são
  esperadas como preditoras fortes isoladamente.
"""),
        md("""
## Outliers

Usando a regra do IQR (1,5x o intervalo interquartil), a maior concentração de
outliers está em `citric_acid` (7,8%), `volatile_acidity` (5,8%) e
`fixed_acidity` (5,5%). `density` e `alcohol` praticamente não têm outliers
por esse critério (0,0%).

Os valores extremos de `residual_sugar` (máximo 65,8 g/L, quando a mediana é
~3 g/L) são fisicamente plausíveis - correspondem a vinhos de sobremesa/colheita
tardia, uma categoria legítima e não um erro de digitação. A mesma amostra
tende a puxar `density` para o extremo superior (correlação física
açúcar-densidade). A decisão é **não remover esses outliers** (são
observações válidas do domínio), mas usar `StandardScaler`/modelos robustos a
escala e, para os modelos baseados em árvore, essa sensibilidade é ainda menor.
"""),
        code("""
outlier_summary = []
for c in features:
    q1, q3 = df[c].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = ((df[c] < low) | (df[c] > high)).sum()
    outlier_summary.append({"feature": c, "n_outliers": n_out, "pct": round(n_out / len(df) * 100, 2)})

outlier_df = pd.DataFrame(outlier_summary).sort_values("pct", ascending=False)
outlier_df
"""),
        code("""
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, col in zip(axes, ["alcohol", "density", "volatile_acidity", "chlorides"]):
    sns.boxplot(data=df, x="high_quality", y=col, ax=ax, palette=["#4C72B0", "#DD8452"])
    ax.set_xticklabels(["Baixa/Média", "Alta"])
    ax.set_title(col)
plt.tight_layout()
plt.savefig(f"{RESULTS}/04_boxplots_top_features.png", dpi=150)
plt.show()
"""),
        md("""
## Resumo da EDA (insumo para a apresentação executiva)

- Dataset limpo (sem nulos), mas com 18,1% de duplicatas a remover antes da
  modelagem.
- Classes desbalanceadas (~80/20) - decide a escolha de métricas e a
  necessidade de ponderar classes no treino.
- `alcohol`, `density`, `volatile_acidity` e `chlorides` são as variáveis mais
  associadas à qualidade e serão o foco da interpretação dos modelos.
- `wine_type` carrega sinal (brancos têm quase o dobro da taxa de alta
  qualidade dos tintos) e será mantido como feature categórica.
"""),
        code("""
summary = {
    "n_amostras": len(df),
    "pct_nulos": 0.0,
    "pct_duplicatas": round(df.duplicated().mean() * 100, 2),
    "pct_alta_qualidade": round(df["high_quality"].mean() * 100, 2),
    "pct_alta_qualidade_tinto": round(df.loc[df.wine_type == "red", "high_quality"].mean() * 100, 2),
    "pct_alta_qualidade_branco": round(df.loc[df.wine_type == "white", "high_quality"].mean() * 100, 2),
    "top_corr_feature": corr["high_quality"].drop(["high_quality", "quality"]).abs().idxmax(),
}
pd.Series(summary).to_csv(f"{RESULTS}/eda_summary.csv", header=["valor"])
summary
"""),
    ]

    nb = new_notebook(cells=cells)
    return nb


def build_preprocessing_modeling_notebook():
    cells = [
        md("""
# 02 - Pré-processamento e Modelagem

Com o entendimento construído na EDA (notebook 01), esta etapa cobre o
pré-processamento dos dados e o treinamento de três modelos de classificação:
**Regressão Logística** (baseline linear e interpretável), **Random Forest**
e **XGBoost** (ensembles de árvore, capazes de capturar não-linearidades e
interações entre variáveis).
"""),
        code("""
import sys
sys.path.insert(0, "../src")
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import StratifiedKFold, cross_val_score

from data_loader import load_dataset
from modeling import get_models
from preprocessing import split_data

sns.set_theme(style="whitegrid")
RESULTS = "../results"

df = load_dataset()
print("Shape original:", df.shape)
"""),
        md("""
## Decisões de pré-processamento

1. **Remoção de duplicatas antes do split** - as 1.177 linhas duplicadas
   identificadas na EDA são removidas primeiro, para que a mesma amostra nunca
   apareça simultaneamente em treino e teste (vazamento de dados).
2. **Split estratificado 80/20** (`random_state=42`) - mantém a proporção
   ~19,7% de Alta Qualidade em treino e teste.
3. **Feature engineering**: `free_so2_ratio = free_sulfur_dioxide /
   total_sulfur_dioxide`. O SO2 total isolado tem correlação quase nula com a
   qualidade (visto na EDA); o que importa enologicamente é a fração que
   permanece livre (ativa como conservante), não o valor absoluto.
4. **Padronização** (`StandardScaler`) das variáveis numéricas e
   **one-hot encoding** de `wine_type` - aplicados dentro de um
   `ColumnTransformer`/`Pipeline` do scikit-learn, para evitar vazamento entre
   treino e teste (o `fit` do scaler ocorre apenas nos dados de treino).
"""),
        code("""
X_train, X_test, y_train, y_test = split_data(df)

print("Treino:", X_train.shape, " Teste:", X_test.shape)
print("Proporção Alta Qualidade - treino:", round(y_train.mean(), 4),
      " teste:", round(y_test.mean(), 4))
"""),
        md("""
## Tratamento do desbalanceamento de classes

Em vez de reamostragem sintética (SMOTE), optou-se por **ponderação de
classe** (`class_weight="balanced"` na Regressão Logística e Random Forest;
`scale_pos_weight` equivalente no XGBoost). Essa escolha evita gerar amostras
sintéticas em um espaço físico-químico onde a plausibilidade dos pontos
gerados é difícil de garantir, mantendo o treino sobre dados reais.
"""),
        code("""
models = get_models(y_train)

for name, pipe in models.items():
    pipe.fit(X_train, y_train)
    print(f"{name} treinado.")
"""),
        md("""
## Validação cruzada no treino (checagem prévia)

Antes de ir para a avaliação final no conjunto de teste (notebook 03), uma
validação cruzada estratificada de 5 folds no treino, usando F1 da classe
"Alta Qualidade" como métrica, dá uma primeira leitura de estabilidade e
desempenho relativo entre os três modelos.
"""),
        code("""
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_results = []
for name, pipe in models.items():
    scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1)
    cv_results.append({"modelo": name, "f1_mean": scores.mean(), "f1_std": scores.std()})
    print(f"{name:20s} F1 CV: {scores.mean():.3f} +- {scores.std():.3f}")

cv_df = pd.DataFrame(cv_results).sort_values("f1_mean", ascending=False)
cv_df
"""),
        code("""
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(cv_df["modelo"], cv_df["f1_mean"], yerr=cv_df["f1_std"], capsize=5,
       color=["#4C72B0", "#55A868", "#C44E52"])
ax.set_ylabel("F1 (classe Alta Qualidade) - média CV 5-fold")
ax.set_title("Comparação preliminar dos modelos (treino)")
plt.tight_layout()
plt.savefig(f"{RESULTS}/05_cv_f1_comparison.png", dpi=150)
plt.show()
"""),
        md("""
## Resultado preliminar

Na validação cruzada do treino, o **Random Forest** apresentou o melhor F1
médio (~0,56), seguido por XGBoost (~0,54) e Regressão Logística (~0,54) - uma
vantagem pequena mas consistente do Random Forest, sugerindo que relações
não-lineares/interações entre variáveis (ex.: álcool e densidade) importam
mais do que efeitos puramente lineares. A confirmação final e a comparação
completa de métricas (precisão, recall, ROC-AUC, matriz de confusão) no
conjunto de teste, nunca visto pelos modelos, são feitas no notebook 03.
"""),
    ]

    nb = new_notebook(cells=cells)
    return nb


def build_evaluation_notebook():
    cells = [
        md("""
# 03 - Avaliação dos Modelos e Interpretação dos Resultados

Avaliação dos três modelos treinados (notebook 02) no conjunto de **teste**
(dados nunca vistos durante o treino), seguida da interpretação de quais
variáveis mais influenciam a previsão de qualidade e das implicações práticas
para o processo produtivo.
"""),
        code("""
import sys
sys.path.insert(0, "../src")
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (ConfusionMatrixDisplay, PrecisionRecallDisplay,
                              RocCurveDisplay, accuracy_score, average_precision_score,
                              confusion_matrix, f1_score, precision_score, recall_score,
                              roc_auc_score)

from data_loader import load_dataset
from modeling import get_models
from preprocessing import split_data

sns.set_theme(style="whitegrid")
RESULTS = "../results"

df = load_dataset()
X_train, X_test, y_train, y_test = split_data(df)

models = get_models(y_train)
for name, pipe in models.items():
    pipe.fit(X_train, y_train)
print("Modelos treinados:", list(models.keys()))
"""),
        md("""
## Escolha das métricas

Como visto na EDA, o target é desbalanceado (~80/20). Um classificador trivial
que sempre previsse "Baixa/Média Qualidade" já atingiria ~80% de acurácia sem
nenhum valor preditivo real. Por isso a avaliação prioriza:

- **Precisão e Recall da classe "Alta Qualidade"** - respectivamente, "das
  vezes que o modelo aposta em alta qualidade, quantas acertou" e "de todos os
  vinhos realmente de alta qualidade, quantos o modelo encontrou".
- **F1-score** - equilíbrio entre as duas.
- **ROC-AUC** - separabilidade geral entre as classes.
- **PR-AUC (average precision)** - mais informativa que ROC-AUC quando a
  classe positiva é minoritária, pois não é inflada pelos muitos verdadeiros
  negativos.
- Acurácia é reportada apenas como referência complementar, não como métrica
  de decisão.
"""),
        code("""
rows = []
proba_by_model = {}
for name, pipe in models.items():
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]
    proba_by_model[name] = y_proba
    rows.append({
        "modelo": name,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "pr_auc": average_precision_score(y_test, y_proba),
    })

metrics_df = pd.DataFrame(rows).set_index("modelo").round(3).sort_values("f1", ascending=False)
metrics_df.to_csv(f"{RESULTS}/metrics_comparison.csv")
metrics_df
"""),
        md("""
## Leitura dos resultados no conjunto de teste

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Random Forest | 0,836 | 0,554 | 0,688 | **0,614** | **0,875** | **0,633** |
| XGBoost | 0,806 | 0,493 | 0,688 | 0,574 | 0,859 | 0,591 |
| Regressão Logística | 0,728 | 0,392 | **0,782** | 0,522 | 0,815 | 0,466 |

- **Random Forest** vence em quase todas as métricas (F1, ROC-AUC, PR-AUC,
  precisão e acurácia) - é o modelo recomendado como escolha principal.
- **Regressão Logística** tem o maior recall (0,78): identifica mais vinhos
  de alta qualidade de fato, mas ao custo de muito mais falsos positivos
  (precisão de apenas 0,39 - menos de 4 em cada 10 vinhos que ela aponta como
  "alta qualidade" realmente são).
- **XGBoost** fica no meio termo, sem superar o Random Forest em nenhuma
  métrica nesta configuração de hiperparâmetros.

**Implicação de negócio**: a escolha entre Random Forest e Regressão Logística
depende do custo relativo do erro. Se o objetivo é **triagem ampla** (não
deixar passar nenhum lote potencialmente premium, aceitando revisar manualmente
alguns falsos positivos), a Regressão Logística's maior recall pode ser
preferível. Se o objetivo é **confiabilidade do rótulo** (por exemplo, decidir
sozinho, sem revisão humana, quais lotes recebem selo de alta qualidade), o
Random Forest é a escolha mais segura por sua precisão muito superior.
"""),
        code("""
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (name, pipe) in zip(axes, models.items()):
    y_pred = pipe.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm, display_labels=["Baixa/Média", "Alta"]).plot(ax=ax, colorbar=False)
    ax.set_title(name)
plt.tight_layout()
plt.savefig(f"{RESULTS}/06_confusion_matrices.png", dpi=150)
plt.show()
"""),
        code("""
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for name, pipe in models.items():
    RocCurveDisplay.from_estimator(pipe, X_test, y_test, ax=axes[0], name=name)
    PrecisionRecallDisplay.from_estimator(pipe, X_test, y_test, ax=axes[1], name=name)
axes[0].set_title("Curva ROC")
axes[1].set_title("Curva Precision-Recall")
plt.tight_layout()
plt.savefig(f"{RESULTS}/07_roc_pr_curves.png", dpi=150)
plt.show()
"""),
        md("""
## Interpretação: quais variáveis mais influenciam a qualidade

Para os modelos de árvore (Random Forest, XGBoost) foi extraída a
importância de cada variável (`feature_importances_`); para a Regressão
Logística, os coeficientes padronizados (comparáveis entre si porque as
variáveis foram escalonadas antes do treino).
"""),
        code("""
feat_names = models["random_forest"].named_steps["preprocessor"].get_feature_names_out()
feat_names = [f.split("__")[-1] for f in feat_names]

rf_imp = pd.Series(models["random_forest"].named_steps["classifier"].feature_importances_, index=feat_names)
xgb_imp = pd.Series(models["xgboost"].named_steps["classifier"].feature_importances_, index=feat_names)
lr_coef = pd.Series(models["logistic_regression"].named_steps["classifier"].coef_[0], index=feat_names)

importance_df = pd.DataFrame({
    "random_forest": rf_imp,
    "xgboost": xgb_imp,
    "logistic_regression_coef": lr_coef,
}).sort_values("random_forest", ascending=False)
importance_df.to_csv(f"{RESULTS}/feature_importance.csv")
importance_df
"""),
        code("""
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

top_rf = importance_df["random_forest"].sort_values()
axes[0].barh(top_rf.index, top_rf.values, color="#4C72B0")
axes[0].set_title("Importância de features - Random Forest")

top_lr = lr_coef.reindex(lr_coef.abs().sort_values().index)
colors = ["#C44E52" if v < 0 else "#55A868" for v in top_lr.values]
axes[1].barh(top_lr.index, top_lr.values, color=colors)
axes[1].set_title("Coeficientes padronizados - Regressão Logística")

plt.tight_layout()
plt.savefig(f"{RESULTS}/08_feature_importance.png", dpi=150)
plt.show()
"""),
        md("""
### Síntese da interpretação

- **Álcool é, de forma consistente, a variável mais importante** nos três
  modelos (importância de 0,21 no Random Forest e 0,34 no XGBoost - a maior
  isoladamente). Confirma o que já aparecia na correlação da EDA (+0,39):
  vinhos com maior teor alcoólico tendem a ser mais bem avaliados.
- **Density, chlorides e volatile_acidity** aparecem consistentemente entre as
  variáveis mais relevantes nos modelos de árvore, replicando o padrão visto
  na EDA.
- A **Regressão Logística diverge parcialmente** dos modelos de árvore: nela,
  `density` tem o maior coeficiente em módulo, e `residual_sugar` e
  `fixed_acidity` aparecem com peso alto e sinal positivo - o que contradiz a
  correlação marginal quase nula dessas duas variáveis vista na EDA. Isso é um
  efeito clássico de **multicolinearidade**: density, residual_sugar, alcohol
  e fixed_acidity são fisicamente relacionadas entre si, e a regressão linear
  redistribui o peso entre elas de forma instável. Os modelos de árvore, mais
  robustos a essa colinearidade, são a leitura mais confiável de importância
  neste caso.
- `wine_type` tem importância baixa em todos os modelos - a diferença de taxa
  de alta qualidade entre tintos e brancos vista na EDA é, portanto,
  majoritariamente **explicada pelas variáveis físico-químicas em si** (que
  diferem sistematicamente entre os dois tipos), não por um efeito
  independente do tipo de vinho.
- `free_so2_ratio` (feature criada) tem importância comparável às variáveis
  originais de SO2 isoladas, validando a decisão de engenharia de feature
  tomada no pré-processamento.

## Implicações para o processo de produção

1. **Controle do teor alcoólico** é a alavanca de maior impacto identificada:
   decisões de colheita (ponto de maturação da uva) e condução da fermentação
   que elevem o álcool dentro da faixa estilística do vinho tendem a
   correlacionar com notas mais altas.
2. **Acidez volátil** é o principal indicador de risco de defeito
   (contaminação bacteriana/acética) associado à queda de qualidade - reforça
   a importância de controle sanitário e de temperatura durante a
   fermentação/armazenamento.
3. **Cloretos**, ligados a características do terroir/água de irrigação,
   aparecem como fator relevante mas de mais difícil controle direto pelo
   enólogo - útil como critério de seleção de fornecedores/vinhedos.
4. **A proporção de SO2 livre sobre o total** (não os valores absolutos)
   importa para a conservação - sugere calibrar a dosagem de sulfitos em
   função do SO2 total já presente no mosto, não apenas por volume fixo.
5. **Modelo recomendado para uso**: Random Forest, por equilibrar melhor
   precisão e recall (F1 = 0,614, PR-AUC = 0,633); a Regressão Logística é uma
   alternativa caso a prioridade do negócio seja não deixar passar nenhum lote
   potencialmente de alta qualidade, mesmo com mais revisão manual de falsos
   positivos.
"""),
    ]

    nb = new_notebook(cells=cells)
    return nb


def execute_and_save(nb, filename: str):
    NOTEBOOKS_DIR.mkdir(exist_ok=True)
    path = NOTEBOOKS_DIR / filename
    client = NotebookClient(nb, resources={"metadata": {"path": str(NOTEBOOKS_DIR)}})
    client.execute()
    with open(path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Notebook executado e salvo: {path}")


if __name__ == "__main__":
    (ROOT / "results").mkdir(exist_ok=True)
    execute_and_save(build_eda_notebook(), "01_eda.ipynb")
    execute_and_save(build_preprocessing_modeling_notebook(), "02_preprocessing_modeling.ipynb")
    execute_and_save(build_evaluation_notebook(), "03_evaluation_interpretation.ipynb")
