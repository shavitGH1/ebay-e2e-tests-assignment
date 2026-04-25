import pytest
import json
from typing import Dict, Any, AsyncGenerator
from playwright.async_api import async_playwright, Page, BrowserContext
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage

@pytest.fixture(scope="module")
def config() -> Dict[str, Any]:
    with open('data/config.json') as config_file:
        data = json.load(config_file)
    return data

@pytest.fixture(scope="function")
async def page_setup(config: Dict[str, Any]) -> AsyncGenerator[Page, None]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        login_page = LoginPage(page)
        await login_page.navigate("https://www.ebay.com")
        await login_page.login(config['username'], config['password'])
        
        try:
            yield page
        finally:
            try:
                # Attempt to clean up the cart, but don't let it block browser closing
                cart_page = CartPage(page)
                await cart_page.navigate_to_cart()
                await cart_page.empty_cart()
            finally:
                # Ensure browser is always closed
                await context.close()
                await browser.close()

@pytest.mark.asyncio
async def test_search_add_to_cart_and_assert_total(page_setup: Page, config: Dict[str, Any]) -> None:
    page = page_setup
    search_page = SearchPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    # 1. Search for items and get URLs
    item_urls = await search_page.search_items_by_name_under_price(
        config['search_query'],
        config['max_price'],
        config['items_limit']
    )
    
    # 2. Add all items to the cart, clicking "See in cart" after each one
    await product_page.add_items_to_cart(item_urls)
    
    # 3. As a final step, navigate to the main cart page to ensure we are in the right place
    await cart_page.navigate_to_cart()

    # 4. Assert the total on the final cart page
    await cart_page.assert_cart_total_not_exceeds(
        config['max_price'],
        len(item_urls)
    )