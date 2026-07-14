"""Pré-processamento e split de dados para o Wine Quality Dataset."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
    "free_so2_ratio",
]
CATEGORICAL_FEATURES = ["wine_type"]
TARGET = "high_quality"


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona features derivadas com significado enológico.

    free_so2_ratio: proporção do SO2 livre (ativo como antioxidante/
    antimicrobiano) sobre o SO2 total - mais informativa do que os dois
    valores absolutos isoladamente, já que é essa proporção que determina a
    eficácia da conservação do vinho.
    """
    df = df.copy()
    df["free_so2_ratio"] = df["free_sulfur_dioxide"] / df["total_sulfur_dioxide"]
    return df


def prepare_features_target(df: pd.DataFrame):
    df = add_engineered_features(df)
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]
    return X, y


def split_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """Remove duplicatas (evita vazamento treino/teste) e faz split estratificado."""
    df = df.drop_duplicates().reset_index(drop=True)
    X, y = prepare_features_target(df)
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(drop="if_binary"), CATEGORICAL_FEATURES),
        ]
    )
