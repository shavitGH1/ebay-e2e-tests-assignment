import allure
from typing import List
from playwright.async_api import Page, TimeoutError
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Using the precise selectors as per your instructions
        self.add_to_cart_button: str = "#atcBtn_btn_1"
        self.options_container_selector: str = "div.x-msku-evo"
        # This is now handled by the logic below, but kept for potential fallback
        self.stay_on_page_button: str = "button[data-test-id='stay-on-page-cta']"

    async def add_items_to_cart(self, urls: List[str]) -> None:
        with allure.step(f"Adding {len(urls)} items to cart"):
            for url in urls:
                await self.navigate(url)

                with allure.step("Handling all product option dropdowns sequentially"):
                    options_container = await self.page.query_selector(self.options_container_selector)
                    if options_container:
                        # Loop until no more dropdowns with "Select" are found.
                        while True:
                            # Find the first dropdown button that still has "Select" as its text.
                            unselected_button = await options_container.query_selector(
                                "button:has-text('Select')"
                            )

                            if not unselected_button:
                                allure.step("No more unselected dropdowns found. Proceeding.")
                                break  # Exit loop if no more dropdowns say "Select"

                            allure.step("Found an unselected dropdown. Making a selection.")
                            
                            listbox_id = await unselected_button.get_attribute("aria-controls")
                            if not listbox_id:
                                break

                            await unselected_button.click()
                            await self.page.wait_for_timeout(500)

                            # Find the first option that is not a placeholder and not disabled (e.g., "Out of stock").
                            first_valid_option = await self.page.query_selector(
                                f"#{listbox_id} div.listbox__option:not([aria-disabled='true']):not(:has-text('Select'))"
                            )
                            
                            if first_valid_option:
                                await first_valid_option.click()
                                # Wait for the page to process the selection before the next loop.
                                await self.page.wait_for_load_state("load", timeout=10000)
                            else:
                                # If no valid options are found, break to avoid an infinite loop.
                                break
                    
                # After handling all dropdowns, click "Add to cart".
                add_to_cart_btn = await self.page.query_selector(self.add_to_cart_button)
                if add_to_cart_btn and await add_to_cart_btn.is_visible():
                    await add_to_cart_btn.click()
                    # The user's latest instruction stops here, but we can add popup handling back if needed.

                await self.take_screenshot(f"Added item from {url}")
