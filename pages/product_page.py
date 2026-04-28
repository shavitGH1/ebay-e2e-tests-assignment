import allure
from typing import List
from playwright.async_api import Page, TimeoutError
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.product_title: str = "h1.x-item-title__mainTitle"
        self.add_to_cart_button: str = "#atcBtn_btn_1"
        self.options_container_selector: str = "div.x-msku-evo"
        self.see_in_cart_button: str = "//div[contains(@class, 'lightbox-dialog__main')]//a[.//span[text()='See in cart']]"
        self.added_to_cart_confirmation: str = "div.page-notice--confirmation"

    async def add_items_to_cart(self, urls: List[str]) -> None:
        with allure.step(f"Adding {len(urls)} items to cart"):
            for i, url in enumerate(urls):
                await self.navigate(url)

                # Take a screenshot of the product page
                title_locator = self.page.locator(self.product_title)
                await title_locator.wait_for(state='visible')
                await self.take_screenshot(f"Product Page - Item #{i + 1}")

                with allure.step(f"Handling options for item #{i + 1}"):
                    options_container = self.page.locator(self.options_container_selector)
                    if await options_container.count() > 0:
                        while True:
                            unselected_button = options_container.locator("button:has-text('Select')").first
                            if not await unselected_button.count():
                                break

                            await unselected_button.click()
                            await self.page.wait_for_timeout(500)

                            listbox_id = await unselected_button.get_attribute("aria-controls")
                            if listbox_id:
                                first_valid_option = self.page.locator(
                                    f"#{listbox_id} div.listbox__option:not([aria-disabled='true']):not(:has-text('Select'))"
                                ).first
                                if await first_valid_option.count() > 0:
                                    await first_valid_option.click()
                                    await self.page.wait_for_load_state("load", timeout=10000)
                                else:
                                    break

                add_to_cart_btn = self.page.locator(self.add_to_cart_button)
                if await add_to_cart_btn.is_visible():
                    await self.utils.click_element(self.add_to_cart_button)

                    # Take screenshot after adding item to cart

                    try:
                        see_in_cart_btn = self.page.locator(self.see_in_cart_button)
                        await see_in_cart_btn.wait_for(state='visible', timeout=5000)
                        await self.take_screenshot(f"Added item #{i + 1}")

                        await self.utils.click_element(self.see_in_cart_button)
                    except TimeoutError:
                        allure.step("Could not find 'See in cart' button. The cart may have opened automatically.")
                        pass
