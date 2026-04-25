import pytest
import json
import asyncio
from typing import Dict, Any
from playwright.async_api import async_playwright, Page
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
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        login_page = LoginPage(page)
        search_page = SearchPage(page)
        product_page = ProductPage(page)
        cart_page = CartPage(page)

        # 1. Navigate and log in
        await login_page.navigate("https://www.ebay.com")
        await login_page.login(config['username'], config['password'])
        
        # 2. Search for items and get URLs
        item_urls = await search_page.search_items_by_name_under_price(
            config['search_query'],
            config['max_price'],
            config['items_limit']
        )
        
        # 3. Add all items to the cart, clicking "See in cart" after each one
        await product_page.add_items_to_cart(item_urls)
        
        # 4. As a final step, navigate to the main cart page to ensure we are in the right place
        await cart_page.navigate_to_cart()

        # 5. Assert the total on the final cart page
        await cart_page.assert_cart_total_not_exceeds(
            config['max_price'],
            len(item_urls)
        )

        # 6. Cleanup - Empty the cart
        await cart_page.empty_cart()

        await context.close()
        await browser.close()

if __name__ == "__main__":
    with open('data/config.json') as f:
        main_config = json.load(f)
    asyncio.run(test_search_add_to_cart_and_assert_total(main_config))
