import allure
from typing import List
from playwright.async_api import Page
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.add_to_cart_button: str = "//span[contains(text(),'Add to cart')]/ancestor::a"
        # More generic selector for any custom dropdown component
        self.custom_dropdown_selector: str = "span.listbox-button"
        self.standard_dropdown_selector: str = "select"
        self.stay_on_page_button: str = "button[data-test-id='stay-on-page-cta']"

    async def add_items_to_cart(self, urls: List[str]) -> None:
        with allure.step(f"Adding {len(urls)} items to cart"):
            for url in urls:
                await self.navigate(url)

                with allure.step("Handling all product option dropdowns"):
                    # 1. Handle all modern, custom-built dropdowns
                    custom_dropdowns = await self.page.query_selector_all(self.custom_dropdown_selector)
                    for dropdown_container in custom_dropdowns:
                        dropdown_button = await dropdown_container.query_selector("button.listbox-button__control")
                        if dropdown_button and await dropdown_button.is_visible():
                            await dropdown_button.click()
                            await self.page.wait_for_timeout(500)  # Wait for animation

                            # Get all options and find the first valid one to click
                            options = await dropdown_container.query_selector_all("div.listbox__option")
                            for option in options:
                                is_disabled = await option.get_attribute("aria-disabled")
                                text_content = await option.inner_text()
                                
                                # A valid option is not disabled and is not a placeholder
                                if is_disabled != "true" and "select" not in text_content.lower():
                                    await option.click()
                                    await self.utils.wait_for_page_load()
                                    break  # Exit the inner loop and move to the next dropdown

                    # 2. Handle all traditional <select> dropdowns as a fallback
                    standard_dropdowns = await self.page.query_selector_all(self.standard_dropdown_selector)
                    for dropdown in standard_dropdowns:
                        if await dropdown.is_visible():
                            # Get all options from the select
                            option_elements = await dropdown.query_selector_all("option")
                            if len(option_elements) > 1:
                                # Select the second option (index 1) to skip any "- Select -" placeholders
                                await dropdown.select_option(index=1)
                                await self.utils.wait_for_page_load()

                # After handling all dropdowns, add to cart
                if await self.page.is_visible(self.add_to_cart_button):
                    await self.utils.click_element(self.add_to_cart_button)
                    try:
                        if await self.page.is_visible(self.stay_on_page_button, timeout=3000):
                            await self.utils.click_element(self.stay_on_page_button)
                    except:
                        pass  # Popup did not appear, continue
                await self.take_screenshot(f"Added item from {url}")
