const API_URL = "https://siteprognoz-1.onrender.com";

async function apiRequest(endpoint, options = {}) {
  const res = await fetch(API_URL + endpoint, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  });

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    throw new Error(data?.detail || "Ошибка запроса");
  }

  return data;
}

async function apiGet(endpoint) {
  return apiRequest(endpoint);
}

async function apiPost(endpoint, data) {
  return apiRequest(endpoint, {
    method: "POST",
    body: JSON.stringify(data)
  });
}

// Оставляем для совместимости со старым кодом.
// Теперь авторизация идёт через HttpOnly cookie.
async function apiPostAuth(endpoint, data) {
  return apiPost(endpoint, data);
}