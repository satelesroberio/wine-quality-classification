# POSTECH Tech Challenge Fase 2

**Aluno:** Robério da Cruz Sá Teles
**Curso:** POSTECH Data Analytics (DTAT)
**Case:** Classificando a qualidade de vinhos com Machine Learning

## Visão geral

Este repositório contém o desenvolvimento do Tech Challenge da Fase 2, cujo objetivo
é construir um modelo de classificação capaz de prever a qualidade de um vinho a
partir de suas características físico-químicas, usando o [Wine Quality Dataset](https://archive.ics.uci.edu/dataset/186/wine+quality)
(UCI/Kaggle). As amostras de vinho tinto e branco foram combinadas em uma única
base (6.497 amostras), com uma feature adicional `wine_type` indicando a origem.

A variável de qualidade original (nota de 0 a 10, atribuída por especialistas) é
transformada em uma classificação binária:

* **Alta Qualidade**: nota ≥ 7
* **Baixa/Média Qualidade**: nota < 7

## Pipeline do desafio

1. Compreensão do Problema
2. Análise Exploratória de Dados (EDA)
3. Pré-processamento de Dados
4. Desenvolvimento de Modelos (mínimo 2 classificadores)
5. Avaliação dos Modelos
6. Interpretação dos Resultados

## Estrutura do repositório

```
wine-quality-classification/
├── data/            # Base de dados utilizada
├── notebooks/       # Notebook com a análise e modelagem
├── src/             # Scripts auxiliares (pré-processamento ou modelagem)
├── results/         # Gráficos e métricas dos modelos
├── requirements.txt # Bibliotecas utilizadas
└── README.md        # Descrição do projeto
```

## Setup

```bash
git clone https://github.com/satelesroberio/wine-quality-classification.git
cd wine-quality-classification

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

O dataset já está versionado em `data/` (`winequality-red.csv`,
`winequality-white.csv` e `winequality_combined.csv`, gerado com `src/data_loader.py`).

## Reprodução dos notebooks

Os três notebooks são gerados e executados de ponta a ponta por um único script:

```bash
python src/build_notebooks.py
```

Isso recria `notebooks/01_eda.ipynb`, `02_preprocessing_modeling.ipynb` e
`03_evaluation_interpretation.ipynb`, e regrava as figuras/métricas em `results/`.

## Resultados

Dataset com 6.497 amostras (1.599 tintos + 4.898 brancos), sem valores nulos,
mas com 18,1% de linhas duplicadas (removidas antes do split treino/teste).
Target binário desbalanceado: 19,7% Alta Qualidade / 80,3% Baixa/Média.

Modelos treinados com pré-processamento (padronização + one-hot) e balanceamento
de classe (`class_weight`/`scale_pos_weight`), avaliados no conjunto de teste (20%, nunca visto no treino):

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| **Random Forest** | 0,836 | 0,554 | 0,688 | **0,614** | **0,875** | **0,633** |
| XGBoost | 0,806 | 0,493 | 0,688 | 0,574 | 0,859 | 0,591 |
| Regressão Logística | 0,728 | 0,392 | **0,782** | 0,522 | 0,815 | 0,466 |

**Random Forest** é o modelo recomendado (melhor F1, ROC-AUC e PR-AUC). A
Regressão Logística tem o maior recall e pode ser preferível em cenários de
triagem ampla, ao custo de muito mais falsos positivos.

**Variáveis mais influentes** (consistentes entre Random Forest e XGBoost):
`alcohol` (a mais importante, de forma isolada), seguida de `density`,
`chlorides` e `volatile_acidity`. Detalhes, gráficos e a discussão completa de
implicações para o processo produtivo estão no notebook
[`03_evaluation_interpretation.ipynb`](notebooks/03_evaluation_interpretation.ipynb).

## Entregáveis

* Repositório GitHub com os códigos utilizados (este repositório).
* [Apresentação executiva](results/apresentacao_executiva.pptx) ([PDF](results/apresentacao_executiva.pdf)) com o storytelling da análise exploratória e os resultados, em linguagem não técnica - inclui notas do apresentador em cada slide como roteiro de narração.
* [Vídeo executivo](results/video_executivo.mp4), em linguagem não técnica, gravado a partir da apresentação acima (duração atual: ~7min45s - acima do limite de 5 minutos do enunciado, considerar cortar antes da entrega final).
