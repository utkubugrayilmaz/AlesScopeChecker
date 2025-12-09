import os
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


def test_gemini():
    print("--- Google Gemini (AI Studio) Testi Başlıyor ---")
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("❌ HATA: GOOGLE_API_KEY .env dosyasında bulunamadı!")
        return

    try:
        genai.configure(api_key=api_key)
        # Gemini 1.5 Flash modelini kullanıyoruz (Hızlı ve Free Tier dostu)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Bana sadece 'Gemini Bağlantısı Başarılı' yaz.")
        print(f"✅ BAŞARILI: {response.text.strip()}")
    except Exception as e:
        print(f"❌ HATA: Gemini bağlantısı başarısız. Hata kodu:\n{e}")


def test_groq():
    print("\n--- Groq (Llama 3) Testi Başlıyor ---")
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("❌ HATA: GROQ_API_KEY .env dosyasında bulunamadı!")
        return

    try:
        client = Groq(api_key=api_key)
        # Llama 3.3 70B modelini deniyoruz (Şu an en popüleri)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Bana sadece 'Groq Bağlantısı Başarılı' yaz."
                }
            ],
            temperature=0.5,
            max_tokens=50,
            top_p=1,
            stream=False,
            stop=None,
        )
        print(f"✅ BAŞARILI: {completion.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ HATA: Groq bağlantısı başarısız. Hata kodu:\n{e}")


if __name__ == "__main__":
    test_gemini()
    test_groq()