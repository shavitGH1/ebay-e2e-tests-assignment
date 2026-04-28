import allure
import re
from playwright.async_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_total_element: str = "div[data-test-id='SUBTOTAL']"
        self.cart_icon: str = "a[href='https://www.ebay.com/cart']"
        self.remove_item_button: str = "button[data-test-id='cart-remove-item']"
        self.cart_items: str = "div.cart-bucket"

    async def navigate_to_cart(self) -> None:
        """Clicks the main cart icon to ensure the test is on the final cart page."""
        with allure.step("Navigating to the main shopping cart page"):
            if await self.page.locator(self.cart_icon).count() > 0:
                await self.utils.click_element(self.cart_icon)

    async def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        with allure.step(f"Asserting cart total is within budget"):
            await self.page.locator(self.cart_items).first.wait_for(state='visible')
            await self.page.locator(self.cart_total_element).wait_for()

            total_price_text = await self.page.locator(self.cart_total_element).inner_text()

            price_match = re.search(r'[\d,]+\.\d{2}', total_price_text.replace(',', ''))
            if not price_match:
                raise ValueError("Could not parse total price from cart.")

            total_price = float(price_match.group(0))
            budget = budget_per_item * items_count

            await self.take_screenshot(f"Cart Page - Budget: ${budget}")
            assert total_price <= budget, f"Cart total ${total_price} exceeds budget ${budget}"

    async def empty_cart(self) -> None:
        """Removes all items from the cart."""
        with allure.step("Emptying the shopping cart"):
            # Create a strict locator for the buttons
            remove_buttons = self.page.locator(self.remove_item_button)

            while True:
                # Check how many remove buttons are currently on the screen
                count = await remove_buttons.count()
                if count == 0:
                    break  # Cart is empty, exit the loop

                # Always click the first button in the list.
                # Locators will automatically wait for the button to be visible and clickable.
                await remove_buttons.first.click()

                # Wait explicitly for the DOM to update by ensuring the count decreases.
                # We pass the selector and the old count directly into the browser context.
                await self.page.wait_for_function(
                    "([selector, oldCount]) => document.querySelectorAll(selector).length < oldCount",
                    arg=[self.remove_item_button, count]
                )
