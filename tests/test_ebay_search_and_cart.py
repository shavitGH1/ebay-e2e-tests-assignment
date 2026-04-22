import pytest
import json
import asyncio
from typing import Dict, Any
from playwright.async_api import async_playwright
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage

@pytest.fixture(scope="module")
def config() -> Dict[str, Any]:
    with open('data/config.json') as config_file:
        data = json.load(config_file)
    return data

@pytest.mark.asyncio
async def test_search_add_to_cart_and_assert_total(config: Dict[str, Any]) -> None:
    """
    Main E2E test flow:
    1. Logs in to eBay.
    2. Searches for an item.
    3. Adds a specified number of items to the cart under a max price.
    4. Navigates to the cart and asserts the total does not exceed the budget.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        login_page = LoginPage(page)
        search_page = SearchPage(page)
        product_page = ProductPage(page)
        cart_page = CartPage(page)

        await login_page.navigate("https://www.ebay.com")
        await login_page.login(config['username'], config['password'])
        
        item_urls = await search_page.search_items_by_name_under_price(
            config['search_query'],
            config['max_price'],
            config['items_limit']
        )
        
        await product_page.add_items_to_cart(item_urls)
        
        await cart_page.assert_cart_total_not_exceeds(
            config['max_price'],
            len(item_urls)
        )

        await context.close()
        await browser.close()

if __name__ == "__main__":
    # This allows running the test directly for debugging.
    with open('data/config.json') as f:
        main_config = json.load(f)
    asyncio.run(test_search_add_to_cart_and_assert_total(main_config))
