import re


def clean_price(price_text: str) -> float | None:
    if not price_text:
        return None

    cleaned = price_text.lower()
    cleaned = cleaned.replace("₸", "")
    cleaned = cleaned.replace("тг", "")
    cleaned = cleaned.replace("kzt", "")
    cleaned = cleaned.replace(",", "")
    cleaned = cleaned.replace(" ", "")
    cleaned = cleaned.replace("от", "")

    numbers = re.findall(r"\d+", cleaned)

    if not numbers:
        return None

    return float("".join(numbers))


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = text.replace("ё", "е")
    text = text.replace("айфон", "iphone")
    text = text.replace("айфона", "iphone")
    text = text.replace("айфону", "iphone")
    text = text.replace("эппл", "apple")
    text = text.replace("самсунг", "samsung")

    return text.strip()


def get_category_rules(category: str) -> dict:
    rules = {
        "smartphones": {
            "required_any": [
                "смартфон",
                "smartphone",
                "iphone",
                "samsung",
                "galaxy",
                "xiaomi",
                "redmi",
                "poco",
                "honor",
                "huawei",
                "oppo",
                "vivo",
                "realme",
                "tecno",
                "infinix",
                "oneplus",
                "телефон",
            ],
            "banned": [
                "чехол",
                "case",
                "cover",
                "стекло",
                "защитное стекло",
                "glass",
                "пленка",
                "плёнка",
                "кабель",
                "зарядка",
                "зарядное",
                "адаптер",
                "переходник",
                "держатель",
                "штатив",
                "монопод",
                "селфи",
                "наушники",
                "гарнитура",
                "power bank",
                "powerbank",
                "повербанк",
                "экран",
                "дисплей",
                "батарея",
                "аккумулятор",
                "корпус",
                "крышка",
                "шлейф",
                "ремонт",
                "брендирование",
                "нанесение",
                "печать",
                "флешка",
                "usb",
                "картридж",
                "лазерный",
                "принтер",
            ],
        },

        "stationery": {
            "required_any": [
                "ручка",
                "карандаш",
                "тетрадь",
                "блокнот",
                "бумага",
                "маркер",
                "ластик",
                "папка",
                "файл",
                "скрепки",
                "степлер",
                "канцтовары",
                "канцелярия",
            ],
            "banned": [
                "держатель",
                "органайзер для телефона",
                "ремонт",
                "услуга",
                "печать на",
                "брендирование",
            ],
        },

        "electronics": {
            "required_any": [
                "ноутбук",
                "принтер",
                "монитор",
                "клавиатура",
                "мышь",
                "роутер",
                "планшет",
                "наушники",
                "колонка",
                "камера",
            ],
            "banned": [
                "ремонт",
                "запчасть",
                "кабель для",
                "чехол",
                "сумка",
                "услуга",
            ],
        },

        "furniture": {
            "required_any": [
                "кресло",
                "стол",
                "стул",
                "шкаф",
                "диван",
                "полка",
                "тумба",
                "мебель",
            ],
            "banned": [
                "ремонт",
                "аренда",
                "чехол",
                "ткань",
                "запчасть",
            ],
        },

        "general": {
            "required_any": [],
            "banned": [
                "услуга",
                "ремонт",
                "аренда",
                "прокат",
                "нанесение",
                "брендирование",
                "печать на",
                "под заказ",
            ],
        },
    }

    return rules.get(category, rules["general"])


def is_relevant_product(title: str, query: str, category: str = "general",strict_title_match: bool = False,) -> bool:
    title_lower = normalize_text(title)
    query_lower = normalize_text(query)

    if not title_lower:
        return False

    rules = get_category_rules(category)

    # 1 Убираем запрещённые слова для категории
    for banned_word in rules["banned"]:
        if banned_word in title_lower:
            return False

    # 2 Если у категории есть обязательные признаки, проверяем их
    required_any = rules["required_any"]

    if required_any:
        has_required_word = any(word in title_lower for word in required_any)

        if not has_required_word:
            return False
        
    if strict_title_match:
        return title_matches_query_strict(title, query)
    
    # 3 Проверяем совпадение с запросом
    query_words = [
        word for word in query_lower.split()
        if len(word) >= 2
    ]

    if not query_words:
        return False

    matched_words = 0

    for word in query_words:
        if word in title_lower:
            matched_words += 1

    # Для короткого запроса достаточно одного совпадения
    if len(query_words) == 1:
        return matched_words >= 1

    # Для длинного запроса достаточно примерно половины совпадений
    return matched_words >= max(1, len(query_words) // 2)


def remove_duplicates(products: list[dict]) -> list[dict]:
    seen = set()
    unique_products = []

    for product in products:
        url_key = product.get("url")
        title_key = normalize_text(product.get("title", ""))
        price_key = product.get("price")

        key = (url_key, title_key, price_key)

        if key in seen:
            continue

        seen.add(key)
        unique_products.append(product)

    return unique_products

def title_matches_query_strict(title: str, query: str) -> bool:
    """
    Строгий поиск по названию.
    Все важные слова из запроса должны быть в названии товара.
    """
    title_lower = normalize_text(title)
    query_lower = normalize_text(query)

    query_words = [
        word for word in query_lower.split()
        if len(word) >= 2
    ]

    if not query_words:
        return False

    for word in query_words:
        if word not in title_lower:
            return False

    return True