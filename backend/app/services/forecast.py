from typing import List

import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def forecast_average(values: List[float], horizon: int) -> List[float]:
    avg = float(np.mean(values))
    return [round(avg, 4)] * horizon


def forecast_moving(values: List[float], horizon: int, window: int = 3) -> List[float]:
    w = min(window, len(values))
    avg = float(np.mean(values[-w:]))
    return [round(avg, 4)] * horizon


def forecast_hw(values: List[float], horizon: int) -> List[float]:
    """
    Holt / Exponential Smoothing.
    Используется тренд без сезонности.
    """

    if len(values) < 2:
        return forecast_average(values, horizon)

    arr = np.array(values, dtype=float)

    model = ExponentialSmoothing(
        arr,
        trend="add",
        seasonal=None
    )

    fit = model.fit(optimized=True)
    fc = fit.forecast(horizon)

    return [round(float(x), 4) for x in fc.tolist()]


def forecast_neural(values: List[float], horizon: int) -> List[float]:
    """
    Нейросетевой прогноз временного ряда.

    Это маленькая MLP-нейросеть:
    - берёт несколько предыдущих значений;
    - обучается предсказывать следующее значение;
    - затем строит прогноз рекурсивно.

    Плюс: не нужны TensorFlow/PyTorch.
    Минус: на очень коротких рядах прогноз может быть нестабильным.
    """

    arr = np.array(values, dtype=float)

    # Для очень коротких рядов нейросеть обучать бессмысленно.
    # Поэтому используем скользящее среднее как запасной вариант.
    if len(arr) < 6:
        return forecast_moving(values, horizon)

    # Окно — сколько прошлых значений нейросеть использует для прогноза следующего.
    window = min(4, len(arr) - 2)

    hidden = 10
    epochs = 1800
    learning_rate = 0.03
    weight_decay = 1e-4

    mean = float(arr.mean())
    std = float(arr.std())

    if std == 0:
        return [round(mean, 4)] * horizon

    # Нормализация нужна, чтобы нейросеть обучалась стабильнее.
    norm = (arr - mean) / std

    X = []
    y = []

    for i in range(len(norm) - window):
        X.append(norm[i:i + window])
        y.append(norm[i + window])

    X = np.array(X, dtype=float)
    y = np.array(y, dtype=float).reshape(-1, 1)

    rng = np.random.default_rng(42)

    W1 = rng.normal(0, 0.4, size=(window, hidden)) / np.sqrt(window)
    b1 = np.zeros((1, hidden))

    W2 = rng.normal(0, 0.4, size=(hidden, 1)) / np.sqrt(hidden)
    b2 = np.zeros((1, 1))

    n = X.shape[0]

    for _ in range(epochs):
        # Forward pass
        z1 = X @ W1 + b1
        a1 = np.tanh(z1)
        pred = a1 @ W2 + b2

        # Ошибка
        error = pred - y

        # Backpropagation
        d_pred = (2.0 / n) * error

        dW2 = a1.T @ d_pred + weight_decay * W2
        db2 = np.sum(d_pred, axis=0, keepdims=True)

        da1 = d_pred @ W2.T
        dz1 = da1 * (1 - a1 * a1)

        dW1 = X.T @ dz1 + weight_decay * W1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2

    # Рекурсивный прогноз
    history = list(norm)
    result = []

    for _ in range(horizon):
        x = np.array(history[-window:], dtype=float).reshape(1, -1)

        z1 = x @ W1 + b1
        a1 = np.tanh(z1)
        yhat = (a1 @ W2 + b2).item()

        history.append(yhat)

        value = yhat * std + mean
        result.append(round(float(value), 4))

    return result


def run_forecast(method: str, values: List[float], horizon: int) -> List[float]:
    method = (method or "").lower().strip()

    if method == "average":
        return forecast_average(values, horizon)

    if method == "moving":
        return forecast_moving(values, horizon)

    if method == "holt":
        return forecast_hw(values, horizon)

    if method == "neural":
        return forecast_neural(values, horizon)

    return []