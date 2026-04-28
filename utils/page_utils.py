import allure
from playwright.async_api import Page


class PageUtils:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Clicking element: {selector}")
    async def click_element(self, selector: str) -> None:
        """Clicks an element and waits for the page to settle."""
        await self.page.locator(selector).click()
        await self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Filling '{text}' into element: {selector}")
    async def fill_element(self, selector: str, text: str) -> None:
        """Fills an element with text, ensuring it is focused first."""
        locator = self.page.locator(selector)
        await locator.wait_for(state='visible')
        await locator.fill(text)
