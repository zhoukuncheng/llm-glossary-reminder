import datetime
import logging
import re

from bs4 import BeautifulSoup
from markdown2 import markdown
from telegraph.aio import Telegraph


async def write_to_telegraph(html: str) -> str:
    telegraph = Telegraph()
    if not telegraph.get_access_token():
        logging.info(await telegraph.create_account(short_name="anonymous"))

    response = await telegraph.create_page(
        f"Glossary {datetime.datetime.now(datetime.UTC)}",
        html_content=html,
    )
    logging.info(response)
    return response["url"]


def markdown_to_text(markdown_string):
    """Converts a markdown string to plaintext"""

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r"<pre>(.*?)</pre>", " ", html)
    html = re.sub(r"<code>(.*?)</code >", " ", html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = "".join(soup.findAll(text=True))

    return text
