#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, os, re, urllib.parse, html
from datetime import datetime

# ------------- CONFIG (bunları kendine göre değiştir) -------------
SITE_URL = "https://github.com/emlakcrm/emlak"   # sitenin ana domaini (sonunda / olmasın)
AGENT_NAME = "Selman Güneş"
PHONE = "+905355739260"                # uluslararası format
PHONE_DISPLAY = "0 535 573 92 60"      # sayfada gösterilecek format
WHATSAPP = "905355739260"              # wa.me için düz numara (ülke kodlu)
AGENT_EMAIL = "selmangunesemlak@gmail.com"
INSTAGRAM = "https://instagram.com/selmangunesemlak"
FACEBOOK = "https://facebook.com/emlakfirma"
OUTPUT_DIR = "output"
TEMPLATE_FILE = "template.html"
CSV_FILE = "mahaller.csv"
# -------------------------------------------------------------------

# otomatik oluşturulacak etiket (en çok aranan emlak kelimeleri)
COMMON_TAGS = [
    "2+1","3+1","güney cepheli","yol cepheli","krediye uygun","dubleks",
    "yüksek giriş","toplu taşımaya yakın","okula yakın","market yakın",
    "sosyal donatı","bahçe","site içi","köşe daire","ara kat","eşyali",
    "tapusu temiz","FuzulEv uyumlu","EminEvim uyumlu"
]

def slugify(text):
    text = text.strip().lower()
    # türkçe karakterleri dönüştür
    replacements = {'ğ':'g','ü':'u','ş':'s','ı':'i','ö':'o','ç':'c'}
    for k,v in replacements.items():
        text = text.replace(k,v)
    text = re.sub(r'[^a-z0-9\- ]','', text)
    text = re.sub(r'\s+','-', text)
    text = re.sub(r'\-+','-', text)
    return text.strip('-')

def urlencode_query(q):
    return urllib.parse.quote_plus(q)

def safe_html(s):
    return html.escape(s or "")

# Template yükle
if not os.path.exists(TEMPLATE_FILE):
    print(f"Hata: {TEMPLATE_FILE} bulunamadı. Aynı klasöre template.html koyun.")
    exit(1)

with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    template = f.read()

os.makedirs(OUTPUT_DIR, exist_ok=True)

# CSV oku
if not os.path.exists(CSV_FILE):
    print(f"Hata: {CSV_FILE} bulunamadı. Örnek bir mahaller.csv oluşturun.")
    exit(1)

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        mahalle = row.get('mahalle','').strip()
        ilce = row.get('ilce','').strip()
        il = row.get('il','').strip()
        meta_desc = row.get('meta_desc','').strip() or f"{il} {ilce} {mahalle} bölgesinde 2+1 ve 3+1 satılık daireler. Güney cepheli, krediye uygun."
        img1 = row.get('img1','').strip() or f"{SITE_URL}/images/{slugify(mahalle)}-1.jpg"
        img2 = row.get('img2','').strip() or f"{SITE_URL}/images/{slugify(mahalle)}-2.jpg"
        img3 = row.get('img3','').strip() or f"{SITE_URL}/images/{slugify(mahalle)}-3.jpg"

        if not mahalle:
            print("Uyarı: mahalle boş — atlandı.")
            continue

        slug = slugify(mahalle)
        filename = f"{slug}.html"
        outpath = os.path.join(OUTPUT_DIR, filename)
        canonical = f"{SITE_URL}/{filename}"
        og_image = row.get('og_image','').strip() or img1

        # Map query
        map_query = urlencode_query(f"{mahalle} Mahallesi {ilce} {il}")

        # WhatsApp text (encode)
        wa_text = urlencode_query(f"{AGENT_NAME} Merhaba, {mahalle} Mahallesi'ndeki daireleri görmek istiyorum. Bilgi alabilir miyim?")

        # tags HTML
        # combine common tags plus mahalle/ilce/il
        tags = [mahalle, ilce, il] + COMMON_TAGS
        tags_html = " ".join([f'<span class="tag">{html.escape(t)}</span>' for t in tags])

        # Yer tutucuları değiştir
        page = template
        replacements = {
            "{{MAHALLE}}": safe_html(mahalle),
            "{{ILCE}}": safe_html(ilce),
            "{{IL}}": safe_html(il),
            "{{META_DESC}}": safe_html(meta_desc),
            "{{IMG1}}": img1,
            "{{IMG2}}": img2,
            "{{IMG3}}": img3,
            "{{PHONE}}": PHONE,
            "{{PHONE_DISPLAY}}": PHONE_DISPLAY,
            "{{WHATSAPP_PLAIN}}": WHATSAPP,
            "{{WHATSAPP_TEXT_ENCODED}}": wa_text,
            "{{WHATSAPP_TEXT}}": wa_text,
            "{{AGENT_NAME}}": safe_html(AGENT_NAME),
            "{{AGENT_EMAIL}}": AGENT_EMAIL,
            "{{INSTAGRAM}}": INSTAGRAM,
            "{{FACEBOOK}}": FACEBOOK,
            "{{SITE_URL}}": SITE_URL,
            "{{CANONICAL}}": canonical,
            "{{OG_IMAGE}}": og_image,
            "{{MAP_QUERY}}": map_query,
            "{{YEAR}}": str(datetime.now().year),
            "{{TAGS_HTML}}": tags_html,
            "{{PHONE_DISPLAY}}": PHONE_DISPLAY
        }

        for k,v in replacements.items():
            page = page.replace(k, v)

        with open(outpath, 'w', encoding='utf-8') as wf:
            wf.write(page)

        print(f"✓ Oluşturuldu: {outpath}")
        count += 1

print(f"\nToplam {count} mahalle sayfası oluşturuldu. Çıktılar: {os.path.abspath(OUTPUT_DIR)}")
