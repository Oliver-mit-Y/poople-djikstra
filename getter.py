from pathlib import Path
import re
import string
from playwright.sync_api import sync_playwright

words = set()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for letter in string.ascii_lowercase:
        page.goto(f'https://poopleplay.com/word-list?letter={letter}')
        page.get_by_text('Four letter word list', exact=False).first.wait_for()
        count_text = page.get_by_text(re.compile(r'^\d+ words?$')).first.inner_text()
        expected = int(count_text.split()[0])
        more = page.get_by_text(re.compile(r'Show more words under', re.I))
        while more.count() and more.first.is_visible():
            before = page.locator('body').inner_text()
            more.first.click()
            page.wait_for_function('(before) => document.body.innerText !== before', arg=before)
        text = page.locator('body').inner_text()
        # Only the dictionary section, before the explanatory content.
        text = text.split(count_text, 1)[1].split('What gets in', 1)[0]
        found = {w.lower() for w in re.findall(r'\b[A-Z]{4}\b', text) if w[0].lower() == letter}
        if len(found) != expected:
            raise RuntimeError(f'{letter}: expected {expected}, got {len(found)}; inspect page markup')
        words.update(found)
        print(letter, len(found))
    browser.close()
if len(words) != 2247:
    raise RuntimeError(f'Expected 2247 words, got {len(words)}')
Path('words.txt').write_text('\n'.join(sorted(words)) + '\n', encoding='utf-8')
print('Created words.txt with', len(words), 'words')