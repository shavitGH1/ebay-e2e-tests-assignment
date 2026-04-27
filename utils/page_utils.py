import allure
from playwright.async_api import Page


class PageUtils:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Clicking element: {selector}")
    async def click_element(self, selector: str, **kwargs) -> None:
        """Clicks an element and waits for the page to settle."""
        await self.page.click(selector, **kwargs)
        await self.wait_for_page_load()

    @allure.step("Filling '{text}' into element: {selector}")
    async def fill_element(self, selector: str, text: str, **kwargs) -> None:
        """Fills an element with text."""
        await self.page.fill(selector, text, **kwargs)

    @allure.step("Waiting for page to load")
    async def wait_for_page_load(self) -> None:
        """Waits for the page's load event to fire."""
        await self.page.wait_for_load_state('load')
