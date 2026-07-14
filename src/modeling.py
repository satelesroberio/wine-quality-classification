"""Definição dos modelos de classificação usados no desafio."""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from preprocessing import build_preprocessor


def get_models(y_train) -> dict:
    """Retorna um dicionário {nome: Pipeline} com pré-processamento + classificador.

    Todos os modelos compensam o desbalanceamento de classes (~80/20) via
    ponderação de classe, em vez de reamostragem sintética, evitando
    distorcer a distribuição real no treino.
    """
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    models = {
        "logistic_regression": LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "xgboost": XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.1,
            scale_pos_weight=scale_pos_weight,
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        ),
    }

    return {
        name: Pipeline([("preprocessor", build_preprocessor()), ("classifier", clf)])
        for name, clf in models.items()
    }
