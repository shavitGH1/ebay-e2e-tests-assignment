import allure
from playwright.async_api import Page
from utils.page_utils import PageUtils


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.utils: PageUtils = PageUtils(page)

    @allure.step("Navigating to {url}")
    async def navigate(self, url: str) -> None:
        await self.page.goto(url)
        await self.utils.wait_for_page_load()

    @allure.step("Waiting for selector: {selector}")
    async def wait_for_selector(self, selector: str) -> None:
        await self.page.wait_for_selector(selector)

    @allure.step("Taking screenshot: {name}")
    async def take_screenshot(self, name: str) -> None:
        screenshot = await self.page.screenshot()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        
