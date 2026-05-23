function showStatus(type, text) {
  const el = document.getElementById("loginStatus");
  el.className = "out " + (type || "");
  el.textContent = text;
}

document.getElementById("btnLogin").addEventListener("click", async () => {
  const login = document.getElementById("login").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!login || !password) {
    showStatus("err", "Введите логин и пароль");
    return;
  }

  try {
    const res = await apiPost("/auth/login", {
      login,
      password
    });

    showStatus("ok", "Успешный вход. Перенаправляю...");

    setTimeout(() => {
      if (res.user.role === "admin") {
        window.location.href = "admin.html";
      } else {
        window.location.href = "account.html";
      }
    }, 500);

  } catch (e) {
    showStatus("err", e.message || "Ошибка входа");
  }
});