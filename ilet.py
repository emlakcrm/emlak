import streamlit as st
import pandas as pd
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. SEO VE SAYFA AYARLARI ---
# Title ve Meta Description botlar için çok kritiktir.
st.set_page_config(
    page_title="Kepez Emlak Fiyat Analizi | Selman Güneş Ücretsiz Ekspertiz",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. JSON-LD YAPILANDIRILMIŞ VERİ (Google için Kimlik Kartı) ---
# Bu kod Google'a senin bir "RealEstateAgent" (Emlak Danışmanı) olduğunu söyler.
st.markdown("""
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Selman Güneş Gayrimenkul",
  "image": "https://emlakcrm.github.io/emlak/img/about.jpg",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Kepez",
    "addressRegion": "Antalya",
    "addressCountry": "TR"
  },
  "description": "Antalya Kepez bölgesinde ücretsiz daire fiyat analizi ve gayrimenkul ekspertizi. Evim ne kadar eder sorusuna en doğru cevap.",
  "telephone": "+905355739260",
  "url": "https://emlakcrm.github.io/emlak/"
}
</script>
""", unsafe_allow_html=True)

# --- 3. CSS VE SEO DOSTU TASARIM ---
st.markdown(f"""
    <style>
        :root {{
            --main-dark: #1A4339;
            --main-light: #C4D8BF;
            --accent-color: #E7A44E;
            --bg-color: #f6f7fb;
        }}

        /* SEO Başlık Stili */
        .seo-h1 {{
            font-size: 32px;
            color: #fff;
            margin: 0;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        header {{
            background: linear-gradient(135deg, var(--main-dark) 0%, #2c5e52 100%);
            color: #fff;
            padding: 40px 0;
            text-align: center;
            border-radius: 0 0 30px 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        
        nav {{ margin-top: 20px; }}
        nav a {{
            color: var(--main-light) !important;
            margin: 0 18px;
            font-weight: 600;
            text-decoration: none !important;
            transition: 0.3s;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        nav a:hover {{
            color: var(--accent-color) !important;
            text-shadow: 0px 0px 15px rgba(231, 164, 78, 1);
        }}

        .stForm {{
            background: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 40px !important;
            box-shadow: 0 15px 35px rgba(0,0,0,0.05) !important;
        }}

        .footer {{
            background: var(--main-dark);
            color: #fff;
            text-align: center;
            padding: 50px;
            margin-top: 60px;
            border-radius: 40px 40px 0 0;
        }}

        /* Mobil Uyumluluk İyileştirmesi */
        @media (max-width: 768px) {{
            .seo-h1 {{ font-size: 24px; }}
        }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SEMANTİK HEADER (SEO Başlıkları) ---
st.markdown("""
    <header>
        <h1 class="seo-h1">Kepez Ücretsiz Ev Fiyat Analizi & Ekspertiz</h1>
        <p style="color:var(--main-light); font-size:18px; margin-top:10px;">
            Selman Güneş ile Antalya Gayrimenkul Pazarında Doğru Değerleme
        </p>
        <nav>
            <a href="https://emlakcrm.github.io/emlak/index.html">Ana Sayfa</a>
            <a href="https://emlakcrm.github.io/emlak/hakkimizda.html">Hakkımızda</a>
            <a href="https://emlakcrm.github.io/emlak/analiz.html">Fiyat Analizi</a>
            <a href="https://emlakcrm.github.io/emlak/iletisim.html">İletişim</a>
        </nav>
    </header>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. ANA İÇERİK (SOL FORM - SAĞ RESİM) ---
col_form, col_img = st.columns([6, 4], gap="large")

with col_form:
    st.markdown("## 🏘️ Dairenizin Değerini Hemen Öğrenin")
    st.write("Antalya Kepez'deki güncel emlak verilerini kullanarak mülkünüz için en gerçekçi fiyat aralığını hesaplıyoruz.")
    
    with st.form("seo_form"):
        c1, c2 = st.columns(2)
        with c1:
            # CSV dosyasındaki Mahalle sütununu SEO uyumlu hale getirmek için kullanıyoruz
            mahalle = st.selectbox("📍 Analiz Yapılacak Mahalle:", ["Varsak", "Güneş", "Sütçüler", "Gülveren", "Kültür", "Ahatlı"]) # Örnek mahalleler
            oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1"])
        with c2:
            m2 = st.number_input("📏 Net Kullanım Alanı (m²):", 30, 500, 100)
            kat = st.selectbox("🏢 Kat Durumu:", ["Giriş Kat", "Ara Kat", "En Üst Kat", "Dubleks"])
        
        st.markdown("<hr>", unsafe_allow_html=True)
        ad = st.text_input("Adınız Soyadınız:")
        tel = st.text_input("WhatsApp İletişim Numaranız:")
        
        # SEO için buton metnini güçlendirdik
        btn_wa = st.form_submit_button("ÜCRETSİZ ANALİZ RAPORU OLUŞTUR")

with col_img:
    st.markdown("### 👨‍💼 Kepez Bölge Uzmanı")
    # Resim Alt Text (SEO için çok önemli)
    st.image(
        "https://emlakcrm.github.io/emlak/img/about.jpg", 
        caption="Selman Güneş - Antalya Kepez Gayrimenkul Danışmanı", 
        use_container_width=True
    )
    
    # Güven Veren Bilgi Kutusu
    st.markdown(f"""
        <div style="background:#fff; padding:25px; border-radius:15px; border:1px solid #eee; border-left: 5px solid var(--accent-color);">
            <h4 style="margin-top:0; color:var(--main-dark);">Selman Güneş</h4>
            <p style="font-size:14px; color:#555;">
                Antalya Kepez bölgesinde <b>Varsak, Sütçüler ve Güneş</b> mahallelerinde uzmanlaşmış lisanslı gayrimenkul danışmanı. 
                Mülkünüzün doğru değerden satılması için <b>piyasa analizi</b> ve <b>stratejik pazarlama</b> desteği sağlar.
            </p>
            <p><b>📞 Tel:</b> {st.secrets.get('WHATSAPP_NUMARASI', '0535 573 92 60')}</p>
            <p><b>📍 Bölge:</b> Kepez / Antalya</p>
        </div>
    """, unsafe_allow_html=True)

# --- 6. SEO ODAKLI ALT METİN (Footer Öncesi) ---
st.markdown("""
<div style="text-align:center; padding: 40px 10%; background:#f0f2f6; border-radius: 20px; margin-top: 30px;">
    <h3>Neden Profesyonel Gayrimenkul Analizi?</h3>
    <p>Antalya emlak piyasası her gün değişiyor. <b>Kepez satılık daire</b> fiyatlarını etkileyen asansör durumu, bina yaşı ve cephe gibi 
    kriterleri uzman gözüyle değerlendiriyoruz. Yanlış fiyatla ilana çıkmak size zaman ve para kaybettirir. 
    <b>Selman Güneş</b> ile doğru fiyata, hızlı sonuca ulaşın.</p>
</div>
""", unsafe_allow_html=True)

# --- 7. FOOTER ---
st.markdown(f"""
    <div class="footer">
        <h3>Selman Güneş Gayrimenkul & Yatırım Danışmanlığı</h3>
        <p>Kepez Antalya Satılık Daire Fiyat Tahmini ve Ekspertiz Hizmetleri</p>
        <p style="font-size:12px; opacity:0.6;">© 2024 Selman Güneş. Tüm hakları saklıdır. Bu araç bir ön bilgilendirme servisidir.</p>
    </div>
    """, unsafe_allow_html=True)
