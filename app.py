import streamlit as st
from src.rag_engine import AlesRagEngine

# Sayfa ayarları
st.set_page_config(page_title="ALES Çıkmış Soru Bulucu", layout="wide")

st.title("🔎 ALES Scope Checker")
st.markdown("Soruyu yaz, daha önce çıkmış mı kontrol edelim.")

# Yan menü (Sidebar)
with st.sidebar:
    st.header("Veritabanı Durumu")
    if st.button("Veritabanını Sıfırla"):
        engine = AlesRagEngine()
        engine.reset_db()
        st.warning("Veritabanı silindi! Tekrar yükleme yapmalısın.")


# Ana Motoru Başlat (Cache kullanarak her seferinde tekrar yüklemesini engelliyoruz)
@st.cache_resource
def get_engine():
    return AlesRagEngine()


engine = get_engine()

# Kullanıcıdan veri alma
query = st.text_area("Soru metnini veya bir kısmını buraya yapıştır:", height=150)
search_btn = st.button("Soruyu Tara")

if search_btn and query:
    with st.spinner('Geçmiş sınavlar taranıyor...'):
        results = engine.search_question(query, k=3)

    st.subheader("Bulunan Benzer Sorular:")

    for i, res in enumerate(results):
        score_display = round(res['skor'], 4)

        # --- YENİ PUANLAMA MANTIĞI ---
        # Cosine Distance: 0 = Birebir Aynı, 1 = Tamamen Farklı
        # Genelde 0.3'ün altı "Oldukça Benzer" demektir.

        match_status = "Bilinmiyor"
        match_color = "grey"

        if res['skor'] < 0.20:
            match_status = "🔥 Birebir / Çok Yüksek Benzerlik"
            match_color = "green"
        elif res['skor'] < 0.40:
            match_status = "⚡ Benzer İçerik / Aynı Konu"
            match_color = "orange"
        else:
            match_status = "Benzerlik Düşük"
            match_color = "red"

        with st.expander(f"Sonuç {i + 1} ({match_status}) - Skor: {score_display}"):
            st.info(f"📄 Kaynak: {res['kaynak']} | Sayfa: {res['sayfa'] + 1}")
            st.write(res['icerik'])

            if res['skor'] < 0.40:
                st.success(f"Bu soru veritabanında bulundu! ({match_status})")
            else:
                st.error("Bu soru pek benzemiyor, emin değilim.")