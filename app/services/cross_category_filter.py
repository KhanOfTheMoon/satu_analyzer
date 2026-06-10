from app.services.cleaner import normalize_text


CATEGORY_REQUIRED_WORDS = {
    "smartphones": [
        "смартфон",
        "iphone",
        "galaxy",
        "redmi",
        "xiaomi",
        "poco",
        "honor",
        "huawei",
        "oppo",
        "vivo",
        "realme",
        "tecno",
        "infinix",
        "oneplus",
    ],

    "stationery": [
        "ручка",
        "карандаш",
        "тетрадь",
        "блокнот",
        "бумага",
        "маркер",
        "ластик",
        "папка",
        "скрепки",
        "степлер",
        "ежедневник",
        "корректор",
    ],

    "electronics": [
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

    "furniture": [
        "кресло",
        "стол",
        "стул",
        "шкаф",
        "диван",
        "полка",
        "тумба",
    ],

    "clothes": [
        "футболка",
        "рубашка",
        "джинсы",
        "брюки",
        "куртка",
        "пальто",
        "кроссовки",
        "обувь",
    ],
}


CATEGORY_CONFLICT_WORDS = {
    "smartphones": [
        "картридж",
        "тонер",
        "принтер",
        "лазерный",
        "чехол",
        "стекло",
        "кабель",
        "зарядка",
        "аккумулятор",
        "батарея",
        "экран",
        "дисплей",
        "переходник",
        "держатель",
        "power bank",
        "повербанк",
        "флешка",
        "usb",
    ],

    "stationery": [
        "смартфон",
        "iphone",
        "galaxy",
        "телефон",
        "ноутбук",
        "принтер",
        "картридж",
        "монитор",
        "кресло",
        "стол",
        "диван",
    ],

    "electronics": [
        "чехол",
        "стекло",
        "ремонт",
        "услуга",
        "аренда",
        "брендирование",
        "нанесение",
    ],

    "furniture": [
        "чехол",
        "ремонт",
        "услуга",
        "аренда",
        "ткань",
        "запчасть",
    ],

    "clothes": [
        "ремонт",
        "услуга",
        "ткань",
        "выкройка",
        "манекен",
    ],
}


def is_wrong_category_product(title: str, category: str) -> bool:
    """
    Возвращает True, если товар похож на товар из другой категории.
    """
    if category == "general":
        return False

    title_lower = normalize_text(title)

    conflict_words = CATEGORY_CONFLICT_WORDS.get(category, [])

    for word in conflict_words:
        if word in title_lower:
            return True

    required_words = CATEGORY_REQUIRED_WORDS.get(category, [])

    if required_words:
        has_required_word = any(word in title_lower for word in required_words)

        if not has_required_word:
            return True

    return False