# POSTECH Tech Challenge Fase 2

**Aluno:** Robério da Cruz Sá Teles
**Curso:** POSTECH Data Analytics (DTAT)
**Case:** Classificando a qualidade de vinhos com Machine Learning

## Visão geral

Este repositório contém o desenvolvimento do Tech Challenge da Fase 2, cujo objetivo
é construir um modelo de classificação capaz de prever a qualidade de um vinho a
partir de suas características físico-químicas, usando o [Wine Quality Dataset](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset).

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

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Entregáveis

* Repositório GitHub com os códigos utilizados (este repositório).
* Apresentação executiva com o storytelling da análise exploratória.
* Vídeo executivo de até 5 minutos, em linguagem não técnica.
