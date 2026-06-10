def filter_price_outliers(products: list[dict]) -> list[dict]:
    if len(products) < 4:
        return products

    prices = sorted([
        product["price"]
        for product in products
        if product.get("price") is not None
    ])

    if len(prices) < 4:
        return products

    q1 = prices[len(prices) // 4]
    q3 = prices[(len(prices) * 3) // 4]

    iqr = q3 - q1

    if iqr == 0:
        return products

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    filtered = []

    for product in products:
        price = product["price"]

        if lower_bound <= price <= upper_bound:
            filtered.append(product)

    return filtered