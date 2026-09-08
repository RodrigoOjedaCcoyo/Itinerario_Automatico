import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel
from playwright.async_api import async_playwright

API_KEY = os.getenv("PDF_SERVICE_API_KEY")

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    state["playwright"] = playwright
    state["browser"] = browser
    yield
    await browser.close()
    await playwright.stop()


app = FastAPI(lifespan=lifespan)


class PdfRequest(BaseModel):
    html: str
    format: str = "A4"
    margin: str = "0"
    print_media_type: bool = True


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/pdf")
async def generate_pdf(payload: PdfRequest, x_api_key: str = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")

    browser = state["browser"]
    page = await browser.new_page()
    try:
        await page.set_content(payload.html, wait_until="load")
        if payload.print_media_type:
            await page.emulate_media(media="print")
        pdf_bytes = await page.pdf(
            format=payload.format,
            print_background=True,
            margin={
                "top": payload.margin,
                "right": payload.margin,
                "bottom": payload.margin,
                "left": payload.margin,
            },
            prefer_css_page_size=True,
        )
    finally:
        await page.close()

    return Response(content=pdf_bytes, media_type="application/pdf")
