"""Screenshot comparison aid for match 878. NOT an availability or booking verifier.

The stadium turf is green even when no seat is available. Visual differences
require manual confirmation on Boca Socios. Do not auto-book from this output.
"""
from PIL import Image, ImageChops, ImageStat

def compare_screenshots(reference, current):
    base = Image.open(reference).convert("RGB")
    other = Image.open(current).convert("RGB")
    if base.size != other.size:
        return {"state": "inconclusive", "reason": "viewport_changed"}
    # Coordinates deliberately NOT used for booking; a changed page could be
    # session expiry, loading overlay, zoom, or an actual sector change.
    diff = ImageChops.difference(base, other)
    avg = sum(ImageStat.Stat(diff).mean) / 3
    return {"state": "manual_review_required" if avg > 2 else "no_significant_change",
            "mean_pixel_difference": round(avg, 2),
            "reservation_confirmed": False,
            "availability_confirmed": False}

if __name__ == "__main__":
    import sys, json
    print(json.dumps(compare_screenshots(sys.argv[1],sys.argv[2])))
