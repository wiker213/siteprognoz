let currentUser = null;

function showUpdateStatus(type, text) {
  const el = document.getElementById("updateStatus");
  el.className = "out " + (type || "");
  el.textContent = text;
}

async function checkAdmin() {
  const box = document.getElementById("adminInfo");

  try {
    currentUser = await apiGet("/auth/me");

    if (currentUser.role !== "admin") {
      box.className = "out err";
      box.textContent = "Доступ запрещён. Нужна роль администратора.";

      setTimeout(() => {
        window.location.href = "account.html";
      }, 800);

      return;
    }

    box.className = "out ok";
    box.innerHTML = `
      <b>Администратор:</b> ${currentUser.username}<br>
      <b>Email:</b> ${currentUser.email}
    `;

  } catch (e) {
    box.className = "out err";
    box.textContent = "Вы не авторизованы. Перенаправляю на вход...";

    setTimeout(() => {
      window.location.href = "login.html";
    }, 700);
  }
}

document.getElementById("btnAddUpdate").addEventListener("click", async () => {
  const date = document.getElementById("updateDate").value.trim();
  const source = document.getElementById("updateSource").value.trim();

  const indicators = document
    .getElementById("updateIndicators")
    .value
    .split(",")
    .map(item => item.trim())
    .filter(Boolean);

  if (!date || !source || indicators.length === 0) {
    showUpdateStatus("err", "Заполните все поля");
    return;
  }

  try {
    await apiPost("/updates", {
      date,
      source,
      indicators
    });

    showUpdateStatus("ok", "Обновление добавлено");

  } catch (e) {
    showUpdateStatus("err", e.message || "Ошибка добавления");
  }
});

document.getElementById("btnLogout").addEventListener("click", async () => {
  try {
    await apiPost("/auth/logout", {});
  } catch (e) {}

  window.location.href = "login.html";
});

checkAdmin();