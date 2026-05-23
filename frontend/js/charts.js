let chartInstance = null;


function showStatus(type, text) {
  const el = document.getElementById("chartStatus");

  if (!el) {
    return;
  }

  el.className = "out " + (type || "");
  el.textContent = text;
}


function parseSeries(raw) {
  const text = String(raw || "").trim();

  if (!text) {
    return {
      ok: false,
      error: "Вставь ряд чисел."
    };
  }

  let parts;

  if (/[;\t\n]/.test(text)) {
    parts = text.split(/[;\t\n]+/);
  } else {
    parts = text.split(",");
  }

  const values = parts
    .map(s => s.trim())
    .filter(Boolean)
    .map(s => Number(s.replace(",", ".")));

  if (!values.length) {
    return {
      ok: false,
      error: "Вставь ряд чисел."
    };
  }

  if (values.some(v => Number.isNaN(v))) {
    return {
      ok: false,
      error: "Есть нечисловые значения. Для списка через запятую дроби вводи точкой: 107.1. Для десятичной запятой используй разделитель ; или перенос строки."
    };
  }

  return {
    ok: true,
    values
  };
}


function buildLabels(n) {
  return Array.from({ length: n }, (_, i) => String(i + 1));
}


function getSelectedMethods() {
  const methods = [];

  const average = document.getElementById("m_avg");
  const moving = document.getElementById("m_mov");
  const holt = document.getElementById("m_holt");
  const neural = document.getElementById("m_neural");

  if (average && average.checked) {
    methods.push({
      id: "average",
      title: "Average"
    });
  }

  if (moving && moving.checked) {
    methods.push({
      id: "moving",
      title: "Moving"
    });
  }

  if (holt && holt.checked) {
    methods.push({
      id: "holt",
      title: "Holt"
    });
  }

  if (neural && neural.checked) {
    methods.push({
      id: "neural",
      title: "Нейросеть MLP"
    });
  }

  return methods;
}


async function buildChart() {
  const seriesEl = document.getElementById("series");
  const horizonEl = document.getElementById("horizon");
  const modeEl = document.getElementById("mode");

  if (!seriesEl || !horizonEl || !modeEl) {
    showStatus("err", "Не найдены элементы формы. Проверь charts.html");
    return;
  }

  const raw = seriesEl.value.trim();
  const horizon = Number(horizonEl.value);
  const mode = modeEl.value;
  const methods = getSelectedMethods();

  const parsed = parseSeries(raw);

  if (!parsed.ok) {
    showStatus("err", "Ошибка: " + parsed.error);
    return;
  }

  if (!methods.length) {
    showStatus("err", "Выбери хотя бы один метод прогнозирования.");
    return;
  }

  const values = parsed.values;

  const hasNeural = methods.some(method => method.id === "neural");

  if (hasNeural && values.length < 6) {
    showStatus(
      "err",
      "Для нейросетевого прогноза желательно минимум 6 значений временного ряда."
    );
    return;
  }

  showStatus("", "Считаю прогнозы…");

  const forecasts = {};

  try {
    for (const method of methods) {
      const res = await apiPost("/forecast", {
        method: method.id,
        values: values,
        horizon: horizon
      });

      if (res && res.error) {
        showStatus("err", `Метод ${method.title}: ${res.error}`);
        return;
      }

      if (!res || !Array.isArray(res.forecast)) {
        showStatus("err", `Метод ${method.title}: backend не вернул forecast`);
        return;
      }

      forecasts[method.id] = res.forecast;
    }

    const datasets = [];

    const fullLen = mode === "append"
      ? values.length + horizon
      : horizon;

    const labels = buildLabels(fullLen);

    if (mode === "append") {
      datasets.push({
        label: "Факт",
        data: values.concat(Array(horizon).fill(null)),
        borderWidth: 2,
        pointRadius: 2,
        tension: 0.25
      });
    }

    for (const method of methods) {
      const forecast = forecasts[method.id] || [];

      const data = mode === "append"
        ? Array(values.length).fill(null).concat(forecast)
        : forecast;

      datasets.push({
        label: "Прогноз • " + method.title,
        data: data,
        borderWidth: 2,
        pointRadius: 2,
        tension: 0.25
      });
    }

    renderChart(labels, datasets);

    let note = "";

    if (methods.some(method => method.id === "average" || method.id === "moving")) {
      note += "\nAverage и Moving часто дают постоянный прогноз.";
    }

    if (methods.some(method => method.id === "holt")) {
      note += "\nHolt учитывает тренд, но не учитывает сезонность.";
    }

    if (methods.some(method => method.id === "neural")) {
      note += "\nНейросеть MLP обучается на введённом ряду. Чем больше данных, тем лучше прогноз.";
    }

    showStatus(
      "ok",
      `График построен. Методы: ${methods.map(method => method.title).join(", ")}.${note}`
    );

  } catch (e) {
    showStatus("err", e.message || "Ошибка построения графика");
  }
}


function renderChart(labels, datasets) {
  const canvas = document.getElementById("chart");

  if (!canvas) {
    showStatus("err", "Не найден canvas #chart");
    return;
  }

  if (typeof Chart === "undefined") {
    showStatus("err", "Chart.js не загружен. Проверь подключение CDN в charts.html");
    return;
  }

  const ctx = canvas.getContext("2d");

  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }

  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,

      interaction: {
        mode: "index",
        intersect: false
      },

      plugins: {
        legend: {
          labels: {
            color: "#1f2937",
            font: {
              size: 13,
              weight: "600"
            },
            padding: 16
          }
        },

        tooltip: {
          enabled: true,
          backgroundColor: "rgba(17, 24, 39, 0.92)",
          titleColor: "#ffffff",
          bodyColor: "#ffffff",
          borderColor: "rgba(255, 255, 255, 0.25)",
          borderWidth: 1,
          padding: 12
        }
      },

      scales: {
        x: {
          ticks: {
            color: "#374151",
            font: {
              size: 12,
              weight: "500"
            }
          },
          grid: {
            color: "rgba(55, 65, 81, 0.12)"
          }
        },

        y: {
          ticks: {
            color: "#374151",
            font: {
              size: 12,
              weight: "500"
            }
          },
          grid: {
            color: "rgba(55, 65, 81, 0.12)"
          }
        }
      }
    }
  });
}


function exportPNG() {
  if (!chartInstance) {
    showStatus("err", "Сначала построй график.");
    return;
  }

  const url = chartInstance.toBase64Image("image/png", 1);
  const a = document.createElement("a");

  a.href = url;
  a.download = "chart.png";
  a.click();
}


function fillUnemployed() {
  const seriesEl = document.getElementById("series");
  const horizonEl = document.getElementById("horizon");
  const modeEl = document.getElementById("mode");

  if (seriesEl) {
    seriesEl.value = "121,110,102,107.1,86.8,76.7,68.7,54.5";
  }

  if (horizonEl) {
    horizonEl.value = "12";
  }

  if (modeEl) {
    modeEl.value = "append";
  }

  showStatus("", "Ряд вставлен. Нажми «Построить график».");
}


document.addEventListener("DOMContentLoaded", () => {
  const btnBuild = document.getElementById("btnBuild");
  const btnFill = document.getElementById("btnFill");
  const btnExport = document.getElementById("btnExport");

  if (btnBuild) {
    btnBuild.addEventListener("click", buildChart);
  }

  if (btnFill) {
    btnFill.addEventListener("click", fillUnemployed);
  }

  if (btnExport) {
    btnExport.addEventListener("click", exportPNG);
  }

  const fileInput = document.getElementById("fileInput");
  const seriesEl = document.getElementById("series");

  if (fileInput && seriesEl) {
    fileInput.addEventListener("change", (event) => {
      const file = event.target.files && event.target.files[0];

      if (!file) {
        return;
      }

      const reader = new FileReader();

      reader.onload = (e) => {
        const text = String(e.target.result || "")
          .replace(/\r\n/g, "\n")
          .trim();

        seriesEl.value = text;

        showStatus(
          "ok",
          `Файл загружен: ${file.name}. Нажми «Построить график».`
        );
      };

      reader.onerror = () => {
        showStatus("err", "Ошибка чтения файла.");
      };

      reader.readAsText(file);
    });
  }
});


window.buildChart = buildChart;
window.exportPNG = exportPNG;
window.fillUnemployed = fillUnemployed;