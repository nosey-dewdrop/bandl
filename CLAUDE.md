# bandl — şu an ne doğru?

## nerede kaldık — DEVRİ DAİM (27 Eyl 2026; mahalle katmanı ve "sana göre" canlı)

**27 Eyl'de ne oldu:** Damla "yap" dedi, iki karar verdi: kapsam 11 ilçenin bütün mahalleleri; ilçenin değer sınıfı
"sana göre" sıralamasına girmez, yanında durur. ABB verisi için: "ticari kullanım yok, bilgi tasnifi sadece".
- Canlıda: 608 mahalle sınırı (yakınlık ≥12'de görünür), mahalle paneli (12 ölçü, medyan, kaynak), "sana göre" paneli
  (12 ölçüte +/−, ilk 10 liste, harita uyuma göre boyanır, seçim adreste `?p=okul,-sel` ve tarayıcıda kalır),
  ilçe panelinde "mahallelerine bak". Telefon (390 px) CDP emülasyonuyla ilk kez doğrulandı.
- **Düzeltme, canlıda yanlış yazıyordu:** "2018 sonrası bina payı +0,87 uzaklıktan bağımsız" hatalıydı. ABB'nin "2007 öncesi"
  kovası atlanmıştı (Çubuk'ta binaların %89'u). Düzeltilince +0,45, zayıf. Ayrıntı PROJECT.md "Okuma".
- Yeni güç: raylı istasyona uzaklık (bina ağırlıklı) r +0,90, uzaklıktan bağımsız; ama Kızılay'a uzaklıkla r 0,91 iç içe.
- `CLAUDE.md` canlıda herkese açıktı; `.vercelignore` eklendi, artık yalnızca `index.html` + `src/data/*.json|geojson` yayında.
- Ekran görüntüsü aracı: `node shot.mjs <url> <png> <w> <h> [mobil] [js]` (CDP; Chrome headless, 390 px emülasyon çalışıyor).
  Script bu oturumun scratchpad'indeydi; lazım olursa aynı yolla yeniden yazılır (Page.navigate + Emulation.setDeviceMetricsOverride).

**DÜŞÜLEN TUZAKLAR — yeni Claude buna düşme:**
- Damla konumlanmayı kararlaştırırken kod yazmaya atlama. 26 Eyl: "ui başlamadık", "hâlâ prensipleri
  kararlaştırma noktasındayız". Önce karar, sonra kod; kodu Damla "yap" deyince.
- Soru üstüne soru sorma. "Hayır, hangilerine uyuyor hangilerine uymuyor" dedi: liste istedi, anket değil.
- Damla'nın "kalsın" dediğini silme. "MVP Ankara; sonra Türkiye, sonra dünya" PROJECT.md'de kalıyor,
  sahnede söyleniyor. Ries'e aykırı, bilerek. Tekrar önüne koyma.
- Demo öncesi canlı siteye büyük değişiklik yok: "değiştirmeyelim, direkt bozabiliriz". Küçük, kanıtlı, tek tek.
- Lovable bitti. 26 Eyl'de 2 saat gitti: Mapbox beyaz ekran, GitHub Connect basılmadı, veri girmedi.
  Damla: "sen yapabilirsen sen yap". Uygulamayı ben yazıyorum. Lovable promptu üretme.
- Araç talimatını tek tek ver, uzun teknik prompt yapıştırtma: "lovable bu terminal değil, tek tek söyle".
- Kanıt: WebGL (MapLibre/Mapbox) headless Chrome'da çizilmiyor, ekran görüntüsüyle doğrulanamıyor.
  Bu yüzden Leaflet (SVG). Değiştirme; her deploy sonrası canlı adresten headless ekran görüntüsü al.
- Eski tuzaklar geçerli: isim önerme (bandl, League of Legends Bandle City'den), uydurma veri yok,
  araştırmayı ürüne bağla, resmî kaynağa (ABB, EGO, meclis) önce git, "olmuyor" deme veriyle dene.

**KONUMLANMA (kilitli, `2609-konumlanma.md`):** kelime "neden", karşıda emlakçı (Endeksa anılmaz),
kategori "Ankara'nın değer haritası", dürüstlük cümlesi Damla'nın: "Paranı nereye yatırman stratejik bir
karar. İstatistiksel bak." Hüküm dili ihtimal, kesin değil. İlan/aracılık/komisyon yok. Ücretsiz.

**GİZLİLİK:**
- İki repo, ikisi private: `nosey-dewdrop/bandl` (araştırma, spec, veri üretimi), `nosey-dewdrop/bandl-app` (uygulama).
- Secret yok. Mapbox kullanılmıyor. Veri gist'i herkese açık (kaynaklı kamu verisi): gist.github.com/nosey-dewdrop/ea413beb0ef06d30a3e41e0d5d69226a
- Emlakjet, sahibinden, hepsiemlak kazıma yasak. ABB ArcGIS toplu çekimden önce yazılı izin.

**KOD DURUMU:**
- Sıra: `python3 data/mahalle.py && python3 data/build.py` (stdlib). `mahalle.py` ABB + OSM'den 608 mahalleyi çeker
  (`data/ham/` önbellek, `--cek` yeniler), `mahalleler.json|geojson` yazar. `build.py` 14 güç + v1 kuralı, `ilceler.json`, `projeler.json`;
  durağa uzaklığı `mahalleler.json`'dan okur. Kopya: `cp bandl/data/*.json bandl/data/*.geojson bandl-app/src/data/`.
- `bandl-app/index.html`: tek dosya, Leaflet 1.9.4 + OSM karo, ilçe boyası, proje katmanı (40 geometri),
  sağ panel (ilçe `#kecioren` ya da mahalle `#cankaya-cayyolu`), sol "sana göre" paneli. Mahalle dosyaları ilk gerektiğinde yüklenir.
- Canlı: https://bandl.noseydewdrop.com (Vercel proje `bandl-app`; `cd bandl-app && vercel deploy --prod --yes`).
- Ölçülenler (11 ilçe, 2019→2026 göreli): Kızılay'a uzaklık r=+0,85 (ana); durağa uzaklık +0,90 (bağımsız, ama uzaklıkla iç içe);
  2018 sonrası bina payı +0,45 (zayıf; 27 Eyl düzeltmesi).
  Tablo PROJECT.md "Nasıl sınıflıyor?".

**AÇIK İŞ — Damla'nın 26 Eyl yönü:** "daha çok veri çeksin, mahalle düzeyine insin, özelleştirilebilsin, +/- onun önceliklerine göre semt önersin."
1. ✅ Mahalle düzeyi ve ✅ +/- öncelik sıralaması (27 Eyl). Mahalle fiyat serisi hâlâ yok (Endeksa 2020+ lisans; REIDIN ücretli;
   TKGM Ankara 2027 ortası); bu yüzden mahalleye sınıf yok, ölçülerin fiyatla ilişkisi mahalle düzeyinde ölçülmedi.
2. Daha çok veri: ✅ durağa uzaklık. Kalan adaylar: kurum giriş/çıkış mahalle düzeyi, ABB jeolojik etüt (katman çoğu yerde boş),
   OSM'de eksik okul/park (resmî MEB listesi aranmadı). Her yeni güç aynı hüküm kuralından geçer.
3. Bütçe süzgeci (10–20 mn TL) yapılamıyor: mahalle m² fiyatı yalnızca PROJECT.md'deki 9 mahallede var ve Emlakjet kaynaklı.
4. Zihne giriş aracı ertelendi; kanal Ankara yerel basını.
5. Veri gist'i (Lovable için) güncellenmedi, eski +0,87 hükmünü taşıyor; Lovable bittiği için kullanılmıyor.

**KALICI KARARLAR:**
- bandl aracı değil, ürün: komisyon yok (25 Eyl). Yetki belgesi önerme.
- Uydurma veri yok; her sayı kaynak URL'li, yoksa "kaynak bulunamadı".
- Nominal TL yok; ölçü 11 ilçe medyanına oran. v1 = yapı + Ankara emsalleri + kural; v0 geri gelmez.
- Uygulama tek dosya, Leaflet, Vercel. Tasarım: beyaz zemin, #16191f, tek aksan #17356b, serif başlık, sans gövde,
  sınıf renkleri #2b5cad / #8a94a3 / #c8602a, kutu ve çizgi yok. Karo renkli (Damla 26 Eyl: "daha güzel görünüyor").
- Bu repo araştırma, spec ve veri; uygulama `bandl-app`.
- Mahalleye değer sınıfı verilmez (fiyat serisi yok); "sana göre" yalnızca kullanıcının +/- seçimine göre sıralar, "yatırım tavsiyesi değildir".
- ABB verisi: ticari kullanım yok, bilgi tasnifi (Damla, 27 Eyl).
