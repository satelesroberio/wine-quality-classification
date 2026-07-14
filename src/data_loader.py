"""Carregamento e preparação do Wine Quality Dataset (UCI/Kaggle)."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

QUALITY_THRESHOLD = 7


def load_raw() -> pd.DataFrame:
    """Carrega e combina os arquivos de vinho tinto e branco."""
    red = pd.read_csv(DATA_DIR / "winequality-red.csv", sep=";")
    white = pd.read_csv(DATA_DIR / "winequality-white.csv", sep=";")

    red["wine_type"] = "red"
    white["wine_type"] = "white"

    df = pd.concat([red, white], ignore_index=True)
    df.columns = [c.replace(" ", "_") for c in df.columns]
    return df


def add_binary_target(df: pd.DataFrame, threshold: int = QUALITY_THRESHOLD) -> pd.DataFrame:
    """Adiciona a coluna binária high_quality (1 = nota >= threshold)."""
    df = df.copy()
    df["high_quality"] = (df["quality"] >= threshold).astype(int)
    return df


def load_dataset() -> pd.DataFrame:
    """Pipeline completo: carrega, combina e binariza o target."""
    return add_binary_target(load_raw())


if __name__ == "__main__":
    data = load_dataset()
    print(data.shape)
    print(data["high_quality"].value_counts(normalize=True))
