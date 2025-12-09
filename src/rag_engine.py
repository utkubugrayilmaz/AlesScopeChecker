# import os
# import shutil
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.documents import Document # Bu satır güncellendi
#
# # Veritabanının ve modelin ayarları
# VECTOR_DB_PATH = "./data/vectordb"
# # Türkçe performansı iyi, ücretsiz ve hafif bir model:
# EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
#
#
# class AlesRagEngine:
#     def __init__(self):
#         # 1. Metni sayılara çeviren model (Embeddings)
#         print("🧠 Model yükleniyor (ilk seferde biraz sürebilir)...")
#         self.embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#
#         # 2. Vektör Veritabanı bağlantısı (ChromaDB)
#         self.db = Chroma(
#             persist_directory=VECTOR_DB_PATH,
#             embedding_function=self.embedding_function,
#             collection_name="ales_questions"
#         )
#         print(f"📂 Veritabanı bağlandı: {VECTOR_DB_PATH}")
#
#     def add_documents(self, documents):
#         """
#         PDF'ten okunan verileri veritabanına ekler.
#         documents: List[Document] formatında olmalı.
#         """
#         if not documents:
#             return "Eklenecek veri yok."
#
#         print(f"🔄 {len(documents)} adet parça veritabanına ekleniyor...")
#         self.db.add_documents(documents)
#         return "✅ Başarıyla eklendi!"
#
#     def search_question(self, query_text, k=3):
#         """
#         Soru metnini alır, veritabanındaki en benzer soruları getirir.
#         k: Kaç tane benzer sonuç getirilsin?
#         """
#         print(f"🔎 Aranıyor: {query_text}")
#
#         # similarity_search_with_score bize benzerlik skorunu da verir
#         results = self.db.similarity_search_with_score(query_text, k=k)
#
#         formatted_results = []
#         for doc, score in results:
#             # ChromaDB'de skor mesafe (distance) cinsindendir.
#             # 0'a ne kadar yakınsa o kadar benzerdir.
#             formatted_results.append({
#                 "icerik": doc.page_content,
#                 "kaynak": doc.metadata.get("source", "Bilinmiyor"),
#                 "sayfa": doc.metadata.get("page", 0),
#                 "skor": score
#             })
#
#         return formatted_results
#
#     def reset_db(self):
#         """Geliştirme aşamasında veritabanını sıfırlamak için"""
#         if os.path.exists(VECTOR_DB_PATH):
#             shutil.rmtree(VECTOR_DB_PATH)
#             print("🗑️ Veritabanı silindi.")

import os
import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document # Bu satır güncellendi

VECTOR_DB_PATH = "./data/vectordb"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class AlesRagEngine:
    def __init__(self):
        print("🧠 Model hazırlanıyor...")
        # encode_kwargs={'normalize_embeddings': True} ekleyerek vektörleri normalize ediyoruz
        self.embedding_function = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            encode_kwargs={'normalize_embeddings': True}
        )

        # collection_metadata={"hnsw:space": "cosine"} ekleyerek
        # Skoru 0 ile 1 arasına sabitliyoruz. (0: Aynı, 1: Alakasız)
        self.db = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=self.embedding_function,
            collection_name="ales_questions",
            collection_metadata={"hnsw:space": "cosine"}
        )
        print(f"📂 Veritabanı bağlandı: {VECTOR_DB_PATH}")

    def add_documents(self, documents):
        if not documents:
            return
        print(f"🔄 {len(documents)} parça veritabanına ekleniyor...")
        self.db.add_documents(documents)

    def search_question(self, query_text, k=3):
        print(f"🔎 Aranıyor: {query_text}")
        results = self.db.similarity_search_with_score(query_text, k=k)

        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "icerik": doc.page_content,
                "kaynak": doc.metadata.get("source", "Bilinmiyor"),
                "sayfa": doc.metadata.get("page", 0),
                "skor": score
            })

        return formatted_results

    def reset_db(self):
        if os.path.exists(VECTOR_DB_PATH):
            shutil.rmtree(VECTOR_DB_PATH)
            print("🗑️ Veritabanı silindi.")