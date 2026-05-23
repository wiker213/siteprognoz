async function loadAccount() {
  const box = document.getElementById("accountInfo");
  const adminLink = document.getElementById("adminLink");

  try {
    const user = await apiGet("/auth/me");

    box.className = "out ok";
    box.innerHTML = `
      <b>Логин:</b> ${user.username}<br>
      <b>Email:</b> ${user.email}<br>
      <b>Роль:</b> ${user.role === "admin" ? "Администратор" : "Пользователь"}
    `;

    if (user.role === "admin") {
      adminLink.innerHTML = `
        <div class="actions">
          <a class="btn" href="admin.html">Перейти в кабинет администратора</a>
        </div>
      `;
    }

  } catch (e) {
    box.className = "out err";
    box.textContent = "Вы не авторизованы. Перенаправляю на вход...";

    setTimeout(() => {
      window.location.href = "login.html";
    }, 700);
  }
}

document.getElementById("btnLogout").addEventListener("click", async () => {
  try {
    await apiPost("/auth/logout", {});
  } catch (e) {}

  window.location.href = "login.html";
});

loadAccount();