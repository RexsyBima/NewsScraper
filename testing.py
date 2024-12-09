import re


def is_webp_url(url):
    # Regular expression pattern to match WebP image URLs
    webp_pattern = r'\.png(?:\?|$)|/format/png|png/'

    # Case-insensitive search for WebP indicators
    return bool(re.search(webp_pattern, url, re.IGNORECASE))


# Test the function
test_urls = [
    "https://dims.apnews.com/dims4/default/efd49ca/2147483647/strip/true/crop/5758x3837+0+1/resize/980x653!/format/webp/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2Fd7%2F35%2Fbf492720d3f8f39c1d731a9aa301%2Fe4e0e569c9bd4adab91f022e56758035",
    "https://example.com/image.webp",
    "https://example.com/image?format=webp",
    "https://example.com/webp/image",
    "https://example.com/image.jpg",
    "https://example.com/image?type=png"
]

for url in test_urls:
    print(f"{url}: {is_webp_url(url)}")
