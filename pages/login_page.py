import allure
import random
from playwright.async_api import Page, TimeoutError
from pages.base_page import BasePage
from utils.wait_utils import random_async_wait, human_like_click

class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.signin_button: str = "//a[text()='Sign in']"
        self.userid_input: str = "//input[@id='userid']"
        self.continue_button: str = "#signin-continue-btn"
        self.password_input: str = "#pass"
        self.signin_submit_button: str = "#sgnBt"
        self.skip_passkey_button: str = "#passkeys-cancel-btn"

    async def navigate(self, url: str) -> None:
        await super().navigate(url)
        await self.page.reload()

    async def login(self, username: str, password: str) -> None:
        with allure.step(f"Logging in as {username}"):
            await human_like_click(self.page, self.signin_button)
            await random_async_wait()

            await self.page.wait_for_selector(self.userid_input, state='visible')
            await self.page.type(self.userid_input, username, delay=random.randint(100, 250))
            await random_async_wait()
            await human_like_click(self.page, self.continue_button)
            await random_async_wait()

            await self.page.wait_for_selector(self.password_input, state='visible')
            await self.page.type(self.password_input, password, delay=random.randint(100, 250))
            await random_async_wait()
            await human_like_click(self.page, self.signin_submit_button)

            with allure.step("Check for and skip Passkey page if it appears"):
                try:
                    await self.page.wait_for_selector(self.skip_passkey_button, state='visible', timeout=5000)
                    await human_like_click(self.page, self.skip_passkey_button)
                    await self.utils.wait_for_page_load()
                except TimeoutError:
                    allure.step("Passkey page did not appear. Continuing.")
                    pass

            await self.take_screenshot("Logged In")
