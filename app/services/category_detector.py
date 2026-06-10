from app.services.cleaner import normalize_text


CATEGORY_KEYWORDS = {
    # =====================
    # Smartphones
    # =====================

    "smartphones": [
        "iphone",
        "айфон",
        "samsung galaxy",
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
        "смартфон",
        "смартфоны",
        "телефон",
        "телефоны",
    ],

    # =====================
    # Stationery
    # =====================

    "stationery_pens": [
        "ручка",
        "ручки",
        "шариковая ручка",
        "гелевая ручка",
        "перьевая ручка",
        "parker",
        "pen",
    ],

    "stationery_pencils": [
        "карандаш",
        "карандаши",
        "pencil",
    ],

    "stationery_markers": [
        "маркер",
        "маркеры",
        "фломастер",
        "фломастеры",
        "текстовыделитель",
        "выделитель",
        "marker",
    ],

    "stationery_notebooks": [
        "блокнот",
        "блокноты",
        "ежедневник",
        "ежедневники",
        "органайзер",
        "органайзеры",
        "notebook",
    ],

    "stationery_school_notebooks": [
        "тетрадь",
        "тетради",
        "дневник",
        "дневники",
    ],

    "stationery_folders": [
        "папка",
        "папки",
        "файл",
        "файлы",
        "скоросшиватель",
        "регистратор",
    ],

    "stationery_paper": [
        "бумага",
        "бумага a4",
        "a4",
        "офисная бумага",
        "бумага для принтера",
    ],

    "stationery_rulers": [
        "линейка",
        "линейки",
        "угольник",
        "угольники",
    ],

    "stationery_glue": [
        "клей",
        "канцелярский клей",
        "клей карандаш",
    ],

    "stationery_clips": [
        "скрепки",
        "кнопки",
        "канцелярские скрепки",
    ],

    "stationery_erasers": [
        "ластик",
        "ластики",
        "стирательная резинка",
    ],

    "stationery_stands": [
        "подставка для канцелярии",
        "подставка для ручек",
        "органайзер для канцелярии",
    ],

    "stationery_scissors": [
        "ножницы",
        "канцелярский нож",
        "канцелярские ножницы",
    ],

    "stationery_calculators": [
        "калькулятор",
        "калькуляторы",
    ],

    "stationery": [
        "канцтовары",
        "канцелярия",
        "канцелярские товары",
        "школьные принадлежности",
    ],

    # =====================
    # Electronics / Computer goods
    # =====================

    "electronics_laptops": [
        "ноутбук",
        "ноутбуки",
        "laptop",
        "macbook",
        "макбук",
        "ultrabook",
        "ультрабук",
        "игровой ноутбук",
        "asus laptop",
        "lenovo laptop",
        "hp laptop",
        "acer laptop",
    ],

    "electronics_laptop_bags": [
        "сумка для ноутбука",
        "сумка для ноута",
        "рюкзак для ноутбука",
        "рюкзак для ноута",
        "чехол для ноутбука",
        "laptop bag",
    ],

    "electronics_laptop_keyboards": [
        "клавиатура для ноутбука",
        "клавиатурный блок ноутбука",
    ],

    "electronics_laptop_batteries": [
        "аккумулятор для ноутбука",
        "батарея для ноутбука",
    ],

    "electronics_laptop_chargers": [
        "зарядка для ноутбука",
        "зарядное устройство для ноутбука",
        "адаптер ноутбука",
        "блок питания для ноутбука",
    ],

    "electronics_laptop_stands": [
        "подставка для ноутбука",
        "подставка ноутбук",
    ],

    "electronics_desktop_computers": [
        "настольный компьютер",
        "компьютер",
        "системный блок",
        "пк",
        "pc",
    ],

    "electronics_monitors": [
        "монитор",
        "мониторы",
        "monitor",
    ],

    "electronics_tablets": [
        "планшет",
        "планшеты",
        "tablet",
        "ipad",
    ],

    "electronics_keyboards": [
        "клавиатура",
        "клавиатуры",
        "keyboard",
        "mechanical keyboard",
        "механическая клавиатура",
    ],

    "electronics_mice": [
        "мышь",
        "мышка",
        "компьютерная мышь",
        "mouse",
    ],

    "electronics_mousepads": [
        "коврик для мыши",
        "коврик мыши",
        "mousepad",
    ],

    "electronics_headphones": [
        "наушники",
        "гарнитура",
        "гарнитуры",
        "headphones",
        "earphones",
        "headset",
    ],

    "electronics_smartwatches": [
        "смарт часы",
        "смарт-часы",
        "умные часы",
        "smart watch",
        "smartwatch",
        "apple watch",
    ],

    "electronics_printers": [
        "принтер",
        "принтеры",
        "сканер",
        "сканеры",
        "мфу",
        "mfu",
        "printer",
    ],

    "electronics_printer_cartridges": [
        "картридж",
        "картриджи",
        "картридж для принтера",
        "фотобарабан",
        "drum cartridge",
    ],

    "electronics_toner_ink": [
        "тонер",
        "чернила",
        "чернила для принтера",
        "тонер для принтера",
    ],

    "electronics_3d_printers": [
        "3d принтер",
        "3д принтер",
        "3d printer",
        "3d scanner",
        "3d сканер",
    ],

    "electronics_routers": [
        "роутер",
        "роутеры",
        "router",
        "wi-fi роутер",
        "wifi роутер",
    ],

    "electronics_modems": [
        "модем",
        "модемы",
        "3g модем",
        "4g модем",
    ],

    "electronics_wifi_adapters": [
        "wi-fi адаптер",
        "wifi адаптер",
        "вай фай адаптер",
        "сетевой адаптер",
    ],

    "electronics_switches": [
        "коммутатор",
        "switch",
        "сетевой коммутатор",
    ],

    "electronics_usb_drives": [
        "флешка",
        "флешки",
        "usb накопитель",
        "usb flash",
        "flash drive",
    ],

    "electronics_storage": [
        "ssd",
        "hdd",
        "жесткий диск",
        "жёсткий диск",
        "накопитель",
        "диск ssd",
    ],

    "electronics_memory_cards": [
        "карта памяти",
        "memory card",
        "microsd",
        "micro sd",
    ],

    "electronics_ram": [
        "оперативная память",
        "озу",
        "ram",
        "ddr4",
        "ddr5",
    ],

    "electronics_video_cards": [
        "видеокарта",
        "видеокарты",
        "gpu",
        "rtx",
        "gtx",
        "geforce",
        "radeon",
    ],

    "electronics_processors": [
        "процессор",
        "процессоры",
        "cpu",
        "intel core",
        "ryzen",
    ],

    "electronics_motherboards": [
        "материнская плата",
        "материнка",
        "motherboard",
    ],

    "electronics_power_supplies": [
        "блок питания для компьютера",
        "блок питания пк",
        "power supply",
    ],

    "electronics_computer_cases": [
        "корпус для компьютера",
        "корпус пк",
        "computer case",
    ],

    "electronics_cooling": [
        "кулер",
        "кулеры",
        "система охлаждения",
        "охлаждение",
        "cooler",
    ],

    "electronics_sound_cards": [
        "звуковая карта",
        "sound card",
    ],

    "electronics_usb_hubs": [
        "usb hub",
        "usb хаб",
        "юсб хаб",
    ],

    "electronics_adapters": [
        "адаптер",
        "переходник",
        "плата расширения",
    ],

    "electronics_gamepads": [
        "геймпад",
        "джойстик",
        "игровой контроллер",
        "gamepad",
    ],

    "electronics_graphic_tablets": [
        "графический планшет",
        "графические планшеты",
        "drawing tablet",
        "graphic tablet",
    ],

    "electronics": [
        "электроника",
        "гаджет",
        "гаджеты",
        "цифровая техника",
    ],

    # =====================
    # Home appliances
    # =====================

    "home_kettles": [
        "чайник",
        "электрочайник",
        "электрический чайник",
    ],

    "home_vacuum_cleaners": [
        "пылесос",
        "пылесосы",
    ],

    "home_robot_vacuum_cleaners": [
        "робот пылесос",
        "робот-пылесос",
        "robot vacuum",
    ],

    "home_vertical_vacuum_cleaners": [
        "вертикальный пылесос",
        "аккумуляторный пылесос",
        "беспроводной пылесос",
    ],

    "home_air_conditioners": [
        "кондиционер",
        "кондиционеры",
        "сплит система",
        "сплит-система",
    ],

    "home_stoves": [
        "кухонная плита",
        "электроплита",
        "газовая плита",
        "плита",
    ],

    "home_coffee_machines": [
        "кофемашина",
        "кофеварка",
        "кофе машина",
    ],

    "home_blenders": [
        "блендер",
        "блендеры",
    ],

    "home_hoods": [
        "вытяжка",
        "кухонная вытяжка",
    ],

    "home_refrigerators": [
        "холодильник",
        "холодильники",
    ],

    "home_freezers": [
        "морозильник",
        "морозильная камера",
        "морозильные камеры",
    ],

    "home_washing_machines": [
        "стиральная машина",
        "стиральные машины",
        "стиралка",
        "washing machine",
    ],

    "home_irons": [
        "утюг",
        "утюги",
        "гладильная система",
    ],

    "home_appliances": [
        "бытовая техника",
        "техника для дома",
        "кухонная техника",
    ],

    # =====================
    # Furniture
    # =====================

    "furniture_computer_desks": [
        "компьютерный стол",
        "стол для компьютера",
        "игровой стол",
        "стол для ноутбука",
    ],

    "furniture_office_chairs": [
        "офисное кресло",
        "компьютерное кресло",
        "игровое кресло",
        "кресло для компьютера",
    ],

    "furniture_sofas": [
        "диван",
        "диваны",
    ],

    "furniture_beds": [
        "кровать",
        "кровати",
    ],

    "furniture_tv_stands": [
        "тумба под телевизор",
        "тумба тв",
        "тв тумба",
    ],

    "furniture_bedside_tables": [
        "прикроватная тумбочка",
        "прикроватная тумба",
    ],

    "furniture_dining_tables": [
        "обеденный стол",
        "обеденные столы",
    ],

    "furniture": [
        "мебель",
        "кресло",
        "стол",
        "стул",
        "шкаф",
        "полка",
        "тумба",
        "комод",
    ],

    # =====================
    # Clothes / Shoes
    # =====================

    "clothes_sneakers": [
        "кроссовки",
        "кеды",
        "sneakers",
    ],

    "clothes_running_shoes": [
        "беговые кроссовки",
        "running shoes",
    ],

    "clothes_womens_boots": [
        "женские ботинки",
        "женские ботильоны",
        "ботильоны",
    ],

    "clothes_mens_boots": [
        "мужские ботинки",
    ],

    "clothes_womens_shoes": [
        "женские туфли",
        "туфли женские",
    ],

    "clothes_mens_shoes": [
        "мужские туфли",
        "туфли мужские",
    ],

    "clothes": [
        "футболка",
        "рубашка",
        "джинсы",
        "брюки",
        "куртка",
        "пальто",
        "обувь",
        "платье",
        "юбка",
        "худи",
    ],
}


def detect_category(query: str) -> str:
    query_lower = normalize_text(query)

    best_category = "general"
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            keyword_normalized = normalize_text(keyword)

            if keyword_normalized in query_lower:
                score += len(keyword_normalized.split()) * 3
                score += len(keyword_normalized)

        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def resolve_category(query: str, selected_category: str = "auto") -> str:
    if selected_category and selected_category != "auto":
        return selected_category

    return detect_category(query)