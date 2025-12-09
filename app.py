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
        # Benzerlik skoru (Distance ne kadar küçükse o kadar iyi)
        # Chroma varsayılan L2 distance kullanır. 0 = birebir aynı. 1 üzeri = alakasız.
        score_display = round(res['skor'], 4)

        with st.expander(f"Sonuç {i + 1} (Benzerlik Skoru: {score_display}) - Kaynak: {res['kaynak']}"):
            st.info(f"📄 Sayfa: {res['sayfa'] + 1}")
            st.write(res['icerik'])

            if res['skor'] < 0.2:
                st.success("🔥 Bu soru çok yüksek ihtimalle çıkmış!")
            elif res['skor'] < 0.5:
                st.warning("⚡ Benzer bir soru olabilir.")
            else:
                st.error("Bu soru pek benzemiyor.")
