const $ = (id) => document.getElementById(id);

const INDICATORS = [
  {
    id: "vrp_production",
    title: "ВРП (производственный метод)",
    formula: "ВРП = Выпуск товаров и услуг − Промежуточное потребление",
    resultUnit: "млн руб.",
    fields: [
      {
        key: "output",
        label: "Выпуск товаров и услуг",
        unit: "млн руб.",
        placeholder: "например: 5000",
        desc: "Общий объём произведённых товаров и услуг"
      },
      {
        key: "intermediate",
        label: "Промежуточное потребление",
        unit: "млн руб.",
        placeholder: "например: 1800",
        desc: "Стоимость товаров и услуг, использованных в производстве"
      }
    ],
    example: {
      output: 5000,
      intermediate: 1800
    }
  },

  {
    id: "vrp_income",
    title: "ВРП (метод доходов)",
    formula: "ВРП = Оплата труда + Прибыль + Налоги",
    resultUnit: "млн руб.",
    fields: [
      {
        key: "wages",
        label: "Оплата труда",
        unit: "млн руб.",
        placeholder: "например: 1200",
        desc: "Совокупная заработная плата работников"
      },
      {
        key: "profit",
        label: "Прибыль",
        unit: "млн руб.",
        placeholder: "например: 900",
        desc: "Валовая прибыль организаций"
      },
      {
        key: "taxes",
        label: "Налоги",
        unit: "млн руб.",
        placeholder: "например: 300",
        desc: "Налоги на производство и импорт"
      }
    ],
    example: {
      wages: 1200,
      profit: 900,
      taxes: 300
    }
  },

  {
    id: "vrp_final",
    title: "ВРП (конечный метод)",
    formula: "ВРП = Потребление + Инвестиции + Чистый экспорт",
    resultUnit: "млн руб.",
    fields: [
      {
        key: "consumption",
        label: "Потребление",
        unit: "млн руб.",
        placeholder: "например: 700",
        desc: "Расходы на конечное потребление"
      },
      {
        key: "investment",
        label: "Инвестиции",
        unit: "млн руб.",
        placeholder: "например: 200",
        desc: "Валовое накопление / инвестиции"
      },
      {
        key: "net_export",
        label: "Чистый экспорт",
        unit: "млн руб.",
        placeholder: "например: 50",
        desc: "Экспорт минус импорт"
      }
    ],
    example: {
      consumption: 700,
      investment: 200,
      net_export: 50
    }
  },

  {
    id: "labor_productivity",
    title: "Коэффициент производительности труда",
    formula: "Ктруд = ВРП / Численность занятого населения × 100",
    resultUnit: "",
    fields: [
      {
        key: "vrp",
        label: "ВРП",
        unit: "млн руб.",
        placeholder: "например: 3500000",
        desc: "Валовой региональный продукт"
      },
      {
        key: "employed",
        label: "Численность занятого населения",
        unit: "тыс. чел.",
        placeholder: "например: 2200",
        desc: "Количество занятого населения"
      }
    ],
    example: {
      vrp: 3500000,
      employed: 2200
    }
  },

  {
    id: "industrial_index",
    title: "Индекс промышленного производства",
    formula: "ИПП = Текущий объём / Базовый объём × 100",
    resultUnit: "%",
    fields: [
      {
        key: "current",
        label: "Текущий объём производства",
        unit: "млн руб.",
        placeholder: "например: 1200",
        desc: "Объём промышленного производства в текущем периоде"
      },
      {
        key: "base",
        label: "Базовый объём производства",
        unit: "млн руб.",
        placeholder: "например: 1000",
        desc: "Объём промышленного производства в базовом периоде"
      }
    ],
    example: {
      current: 1200,
      base: 1000
    }
  },

  {
    id: "unemployment",
    title: "Уровень безработицы",
    formula: "Уровень безработицы = Безработные / Рабочая сила × 100",
    resultUnit: "%",
    fields: [
      {
        key: "unemployed",
        label: "Численность безработных",
        unit: "тыс. чел.",
        placeholder: "например: 121.0",
        desc: "Количество безработных"
      },
      {
        key: "labor",
        label: "Рабочая сила",
        unit: "тыс. чел.",
        placeholder: "например: 2155.7",
        desc: "Занятые + безработные"
      }
    ],
    example: {
      unemployed: 121.0,
      labor: 2155.7
    }
  },

  {
    id: "inflation",
    title: "Уровень инфляции",
    formula: "Инфляция = (Текущий индекс цен − Базовый индекс цен) / Базовый индекс цен × 100",
    resultUnit: "%",
    fields: [
      {
        key: "current",
        label: "Текущий индекс цен",
        unit: "",
        placeholder: "например: 112",
        desc: "Индекс цен в текущем периоде"
      },
      {
        key: "base",
        label: "Базовый индекс цен",
        unit: "",
        placeholder: "например: 100",
        desc: "Индекс цен в базовом периоде"
      }
    ],
    example: {
      current: 112,
      base: 100
    }
  },

  {
    id: "salary",
    title: "Средняя заработная плата",
    formula: "Средняя зарплата = Фонд оплаты труда / Численность работников",
    resultUnit: "руб.",
    fields: [
      {
        key: "total",
        label: "Фонд оплаты труда",
        unit: "руб.",
        placeholder: "например: 90000000",
        desc: "Общая сумма выплат работникам"
      },
      {
        key: "workers",
        label: "Численность работников",
        unit: "чел.",
        placeholder: "например: 3000",
        desc: "Количество работников"
      }
    ],
    example: {
      total: 90000000,
      workers: 3000
    }
  },

  {
    id: "investment",
    title: "Темп роста инвестиций",
    formula: "Темп роста инвестиций = (Текущий объём − Базовый объём) / Базовый объём × 100",
    resultUnit: "%",
    fields: [
      {
        key: "current",
        label: "Текущий объём инвестиций",
        unit: "млн руб.",
        placeholder: "например: 1500",
        desc: "Инвестиции в текущем периоде"
      },
      {
        key: "base",
        label: "Базовый объём инвестиций",
        unit: "млн руб.",
        placeholder: "например: 1200",
        desc: "Инвестиции в базовом периоде"
      }
    ],
    example: {
      current: 1500,
      base: 1200
    }
  },

  {
    id: "budget",
    title: "Сальдо бюджета",
    formula: "Сальдо бюджета = Доходы бюджета − Расходы бюджета",
    resultUnit: "млн руб.",
    fields: [
      {
        key: "income",
        label: "Доходы бюджета",
        unit: "млн руб.",
        placeholder: "например: 2500",
        desc: "Доходная часть бюджета"
      },
      {
        key: "expense",
        label: "Расходы бюджета",
        unit: "млн руб.",
        placeholder: "например: 2100",
        desc: "Расходная часть бюджета"
      }
    ],
    example: {
      income: 2500,
      expense: 2100
    }
  }
];


function getCurrentIndicator() {
  const selectedId = $("indicator").value;
  return INDICATORS.find(item => item.id === selectedId);
}


function initIndicators() {
  const select = $("indicator");

  select.innerHTML = INDICATORS
    .map(item => `<option value="${item.id}">${item.title}</option>`)
    .join("");

  select.addEventListener("change", () => {
    renderFields();
    clearResult();
  });

  renderFields();
}


function renderFields() {
  const cfg = getCurrentIndicator();

  if (!cfg) {
    return;
  }

  $("formulaHint").innerHTML = `
    <strong>Формула:</strong> ${cfg.formula}
  `;

  $("dynamicFields").innerHTML = cfg.fields.map(field => {
    return `
      <div class="field-row">
        <label for="${field.key}">
          ${field.label}
          ${field.unit ? `<span class="muted">(${field.unit})</span>` : ""}
        </label>

        <input
          id="${field.key}"
          data-key="${field.key}"
          type="text"
          inputmode="decimal"
          placeholder="${field.placeholder}"
        >

        <div class="hint small">
          ${field.desc}
        </div>
      </div>
    `;
  }).join("");

  renderRightHint(cfg);
}


function renderRightHint(cfg) {
  if (!$("rightHint")) {
    return;
  }

  if (cfg.id === "unemployment") {
    $("rightHint").innerHTML = `
      <strong>Пример расчёта безработицы:</strong><br>
      Безработные: <code>121.0</code> тыс. чел.<br>
      Рабочая сила: <code>2155.7</code> тыс. чел.<br><br>
      <code>121.0 / 2155.7 × 100 ≈ 5.61%</code>
    `;
  } else if (cfg.id === "labor_productivity") {
    $("rightHint").innerHTML = `
      <strong>Новый показатель:</strong><br>
      <code>Ктруд = ВРП / Численность занятого населения × 100</code><br><br>
      Пример:<br>
      ВРП: <code>3500000</code> млн руб.<br>
      Занятое население: <code>2200</code> тыс. чел.<br><br>
      <code>3500000 / 2200 × 100 = 159090.91</code>
    `;
  } else {
    $("rightHint").innerHTML = `
      • Значения вводятся числами.<br>
      • Можно использовать точку или запятую для дробных чисел.<br>
      • После выбора показателя форма подстроится автоматически.<br>
      • Для расчёта нажмите кнопку <code>Рассчитать</code>.
    `;
  }
}


function parseNumber(value) {
  if (typeof value !== "string") {
    return NaN;
  }

  const normalized = value
    .trim()
    .replace(/\s/g, "")
    .replace(",", ".");

  return Number(normalized);
}


function collectData() {
  const cfg = getCurrentIndicator();
  const data = {};

  for (const field of cfg.fields) {
    const input = $(field.key);
    const value = parseNumber(input.value);

    if (Number.isNaN(value)) {
      throw new Error(`Поле "${field.label}" должно быть числом`);
    }

    data[field.key] = value;
  }

  return data;
}


function formatNumber(value) {
  if (typeof value !== "number") {
    return value;
  }

  return value.toLocaleString("ru-RU", {
    maximumFractionDigits: 2
  });
}


async function runCalculation() {
  const cfg = getCurrentIndicator();
  const resultBox = $("result");

  try {
    const data = collectData();

    resultBox.className = "out";
    resultBox.textContent = "Выполняется расчёт...";

    const response = await apiPost("/calculate", {
      indicator: cfg.id,
      data: data
    });

    if (response.error) {
      resultBox.className = "out err";
      resultBox.textContent = response.error;
      return;
    }

    const unit = cfg.resultUnit ? ` ${cfg.resultUnit}` : "";

    resultBox.className = "out ok";
    resultBox.innerHTML = `
      <strong>${cfg.title}</strong><br>
      Результат: <code>${formatNumber(response.result)}${unit}</code>
    `;

  } catch (e) {
    resultBox.className = "out err";
    resultBox.textContent = e.message || "Ошибка расчёта";
  }
}


function fillExample() {
  const cfg = getCurrentIndicator();

  for (const field of cfg.fields) {
    const input = $(field.key);

    if (input && cfg.example[field.key] !== undefined) {
      input.value = cfg.example[field.key];
    }
  }

  clearResult();
}


function clearFields() {
  const cfg = getCurrentIndicator();

  for (const field of cfg.fields) {
    const input = $(field.key);

    if (input) {
      input.value = "";
    }
  }

  clearResult();
}


function clearResult() {
  const resultBox = $("result");

  if (resultBox) {
    resultBox.className = "out";
    resultBox.textContent = "Результат расчёта появится здесь…";
  }
}


document.addEventListener("DOMContentLoaded", () => {
  initIndicators();
});