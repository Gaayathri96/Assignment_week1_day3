
from playwright.sync_api import sync_playwright, TimeoutError
import re

URL = "https://m.cricbuzz.com/cricket-match/live-scores"
SCREENSHOT = "cricbuzz_screenshot.png"

SCORE_PATTERN = re.compile(
    r"\b[A-Z]{2,6}\s+\d{1,3}[-/]\d{1,2}"
    r"(?:\s*\(\d+(?:\.\d+)?(?:\s*Ov)?\))?"
)

STATUS_PATTERN = re.compile(
    r"need \d+ runs?|trail by|lead by|won by|"
    r"opt to bat|opt to bowl|innings break|stumps",
    re.IGNORECASE,
)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1366, "height": 900})

        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)

            try:
                page.wait_for_function(
                    """() => {
                        const t = document.body?.innerText || "";
                        return /Access Denied/i.test(t) ||
                               /[A-Z]{2,6}\\s+\\d{1,3}[-/]\\d{1,2}/.test(t);
                    }""",
                    timeout=30000,
                )
            except TimeoutError:
                print("Timed out waiting for a score.")

            # Save screenshot whether or not a score was found.
            page.screenshot(path=SCREENSHOT, full_page=True)
            print(f"Screenshot saved: {SCREENSHOT}")

            text = page.locator("body").inner_text()

            if "Access Denied" in text:
                print("Cricbuzz denied access; no score was retrieved.")
                return

            lines = [line.strip() for line in text.splitlines() if line.strip()]

            for i, line in enumerate(lines):
                if not SCORE_PATTERN.search(line):
                    continue

                # Find a nearby status for the same match.
                for j in range(i, min(i + 5, len(lines))):
                    if STATUS_PATTERN.search(lines[j]):
                        print(line)
                        if lines[j] != line:
                            print(lines[j])
                        return

            print("No matching score and status found.")
            print("Open the screenshot to inspect the loaded page.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            browser.close()


if __name__ == "__main__":
    main()
