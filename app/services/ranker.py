def rank_products(products: list[dict], stats: dict) -> list[dict]:
    average_price = stats.get("average_price")

    if not average_price:
        return products

    ranked_products = []

    for product in products:
        score = 0
        price = product["price"]

        # Цена ниже средней — хорошо
        if price < average_price:
            score += 30

        # Цена сильно ниже средней — подозрительно
        if price < average_price * 0.6:
            score -= 20

        # Цена около медианы или ниже — хорошо
        median_price = stats.get("median_price")
        if median_price and price <= median_price:
            score += 20

        # Есть поставщик — плюс
        if product.get("supplier"):
            score += 10

        # Есть рейтинг — плюс
        rating = product.get("rating")
        if rating:
            score += rating * 5

        # Есть отзывы — плюс
        reviews_count = product.get("reviews_count")
        if reviews_count:
            if reviews_count >= 100:
                score += 15
            elif reviews_count >= 20:
                score += 8
            elif reviews_count >= 5:
                score += 4

        # Товар в наличии — плюс
        if product.get("available", True):
            score += 10

        product["score"] = round(score, 2)
        product["reason"] = generate_reason(product, average_price)

        ranked_products.append(product)

    return sorted(ranked_products, key=lambda x: x["score"], reverse=True)


def generate_reason(product: dict, average_price: float) -> str:
    reasons = []

    if product["price"] < average_price:
        reasons.append("цена ниже средней")

    if product.get("supplier"):
        reasons.append("указан поставщик")

    if product.get("rating"):
        reasons.append("есть рейтинг товара")

    if product.get("reviews_count"):
        reasons.append("есть отзывы")

    if product.get("available", True):
        reasons.append("товар доступен")

    if not reasons:
        return "обычное предложение"

    return ", ".join(reasons)