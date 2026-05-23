function showStatus(type, text) {
  const el = document.getElementById("registerStatus");
  el.className = "out " + (type || "");
  el.textContent = text;
}

document.getElementById("btnRegister").addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !email || !password) {
    showStatus("err", "Заполните все поля");
    return;
  }

  try {
    await apiPost("/auth/register", {
      username,
      email,
      password
    });

    showStatus("ok", "Аккаунт создан. Теперь можно войти.");

    setTimeout(() => {
      window.location.href = "login.html";
    }, 800);

  } catch (e) {
    showStatus("err", e.message || "Ошибка регистрации");
  }
});