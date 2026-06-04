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
    if len(values) < 2:
        return forecast_average(values, horizon)
    arr = np.array(values, dtype=float)
    model = ExponentialSmoothing(arr, trend="add", seasonal=None)
    fit = model.fit(optimized=True)
    fc = fit.forecast(horizon)
    return [round(float(x), 4) for x in fc.tolist()]

def forecast_neural(values: List[float], horizon: int) -> List[float]:
    arr = np.array(values, dtype=float)
    if len(arr) < 6:
        return forecast_moving(values, horizon)
    window = min(4, len(arr) - 2)
    hidden = 10
    epochs = 1800
    lr = 0.03
    wd = 1e-4
    mean = float(arr.mean())
    std = float(arr.std())
    if std == 0:
        return [round(mean, 4)] * horizon
    norm = (arr - mean) / std
    X, y = [], []
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
        z1 = X @ W1 + b1
        a1 = np.tanh(z1)
        pred = a1 @ W2 + b2
        error = pred - y
        d_pred = (2.0 / n) * error
        dW2 = a1.T @ d_pred + wd * W2
        db2 = np.sum(d_pred, axis=0, keepdims=True)
        da1 = d_pred @ W2.T
        dz1 = da1 * (1 - a1 * a1)
        W1 -= lr * (X.T @ dz1)
        b1 -= lr * np.sum(dz1, axis=0, keepdims=True)
        W2 -= lr * dW2
        b2 -= lr * db2
    history = list(norm)
    result = []
    for _ in range(horizon):
        x = np.array(history[-window:], dtype=float).reshape(1, -1)
        z1 = x @ W1 + b1
        a1 = np.tanh(z1)
        yhat = (a1 @ W2 + b2).item()
        history.append(yhat)
        result.append(round(float(yhat * std + mean), 4))
    return result

# --- Новый метод regression ---
def forecast_regression(values: List[float], horizon: int) -> List[float]:
    """
    values: простой числовой ряд
    horizon: количество прогнозируемых периодов
    """
    result = []
    series = list(values)

    for _ in range(horizon):
        # K_trud = 1, L = последний элемент ряда
        # delta_L = разница между последними элементами
        # delta_K_trud = 0, epsilon = 0
        L = series[-1]
        dL = series[-1] - series[-2] if len(series) > 1 else 0
        forecast = 1 * L + 0 * dL + 0
        forecast = round(float(forecast), 4)
        result.append(forecast)
        series.append(forecast)

    return result

def run_forecast(method: str, values: List, horizon: int) -> List[float]:
    method = (method or "").lower().strip()
    if method == "average":
        return forecast_average(values, horizon)
    if method == "moving":
        return forecast_moving(values, horizon)
    if method == "holt":
        return forecast_hw(values, horizon)
    if method == "neural":
        return forecast_neural(values, horizon)
    if method == "regression":
        return forecast_regression(values, horizon)
    return []