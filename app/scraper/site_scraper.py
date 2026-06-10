import asyncio

from app.scraper.satu_scraper import scrape_products as scrape_satu_products
from app.scraper.ozon_scraper import scrape_products as scrape_ozon_products


async def scrape_products(
    query: str,
    start_page: int = 1,
    end_page: int = 1,
    strict_title_match: bool = False,
    selected_category: str = "auto",
    selected_source: str = "all",
) -> list[dict]:
    tasks = []

    if selected_source in ["all", "satu"]:
        tasks.append(
            scrape_satu_products(
                query=query,
                start_page=start_page,
                end_page=end_page,
                strict_title_match=strict_title_match,
                selected_category=selected_category,
            )
        )

    if selected_source in ["all", "ozon"]:
        tasks.append(
            scrape_ozon_products(
                query=query,
                start_page=start_page,
                end_page=end_page,
                strict_title_match=strict_title_match,
                selected_category=selected_category,
            )
        )

    if not tasks:
        return []

    results = await asyncio.gather(*tasks, return_exceptions=True)

    products = []

    for result in results:
        if isinstance(result, Exception):
            print("SCRAPER ERROR:", result)
            continue

        products.extend(result)

    return products