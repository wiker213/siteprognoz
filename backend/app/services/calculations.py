from typing import Dict, Any


def calculate_indicator(indicator: str, data: Dict[str, float]) -> Dict[str, Any]:
    """
    Возвращает:
      - {"indicator": "...", "result": <число>}
      - или {"error": "..."}
    """

    try:
        if indicator == "vrp_production":
            output = data["output"]
            intermediate = data["intermediate"]
            result = output - intermediate

        elif indicator == "vrp_income":
            wages = data["wages"]
            profit = data["profit"]
            taxes = data["taxes"]
            result = wages + profit + taxes

        elif indicator == "vrp_final":
            consumption = data["consumption"]
            investment = data["investment"]
            net_export = data["net_export"]
            result = consumption + investment + net_export

        elif indicator == "labor_productivity":
            vrp = data["vrp"]
            employed = data["employed"]
            result = (vrp / employed) * 100

        elif indicator == "industrial_index":
            current = data["current"]
            base = data["base"]
            result = (current / base) * 100

        elif indicator == "unemployment":
            unemployed = data["unemployed"]
            labor = data["labor"]
            result = (unemployed / labor) * 100

        elif indicator == "inflation":
            current = data["current"]
            base = data["base"]
            result = ((current - base) / base) * 100

        elif indicator == "salary":
            total = data["total"]
            workers = data["workers"]
            result = total / workers

        elif indicator == "investment":
            current = data["current"]
            base = data["base"]
            result = ((current - base) / base) * 100

        elif indicator == "budget":
            income = data["income"]
            expense = data["expense"]
            result = income - expense

        else:
            return {"error": "Неизвестный показатель"}

        return {
            "indicator": indicator,
            "result": round(float(result), 2)
        }

    except KeyError as e:
        return {
            "error": f"Не хватает поля: {str(e)}"
        }

    except ZeroDivisionError:
        return {
            "error": "Деление на ноль. Проверь, что знаменатель не равен 0"
        }

    except Exception as e:
        return {
            "error": str(e)
        }