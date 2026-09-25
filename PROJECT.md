# bandl

Ankara'nın ilçelerini **değerlenebilir / değer korur / değeri düşer** diye sınıflayan
ve bu sınıfın nedenini, haritada gösterilen projelere ve tarihte olanlara kaynaklı olarak
bağlayan harita. MVP Ankara; sonra Türkiye, sonra dünya.

Yapım: Lovable. İlk sahne: 26 Eyl 2026, GarajX "Ship in Ankara".

---

## Neden var?

Ankara'da ev alan biri "bu semt değer kazanır mı?" sorusunu bugün emlakçının sözü ve
ilan fiyatlarıyla cevaplıyor.

**Rakip gerçeği (bunu bilmeden pitch yapma):** Endeksa (Şubat 2026'dan beri Emlakjet'in
parçası) zaten şunları veriyor:
- mahalle düzeyinde fiyat
- nominal/reel geçiş
- ilçe "yatırım skoru"
- 1 yıllık fiyat beklentisi
- iki yapay zekâ asistanı

Yani **sadece "3 sınıfa ayırmak" fark değil**; Endeksa'nın skoru bunu yapıyor.

**Boşluk:** hiçbir ürün fiyatın **neden** oynadığını (metro, hastane, dönüşüm, imar,
kurum taşınması) fiyat serisine bağlayıp kaynağıyla göstermiyor. Endeksa'nın skoru
kapalı kutu. bandl'ın farkı = **neden katmanı**: her sınıfın yanında hangi projenin,
hangi tarihte, hangi kaynağa göre olduğu.

## Ne yapıyor?

1. **Harita:** Ankara ilçeleri 3 renkte.
2. **Proje katmanı:** raylı sistem (açık / yapımda / planlı), şehir hastanesi, AVM,
   kentsel dönüşüm, imar kararı. Her birinde tarih, durum ve kaynak linki var.
3. **İlçe paneli** (tıklayınca, sağda):
   - sınıf ve tek paragraf neden
   - Ankara medyanına göre fiyat (2019 → 2020 → 2026)
   - olay zaman çizelgesi (ne oldu, ne zaman, kaynak)
4. **Haber listesi:** "bu ilçede yeni proje ya da değişiklik olursa haber ver". Yalnızca
   e-posta ve ilçe seçimi alınır. Üyelik yok.
5. **(zaman kalırsa) dinle:** ilçenin hikâyesini ElevenLabs sesli okur.

Kapsam dışı (MVP): üyelik, ödeme, canlı veri çekme, ML modeli, mahalle poligonları,
Türkiye geneli.

## Nasıl sınıflıyor?

**Nominal TL kullanılmaz.** Ankara'da fiyatlar bir yılda %28 arttı, reel olarak ise
yaklaşık %3 düştü. Ölçü: ilçenin m² fiyatının, veri olan 11 ilçenin medyanına oranı
(göreli fiyat).

Sınıf üç adımda verilir: önce şehri ne sürüklüyor (yapı), sonra projeler bunun üstüne
ne eklemiş (emsal), en son kural.

### 1. Yapı: Ankara'yı ne sürüklüyor?

Test edildi (11 ilçe, göreli değişim 2019 → 2026):

| Açıklama | r | Sonuç |
|---|---|---|
| Kızılay'a uzaklık (ilçenin orta noktası) | **+0,85** | güçlü |
| Bina yoğunluğu (bina/km², log; ABB deprem verisi) | **−0,85** | güçlü, uzaklığın aynası |
| Yeni bina payı (2007 ve 2018 yönetmeliği) | −0,27 | tutmadı |
| 2019'daki başlangıç fiyatı | −0,08 | tutmadı |

- **Sağlamlık:**
  - Hangi ilçe çıkarılırsa çıkarılsın r +0,78 ile +0,91 arasında kalıyor.
  - İki dönemde de var: 2019→2020 +0,63, 2020→2026 +0,79.
  - Ham gidişin kendisi daha zayıf sürüyor: 2019–20 gidişi ile 2020–26 gidişi arasında r = 0,44.
- **Eğim:** Kızılay'dan her 10 km uzaklık, göreli fiyata yaklaşık +10 puan.
- **Sonuç:** son 7 yılda Ankara'da değeri belirleyen ana güç tek tek projeler değil,
  **merkezden seyrek çevreye kayış**.

### 2. Emsal: projeler bunun üstüne ne eklemiş?

Uzaklığın beklediği değişim çıkarılınca kalan fark:

| İlçe | Gerçek | Beklenen | Fark | O dönemde ne oldu? |
|---|---|---|---|---|
| Çankaya | +12 | −1 | **+12** | Bilkent Şehir Hastanesi açıldı (2019) |
| Akyurt | +28 | +20 | +8 | kaynaklı olay yok |
| Etimesgut | +14 | +9 | +5 | — |
| Yenimahalle | +4 | +2 | +2 | Etlik Şehir Hastanesi açıldı (2022) |
| Çubuk | +36 | +34 | +2 | — |
| Gölbaşı | +30 | +27 | +3 | İncek imarı iptal (2017) |
| Mamak | 0 | +3 | −3 | Yeni Mamak dönüşümü sürüyor |
| Keçiören | −1 | +3 | **−4** | **M4 Kızılay'a bağlandı (2023)** |
| Pursaklar | +3 | +8 | −5 | — |
| Altındağ | −7 | +1 | **−8** | **Numune (2019) ve Dışkapı (2022) hastaneleri taşındı** |
| Sincan | +10 | +23 | **−13** | kaynak bulunamadı |

**Ankara'nın kendi emsalleri:**
- **Metro yoğun merkez ilçeyi tek başına çevirmedi.** Keçiören'in hattı 2023'te Kızılay'a
  bağlandı, ilçe beklenenin altında kaldı.
  - Bu, v0 kuralının ("metro geliyorsa değerlenebilir") tersini söylüyor. v0 bu yüzden bırakıldı.
- **Büyük kurum çıkışı eksi yazıyor.** Altındağ, iki hastanesini kaybettiği dönemde en çok geride kalan merkez ilçe.
- **Şehir hastanesi açılışı** bir yerde büyük (Çankaya +12), bir yerde küçük (Yenimahalle +2) farkla örtüşüyor.
- **Bunlar örtüşme, kanıtlanmış neden değil.** 11 ilçe ve 3 fiyat noktası nedensellik kurmaya yetmez.
- **Metro ve istasyonun asıl etkisi mahalle düzeyinde olmalı** (durağa ~1 km). Mahalle fiyat geçmişi elimizde yok.

### 3. Kural (v1, sırayla)

1. **değeri düşer:** yoğun merkez ilçesi (≥150 bina/km²) **ve** göreli fiyatı 2019'dan beri artmamış.
2. **değerlenebilir:** çevre ilçesi (Kızılay'a ≥30 km) **ve** göreli fiyatı artmış **ve** arz fazlası uyarısı yok.
3. **değer korur:** geri kalan her şey.

Eşikler 11 ilçenin doğal kırılımlarından seçildi:
- uzaklık: 16 → 21 → 33 km
- yoğunluk: 93 → 143 → 197 bina/km²

**v1 sonucu:**

| Sınıf | İlçeler |
|---|---|
| değerlenebilir | Çubuk, Akyurt, Sincan |
| değer korur | Çankaya, Gölbaşı (arz fazlası uyarısı), Etimesgut, Yenimahalle, Pursaklar, Mamak |
| değeri düşer | Keçiören, Altındağ |

Pursaklar ve Mamak'ta metro geliyor, ama Keçiören emsali yüzünden "değer korur" kalıyorlar.
Panel bunu açıkça yazar: etki durak çevresindeki mahallelerde aranmalı.

**Bu sınıflamanın zayıf yerleri:**
- 11 ilçe ve 3 fiyat noktası var. Korelasyon neden değil.
- **Endeksa ilan tabanlı.** Çevrede yeni ve lüks site ilanları çoğaldıkça ortalama m² fiyatı
  karışım yüzünden de yükselebilir. Bunu ayırmak için karışımdan arındırılmış bir seri gerek;
  TCMB'ninki var ama yalnızca il düzeyinde.
- **Gidişin süreceği varsayılıyor.** Pandemi (2020–21) ve deprem (Şubat 2023) sonrası çevre
  talebi kalıcı olmayabilir. Ankara'da Mayıs 2026'da satışlar %33 düştü.
- **Sincan** çevre ilçesi ama beklenenin 13 puan altında, nedeni bulunamadı. "Değerlenebilir"
  sınıfının en zayıf üyesi.

**Sıradaki adım (etkinlikten sonra):**
- Durak ve proje etkisini görmek için mahalle düzeyine inmek gerekiyor.
- ABB verisi hazır: mahalle sınırları, mahalle başına bina yaşı, imar değişiklikleri.
- Eksik olan mahalle fiyat geçmişi: Endeksa ya da REIDIN lisansı.

## Veri nereden?

| Veri | Kaynak | Düzey | Durum |
|---|---|---|---|
| m² fiyatı 2019, 2020 | Endeksa, [Baret tablosu](https://www.baretdergisi.com/ankarada-konut-fiyatlari-2020-yilinin-ilk-6-ayinda-yuzde-799-artti/20007/) | ilçe | ücretsiz, yayımlanmış |
| m² fiyatı Ağu 2026 | Endeksa, [Emlakjet sayfaları](https://www.emlakjet.com/emlak-piyasasi/satilik-konut/ankara) | ilçe, mahalle | görünür, kazıma yasak |
| Ankara reel değişim | [TCMB KFE](https://www.tcmb.gov.tr/wps/wcm/connect/8bbac42a-c854-4c58-8b0c-e7e55c35ec2d/KFE.pdf?MOD=AJPERES), BETAM | il | ücretsiz |
| Satış adedi | TÜİK, ilçe düzeyi (yerel basın) | ilçe | ücretsiz, likidite sinyali |
| İlçe sınırları | OpenStreetMap | ilçe | ODbL, atıf şart |
| Projeler | EGO, ABB, Wikipedia, haber | nokta, hat | ücretsiz, satır satır kaynaklı |
| İmar değişiklikleri, emsal/KAKS, dönüşüm alanları, deprem dönemi bina stoku | ABB ArcGIS sunucusu (README'de ABB bölümü) | imar adası, mahalle | anonim erişim, kullanım koşulu yok. Toplu çekimden önce ABB'den yazılı izin. | MVP'de yok; etkinlikten sonraki ilk katman |

**Lisans gerçeği:**
- Emlakjet'in kullanım koşulları robot, kazıma ve veritabanının ticari kullanımını
  yazılı izin olmadan yasaklıyor.
- Etkinlik demosunda yayımlanmış rakamlar atıfla kullanılır.
- Ürün olacaksa ya Endeksa/REIDIN lisansı ya da kendi veri kaynağı şart.
- Mahalle düzeyinde 2007'den geriye giden tek seri REIDIN'de (ücretli, 481 mahalle).

**Ürünün asıl varlığı** fiyat değil, **kaynaklı olay veritabanı**: hangi proje, ne
zaman, nerede, hangi durumda. Bunu kimse tutmuyor.

**Sonraki katman ABB'nin kendi imar verisi.** 15.371 plan değişikliği karar numarasıyla,
187 bin imar adasının emsal değeri, 118 dönüşüm alanı. Bununla "neden" elle derlenmiş bir
listeden ölçülen bir sinyale dönüşür: "bu ilçede 2025'ten beri şu kadar alanın emsali
arttı". Mahalle başına 1998 öncesi bina payı da "değeri düşer" sınıfının kanıtı olur.

## Seed: ilçe → olaylar

Hepsi kaynaklı; URL'ler `data/` dosyalarında. (D) = doğrulanmadı.

- **Çankaya:**
  - M2 Kızılay–Koru (13 Mar 2014)
  - Ankara YHT Garı (29 Eki 2016; OSM sınırına göre Çankaya'da)
  - Bilkent Şehir Hastanesi (14 Mar 2019)
  - Eskişehir yolu AVM'leri: Armada 2002, Cepa 2007, Next Level Eki 2013
  - Panora 2007
  - Dikmen Vadisi (1996–2009, son etap sürüyor)
  - Portakal Çiçeği Vadisi (1994–97)
  - M5 Kızılay–Dikmen planlı (kesin proje 30 Nis 2025)
  - Koru–Yaşamkent uzatması (ihale Tem 2026, sonuç bulunamadı)
- **Etimesgut:**
  - M3 Eryaman durakları (Şub 2014)
  - Başkentray (12 Nis 2018)
  - Optimum (2004)
  - M6 Bağlıca–Eryaman planlı (meclis 8 Ara 2025)
- **Sincan:**
  - M3 Törekent (2014)
  - Başkentray (2018)
  - M6 planlı
- **Yenimahalle:**
  - M1 Batıkent (Ara 1997)
  - Atlantis (2011)
  - Cumhurbaşkanlığı Külliyesi, Beştepe (29 Eki 2014)
  - Etlik Şehir Hastanesi (28 Eyl 2022; adı Etlik ama OSM sınırına göre Yenimahalle'de)
  - Yamaçevler dönüşümü sürüyor
  - Demetevler dönüşümü başlamadı
- **Keçiören:**
  - M4 Şehitler–AKM (5 Oca 2017), Kızılay bağlantısı (12 Nis 2023)
  - Kuzey Ankara Girişi dönüşümü (2005–)
- **Altındağ:**
  - Ulus Tarihi Kent Merkezi (2005)
  - Gültepe–Aktaş (2006, 3210 konut)
  - Numune Hastanesi kapandı, Bilkent'e taşındı (26 May 2019; OSM'de Altındağ, Hacettepe Mah.)
  - Dışkapı hastaneleri Etlik'e taşındı (Ağu 2022)
  - Hıdırlıktepe dönüşümü (30 Oca 2026, 60 ay)
  - Esenboğa hattının Siteler ve Solfasol durakları (OSM'de iki mahalle de Altındağ)
- **Mamak:**
  - Dikimevi–Natoyolu (temel 13 Haz 2025, hedef 14 Oca 2029, 8 durak)
  - Yeni Mamak (2008–, 8006 konut, 1363 teslim)
  - Esenboğa hattının Demirlibahçe durağı (OSM'de Mamak)
- **Pursaklar:**
  - Esenboğa metrosu: Pursaklar ve Sarayköy durakları, 36 km, 12 durak
  - Sözleşmeler Ağu–Eyl 2026: 34,0 + 42,4 + 54,4 mlr TL
  - Esenboğa yeni terminal (2006)
- **Gölbaşı:**
  - İncek imar değişikliği (14 Şub 2017, emsal 0,33→2, iptal)
  - Ankara–Niğde otoyolu (Ara 2020)
  - Arz fazlası uyarısı (2026)
- **Çubuk:**
  - Esenboğa Havalimanı yeni terminal (16 Eki 2006; OSM sınırına göre Çubuk'ta)
  - Esenboğa metrosunun havalimanı ucu
- **Akyurt:** kaynaklı olay bulunamadı.

## Haber listesi ve KVKK nasıl?

- Lovable Cloud tablosu `subscribers`: email, ilçeler, consent_at, consent_version,
  unsubscribe_token.
- RLS: anonim kullanıcı yalnızca ekleyebilir, okuyamaz.
- Onay kutusu işaretsiz gelir; aydınlatma metni linki; gönder, kutu işaretlenene kadar kapalı.
- Her mailde tek tıkla çıkış (token ile).
- Aydınlatma metni Damla yazar.
- Ticari ileti göndermeden önce İYS kaydı gerekebilir (D).
- Sayfa altında sabit not: "yatırım tavsiyesi değildir".

## Tasarım ne?

Referans: ir-globe'un onaylı editoryal dili.

| Öğe | Değer |
|---|---|
| Zemin | #ffffff |
| Mürekkep | #16191f |
| İkincil | #6b7280 |
| Tek aksan | lacivert #17356b |
| Başlık / gövde | serif / sans |
| Ayraç | çizgi yok, kutu yok |

- Harita sayfanın kendisi; hero yok, kart ızgarası yok.
- Sınıf renkleri: değerlenebilir #2b5cad, korur #8a94a3, düşer #c8602a
  (kırmızı-yeşil değil: renk körlüğü).
- Lovable'ın varsayılanları promptta yasaklanır: rounded-xl kart, mor, gradient, pill
  rozet, gölge, emoji.
- Başlık cümlesi ve tüm metin Damla'nın.

## Bu gece ne hazırlanıyor?

| Kim | İş |
|---|---|
| Damla | Lovable Pro. Ücretsiz plan günde 5 kredi, yetmez; Pro $25/ay, akademik maille %50. Etkinlikte kredi dağıtılabilir (D). |
| Damla | Mapbox hesabı + public token (`pk.`). Lovable'ın resmî Mapbox connector'ı var. |
| Damla | (isteğe bağlı) ElevenLabs hesabı + API key, aylık kredi limitiyle. Lovable'ın resmî connector'ı var. |
| Ben | tamam: `data/ilceler.geojson`, 11 ilçe, OSM |
| Ben | tamam: `data/ilceler.json` ve `data/projeler.json`, 49 kaynaklı proje. `python3 data/build.py` ile yeniden üretilir. |

Lovable mevcut repoyu içeri alamaz, bağlanınca kendi reposunu açar. Bu repo spec ve
veriyi tutar. Yarın Lovable reposu açılınca `data/` oraya basılır: Damla repo adını
söyler, ben push'larım.

## Yarın akış nasıl?

Luma: 11:00–16:00, Yenimahalle. Bina süresi yaklaşık 2 saat 15 dakika.

| Saat | Ne |
|---|---|
| 11:00–12:30 | Atölye: iş modeli kanvası (BMC), Lovable, ElevenLabs. Kanvasın problem/çözüm/rakip kutuları bu belgedeki "Neden var?" bölümünden dolar. |
| 12:30–13:30 | Build I: Prompt 1, GitHub bağla, veri push, Prompt 2 |
| 14:30–15:45 | Build II: Prompt 3, Prompt 4, (Prompt 5), publish |
| 15:45–16:00 | Showcase. Mart etkinliğinde kişi başı 30 sn'ydi; bu etkinlik için (D). |

Demo tıklama yolu:
1. Harita açılır: merkez turuncu, çevre mavi.
2. Keçiören'e tıkla. Panelde görünen:
   - değeri düşer
   - "M4 2023'te Kızılay'a bağlandı, göreli fiyat yerinde saydı"
   - kaynak linki
3. Çubuk'a tıkla. Panelde görünen:
   - değerlenebilir
   - merkezden 46 km, fiyat Ankara medyanına göre +%36
   - havalimanı ve yeni imar planı

Cümleler Damla'nın.

Seçilirse: 3 Ekim Sell Sprint + VC Demo Hour.

## Lovable promptları

**Project knowledge** (Settings → Knowledge, 10k karakter sınırı):

```
bandl: Ankara district real-estate value map. Turkish UI, all lowercase.
Data: only from src/data/*.json. Never invent numbers, dates or sources. Every fact
shown in the UI has a source link from the data. If a field is empty, show
"kaynak bulunamadı", never a guess.
Design: white #ffffff background, ink #16191f text, secondary #6b7280, single accent
navy #17356b. Serif headings, sans body. No borders or divider lines; separate with
whitespace and size. Corner radius max 3px. Forbidden: purple, gradients, shadows,
pill badges/chips, emoji, card grids, hero sections, glassmorphism, toasts.
Class colors: "değerlenebilir" #2b5cad, "değer korur" #8a94a3, "değeri düşer" #c8602a.
Footer, always visible: "yatırım tavsiyesi değildir".
Schema:
- src/data/ilceler.geojson: FeatureCollection, each feature has properties.id.
- src/data/ilceler.json: [{ id, ad, sinif: "degerlenebilir"|"korur"|"duser",
  kural, neden, goreli: {"2019","2020","2026": ratio to Ankara median},
  goreli_degisim, yapi: { kizilay_km, bina_km2, beklenen, fark, bina_kaynak_url },
  fiyat: [{ yil, ay, tl_m2, kaynak, kaynak_url }],
  olaylar: [{ id, tarih, baslik, tur, durum, not, kaynak_url }] }]
- src/data/projeler.json: [{ id, ad, tur: "rayli"|"ulasim"|"hastane"|"kurum"|"avm"|
  "donusum"|"imar"|"yol"|"havalimani"|"risk", durum: "acik"|"onaylandi"|"sozlesmeli"|
  "yapimda"|"planli"|"iptal"|"kapandi"|"belirsiz", tarih, hedef?, ilceler: [id], yaklasik: bool, not?,
  geometri: GeoJSON Point|LineString|MultiLineString|null, kaynak_url }]
Status labels in UI: acik "açık", onaylandi "onaylandı", sozlesmeli "sözleşmeli", yapimda "yapımda",
planli "planlı", iptal "iptal", kapandi "kapandı", belirsiz "durumu belirsiz".
```

**Prompt 1: iskelet ve harita**
```
Build a single-page app: a full-screen Mapbox map of Ankara (use the Mapbox
connector), centered on 39.93, 32.85, zoom 9.5, a light/white base style.
Load district polygons from src/data/ilceler.geojson and district data from
src/data/ilceler.json (join on "id"). Fill each district with its class color at
0.55 opacity; hover darkens it. Top-left: the word "bandl" and one line of
placeholder text I will replace. Bottom-left: legend with the three classes.
Clicking a district opens a right-side panel (not a modal), 420px wide, full height,
scrollable; clicking the map outside closes it. For now the panel shows the district
name and class. If the data files do not exist yet, create them with the schema in
the knowledge and one example district.
```

**Prompt 2: ilçe paneli**
```
Fill the district panel from ilceler.json:
1) class name in its color, large; below it the rule that produced it (field "kural").
2) "neden" paragraph (field "neden").
3) One line from "yapi": "kızılay'a {kizilay_km} km · {bina_km2} bina/km² ·
   beklenen {beklenen} · gerçek {goreli_degisim}" (format ratios as signed percent),
   with the building-count source link (bina_kaynak_url).
4) Price relative to the Ankara median (field "goreli": 2019, 2020, 2026). Show the
   three ratios as a small line with labeled points (1.00 = median, draw that as a
   faint reference), then the TL/m² values from "fiyat" with month, year and source
   link. Label it "ankara medyanına göre".
5) Timeline (field "olaylar"): sorted by date, newest first: date, title, type,
   status label, "not" in smaller text, source link. Items with status "sozlesmeli",
   "yapimda" or "planli" appear first under a "gelecek" heading. If "olaylar" is
   empty: "bu ilçe için kaynaklı olay bulunamadı".
```

**Prompt 3: proje katmanı**
```
Add a projects layer from src/data/projeler.json (skip items whose geometri is
null; they only appear in district panels). Lines: solid if "acik", dashed if
"sozlesmeli", "yapimda" or "planli". Points: small navy circles, hollow if not
"acik"; "kapandi" and "iptal" in #6b7280. Hover shows name, date, status label and,
if yaklasik is true, "güzergâh yaklaşık". Click opens the first district in
"ilceler" and scrolls its panel to that event. A plain text toggle top-right:
"projeleri göster / gizle".
```

**Prompt 4: haber listesi**
```
Enable Lovable Cloud. Create table subscribers (id uuid pk, email text unique not
null, ilceler text[] not null, consent_at timestamptz not null, consent_version text
not null, unsubscribe_token uuid default gen_random_uuid(), created_at timestamptz
default now()). RLS: anon can INSERT only; no select, update or delete for anon.
At the bottom of the district panel: "bu ilçede yeni proje olursa haber ver" -
email field, an UNCHECKED consent checkbox linking to /aydinlatma, submit disabled
until checked. Pre-select the open district. Success: inline sentence, no toast.
Page /aydinlatma with placeholder text I will write. Page /cik?token=... that calls
an edge function which deletes the row with that token and confirms in one sentence.
```

**Prompt 5: dinle (zaman kalırsa)**
```
Connect ElevenLabs. In the district panel add a "dinle" text button. It sends the
district's "neden" text to an edge function that calls ElevenLabs text-to-speech
with a multilingual model that supports Turkish, stores the mp3 in Cloud storage
keyed by district id + text hash (reuse if it exists, to save credits), and plays it.
```

## Açık kalanlar

- Esenboğa hattı durakları:
  - Siteler ve Solfasol OSM'de Altındağ, Demirlibahçe Mamak mahallesi. İlçe, durakla aynı adı taşıyan mahalleden geliyor; durağın kendi koordinatı değil.
  - Kuyubaşı, Sarayköy, Kuzey Ankara, Fuar, YBÜ bulunamadı.
- Çubuk ve Akyurt'un göreli yükselişinin nedeni bulunamadı.
- M1 açılışı 28 mi 29 Ara 1997 mi, M3 12 Şub mu 13 Mar 2014 mü: kaynaklar çelişiyor.
- İYS kaydı eşiği doğrulanmadı.
