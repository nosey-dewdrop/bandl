# bandl — şu an ne doğru?

## nerede kaldık — DEVRİ DAİM (26 Eyl 2026 gece; GarajX bugün 11:00)

**DÜŞÜLEN TUZAKLAR — yeni Claude buna düşme:**
- Siteyi sen kodlamazsın; uygulamayı Lovable yapar. Senin işin plan, mentorluk, veri, araştırma.
  Damla: "ben sana plan yap demiştim, web sitesi yap dememiştim."
- Araştırmayı öldürme. "saçmalıkları sil" deyince ajanları durdurdum; Damla: "bunları araştırsana."
- Resmî kaynağa önce git (ABB, EGO, meclis kararları). Damla: "daha çok abb incelemek iyiydi."
- "Olmuyor" deme, veriyle dene. Damla: "denesene tekrar nasıl olmuyo." v0 kuralı ("metro geliyorsa
  değerlenebilir") veriyle test edilince çöktü.
- İsim Damla'nın: bandl. "emsal"i önerdim, reddetti. İsim önerme, anlam uydurma.
- Araştırmayı yığın olarak verme; ürüne bağla, tasnife çevir. Damla: "sadece araştırma yığını mı var",
  "araştırmada kalmasını istemiyorum". MVP ilçe düzeyinde kalıyor; mahalle ve ilanlar etkinlikten sonra.
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
2. "Sonraki ürün": blokörler 25 Eyl gece araştırıldı (PROJECT.md "Blokörler: ne bulundu?", kaynaklar README'de).
   Damla karar verdi: komisyon yok, aracılık yok, "sadece ürün". Yetki belgesi ve ofis yok; ilan gelince EİDS. Plan: PROJECT.md "Plan: ürün ne, veri nereden?". Türkiye'de "Fine Estate" adlı şirket bulunamadı; tahminle bir şirkete bağlama.
2b. MVP'ye "neye göre" eklendi (26 Eyl gece): 13 güç, 11 ilçe, hüküm sayıdan (`build.py` GUC_HAM + guc_hukum);
   `ilceler.json`'da `gucler` ve `gelecek`. Lovable Prompt 2 buna göre güncel. Sınıf kuralı v1, değişmedi.
3. Premium aks: 18 mahalle için ABB bina yaşı, plan değişikliği, dönüşüm tablosu PROJECT.md'de. Mahalle fiyat serisi hâlâ yok
   (açık seri yok; Endeksa ya da REIDIN lisansı; TKGM Değer Bilgi Merkezi Ankara'ya 2027 ortası).

**KALICI KARARLAR:**
- bandl aracı değil, ürün: komisyon almaz (Damla, 25 Eyl 2026). Emlakçı yetki belgesi önerme.
- Uydurma veri yok. Her sayı kaynak URL'li; kaynak yoksa "kaynak bulunamadı".
- Nominal TL yok; ölçü ilçe m² fiyatının 11 ilçe medyanına oranı. v1 = yapı + Ankara emsalleri + kural; v0'ı geri getirme.
- Bu repo araştırma, spec ve veri. Uygulama: `nosey-dewdrop/bandl-app` (26 Eyl 2026, Damla: "repo aç, araştırmalar ayrı").
- Tasarım referansı ir-globe'un editoryal dili (PROJECT.md).
