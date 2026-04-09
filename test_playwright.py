import asyncio
from playwright.async_api import async_playwright

async def scrape_members():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # reuse saved session
        context = await browser.new_context(storage_state="session.json")
        page = await context.new_page()

        # go directly to members page
        await page.goto("https://trello.com/w/userworkspace73676029/members")

        # wait for UI
        await page.wait_for_timeout(5000)

        # extract members
        members = await page.evaluate("""
        () => {
            const rows = document.querySelectorAll('[data-testid="workspace-member-item"]');

            return Array.from(rows)
                .map(row => {
                    const name = row.querySelector("strong")?.innerText.trim() || "";

                    const username = Array.from(row.querySelectorAll("span"))
                        .map(el => el.innerText.trim())
                        .find(text => text.startsWith("@")) || "";

                    return { name, username };
                })
                .filter(user => user.name.length > 0);
        }
        """)

        print(members)

        input("Press Enter to close...")
        await browser.close()

asyncio.run(scrape_members())