# import os
# from langchain_community.document_loaders import PyPDFLoader
# from src.rag_engine import AlesRagEngine
#
# # PDF'lerin olduğu klasör
# PDF_FOLDER_PATH = "./data/raw_pdfs"
#
#
# def ingest_pdfs():
#     # 1. Motoru başlat
#     engine = AlesRagEngine()
#
#     # 2. Klasördeki tüm PDF'leri bul
#     if not os.path.exists(PDF_FOLDER_PATH):
#         os.makedirs(PDF_FOLDER_PATH)
#         print("Uyarı: PDF klasörü yoktu, oluşturuldu. İçine dosya atın.")
#         return
#
#     pdf_files = [f for f in os.listdir(PDF_FOLDER_PATH) if f.endswith('.pdf')]
#
#     if not pdf_files:
#         print("❌ Klasörde hiç PDF bulunamadı!")
#         return
#
#     all_documents = []
#
#     # 3. Her PDF'i oku
#     for pdf_file in pdf_files:
#         file_path = os.path.join(PDF_FOLDER_PATH, pdf_file)
#         print(f"📖 Okunuyor: {pdf_file}")
#
#         loader = PyPDFLoader(file_path)
#         pages = loader.load()
#
#         # Metadata'ya yıl vs eklenebilir, şimdilik dosya adını kaynak yapalım
#         for page in pages:
#             page.metadata["source"] = pdf_file
#
#         all_documents.extend(pages)
#
#     # 4. Veritabanına kaydet
#     if all_documents:
#         engine.add_documents(all_documents)
#         print(f"🎉 İşlem tamam! Toplam {len(all_documents)} sayfa işlendi.")
#
#
# if __name__ == "__main__":
#     # Bu dosya direkt çalıştırılırsa yüklemeyi yap
#     ingest_pdfs()


import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  # YENİ EKLENEN
from src.rag_engine import AlesRagEngine

PDF_FOLDER_PATH = "./data/raw_pdfs"


def ingest_pdfs():
    # Veritabanını temiz bir başlangıç için sıfırlayalım mı?
    # Eğer üzerine ekleme yapmak istiyorsan burayı yorum satırı yap.
    engine = AlesRagEngine()

    if not os.path.exists(PDF_FOLDER_PATH):
        os.makedirs(PDF_FOLDER_PATH)
        print("Uyarı: PDF klasörü yoktu, oluşturuldu.")
        return

    pdf_files = [f for f in os.listdir(PDF_FOLDER_PATH) if f.endswith('.pdf')]

    if not pdf_files:
        print("❌ Klasörde hiç PDF bulunamadı!")
        return

    all_splits = []

    # --- PARÇALAMA AYARLARI ---
    # chunk_size=600: Her parça ortalama 600 karakter olsun (yaklaşık 1 soru uzunluğu)
    # chunk_overlap=100: Parçalar birbirinin ucundan 100 karakter tekrar etsin (cümle bölünürse anlam kopmasın)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]  # Önce paragraflardan bölmeye çalışır
    )

    for pdf_file in pdf_files:
        file_path = os.path.join(PDF_FOLDER_PATH, pdf_file)
        print(f"📖 Okunuyor: {pdf_file}")

        loader = PyPDFLoader(file_path)
        pages = loader.load()

        # Sayfaları parçalara ayırıyoruz
        splits = text_splitter.split_documents(pages)

        # Her parçaya kaynak bilgisini ekleyelim
        for split in splits:
            split.metadata["source"] = pdf_file
            # split.metadata["page"] zaten PyPDFLoader tarafından ekleniyor

        all_splits.extend(splits)
        print(f"   > {len(pages)} sayfa -> {len(splits)} küçük parçaya bölündü.")

    # Veritabanına kaydet
    if all_splits:
        print(f"💾 Toplam {len(all_splits)} parça vektör veritabanına yazılıyor...")
        engine.add_documents(all_splits)
        print("🎉 İşlem tamam!")


if __name__ == "__main__":
    ingest_pdfs()