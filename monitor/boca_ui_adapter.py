"""Read-only UI adapter for the official match 878 page.

Requires an already authenticated Playwright page. No private API calls, no clicks,
no credential extraction. CSS color alone never confirms availability.
"""
from monitor.state import Observation

JS = r"""() => {
 const text = document.body?.innerText || "";
 const atSeat = /ASIENTO/.test(text) && /BUSCAR ASIENTO DISPONIBLE/.test(text);
 const mapNodes = [...document.querySelectorAll('svg path,svg polygon,svg rect,svg g,[role=button]')];
 const candidates = mapNodes.filter(e=>{
   const box=e.getBoundingClientRect();
   return box.width>8 && box.height>8 &&
     (e.getAttribute('aria-label') || e.getAttribute('data-sector') ||
      e.getAttribute('data-testid') || e.getAttribute('title'));
 });
 return {
   title: document.title, url:location.href,
   pageHasSectorStep: /SECTOR/.test(text),
   hasCart: /TU CARRITO/.test(text),
   cartCount: (text.match(/(\d+)\s+Reservas?/) || [])[1] ?? null,
   svgCount:document.querySelectorAll('svg').length,
   canvasCount:document.querySelectorAll('canvas').length,
   candidateCount:candidates.length,
   candidates:candidates.slice(0,300).map(e=>{
     const style=getComputedStyle(e);
     return {label:e.getAttribute('aria-label') || e.getAttribute('title') || e.getAttribute('data-sector') || e.getAttribute('data-testid'),
       fill:style.fill, clickable:style.pointerEvents!=='none', disabled:e.hasAttribute('disabled') || e.getAttribute('aria-disabled')==='true'};
   }),
   atSeat
 };
}"""

def read_ui(page):
    raw=page.evaluate(JS)
    # Nonzero SVG nodes alone can be decorative pitch. Never classify a map as
    # valid unless sector semantics were independently established.
    labelled=[x for x in raw["candidates"] if x["label"]]
    authenticated=bool(raw["hasCart"] and raw["pageHasSectorStep"])
    return {"raw":raw,"semantic_candidates":labelled,
            "requires_sector_mapping":True,
            "observation":Observation(authenticated=authenticated,
              map_loaded=False,sector_count=0)}
