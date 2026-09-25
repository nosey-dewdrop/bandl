# bandl — şu an ne doğru?

## nerede kaldık — DEVRİ DAİM (25 Eyl 2026 gece)

**DÜŞÜLEN TUZAKLAR — yeni Claude buna düşme:**
- **Siteyi sen kodlamazsın.** Uygulamayı Lovable yapar; senin işin plan, mentorluk, veri, araştırma.
  Damla: "ben sana plan yap demiştim, web sitesi yap dememiştim."
- **Araştırmayı öldürme.** "yaptığın saçmalıkları sil" deyince araştırma ajanlarını durdurdum.
  Damla: "bunları araştırsana." "Sil" belirsizse önce neyi kastettiğini bul.
- **Resmî kaynağa önce git.** Damla: "bunun için daha çok abb incelemek iyiydi."
  ABB/EGO/meclis kararları haber sitelerinden önce gelir.
- **"Olmuyor" deme, veriyle dene.** Damla: "sınıflama için daha ileri gitmemiz lazım… denesene tekrar nasıl olmuyo."
  Kaba kural (v0 "metro geliyorsa değerlenebilir") veriyle test edilince çöktü.
- **İsim Damla'nın: bandl.** Ben "emsal"i önerdim, reddetti. İsim önerme, bandl'a anlam uydurma.
- **Ürünü haritaya küçültme.** Yeni yön (Damla, 25 Eyl): "maps + sahibinden + hürriyet emlak karışımı
  ama üstüne yatırım tavsiyeli, remax / fine estate gibi, ama 10-20m'a ev alabilecek insanlar için".
  Ayrıntı: PROJECT.md en üstteki "Sonraki ürün" bölümü.

**GİZLİLİK:**
- Repo private (github.com/nosey-dewdrop/bandl). Secret yok.
- `.gitignore`: rabadon oturum dosyaları, .DS_Store, __pycache__.
- ElevenLabs `sk_` anahtarı yalnızca Lovable secrets'ta durur, repoya girmez.
- Emlakjet/sahibinden/hepsiemlak otomatik kazıma yasak (kullanım koşulları).
- ABB ArcGIS'in kullanım koşulu yok. Toplu çekimden önce ABB'den yazılı izin.

**KOD DURUMU:**
- `data/build.py`: yalnızca stdlib. Seed verisi ve v1 kuralı burada; raylı hatları OSM API'sinden çeker.
- Çıktılar:
  - `ilceler.json`: 11 ilçe
  - `projeler.json`: 49 kaynaklı proje
  - `ilceler.geojson`: OSM poligonları
- Ölçülenler (11 ilçe, göreli değişim 2019→2026):
  - Kızılay'a uzaklık r=+0,85; bir ilçe çıkarılınca aralık +0,78 ile +0,91
  - bina yoğunluğu r=−0,85
  - yeni bina payı −0,27; başlangıç fiyatı −0,08: tutmadı
- Uygulama henüz yok.

**AÇIK İŞ (blokör):**
1. 26 Eyl GarajX, Lovable ile MVP.
   - Damla: Lovable Pro, Mapbox `pk.` token.
   - Ben: Lovable repo adı gelince `data/`yı oraya `src/data/` olarak push'larım.
2. "Sonraki ürün" spec'i. Blokörler PROJECT.md'de:
   - ilan kaynağı
   - yetki belgesi / yatırım tavsiyesi hukuku
   - mahalle fiyat geçmişi lisansı
3. Mahalle düzeyi "neden": ABB mahalle sınırı, bina yaşı, imar değişikliği katmanları hazır; fiyat serisi yok.

**KALICI KARARLAR:**
- Uydurma veri yok. Her sayı ve olay kaynak URL'li. Kaynak yoksa "kaynak bulunamadı" yazılır.
- Nominal TL ile sınıflama yok. Ölçü: ilçe m² fiyatının 11 ilçe medyanına oranı.
- Sınıflama v1 = yapı (uzaklık/yoğunluk) + Ankara emsalleri + kural. v0'ı geri getirme.
- Lovable mevcut repoyu içeri alamaz. Bu repo spec ve veriyi tutar, uygulama reposu ayrı.
- Tasarım referansı ir-globe'un editoryal dili (renkler PROJECT.md'de).
