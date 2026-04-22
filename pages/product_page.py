import allure
from typing import List
from playwright.async_api import Page
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.add_to_cart_button: str = "a[data-testid='ux-call-to-action']"
        self.size_dropdown: str = "select[name='Size']"
        self.color_dropdown: str = "select[name='Color']"
        self.stay_on_page_button: str = "button[data-test-id='stay-on-page-cta']"

    async def add_items_to_cart(self, urls: List[str]) -> None:
        with allure.step(f"Adding {len(urls)} items to cart"):
            for url in urls:
                await self.navigate(url)

                if await self.page.is_visible(self.size_dropdown):
                    await self.page.select_option(self.size_dropdown, index=1)
                
                if await self.page.is_visible(self.color_dropdown):
                    await self.page.select_option(self.color_dropdown, index=1)

                if await self.page.is_visible(self.add_to_cart_button):
                    await self.utils.click_element(self.add_to_cart_button)
                    if await self.page.is_visible(self.stay_on_page_button):
                        await self.utils.click_element(self.stay_on_page_button)
                await self.take_screenshot(f"Added item from {url}")
