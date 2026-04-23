import allure
from typing import List
from playwright.async_api import Page, TimeoutError
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.add_to_cart_button: str = "#atcBtn_btn_1"
        self.options_container_selector: str = "div.x-msku-evo"
        # Precise selector for the "See in cart" button within the main dialog overlay
        self.see_in_cart_button: str = "//div[contains(@class, 'lightbox-dialog__main')]//a[.//span[text()='See in cart']]"

    async def add_items_to_cart(self, urls: List[str]) -> None:
        with allure.step(f"Adding {len(urls)} items to cart"):
            for url in urls:
                await self.navigate(url)

                with allure.step("Handling all product option dropdowns sequentially"):
                    options_container = await self.page.query_selector(self.options_container_selector)
                    if options_container:
                        while True:
                            unselected_button = await options_container.query_selector(
                                "button:has-text('Select')"
                            )
                            if not unselected_button:
                                allure.step("No more unselected dropdowns found. Proceeding.")
                                break

                            allure.step("Found an unselected dropdown. Making a selection.")
                            listbox_id = await unselected_button.get_attribute("aria-controls")
                            if not listbox_id:
                                break

                            await unselected_button.click()
                            await self.page.wait_for_timeout(500)

                            first_valid_option = await self.page.query_selector(
                                f"#{listbox_id} div.listbox__option:not([aria-disabled='true']):not(:has-text('Select'))"
                            )
                            
                            if first_valid_option:
                                await first_valid_option.click()
                                await self.page.wait_for_load_state("load", timeout=10000)
                            else:
                                break
                    
                add_to_cart_btn = await self.page.query_selector(self.add_to_cart_button)
                if add_to_cart_btn and await add_to_cart_btn.is_visible():
                    await add_to_cart_btn.click()
                    
                    try:
                        see_in_cart_btn = await self.page.wait_for_selector(self.see_in_cart_button, state='visible', timeout=5000)
                        await see_in_cart_btn.click()
                    except TimeoutError:
                        allure.step("Could not find 'See in cart' button. The cart may have opened automatically.")

                await self.take_screenshot(f"Added item from {url}")
