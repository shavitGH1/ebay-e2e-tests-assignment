import allure
import re
from playwright.async_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_total_element: str = "div[data-test-id='SUBTOTAL']"

    async def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        with allure.step(f"Asserting cart total is within budget"):
            await self.navigate("https://www.ebay.com/cart")
            await self.wait_for_selector(self.cart_total_element)
            
            total_price_text = await self.page.inner_text(self.cart_total_element)
            
            # Extract the float value from the text
            price_match = re.search(r'[\d,]+\.\d{2}', total_price_text.replace(',', ''))
            if not price_match:
                raise ValueError("Could not parse total price from cart.")
            
            total_price = float(price_match.group(0))
            budget = budget_per_item * items_count
            
            allure.attach(f"Actual Total: ${total_price}, Budget: ${budget}", name="Price Comparison")
            assert total_price <= budget, f"Cart total ${total_price} exceeds budget ${budget}"
