import allure
import re
from playwright.async_api import Page
from pages.base_page import BasePage
from utils.wait_utils import random_async_wait, human_like_click

class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_total_element: str = "div[data-test-id='SUBTOTAL']"
        self.cart_icon: str = "a[href='https://www.ebay.com/cart']"
        self.remove_item_button: str = "button[data-test-id='cart-remove-item']"

    async def navigate_to_cart(self) -> None:
        with allure.step("Navigating to the main shopping cart page"):
            await human_like_click(self.page, self.cart_icon)
            await self.page.wait_for_load_state("domcontentloaded")

    async def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        with allure.step(f"Asserting cart total is within budget"):
            await self.wait_for_selector(self.cart_total_element)
            await random_async_wait()

            total_price_text = await self.page.inner_text(self.cart_total_element)

            price_match = re.search(r'[\d,]+\.\d{2}', total_price_text.replace(',', ''))
            if not price_match:
                raise ValueError("Could not parse total price from cart.")

            total_price = float(price_match.group(0))
            budget = budget_per_item * items_count

            await self.take_screenshot(f"Cart Page - Budget: ${budget}")
            assert total_price <= budget, f"Cart total ${total_price} exceeds budget ${budget}"

    async def empty_cart(self) -> None:
        with allure.step("Emptying the shopping cart"):
            remove_buttons = self.page.locator(self.remove_item_button)

            while True:
                count = await remove_buttons.count()
                if count == 0:
                    break

                await human_like_click(self.page, self.remove_item_button)
                await random_async_wait()

                await self.page.wait_for_function(
                    "([selector, oldCount]) => document.querySelectorAll(selector).length < oldCount",
                    arg=[self.remove_item_button, count]
                )
