"""Diagnóstico PASIVO de la pantalla de plateas. No reserva ni monitorea en segundo plano."""
import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright

URL="https://bocasocios.bocajuniors.com.ar/matches/878/plateas"
async def run():
    out=Path("diagnostics"); out.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=False)
        page=await browser.new_page()
        await page.goto(URL,wait_until="domcontentloaded",timeout=60000)
        input("Iniciá sesión manualmente y presioná Enter para capturar el mapa: ")
        await page.screenshot(path=str(out/"mapa.png"),full_page=True)
        data=await page.evaluate("""() => ({
            title:document.title,
            url:location.href,
            text:document.body?.innerText?.slice(0,2500),
            graphics:{svg:document.querySelectorAll('svg').length,canvas:document.querySelectorAll('canvas').length},
            candidates:[...document.querySelectorAll('button,[aria-label],[data-testid]')].slice(0,200).map(e=>({
                tag:e.tagName,aria:e.getAttribute('aria-label'),testid:e.getAttribute('data-testid'),
                disabled:e.hasAttribute('disabled'),text:e.textContent?.trim().slice(0,60)
            }))
        })""")
        data["reservation_confirmed"]=False
        (out/"mapa.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
        await browser.close()
if __name__=="__main__": asyncio.run(run())
