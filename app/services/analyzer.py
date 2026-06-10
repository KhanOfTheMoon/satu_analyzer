import statistics


def analyze_prices(products: list[dict]) -> dict:
    prices = [
        product["price"]
        for product in products
        if product.get("price") is not None
    ]

    if not prices:
        return {
            "min_price": None,
            "max_price": None,
            "average_price": None,
            "median_price": None,
            "normal_range": None,
        }

    sorted_prices = sorted(prices)

    min_price = min(sorted_prices)
    max_price = max(sorted_prices)
    average_price = sum(sorted_prices) / len(sorted_prices)
    median_price = statistics.median(sorted_prices)

    q1_index = len(sorted_prices) // 4
    q3_index = (len(sorted_prices) * 3) // 4

    q1 = sorted_prices[q1_index]
    q3 = sorted_prices[q3_index]

    return {
        "min_price": round(min_price, 2),
        "max_price": round(max_price, 2),
        "average_price": round(average_price, 2),
        "median_price": round(median_price, 2),
        "normal_range": {
            "from": round(q1, 2),
            "to": round(q3, 2),
        },
    }


def analyze_suppliers(products: list[dict]) -> list[dict]:
    suppliers = {}

    for product in products:
        supplier = product.get("supplier") or "Unknown"

        if supplier not in suppliers:
            suppliers[supplier] = {
                "name": supplier,
                "products_count": 0,
                "prices": [],
            }

        suppliers[supplier]["products_count"] += 1
        suppliers[supplier]["prices"].append(product["price"])

    result = []

    for supplier_data in suppliers.values():
        prices = supplier_data["prices"]

        result.append({
            "name": supplier_data["name"],
            "products_count": supplier_data["products_count"],
            "average_price": round(sum(prices) / len(prices), 2),
            "min_price": round(min(prices), 2),
            "max_price": round(max(prices), 2),
        })

    return sorted(result, key=lambda x: x["average_price"])