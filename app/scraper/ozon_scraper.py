import re
from urllib.parse import quote_plus

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from app.services.category_detector import resolve_category
from app.services.cleaner import is_relevant_product
from app.services.cross_category_filter import is_wrong_category_product


BASE_URL = "https://www.ozon.kz"


def build_ozon_search_url(query: str, page: int) -> str:
    encoded_query = quote_plus(query)

    if page <= 1:
        return f"{BASE_URL}/search/?text={encoded_query}"

    return f"{BASE_URL}/search/?text={encoded_query}&page={page}"


def normalize_ozon_url(url: str | None) -> str:
    if not url:
        return BASE_URL

    url = str(url).strip()

    if url.startswith("http://") or url.startswith("https://"):
        return url

    if url.startswith("//"):
        return "https:" + url

    if url.startswith("/"):
        return BASE_URL + url

    return BASE_URL + "/" + url


def normalize_image_url(url: str | None) -> str | None:
    if not url:
        return None

    url = str(url).strip()

    if not url:
        return None

    # Если это srcset, берём последний вариант, обычно он крупнее.
    # Пример:
    # https://ir-21.ozone.ru/.../wc50/xxx.jpg 1x,
    # https://ir-21.ozone.ru/.../wc100/xxx.jpg 2x
    if "," in url:
        parts = [part.strip() for part in url.split(",") if part.strip()]

        if parts:
            url = parts[-1].split(" ")[0].strip()

    if " " in url:
        url = url.split(" ")[0].strip()

    if url.startswith("data:"):
        return None

    if url.startswith("http://") or url.startswith("https://"):
        return url

    if url.startswith("//"):
        return "https:" + url

    if url.startswith("/"):
        return BASE_URL + url

    return url


def is_good_ozon_image_url(url: str | None) -> bool:
    if not url:
        return False

    lower_url = str(url).lower()

    return (
        "ozone.ru" in lower_url
        or "ozon-st.cdn" in lower_url
        or "multimedia" in lower_url
        or ".jpg" in lower_url
        or ".jpeg" in lower_url
        or ".png" in lower_url
        or ".webp" in lower_url
    )


def clean_price_from_text(text: str | None) -> float | None:
    if not text:
        return None

    lines = [
        line.strip()
        for line in str(text).split("\n")
        if line.strip()
    ]

    normal_prices = []
    old_prices = []
    fallback_prices = []

    price_patterns = [
        r"(\d[\d\s]*)\s*₸",
        r"(\d[\d\s]*)\s*тг",
        r"(\d[\d\s]*)\s*тенге",
    ]

    for line in lines:
        lower_line = line.lower()

        # Игнорируем рассрочку: "39 238 ₸ × 12 мес"
        is_installment = (
            "мес" in lower_line
            or "×" in lower_line
            or " x " in lower_line
            or "x " in lower_line
            or "рассроч" in lower_line
        )

        for pattern in price_patterns:
            matches = re.findall(pattern, line, flags=re.IGNORECASE)

            for match in matches:
                digits = re.sub(r"[^\d]", "", match)

                if not digits:
                    continue

                try:
                    price = float(digits)
                except ValueError:
                    continue

                if price <= 0:
                    continue

                # Слишком маленькие цены для смартфонов чаще всего рассрочка
                if price < 10000:
                    continue

                if is_installment:
                    continue

                # Старую цену часто показывают рядом со скидкой
                if "%" in line or "−" in line or "-" in line:
                    old_prices.append(price)
                else:
                    normal_prices.append(price)

                fallback_prices.append(price)

    # Самый правильный вариант — первая обычная цена без рассрочки
    if normal_prices:
        return normal_prices[0]

    # Если обычной нет, берём минимальную из старых/скидочных
    if old_prices:
        return min(old_prices)

    if fallback_prices:
        return min(fallback_prices)

    return None


def clean_rating_from_text(text: str | None) -> float | None:
    if not text:
        return None

    text = str(text).replace(",", ".")

    patterns = [
        r"★\s*(\d+(\.\d+)?)",
        r"(\d+(\.\d+)?)\s*★",
        r"рейтинг\s*(\d+(\.\d+)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if not match:
            continue

        try:
            rating = float(match.group(1))

            if 0 <= rating <= 5:
                return rating

        except ValueError:
            continue

    return None


def clean_reviews_from_text(text: str | None) -> int | None:
    if not text:
        return None

    text = str(text).lower()

    patterns = [
        r"(\d[\d\s]*)\s*отзыв",
        r"(\d[\d\s]*)\s*оцен",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if not match:
            continue

        digits = re.sub(r"[^\d]", "", match.group(1))

        if not digits:
            continue

        try:
            return int(digits)
        except ValueError:
            continue

    return None


async def block_unnecessary_resources(route):
    request = route.request
    resource_type = request.resource_type
    url = request.url.lower()

    # ВАЖНО: image не блокируем, иначе фото товара не загрузятся.
    blocked_resource_types = {
        "font",
        "media",
        "websocket",
        "manifest",
    }

    blocked_domains = [
        "google-analytics",
        "googletagmanager",
        "doubleclick",
        "facebook",
        "yandex.ru/metrika",
        "mc.yandex",
        "vk.com",
        "analytics",
        "tracking",
        "advert",
    ]

    if resource_type in blocked_resource_types:
        await route.abort()
        return

    if any(domain in url for domain in blocked_domains):
        await route.abort()
        return

    await route.continue_()


async def fast_scroll(page, scroll_count: int = 3):
    for _ in range(scroll_count):
        await page.mouse.wheel(0, 1600)
        await page.wait_for_timeout(700)


async def extract_product_data_from_link(link) -> dict | None:
    """
    Берём данные товара прямо из ссылки /product/.

    По твоему скрину:
    - ссылка товара: <a href="/product/...">
    - фото внутри этой же ссылки: <img src="https://ir-21.ozone.ru/...jpg" srcset="...">
    - название внутри этой же ссылки: span.tsBody500Medium
    """

    try:
        data = await link.evaluate(
            """
            (link) => {
                function normalizeSrcset(value) {
                    if (!value) return null;

                    value = value.trim();

                    if (!value) return null;
                    if (value.startsWith("data:")) return null;

                    if (value.includes(",")) {
                        const parts = value
                            .split(",")
                            .map(part => part.trim())
                            .filter(Boolean);

                        if (parts.length > 0) {
                            value = parts[parts.length - 1].split(" ")[0];
                        }
                    }

                    if (value.includes(" ")) {
                        value = value.split(" ")[0];
                    }

                    return value;
                }

                function isGoodImageUrl(value) {
                    if (!value) return false;

                    const lower = value.toLowerCase();

                    return (
                        lower.includes("ozone.ru") ||
                        lower.includes("ozon-st.cdn") ||
                        lower.includes("multimedia") ||
                        lower.includes(".jpg") ||
                        lower.includes(".jpeg") ||
                        lower.includes(".png") ||
                        lower.includes(".webp")
                    );
                }

                function getImageFromRoot(root) {
                    if (!root) return null;

                    const images = Array.from(root.querySelectorAll("img"));

                    for (const img of images) {
                        const candidates = [
                            img.getAttribute("srcset"),
                            img.getAttribute("data-srcset"),
                            img.currentSrc,
                            img.src,
                            img.getAttribute("src"),
                            img.getAttribute("data-src"),
                            img.getAttribute("data-original")
                        ];

                        for (let value of candidates) {
                            value = normalizeSrcset(value);

                            if (isGoodImageUrl(value)) {
                                return value;
                            }
                        }
                    }

                    const allElements = Array.from(root.querySelectorAll("*"));

                    for (const child of allElements) {
                        const style = window.getComputedStyle(child);
                        const bg = style.getPropertyValue("background-image");

                        if (!bg || bg === "none") continue;

                        const match = bg.match(/url\\(["']?(.*?)["']?\\)/);

                        if (match && match[1]) {
                            const value = normalizeSrcset(match[1]);

                            if (isGoodImageUrl(value)) {
                                return value;
                            }
                        }
                    }

                    return null;
                }

                function findCard(link) {
                    let element = link;

                    for (let i = 0; i < 12; i++) {
                        if (!element.parentElement) break;

                        element = element.parentElement;

                        const text = element.innerText || "";
                        const images = element.querySelectorAll("img");
                        const productLinks = element.querySelectorAll("a[href*='/product/']");

                        if (
                            text.length > 40 &&
                            text.length < 3000 &&
                            images.length >= 1 &&
                            productLinks.length >= 1
                        ) {
                            return element;
                        }
                    }

                    return link.parentElement || link;
                }

                function getTitle(link, card) {
                    const titleSelectors = [
                        "span.tsBody500Medium",
                        "span.tsBody500Medium.tsBodyControl500Medium",
                        "span[class*='tsBody500Medium']",
                        "span[class*='tsBodyControl500Medium']"
                    ];

                    // 1. Сначала ищем название внутри самой ссылки
                    for (const selector of titleSelectors) {
                        const titleElement = link.querySelector(selector);

                        if (titleElement && titleElement.innerText && titleElement.innerText.trim()) {
                            return titleElement.innerText.trim();
                        }
                    }

                    // 2. Потом внутри карточки
                    for (const selector of titleSelectors) {
                        const titleElement = card.querySelector(selector);

                        if (titleElement && titleElement.innerText && titleElement.innerText.trim()) {
                            return titleElement.innerText.trim();
                        }
                    }

                    // 3. Fallback: берём нормальную строку из текста ссылки
                    const linkText = link.innerText || "";
                    const lines = linkText
                        .split("\\n")
                        .map(line => line.trim())
                        .filter(Boolean);

                    for (const line of lines) {
                        const lower = line.toLowerCase();

                        if (
                            line.length >= 5 &&
                            line.length <= 220 &&
                            !line.includes("₸") &&
                            !lower.includes("отзыв") &&
                            !lower.includes("доставка") &&
                            !lower.includes("рассрочка") &&
                            !lower.includes("скидка") &&
                            !lower.includes("цена") &&
                            !lower.includes("оригинал") &&
                            !lower.includes("официальный") &&
                            !lower.includes("магазин") &&
                            !lower.includes("стало дешевле")
                        ) {
                            return line;
                        }
                    }

                    return null;
                }

                const card = findCard(link);
                const href = link.getAttribute("href");
                const title = getTitle(link, card);

                // Главное исправление:
                // сначала ищем фото внутри самой ссылки <a>, потому что фото товара находится там.
                let imageUrl = getImageFromRoot(link);

                if (!imageUrl) {
                    imageUrl = getImageFromRoot(card);
                }

                const cardText = card.innerText || "";

                return {
                    href,
                    title,
                    text: cardText,
                    imageUrl
                };
            }
            """
        )

        if not data:
            return None

        return data

    except Exception as error:
        print("OZON EXTRACT LINK DATA ERROR:", error)
        return None


async def parse_ozon_product_link(
    link,
    query: str,
    category: str,
    source_page: int,
    strict_title_match: bool,
) -> dict | None:
    raw_data = await extract_product_data_from_link(link)

    if not raw_data:
        return None

    title = raw_data.get("title")
    href = raw_data.get("href")
    text = raw_data.get("text") or ""

    if not title:
        print("OZON SKIPPED: NO TITLE")
        return None

    title = str(title).strip()

    if len(title) < 5:
        return None

    price = clean_price_from_text(text)

    if price is None:
        print("OZON SKIPPED NO PRICE:", title)
        return None

    if is_wrong_category_product(title, category):
        print("OZON FILTERED WRONG CATEGORY:", title)
        return None

    if not is_relevant_product(
        title=title,
        query=query,
        category=category,
        strict_title_match=strict_title_match,
    ):
        print("OZON FILTERED BY RELEVANCE:", title)
        return None

    product_url = normalize_ozon_url(href)
    image_url = normalize_image_url(raw_data.get("imageUrl"))

    rating = clean_rating_from_text(text)
    reviews_count = clean_reviews_from_text(text)

    print("OZON ADDED:", title, price, image_url)

    return {
        "title": title,
        "price": price,
        "url": product_url,
        "image_url": image_url,

        "supplier": "Ozon.kz",
        "supplier_id": "ozon",

        "product_id": None,
        "rating": rating,
        "reviews_count": reviews_count,

        "available": True,
        "source_page": source_page,
        "category": category,
        "source": "ozon",

        "company_region": None,
        "company_slug": None,
        "company_positive_percent": None,
        "company_opinion_total": None,
    }


async def scrape_products(
    query: str,
    start_page: int = 1,
    end_page: int = 1,
    strict_title_match: bool = False,
    selected_category: str = "auto",
) -> list[dict]:
    category = resolve_category(query, selected_category)

    print("FAST PLAYWRIGHT OZON SCRAPER")
    print("USER QUERY:", query)
    print("SELECTED CATEGORY:", selected_category)
    print("RESOLVED CATEGORY:", category)
    print("PAGE RANGE:", start_page, "-", end_page)
    print("STRICT TITLE MATCH:", strict_title_match)

    products = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-extensions",
                    "--disable-background-networking",
                    "--disable-sync",
                    "--disable-default-apps",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )

            context = await browser.new_context(
                locale="ru-RU",
                viewport={"width": 1366, "height": 768},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )

            await context.route("**/*", block_unnecessary_resources)

            page = await context.new_page()

            for page_number in range(start_page, end_page + 1):
                url = build_ozon_search_url(query, page_number)

                print("FETCHING OZON PAGE:", url)

                try:
                    await page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=25000,
                    )
                except PlaywrightTimeoutError:
                    print("OZON PAGE TIMEOUT:", page_number)
                    continue

                current_url = page.url.lower()

                if "challenge" in current_url:
                    print("OZON CHALLENGE DETECTED. STOPPING OZON SCRAPER.")
                    break

                await page.wait_for_timeout(2500)
                await fast_scroll(page, scroll_count=3)

                links = await page.locator("a[href*='/product/']").all()

                print(f"OZON PAGE {page_number} PRODUCT LINKS:", len(links))

                if not links:
                    print("NO OZON PRODUCT LINKS FOUND")
                    continue

                page_added = 0
                max_links_per_page = 80

                for link in links[:max_links_per_page]:
                    parsed_product = await parse_ozon_product_link(
                        link=link,
                        query=query,
                        category=category,
                        source_page=page_number,
                        strict_title_match=strict_title_match,
                    )

                    if not parsed_product:
                        continue

                    products.append(parsed_product)
                    page_added += 1

                print(f"OZON PAGE {page_number} ADDED:", page_added)

            await browser.close()

    except Exception as error:
        print("Ozon Playwright scraping error:", error)
        return []

    unique_products = []
    seen = set()

    for product in products:
        key = (
            product.get("url"),
            product.get("title"),
            product.get("price"),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_products.append(product)

    print("OZON FINAL PRODUCTS:", len(unique_products))

    return unique_products