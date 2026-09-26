# bandl — şu an ne doğru?

## nerede kaldık — DEVRİ DAİM (26 Eyl 2026, 15:00; GarajX demosu yapıldı)

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
- `bandl/data/build.py` (stdlib): seed + v1 kuralı + 13 güç; çıktılar `ilceler.json`, `projeler.json`, `ilceler.geojson`.
  Çıktılar `bandl-app/src/data/` altına kopyalanır (elle: `cp bandl/data/*.json* bandl-app/src/data/`).
- `bandl-app/index.html`: tek dosya, Leaflet 1.9.4 + OSM karo, ilçe boyası, proje katmanı (40 geometri),
  sağ panel (sınıf, neden, güçler, gelecek, geçmiş, kaynak linkleri), ilçe linki `#kecioren`.
- Canlı: https://bandl.noseydewdrop.com (Vercel proje `bandl-app`; `cd bandl-app && vercel deploy --prod --yes`).
- Ölçülenler (11 ilçe, 2019→2026 göreli): Kızılay'a uzaklık r=+0,85; 2018 sonrası bina payı +0,87 (uzaklıktan bağımsız +0,66).
  Tablo PROJECT.md "Nasıl sınıflıyor?".

**AÇIK İŞ — Damla'nın 26 Eyl 15:00 yönü:** "daha çok veri çeksin, mahalle düzeyine insin, özelleştirilebilsin,
+/- onun önceliklerine göre semt önersin."
1. Mahalle düzeyi. Blokör: mahalle fiyat serisi yok (Endeksa 2020+, lisans; REIDIN 2007+, ücretli; TKGM Ankara 2027 ortası).
   Fiyatsız yapılabilen: 18 premium mahallenin ABB verisi (bina yaşı, plan değişikliği, dönüşüm, plan adası emsal) zaten çekildi,
   PROJECT.md "Premium aks". Önce bunu haritaya taşımak fiyat lisansı beklemez.
2. Daha çok veri. Adaylar PROJECT.md "Güçler" tablosunda: durağa mesafe (hesaplanmadı), kurum giriş/çıkış mahalle düzeyi,
   ABB jeolojik etüt (katman çoğu yerde boş). Her yeni güç aynı hüküm kuralından geçer (r, tek ilçe çıkarma, uzaklık sabit).
3. Özelleştirme: kullanıcı önceliklerini seçer (metro, yeni yapı, merkeze yakınlık, sel riski, okul...), güçler ağırlıklanır,
   ilçe/mahalle sıralaması buna göre değişir, "sana göre" listesi çıkar. Tasarım kararı Damla'nın; önce kâğıt üstünde ne
   sorulacağı, sonra kod. Hukuk: "sana şu semti öneriyoruz" reklam iddiasıdır; kaynaklı ve "yatırım tavsiyesi değildir" ile.
4. Zihne giriş aracı (Ries "zihin") ertelendi; kanal Ankara yerel basını.
5. Telefonda gerçek görünüm DOĞRULANMADI (headless 390 px'e inmiyor). Damla'dan bir bakış yeter.

**KALICI KARARLAR:**
- bandl aracı değil, ürün: komisyon yok (25 Eyl). Yetki belgesi önerme.
- Uydurma veri yok; her sayı kaynak URL'li, yoksa "kaynak bulunamadı".
- Nominal TL yok; ölçü 11 ilçe medyanına oran. v1 = yapı + Ankara emsalleri + kural; v0 geri gelmez.
- Uygulama tek dosya, Leaflet, Vercel. Tasarım: beyaz zemin, #16191f, tek aksan #17356b, serif başlık, sans gövde,
  sınıf renkleri #2b5cad / #8a94a3 / #c8602a, kutu ve çizgi yok. Karo renkli (Damla 26 Eyl: "daha güzel görünüyor").
- Bu repo araştırma, spec ve veri; uygulama `bandl-app`.
