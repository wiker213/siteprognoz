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
def forecast_regression(values: List[dict], horizon: int) -> List[float]:
    """
    values: список словарей с ключами K_trud, L, delta_K_trud, delta_L, epsilon
    horizon: сколько периодов вперед
    """
    result = []
    for i in range(horizon):
        last = values[-1] if values else {"K_trud":1,"L":1,"delta_K_trud":0,"delta_L":0,"epsilon":0}
        K = last.get("K_trud", 1)
        L = last.get("L", 1)
        dK = last.get("delta_K_trud", 0)
        dL = last.get("delta_L", 0)
        eps = last.get("epsilon", 0)
        forecast = K * L + dK * dL + eps
        result.append(round(float(forecast), 4))
        values.append({"K_trud": K, "L": L, "delta_K_trud": dK, "delta_L": dL, "epsilon": eps})
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