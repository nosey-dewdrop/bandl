# bandl — şu an ne doğru?

## nerede kaldık — DEVRİ DAİM (25 Eyl 2026 gece)

**DÜŞÜLEN TUZAKLAR — yeni Claude buna düşme:**
- Siteyi sen kodlamazsın; uygulamayı Lovable yapar. Senin işin plan, mentorluk, veri, araştırma.
  Damla: "ben sana plan yap demiştim, web sitesi yap dememiştim."
- Araştırmayı öldürme. "saçmalıkları sil" deyince ajanları durdurdum; Damla: "bunları araştırsana."
- Resmî kaynağa önce git (ABB, EGO, meclis kararları). Damla: "daha çok abb incelemek iyiydi."
- "Olmuyor" deme, veriyle dene. Damla: "denesene tekrar nasıl olmuyo." v0 kuralı ("metro geliyorsa
  değerlenebilir") veriyle test edilince çöktü.
- İsim Damla'nın: bandl. "emsal"i önerdim, reddetti. İsim önerme, anlam uydurma.
- Ürünü haritaya küçültme. Yeni yön: "maps + sahibinden + hürriyet emlak karışımı ama üstüne yatırım
  tavsiyeli, remax / fine estate gibi, ama 10-20m'a ev alabilecek insanlar için". Ayrıntı: PROJECT.md "Sonraki ürün".

**GİZLİLİK:**
- Repo private (nosey-dewdrop/bandl), secret yok. `.gitignore`: rabadon oturum dosyaları, .DS_Store, __pycache__.
- ElevenLabs `sk_` anahtarı yalnızca Lovable secrets'ta durur.
- Emlakjet, sahibinden ve hepsiemlak otomatik kazımayı yasaklıyor.
- ABB ArcGIS'in kullanım koşulu yok; toplu çekimden önce ABB'den yazılı izin.

**KOD DURUMU:**
- `data/build.py`: stdlib. Seed ve v1 kuralı burada; hatları OSM API'sinden çeker.
- Çıktılar: `ilceler.json` (11), `projeler.json` (49 kaynaklı), `ilceler.geojson` (OSM).
- Ölçülenler (11 ilçe, 2019→2026 göreli değişim):
  - Kızılay'a uzaklık r=+0,85 (bir ilçe çıkarılınca +0,78 ile +0,91)
  - yoğunluk r=−0,85
  - yeni bina payı −0,27 ve başlangıç fiyatı −0,08: tutmadı
- Uygulama henüz yok.

**AÇIK İŞ (blokör):**
1. 26 Eyl GarajX MVP. Damla: Lovable Pro, Mapbox `pk.` token. Ben: Lovable repo adı gelince `data/` → `src/data/`.
2. "Sonraki ürün" spec'i. Blokörler: ilan kaynağı, yetki belgesi ve tavsiye hukuku, mahalle fiyat lisansı (PROJECT.md).
3. Premium aksta mahalle düzeyi "neden". ABB katmanları (mahalle, bina yaşı, imar değişikliği) hazır; fiyat serisi yok.

**KALICI KARARLAR:**
- Uydurma veri yok. Her sayı kaynak URL'li; kaynak yoksa "kaynak bulunamadı".
- Nominal TL yok; ölçü ilçe m² fiyatının 11 ilçe medyanına oranı. v1 = yapı + Ankara emsalleri + kural; v0'ı geri getirme.
- Lovable mevcut repoyu içeri alamaz: bu repo spec ve veriyi tutar, uygulama reposu ayrı.
- Tasarım referansı ir-globe'un editoryal dili (PROJECT.md).
