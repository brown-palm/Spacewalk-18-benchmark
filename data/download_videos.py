import os

urls = {
    "01152020": "https://www.youtube.com/watch?v=84CRZYioFRs",
    "01252020": "https://www.youtube.com/watch?v=cOzMVW1GdDc",
    "01272021": "https://www.youtube.com/watch?v=q3tVWmP0CMc",
    "02012021": "https://www.youtube.com/watch?v=XwuRiIh2IlM",
    "02282021": "https://www.youtube.com/watch?v=gcv6beMn750",
    "03152022": "https://www.youtube.com/watch?v=s4TVhE8NDLs",
    "03232022": "https://www.youtube.com/watch?v=uZqaTsbDcgU",
    "06092023": "https://www.youtube.com/watch?v=wS4z42KaeGk",
    "06162021": "https://www.youtube.com/watch?v=gCKsedpraVg",
    "06262020": "https://www.youtube.com/watch?v=KlK_bLnqmas",
    "09122021": "https://www.youtube.com/watch?v=vvsMOSAfHG0",
    "10062019": "https://www.youtube.com/watch?v=z0Ut8daLD6I",
    "11152019": "https://www.youtube.com/watch?v=evaBhht5uGA",
    "11152022": "https://www.youtube.com/watch?v=sNvIV3UUcQw",
    "11222019": "https://www.youtube.com/watch?v=sIpjW-KUcEA",
    "12022019": "https://www.youtube.com/watch?v=gH1OHoszYcw",
    "12022021": "https://www.youtube.com/watch?v=ScAtmwgIXwU",
    "12032022": "https://www.youtube.com/watch?v=zvxenTNLjWE"
}

os.makedirs('videos', exist_ok=True)
for date, url in urls.items():
    print(url)
    os.system(f'yt-dlp -o videos/{date}.mp4 {url}')