# bandl

Ankara'nın ilçelerini **değerlenebilir / değer korur / değeri düşer** diye sınıflayan ve
bu sınıfın nedenini haritadaki projelere ve tarihte olanlara kaynaklı olarak bağlayan harita.

Ürün tanımı, sınıflama kuralları ve Lovable promptları: [PROJECT.md](PROJECT.md).
Uygulama ayrı repoda: `nosey-dewdrop/bandl-app` (`data/` çıktıları orada `src/data/`).
Bu dosya: neden var, hangi kaynaklara bakıldı, repoda hangi varlıklar var.

---

## Neden var?

**Nominal fiyat yanıltıyor.**
- Ankara'da konut fiyatı Ağustos 2026'da bir yılda nominal %28,2 arttı, reel olarak %2,6
  düştü (Endeksa).
- TCMB'nin endeksine göre Ankara nominal %24,8; ulusal enflasyonla reel karşılığı yaklaşık −%5.
- Nominal fiyata bakan herkes her semtin "değerlendiğini" görüyor.

**Göreli bakınca tablo değişiyor.** Her ilçeyi veri olan 11 ilçenin medyanına bölünce,
2019'dan 2026'ya:
- Çubuk %36, Gölbaşı %30 öne geçmiş
- Mamak yerinde saymış
- Altındağ %7 geride kalmış

Hangi semtin gerçekten öne geçtiği ancak böyle görünüyor.

**Ankara'yı son 7 yılda projeler değil, merkezden çevreye kayış sürükledi.**
- İlçenin Kızılay'a uzaklığı ile göreli fiyat değişimi arasında r = 0,85 (11 ilçe).
- Keçiören'in metrosu 2023'te Kızılay'a bağlandı; ilçenin göreli fiyatı yerinde saydı.
- Hastanelerini kaybeden Altındağ en çok geride kalan merkez ilçe oldu.

Bu, "metro geliyorsa değer artar" sezgisinin Ankara'da ilçe düzeyinde tutmadığını gösteriyor.
Ayrıntı: PROJECT.md, "Nasıl sınıflıyor?".

**Mevcut araçlar "neden" sorusunu cevaplamıyor.** Endeksa/Emlakjet şunları gösteriyor:
- mahalle fiyatı
- reel/nominal geçiş
- kapalı kutu bir yatırım skoru
- 1 yıllık fiyat beklentisi

Fiyatın neden oynadığını (metro, şehir hastanesi, kentsel dönüşüm, imar kararı, kurum
taşınması) göstermiyor.

**O bilgi dağınık:** EGO sayfaları, ABB proje sayfaları, meclis kararları, haberler,
akademik makaleler. bandl bunları tek haritada, tarih ve kaynakla, fiyat serisinin yanına koyuyor.

**Kural:** uydurma veri yok. Her sayı ve her olayın yanında kaynak linki var. Kaynağı
bulunamayan yerde "kaynak bulunamadı" yazar.

## Durum ne?

| Tarih | Ne |
|---|---|
| 25 Eyl 2026 | İsim, spec, kaynak araştırması, ABB araştırması, veri: 11 ilçe, 49 proje, 7 raylı hat. |
| 25 Eyl 2026 gece | Sınıflama v1 (yapı + emsal). Yeni yön: 10–20 mn TL alıcı için ilan + harita + yatırım katmanı. |
| 26 Eyl 2026 | GarajX "Ship in Ankara": Lovable ile ilk sürüm. |

---

## Hangi kaynaklara bakıldı?

Araştırma 25 Eyl 2026'da yapıldı. **(D)** = doğrulanmadı ya da kaynak zayıf.

### Fiyat verisi

| Kaynak | Düzey | Derinlik | Erişim | Kullanıldı mı? |
|---|---|---|---|---|
| [Endeksa / Emlakjet](https://www.emlakjet.com/emlak-piyasasi/satilik-konut/ankara) | il, ilçe, mahalle | Oca 2020'den beri, nominal/reel | anlık görüntü ücretsiz, geçmiş API'si captcha'lı | Evet: Ağu 2026 ilçe ve mahalle fiyatları |
| [Baret Dergisi, Endeksa tablosu](https://www.baretdergisi.com/ankarada-konut-fiyatlari-2020-yilinin-ilk-6-ayinda-yuzde-799-artti/20007/) | ilçe | Haz 2019, Haz 2020 | ücretsiz | Evet: 2019 ve 2020 ilçe fiyatları. Metin 1.993, tablo 1.933 diyor. |
| sahibinden Emlak Endeksi ([yardım](https://yardim.sahibinden.com/hc/tr/articles/115004672233-Emlak-Endeksi-nden-Kimler-Faydalanabilir)) | il, ilçe, mahalle | son 3–4 yıl | giriş şart, Cloudflare 403 | Hayır |
| [BETAM sahibindex](https://betam.bahcesehir.edu.tr/2026/09/sahibindex-satilik-konut-piyasasi-gorunumu-eylul-2026/) | il (İst, Ank, İzm) | aylık | ücretsiz | Reel değişim karşılaştırması için |
| REIDIN: [Ağu 2026 raporu](https://reidin.com/wp-content/uploads/2026/09/REIDIN-RESIDENTIAL-PROPERTY-PRICE-INDICES_202608.pdf), [eski broşür](http://content.reidin.com/PublicReports/REIDINTRKonutFiyatEndeksleri.pdf) | 81 il, 258 ilçe, 1.255 mahalle (eski broşür: 481) | Haz 2007'den beri | ücretli, ilan tabanlı | Hayır. Mahalle düzeyinde en uzun seri bu. |
| TCMB KFE: [Ağu 2026 PDF](https://www.tcmb.gov.tr/wps/wcm/connect/8bbac42a-c854-4c58-8b0c-e7e55c35ec2d/KFE.pdf?MOD=AJPERES), [EVDS](https://evds3.tcmb.gov.tr/tumSeriler/2003/bie_kfe), [revizyon notu](https://tcmb.gov.tr/wps/wcm/connect/blog/tr/main+menu/analizler/konut+fiyat+endeksi+hesaplamalarinda+yapilan+revizyona+iliskin+bir+degerlendirme) | Ankara yalnız il düzeyi | 2010'dan beri (2023=100) | ücretsiz | Reel değişim için |
| TCMB il medyan TL/m²: [2022 PDF](https://www.bmd.com.tr/application/files/9816/5943/7087/Konut_Fiyat_Endeksi-_Nisan_2022.pdf), [2025 PDF](https://www.bmd.com.tr/application/files/9617/5274/4280/Konut_Fiyat_Endeksi_-_Haziran_2025.pdf) | il | çeyreklik | ücretsiz | Karşılaştırma için |
| TÜİK ilçe satış adedi: [Ağu 2026](https://www.ekonomiankara.com/ankaranin-agustos-ayi-ilce-duzeyinde-konut-satis-verileri/14558), [Kas 2024](https://www.yeniankara.com.tr/ankara/ankarada-ilce-ilce-satilan-konut-sayisi-belli-oldu-91312) | ilçe | aylık | yerel basın üzerinden | Henüz değil. Likidite sinyali olur. |
| [e-Devlet arsa rayiç değeri](https://www.turkiye.gov.tr/cankaya-belediyesi-arsa-rayic-degeri-sorgulama-v2) | sokak | 4 yılda bir | tek tek sorgu | Hayır. Vergi değeri, piyasanın çok altında. |
| [Dolar bazlı konut fiyatları](https://sanayilesmeliyiz.com/dolar-bazli-konut-fiyatlari/) | Türkiye, İstanbul | — | görsel | Hayır. Ankara yok. |
| Hepsiemlak | — | — | 403 | Erişilemedi |

Reel değişim haberleri:
- [TCMB Ara 2025 (apara)](https://www.apara.com.tr/piyasalar/2026/01/19/tcmb-acikladi-konut-fiyatlari-aralikta-reel-olarak-azaldi)
- [Endeksa Ağu 2026 (Foreks)](https://www.foreks.com/haber/detay/6ab0d8fe24008d7d43734638/FRKS/tr/emlakjet-ve-endeksa-agustos-2026-konut-deger-raporu-ankara-fiyat-artisinda-lider-istanbul-satislarda-one-cikti-21-09-26/)
- [Endeksa Haz 2024 (AA)](https://www.aa.com.tr/tr/isdunyasi/gayrimenkul/endeksa-gayrimenkul-deger-raporunu-yayimladi/688932)
- [TCMB reel düşüş (ekonomiankara)](https://www.ekonomiankara.com/tcmb-acikladi-konut-fiyatlarinda-reel-dusus-kiralar-ne-kadar-oldu-7643692)
- [Habertürk KFE](https://www.haberturk.com/son-dakika-konut-fiyat-endeksi-3891941-ekonomi)
- [TÜFE 2026 güncellemesi (TCMB blog)](https://tcmbblog.org/wps/wcm/connect/blog/tr/main+menu/analizler/2026+yili+tuketici+fiyat+endeksindeki+guncellemeler+ve+etkileri)

Herkes ulusal TÜFE ile reelleştiriyor; Ankara'ya özel enflasyon kullanan yok.

### Rakipler

- **Endeksa / Emlakjet**
  - Şubat 2026'da birleştiler ([haber](https://www.ekonomiankara.com/emlakjetten-a-yatirimcilar-icin-yapay-zeka-destekli-yeni-donem/13716)).
  - İlçe yatırım skoru: [Mar 2025 Ankara sıralaması](https://analizgazetesi.com.tr/haber/endeksa-ankaranin-yatirim-skoru-en-yuksek-ilcelerini-acikladi-8205/),
    [2026 strateji bazlı](https://www.yeniankara.com.tr/ankara/konut-piyasasi-sekillendi-ankarada-en-cok-kazandiran-ilce-hangisi-176258).
  - Ağu 2026'dan beri ilanlar [yatırım getirisine göre sıralanabiliyor](https://www.emlakhaberi.com/emlakjetten-bir-ilk-konut-aramalari-artik-yatirim-getirisine-gore-siralaniyor).
  - İki yapay zekâ asistanı var: EmlakZeka ve Atlas.
- **sahibinden:** 6 aylık tahmin, yalnızca kurumsal hesaplara.
- **REIDIN:** ücretli analitik.
- **Yeniden paketleyenler:** evarsadegeri.com, mulkunuhesapla.com, birilanver. Endeksa ve TCMB verisini sunuyorlar.
- **Boşluk:** fiyatın neden oynadığını projeye ve tarihe bağlayan ürün bulunamadı.

### Projeler

**Raylı sistem**

| Proje | Durum | Kaynak |
|---|---|---|
| A1 Ankaray, M1, M2, M3, M4 tarihçesi | açık | [doğrula.org, ABB raylı sistem tarihçesi](https://www.dogrula.org/ekipten/ankara-buyuksehir-belediyesi-rayli-sistem-tarihcesi/), [Ankara Metro (Wikipedia)](https://en.wikipedia.org/wiki/Ankara_Metro), [Koru](https://en.wikipedia.org/wiki/Koru_(Ankara_Metro)), [Batıkent](https://en.wikipedia.org/wiki/Batıkent_(Ankara_Metro)), [OSB-Törekent](https://en.wikipedia.org/wiki/OSB-Törekent_(Ankara_Metro)), [Dikimevi](https://en.wikipedia.org/wiki/Dikimevi_(Ankara_Metro)), [Ankaray](https://en.wikipedia.org/wiki/Ankaray) |
| Başkentray | açık (12 Nis 2018) | [Yeni Şafak](https://www.yenisafak.com/ekonomi/dev-proje-bugun-aciliyor-3224470) |
| Ankara YHT Garı ve YHT hatları | açık | [Gar](https://en.wikipedia.org/wiki/Ankara_Tren_Gar%C4%B1), [Ankara–Eskişehir YHT](https://tr.wikipedia.org/wiki/Ankara-Eski%C5%9Fehir_Y%C3%BCksek_H%C4%B1zl%C4%B1_Treni) |
| Dikimevi–Natoyolu | yapımda, hedef 14 Oca 2029 | [EGO](https://www.ego.gov.tr/sayfa/2281/dikimevinatoyolu-ankaray-hafif-rayli-sistem-hatti), [Yeni Ankara](https://www.yeniankara.com.tr/ankara/dikimevi-natoyolu-mamak-metrosunda-son-durum-ne-149114) |
| Gar–Esenboğa (M7) | sözleşmeler Ağu–Eyl 2026 | [Haber Ankara](https://www.haberankara.com/ankara/pursaklar-esenboga-metro-ihalesi-tamamlandi-319433), [yatirimlar.com](https://yatirimlar.com/haber/esenboga-havalimani-metro-calismalarina-2026-yilinda-baslanacak_244111) |
| Koru–Yaşamkent / Bağlıca | ihale Tem 2026, sonuç bulunamadı | [Rayhaber](https://rayhaber.com/2026/07/koru-yasamkent-ve-koru-baglica-metrosunda-geri-sayim-basladi/) |
| M5 Kızılay–Dikmen | planlı, yatırım programında değil | [EGO](https://www.ego.gov.tr/sayfa/2284/m5-kizilaydikmen-hatti) |
| M6 Çayyolu–Sincan | planlı, meclis 8 Ara 2025 | [yatirimlar.com](https://yatirimlar.com/haber/ankara-ya-4-yeni-metro-hatti-toplam-44-kilometrelik-dev-ulasim-hamlesi_249147) |
| Hayata geçmemiş 7 raylı proje | (D) | [Yeni Ankara](https://www.yeniankara.com.tr/ankara/ankaranin-trafigini-rahatlatacak-henuz-hayata-gecmeyen-7-rayli-sistem-projesi-180908) |

**Şehir hastaneleri:**
- [Bilkent (14 Mar 2019)](https://en.wikipedia.org/wiki/Ankara_Bilkent_City_Hospital)
- [Etlik (28 Eyl 2022)](https://en.wikipedia.org/wiki/Ankara_Etlik_City_Hospital)

**AVM'ler (açılış yılı):**
- [ANKAmall 1999](https://en.wikipedia.org/wiki/ANKAmall)
- [Armada 2002](https://tr.wikipedia.org/wiki/Armada_Al%C4%B1%C5%9Fveri%C5%9F_ve_%C4%B0%C5%9F_Merkezi)
- [Optimum 2004](https://optimumankara.com/tr/hakkimizda)
- [Cepa 2007](https://cepaavm.com.tr/hakkimizda/)
- [Panora 2007](https://www.yeniankara.com.tr/ankara/panora-avm-ne-zaman-acildi-nerede-ve-nasil-gidilir-110667)
- [Acity 2008](https://www.milliyet.com.tr/emlak/acity-outlet-bir-ilkle-aciliyor-66466)
- [Gordion 2009](https://www.hurriyet.com.tr/ekonomi/gordion-avm-17-eylulde-acilacak-12443678)
- [Kentpark 2010 (D)](https://www.tercihiniyap.net/kentpark-avm-kacta-acilir-kacta-kapanir-calisma-saatleri-nasil-h11234.html)
- [Atlantis 2011](https://www.aksam.com.tr/ekonomi/atlantis-avm-acildi--63965h/haber-63965)
- [Next Level 2013](https://www.haberler.com/politika/next-level-avm-nin-acilisi-5212253-haberi/)
- [Taurus 2013](https://retailturkiye.com/avm/taurus-avm-acildi/)
- [Metromall 2017](https://tr.wikipedia.org/wiki/Metromall_AVM)
- [Forum Ankara (D)](https://www.malls.com/malls/forum_ankara_outlet/)
- [Podium (D)](https://www.kariyer.net/avm-rehberi/podium+ankara+avm)

**Kentsel dönüşüm:**
- [Portakal Çiçeği Vadisi](https://kentselstrateji.com/ankara-portakal-cicegi-vadisi-kentsel-donusum-projesi/)
- [Dikmen Vadisi son etap (ABB)](https://www.ankara.bel.tr/proje/dikmen-vadisi-son-etap-kentsel-donusum-projesi-84)
- [Kuzey Ankara Girişi kanunu](https://www.lexpera.com.tr/mevzuat/kanunlar/kuzey-ankara-girisi-kentsel-donusum-projesi-kanunu)
- [Ulus Tarihi Kent Merkezi](https://ankaradergisi.org/jvi.aspx?pdir=jas&plng=tur&un=JAS-44154)
- [Hıdırlıktepe–Atıfbey–İsmetpaşa (ABB)](https://www.ankara.bel.tr/en/proje/hidirliktepe-atifbey-ismetpasa-kentsel-donusum-ve-gelisim-projesi-305)
- [Yeni Mamak](https://www.yeniankara.com.tr/mamak/yeni-mamak-kentsel-donusumde-son-durum-2026da-hangi-etaplar-teslim-edilecek-170851)
- [Gültepe–Aktaş](https://www.yapi.com.tr/ankaranin-olayli-mahallesi-cincine-3-bin-210-konut)
- [Yamaçevler](https://www.yenimahalle.bel.tr/ProjeDetay/yamacevler-kentsel-donusum-projesi/15)
- [Demetevler](https://www.haberturk.com/ankara-haberleri/30530321-yenimahalle-belediyesinden-demetevlerde-kentsel-donusum-cagrisi)

**İmar ve plan:**
- [Başkent 2023 nazım imar planı (ABB)](https://www.ankara.bel.tr/ankara-buyuksehir-belediyesi-nazim-plan/1-25-000-baskent-ankara-nazim-mar-plani).
  2038 planını mahkeme 30 Ara 2020'de iptal etti; ABB stratejik planı iptal yılını 2021 veriyor.
  Ankara'nın geçerli üst planı yok.
- [İncek imar değişikliği iptali](https://www.gazeteduvar.com.tr/yargi-gokcekin-incekteki-imar-plani-degisikligini-iptal-etti-haber-1552615)

**Diğer tetikleyiciler:**
- [Bilkent Üniversitesi](https://tr.wikipedia.org/wiki/Bilkent_%C3%9Cniversitesi)
- [Ankara–Niğde otoyolu](https://www.aa.com.tr/tr/turkiye/ankara-nigde-otoyolunun-tamami-hizmete-girdi/2078934)
- [Esenboğa](https://en.wikipedia.org/wiki/Esenbo%C4%9Fa_International_Airport)
- [Cumhurbaşkanlığı Külliyesi](https://en.wikipedia.org/wiki/Presidential_Complex_(Turkey))
- [Ankapark](https://www.sozcu.com.tr/750-milyon-dolar-harcanan-ankapark-kapatildi-wp5618555)
- [Merkezin batıya kayması (D)](https://www.yeniankara.com.tr/ankara/ankarada-sehrin-merkezi-neden-batiya-dogru-kayiyor-183801)

### ABB (Ankara Büyükşehir Belediyesi)

25 Eyl 2026'da tek tek curl ile denendi.

**1. Harita veri sunucusu (ArcGIS REST, anonim erişim). bandl için en değerli kaynak bu.**
- Sunucular: `https://baskentcbs.ankara.bel.tr/server/rest/services` ve `https://planaski.ankara.bel.tr/webgis/rest/services`.
- Sorgu JSON, GeoJSON ya da PBF döndürüyor. Bir sorgu en fazla 2000 kayıt veriyor, fazlası için sayfalamak gerekiyor.
- WMS açık, WFS kapalı. `icdp_yeni` klasörü token istiyor.

| Katman | İçerik |
|---|---|
| `plan/PlanRaporu/MapServer/3` ve `/4` | **11.778 uygulama imar planı (UİP) ve 3.593 nazım imar planı (NİP) değişikliği**: onay tarihi, meclis karar no ve tarihi, askı tarihleri, mahkeme durumu (sayılar tarafımızca doğrulandı). 1 Oca 2025'ten beri 583 UİP değişikliği. Alanların çoğu boş. |
| `plan/UIP_Goruntuleme/MapServer/19` (plan adası) | **186.703 imar adası**: kullanım, **emsal, TAKS, KAKS**, kat, azami yükseklik, başlangıç tarihi. İlçe alanı çoğunlukla boş, mekânsal eşleştirme gerek. |
| `Hosted/plan/FeatureServer/0` | 214.116 poligon: taks, kaks, emsal, hmax, ilçe kodu |
| `plan/PlanRaporu/MapServer/2` | **118 kentsel dönüşüm alanı**: ad, ilçe, meclis kararı, İPTAL / yürütmeyi durdurma notu (sayı doğrulandı) |
| `aktifAski/SinirNipAski`, `SinirUipAski` | şu an askıdaki planlar |
| `plan/mahkemeKarari`, `plan/mahkemeDurumu` | plan davaları (523 NİP poligonu) |
| `plan/NIP5000Etkin_Goruntuleme/54` ve 57–83 | 27.718 kentsel kullanım poligonu; sel alanları, dere yatakları, afete maruz alanlar, havalimanı koridoru |
| `deprem/ilceMahalleRapor/2` | **1.434 mahallede bina sayısı, deprem yönetmeliği dönemine göre** (1998 öncesi, 1998, 2007, 2018) |
| `deprem/depremYonetmeligineGoreBinalar`, `deprem/diriFay`, `jeolojikEtut`, `hidroloji_analizi` | 520.761 bina, diri faylar, yapılaşmaya uygunluk, sel noktaları |
| `kentrehberi/ego_kent_Rehberi` | metro, Ankaray, Başkentray ve teleferik istasyonları (yalnızca nokta) |
| `Hosted/ABB_Mahalleler`, `ortak/adres` | 1.437 mahalle poligonu, adres, yol, bina |

Kentsel dönüşüm alanlarının ilçelere dağılımı (sorgu, 25 Eyl 2026):

| İlçe | Alan sayısı |
|---|---|
| Çankaya | 36 |
| Yenimahalle | 17 |
| Mamak | 14 |
| Beypazarı | 14 |
| Gölbaşı | 11 |
| Etimesgut | 6 |
| Altındağ | 5 |
| Keçiören | 4 |
| Akyurt, Sincan, Kızılcahamam | 1'er |
| İlçesiz | 8 |

**2. Meclis kararları**
- [Karar tablosu](https://www.ankara.bel.tr/meclis/kararlar): 1.202 sayfa, yaklaşık 24 bin karar, 12 Haz 2012'den beri.
- Tam metinler `s.ankara.bel.tr` üzerinde; 2019'a kadar .doc, sonra .docx.
- Arama formu CSRF token'lı bir POST.
- Gündem kararlardan önce yayımlanıyor: `/meclis/gundem`. UKOME kararları: `/ukome`.
- Tam metin eski ve yeni kullanım ile yoğunluğu veriyor. Örnek: [karar 1165](https://s.ankara.bel.tr/s3/abb/2026/09/18/3fd58fda-4fd3-4453-922b-76737ba77c10.docx),
  Çayyolu, spor alanı → ticaret, E=0,50.
- Diğer örnekler:
  - [Çubuk merkez ~165 ha plan, 1023](https://s.ankara.bel.tr/s3/abb/2026/08/24/0277fdc9-cbc8-4a2c-8a06-961a245b4234.docx)
  - [Yeni Mamak 11 etap UİP revizyonu, 1150](https://s.ankara.bel.tr/s3/abb/2026/09/18/3037342d-1c12-4144-8fb2-f8b9c0647239.docx)
  - [M5, M4, M2–M3'ü 2026 yatırım programına alma talebi, 496](https://s.ankara.bel.tr/s3/abb/2026/04/27/04459dee-ed34-4cca-8bcb-3ffecc0644c7.docx)

**3. Proje kataloğu** (`ankara.bel.tr/proje/x-{id}`)
- **Boyut:** 19 kategori sayfasında 271 proje, kategoriye bağlı olmayan 35 sayfa daha. Toplam yaklaşık 306.
- **Alanlar:** yalnızca başlık, metin ve "Proje Durumu". İlçe, tarih ya da konum alanı yok.
- **Durum alanı güvenilmez.** M5'in sayfası [179](https://www.ankara.bel.tr/proje/x-179) "Tamamlandı" diyor, metni "oluşacak" diyor.
- **Değere dokunanlar:**
  - [Dikimevi–Natoyolu (87)](https://www.ankara.bel.tr/proje/x-87)
  - [Koru uzatması (177)](https://www.ankara.bel.tr/proje/x-177)
  - [M4 Şehitler–Forum (178)](https://www.ankara.bel.tr/proje/x-178)
  - [M6 Çayyolu–Sincan (258)](https://www.ankara.bel.tr/proje/x-258)
  - [Mamak dönüşümü (182)](https://www.ankara.bel.tr/proje/x-182)
  - [Hıdırlıktepe (305)](https://www.ankara.bel.tr/proje/x-305)
  - [Ulus yayalaştırma (240)](https://www.ankara.bel.tr/proje/x-240)
  - Yaklaşık 20 kavşak ve bağlantı yolu, parklar ve rekreasyon alanları
- **Hastane, AVM, fuar yok:** bunlar merkezî hükümet ya da özel sektör işi.

**4. Planlar ve bütçe**
- [2025–2029 Stratejik Plan](https://s.ankara.bel.tr/s3/abb/2025/11/27/5af9c32a-489b-4ffe-9ddb-937be66a0ccc.pdf):
  - 2038 Çevre Düzeni Planı'nın 2021'de iptal edildiğini yazıyor.
  - Ulaşım ana planı ve üst ölçek plan olmadığını yazıyor.
- [2026 Performans Programı](https://s.ankara.bel.tr/s3/abb/2026/01/30/91a36f2f-cac5-4b36-9f97-630237507179.pdf):
  - Raylı sistem bütçesi 5,335 mlr TL, yalnızca Dikimevi–Natoyolu için.
  - Kentsel dönüşüm bütçesi 1,375 mlr TL: Hıdırlıktepe, Şirindere Vadisi planı, Yeni Mamak parselasyonu, Demetevler hazırlığı.
  - Hacıbayram–Kale–Hıdırlıktepe teleferiği.
  - Yeni Ankara Çevre Düzeni Planı.
  - Yapracık–Bağlıca bulvarı.
- [2025 Faaliyet Raporu](https://s.ankara.bel.tr/s3/abb/2026/04/30/ba1b84c3-8294-4b5a-8cf5-85195a1200fa.pdf): 336 sayfa, yalnızca görüntü; kullanmak için OCR gerek.

**5. EGO**
- [Raylı sistem dizini](https://www.ego.gov.tr/sayfa/1075/rayli-sistem); proje sayfaları 2281–2284 ve 2291.
- Güzergâhlar yalnızca resim olarak var; indirilebilir geometri yok.

**6. Açık veri (Şeffaf Ankara)**
- Harita katmanları:
  - `teo_abb_onemli_projeler`: ad, tarih, mahalle, ilçe, koordinatlı
  - `teo_abb_demografi`: mahalle nüfusu
  - `teo_abb_sel_oncelikli_yapilacaklar`: sel öncelikli işler
- API istek gövdesi şifreli ve token'lı; yalnızca arayüzden indirilebiliyor.
- `teo_ruhsat` yapı ruhsatı değil, kazı izni olabilir (D).

**7. İlçe belediyelerinin imar portalları**

| İlçe | Adres |
|---|---|
| Çankaya | imardurumu.cankaya.bel.tr |
| Yenimahalle | kentrehberi.yenimahalle.bel.tr |
| Keçiören | keos.kecioren.bel.tr/imardurumu |
| Mamak | ims.mamak.bel.tr |
| Etimesgut | keos.etimesgut.bel.tr |
| Sincan | cbs.sincan.bel.tr |
| Altındağ | cbs.altindag.bel.tr |
| Pursaklar | açık ArcGIS: cbs.pursaklar.bel.tr/webgis/rest/services |
| Gölbaşı | cbs.ankaragolbasi.bel.tr, uygulama yolu bulunamadı (D) |

**8. Ulusal kaynaklar**
- **e-Plan (eplan.csb.gov.tr):** askıdaki ve yürürlükteki planlar açık. Değer Artış Payı modülünün açık olup olmadığı (D).
- **[ÇŞB Ankara duyuruları](https://ankara.csb.gov.tr/duyurular):** ABB meclisinden geçmeyen, bakanlığın 6306 sayılı kanunla (riskli alan) yaptığı planlar. Örnekler:
  - Altındağ Beşikkaya riskli alan, 16 Eyl 2026
  - Çankaya Fakülteler UİP, 25 Eyl 2026
  - Etimesgut askerî havaalanı–Ayyıldız bağlantı yolu, 18 Eyl 2026
- **TKGM:** parselsorgu.tkgm.gov.tr açık. Belgelenmemiş bir GeoJSON API'si var, koşulları belli değil.

**bandl için sıralama:**
1. **UİP/NİP değişiklik katmanları ve imar adaları.** Tarihli, karar numaralı emsal değişikliği; "bu ilçe neden değer kazanıyor" sorusunun en doğrudan cevabı.
2. **Meclis kararlarının tam metni.** Değişikliğin öncesi, sonrası ve gerekçesi; 2012'ye kadar geri gidiyor.
3. **Kentsel dönüşüm sınırları ve 2026 performans programı.** Nerede dönüşüm var, nerede iptal edilmiş, sıradaki hangisi.
4. **EGO, 2026 programı ve 496 ile 933 sayılı kararlar.** Parası ayrılmış raylı hattı çizimde kalandan ayırıyor.
5. **Mahalle başına deprem dönemi bina sayısı ve risk katmanları.** "Değeri düşer" sınıfının kanıtı olur.
6. **ÇŞB duyuruları.** ABB kaynaklarının kaçırdığı 6306 planları.

### Fiyat etkisi kanıtı

| İddia | Kaynak | Not |
|---|---|---|
| Metroya yakınlık fiyatı artırıyor, Batıkent'te Koru'dan güçlü | [Erdoğanaras vd. 2023](https://dergipark.org.tr/en/pub/mbud/article/1284843) | hedonik; erişilebilen özette katsayı yok |
| M4 Kızılay bağlantısından sonra Keçiören'de otobüs durağı fiyatı etkilemez oldu | [Akdemir ve Baytekin 2024](https://dergipark.org.tr/tr/pub/maddergi/article/1449342) | büyüklük yok |
| En çok değerlenen istasyonlar 2011–2017 (TSKB) | [Ekonomist](https://www.ekonomist.com.tr/emlak/ankaranin-metrosu-konuta-deger-katiyor.html) | yüzde yok |
| M2 ve M3 istasyon bölgeleri 2018 fiyatları | [Ekonomist](https://www.ekonomist.com.tr/emlak/ankara-metrosunun-parlattigi-bolgeler.html) | tek zaman noktası |
| Şehir hastaneleri çevresinde rant | [Aliefendioğlu ve Bostancı 2021](https://dergipark.org.tr/tr/download/article-file/1105037) | nitel |
| Etlik hastanesi açılmadan fiyatlar arttı | [Ekşi Sözlük](https://eksisozluk.com/etlik-sehir-hastanesi--5166508) | (D) |
| Kızılay'ın çekim kaybı | [Yeni Ankara](https://www.yeniankara.com.tr/ankara/ankarada-eski-populerligini-kaypeden-7-semt-183561) | nitel |
| Gölbaşı–İncek arz fazlası riski | [Ekonomi Ankara](https://www.ekonomiankara.com/ankaraya-binlerce-yeni-konut-geliyor-hangi-bolgelerde-arz-yogunlasacak/14501) | |
| Sel riski: Dikmen Deresi, Hatip Çayı | [Yeni Ankara](https://www.yeniankara.com.tr/ankara/ankarada-sel-riski-tasiyan-bolgeler-hangi-ilceler-one-cikiyor-182118) | ikincil kaynak |

Ankara için "şu proje fiyatı şu kadar artırdı" diyen sayısal bir kaynak yok. İstanbul'da
var. Önce/sonra karşılaştırması kendi fiyat serimizden kurulacak.

### Coğrafya

| Ne | Kaynak | Nasıl |
|---|---|---|
| 11 ilçe sınırı | OpenStreetMap, Nominatim | OSM relation ID'leri `data/ilceler.geojson` içinde; 0,0003° sadeleştirme |
| Raylı hat güzergâhları | OpenStreetMap, Overpass | A1, M1–M4, Başkentray, OSM'deki M5 taslağı |
| Durak adı → ilçe | Nominatim mahalle araması | Siteler ve Solfasol Altındağ, Demirlibahçe Mamak |
| AVM, hastane, dönüşüm noktaları | Nominatim adla arama | 29 nokta. Yamaçevler, Kuzey Ankara Girişi ve Yeni Mamak bulunamadı; haritada yoklar, panelde varlar. |
| Planlı hatlar | durak adlarının mahalle merkezleri | Dikimevi–Natoyolu, Gar–Esenboğa, Koru uzatması: `yaklasik: true` |
| Kontrol | nokta-poligon testi | Kızılay → Çankaya, Batıkent → Yenimahalle, Esenboğa → Çubuk, Etlik Şehir Hastanesi → Yenimahalle, Ankara Garı → Çankaya, Numune → Altındağ |

### Araçlar

**Lovable:**
- [kredi](https://docs.lovable.dev/introduction/credits-and-usage) ve [planlar](https://docs.lovable.dev/introduction/subscription-plans):
  ücretsiz plan günde 5 kredi; Pro $25/ay, akademik maille %50
- [Cloud](https://docs.lovable.dev/features/cloud)
- [Mapbox connector](https://docs.lovable.dev/integrations/mapbox)
- [Google Maps](https://docs.lovable.dev/integrations/google-maps): özel alan adında çalışmıyor
- [GitHub](https://docs.lovable.dev/integrations/github): mevcut repo içeri alınamaz
- [özel alan adı](https://docs.lovable.dev/features/custom-domain)
- [knowledge](https://docs.lovable.dev/features/knowledge): 10k karakter; repodaki AGENTS.md ve CLAUDE.md de okunur
- [prompt rehberi](https://docs.lovable.dev/prompting/prompting-one)

**ElevenLabs:**
- [Lovable connector](https://docs.lovable.dev/integrations/eleven-labs)
- [widget](https://elevenlabs.io/docs/agents-platform/customization/widget)
- [React SDK](https://elevenlabs.io/docs/agents-platform/libraries/react)
- [fiyat](https://elevenlabs.io/pricing): ücretsiz plan 10k kredi/ay; Startup Grants var

**Leaflet + Lovable:** [üçüncü taraf rehber](https://www.rapidevelopers.com/how-to-build-lovable/map-application) (D). Mapbox seçildi.

### Etkinlik

- [Luma sayfası](https://luma.com/uf5fjzt7): 26 Eyl, 11:00–16:00, Yenimahalle, adres onaylı katılımcılara
- [Lovable topluluk takvimi](https://community.lovable.app/events)
- Organizatörler: [Shipin](https://www.shipin.city/), [Garaj X TEKMER](https://garajx.com.tr/)
- Önceki Garaj X etkinlikleri: [Mart](https://luma.com/w8pheoab), [Nisan](https://luma.com/rai7mi3d)

### Sonraki ürün araştırması (25 Eyl 2026 gece)

Bulguların özeti PROJECT.md "Blokörler: ne bulundu?" bölümünde. Buradakiler kaynaklar.

**Referanslar ve rakipler**
- **RE/MAX:**
  - [hakkımızda](https://remax.com.tr/en/hakkimizda), [ofis dizini](https://www.remax.com.tr/offices)
  - [haritada arama](https://www.remax.com.tr/tr/haritada-arama)
  - [ChatGPT uygulaması koşulları](https://www.remax.com.tr/tr/chatgpt-app-kullanim-kosullari): "yatırım tavsiyesi … niteliğinde değildir"
  - "API Erişim Talebi" formu: remax.com.tr/tr altbilgisinde
- **Fine Estate adayları** (hiçbiri Ankara'da değil):
  - [Fine & Country](https://www.fineandcountry.com/about/why-fine-country)
  - [Türkiye Sotheby's](https://www.prnewswire.com/news-releases/sothebys-international-realty-opens-office-in-turkey-301895337.html)
  - [EV Bodrum](https://evbodrum.com/en/about-us/): eski Engel & Völkers lisansı, 2021'de bitmiş
- **Ankara premium:**
  - [TRUEMAX bölge raporları](https://www.truemaxgayrimenkul.com/bolge-raporlari/): kaynaksız rakamlar, "garanti" dili
  - [Coldwell Banker Ankara ofisleri](https://www.cb.com.tr/en/offices/ankara)
- **Emlakjet + Endeksa:**
  - [yöntem](https://www.emlakjet.com/verilerimiz)
  - [Çayyolu sayfası](https://www.emlakjet.com/satilik-konut/ankara-cankaya-cayyolu-mahallesi)
  - [EmlakZeka feragatnamesi](https://www.emlakjet.com/emlakzeka)
  - [birleşme (AA)](https://www.aa.com.tr/tr/isdunyasi/gayrimenkul/emlakjet-ve-endeksa-guclerini-birlestiriyor/700687)
- [EvSkor](https://evskor.net/): RE/MAX'in kullandığı mahalle yorum verisi

**İlan kaynağı**
- **sahibinden API'si:**
  - [Rekabet Kurulu kararı 25-23/574-365](https://www.rekabet.gov.tr/Karar?kararId=f5a4294d-b953-4a07-96c8-189f8c1c505e)
  - [yardım 1](https://yardim.sahibinden.com/hc/tr/articles/19749005158172), [yardım 2](https://yardim.sahibinden.com/hc/tr/articles/19780244786460)
  - [başvuru formu](https://www.sahibinden.com/veri-transferi-formu)
- [Emlakjet'in sahibinden API'sini kullanması](https://www.emlakjet.com/blog/api-ile-ilan-transfer-sistemi-nedir-ve-nasil-kullanilir)
- [Hepsiemlak geliştirici portalı](https://developers.hemlak.com): Cloudflare nedeniyle okunamadı (D)
- **EİDS:**
  - [entegre firma listesi, 17 Eyl 2026 (257 firma)](https://icticaret.ticaret.gov.tr/duyurular/tasinmaz-ilanlarinda-eidsye-entegre-olan-firmalara-iliskin-duyuru-eylul-2026)
  - [Bakanlık yetki doğrulama duyurusu](https://ticaret.gov.tr/kurumsal-haberler/elektronik-ilan-dogrulama-sistemi-eids-yetki-dogrulama-uygulamasi-hayata-gecirildi)
  - [entegrasyon dokümanı v2.2](https://www.kayserito.tr/dokuman/eids-yetki-dogrulama-uygulama-esaslari-ve-faz1-faz2-dokumanlar.pdf)
  - [uygulama esasları (TOBB yazısı)](https://www.naztic.org.tr/eids-yetki-dogrulama-sistemi-uygulama-esaslari/)
- [RG 31 Ağu 2023, 32295](https://www.resmigazete.gov.tr/eskiler/2023/08/20230831-6.htm): platform yükümlülükleri
- **CRM ve portföy yazılımları** (akış ofis → portal):
  - [RE-OS](https://re-os.com/entegrasyonlar)
  - [Emlaksis](https://suaresoft.com/emlak-ilan-sistemi/)
  - [PortföyCRM](https://www.portfoycrm.com/)
- Tek emlakçı yetkisi ve sözleşmenin e-Devlet'e yüklenmesi: yalnızca haber, taslak metin yok (D). [Karar](https://www.karar.com/ekonomi-haberleri/gayrimenkul-ilanlarinda-yeni-donem-birden-fazla-emlakciya-yetki-devri-2074152)

**Hukuk**
- **Taşınmaz Ticareti Hakkında Yönetmelik:**
  - [güncel metin](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=24645&MevzuatTur=7&MevzuatTertip=5)
  - [TTBS belge sorgu](https://ttbs.gtb.gov.tr/Home/BelgeSorgula), [TTBS SSS](https://ttbs.gtb.gov.tr/Home/SikcaSorulanSorularDok)
- [Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=20435&MevzuatTur=7&MevzuatTertip=5): son değişiklik RG 1 Tem 2026
- **Reklam Kurulu bültenleri:**
  - Adres kalıbı: `ticaret.gov.tr/data/5d1c9edd13b87615344cd4c8/_nnn_Reklam_Kurulu_Basin_Bulteni.pdf`
  - Metafor Ankara: 365. bülten
  - Arsavev: 369. bülten
- [Meta'ya EİDS cezası](https://ticaret.gov.tr/haberler/ticaret-bakanligi-sosyal-medyadaki-sahte-ilanlara-gecit-vermiyor-eids-kurallarina-aykiri-paylasimlara-karsi-yaptirimlar-kararlilikla-uygulaniyor)
- [Güvenli ödeme sistemi 1 Ekim 2026](https://ticaret.gov.tr/haberler/tasinmaz-satislarinda-guvenli-odeme-sisteminin-devreye-alinma-tarihi-1-ekim-2026ya-ertelendi)
- [Emlak sektörüne kesilen cezalar](https://ticaret.gov.tr/haberler/emlak-sektorune-yonelik-faaliyetler-ve-uygulanan-idari-para-cezalarina-iliskin-basin-aciklamasi): 782 firma, 88,9 mn TL
- [SPK izinsiz faaliyetler](https://spk.gov.tr/yatirimcilar/izinsiz-sermaye-piyasasi-faaliyetleri): taşınmazdan söz etmiyor

**Mahalle fiyat geçmişi**
- [REIDIN Ağu 2026 sonuçları](https://reidin.com/reidin-residential-property-price-indices-august-2026-results/), [R-INSIGHT](https://reidin.com/r-insight/)
- **Emlakjet sözleşmeleri:**
  - [kullanım koşulları](https://www.emlakjet.com/kullanim-kosullari): md. 6.2 kazıma ve ticari kullanım yasağı
  - [üyelik sözleşmesi](https://www.emlakjet.com/uyelik-sozlesmesi): md. 9.3
- [TCMB KFE metaverisi](https://www.tcmb.gov.tr/wps/wcm/connect/b4628fa9-11a7-4426-aee6-dae67fc56200/KFE-Metaveri.pdf): kaynak kredi değerlemeleri, mikro veri gizli
- **MKK GABİM:**
  - [hakkında](https://www.mkkgabim.com.tr/kurumsal/hakkimizda)
  - [TADEVES değişken seti](https://cdn.mkkgabim.com.tr/uploads/20260203_TasinmazDegerlemeDegiskenSeti_doldurulacakAlanlar_v2.xlsx): mahalle, ada, koordinat, m² değeri
  - [TDUB 2025 rapor sayıları](https://tdub.org.tr/uploads/documents/1775112360_8eb9577411988bbbaef9.pdf): Ankara 77.941 rapor
- **TKGM:**
  - [Değer Bilgi Merkezi duyurusu](https://www.csb.gov.tr/bakan-kurum-deger-bilgi-merkezi-ile-turkiye-adil-ve-erisilebilir-tasinmaz-degerleme-sistemine-kavusacak-bakanlik-faaliyetleri-41653)
  - [Gölbaşı toplu değerleme pilotu](https://www.tkgm.gov.tr/tasinmaz-degerleme-dairesi-baskanligi/projeler/tasinmaz-degerleme-dairesi-baskanligi-ankara-ili-golbasi-ilcesi-toplu-degerleme-pilot-projesi)
- [Gülnerman Gengeç ve Memişoğlu Baykal 2025](https://dergipark.org.tr/tr/pub/rsgis/article/1731127): Çankaya mahalle m² 2020–2024, Endeksa'dan; CC BY-NC-ND; tablo yok
- [BETAM sahibindex Eyl 2026](https://betam.bahcesehir.edu.tr/2026/09/sahibindex-satilik-konut-piyasasi-gorunumu-eylul-2026/): Ankara ilan m² 39.636 TL, reel −%2,9
- [Gölbaşı arsa rayiç değerleri](https://ebelediye.golbasi.bel.tr/ebelediye/bilgilendirme/arsaRayic.xhtml): 1986–2026, idari değer
- **Yayımlanmış eski premium mahalle noktaları:**
  - [2013, Hürriyet Emlak endeksi](https://www.memurlar.net/album/2343/iste-turkiye-nin-en-degerli-semtleri.html)
  - [2014](https://www.fortuneturkey.com/iste-turkiyenin-en-degerli-semtleri-2568)
  - [Ağu 2026, Emlakjet](https://www.yeniankara.com.tr/cankaya/cankayanin-en-pahali-mahallesi-hangisi-iste-ankaranin-prestij-haritasi-180054)
  - 2015–2024 arasında kaynaklı mahalle noktası bulunamadı.

**ABB, premium aks** (PROJECT.md tablosu)
- `deprem/ilceMahalleRapor/MapServer/2`, `plan/PlanRaporu/MapServer/2,3,4`; sunucular ABB bölümünde.
- Rezerv yapı alanı: [ÇŞB plan dosyası (2023)](https://webdosya.csb.gov.tr/db/ankara/duyurular/plan-dosyasi-20231215143640.pdf), [Yeni Ankara (1 Şub 2026)](https://www.yeniankara.com.tr/ankara/ankarada-milyarlik-arazi-bilmecesi-yarginin-iptal-ettigi-proje-deprem-kilifiyla-geri-mi-donuyor-153536). ÇŞB dosyası sertifika hatası verdi, okunamadı.
- İtfaiye alanı: [soL](https://haber.sol.org.tr/haber/cayyolunda-itfaiye-alanina-ticaret-plani-belediye-meclisinin-ilahlastigi-anlara-taniklik)

**Güç ölçümleri (26 Eyl 2026 gecesi, 11 ilçe; değerler `build.py` içinde `GUC_HAM`)**
- ABB, ilçe katmanı: bina yapım dönemi. `planaski…/deprem/ilceMahalleRapor/MapServer/3`
- ABB, UİP ve NİP değişiklik sınırları: toplam sayı, 2020 sonrası, davalı (iptal, YD, kısmi iptal). İlçe poligonuyla kesişen sayıldı. `baskentcbs…/plan/PlanRaporu/MapServer/3`, `/4`
- ABB, kentsel dönüşüm alanları: `…/PlanRaporu/MapServer/2`
- ABB, raylı istasyonlar: `…/kentrehberi/ego_kent_Rehberi/MapServer/4` (metro), `/5` (Ankaray), `/6` (Başkentray)
- ABB, su baskını kayıtları 2017–2025: 20.990 nokta, ilçe alanına göre sayıldı. `…/hidroloji_analizi/Ankara_Hidroloji_Analizi/MapServer/0`
- ABB, diri fay: `planaski…/deprem/diriFay/MapServer/0`. Türkiye geneli katman; 11 ilçenin içinde fay yok, en yakın nokta Kızılay'a 39,5 km.
- ABB, yerleşime uygunluk: `…/jeolojikEtut/jeolojikEtut/MapServer/1`. Çoğu ilçede boş ya da hata veriyor, kullanılmadı.
- OSM, Overpass: `amenity=school`, `leisure=park`, `amenity=hospital|clinic` sayısı, ilçe relation alanında. © OpenStreetMap katkıcıları, ODbL.
- ABB, plan adası (emsal, kat): `…/plan/UIP_Goruntuleme/MapServer/19`. Yalnızca 18 premium mahallede, mahalle ölçümü için.

**Bu turda erişilemeyenler ve iz**
- Araştırma ajanlarının web arama kotası (200) doldu.
  - MLS ve oda girişimleri, SPK III-37.1 tebliği ve 2015–2024 mahalle fiyatları yarım kaldı.
  - Bu konularda "bulunamadı", "yok" demek değil.
- **Okunamayanlar:**
  - endeksa.com: JavaScript ve bot kontrolü
  - hepsiemlak.com: 403
  - sahibinden.com ana sitesi: 403
  - EİDS taşınmaz yetki API dokümanı (Faz 2)
- **robots.txt ihlali:** Ajanlardan biri, remax.com.tr'nin robots.txt'de kapattığı `?page=` yoluna 11 istek attı. Fark edince durdu ve izinli sitemap'e geçti.

### Erişilemeyenler

- **Kazıma engelli:**
  - Hepsiemlak ve sahibinden: 403 (Cloudflare)
  - endeksa.com
  - Emlakjet geçmiş API'si: captcha
- **Sayfası JavaScript uygulaması, okunamadı:** TÜİK ve EVDS3 portalları
- `acikveri.ankara.bel.tr` çözülmüyor.
- **ABB tarafı:**
  - Şeffaf Ankara API'si istek gövdesini şifreliyor, token istiyor.
  - ArcGIS'in `icdp_yeni` klasörü token istiyor.
  - 2025 faaliyet raporu yalnızca görüntü.
  - e-imar'ın TKGM vekili resmî bir API değil, kullanılmaz.
- **Etkinlik tarafı:** Shipin'in Instagram/LinkedIn'i, etkinlik adresi

### Güvenilmez bulunanlar

- **HaberGo:** M4'ü Koru/Bilkent'e bağlıyor. Birkaç yerel site yapay zekâ üretimi gibi; kaynak yapılmaz.
- **evarsadegeri:** "Mar 2026" ilçe rakamları bayat görünüyor.
- **Wikipedia Kayaş koordinatı yanlış:** Kızılay'ı gösteriyor.
- **Tarih çelişkileri:** M1 açılışı 28 mi 29 Ara 1997 mi; M3 12 Şub mu 13 Mar 2014 mü.
- **Natoyolu–Ege "+%40–50" iddiası:** enflasyonun çok altında, M4'e bağlanmış ama M4 oraya gitmiyor.

---

## Repoda neler var?

| Dosya | İçerik | Nasıl üretildi |
|---|---|---|
| `PROJECT.md` | spec: ürün, sınıflama kuralı, veri, akış, Lovable promptları | elle |
| `data/ilceler.geojson` | 11 ilçe poligonu, `properties.id` ile | OSM Nominatim, relation ID'leriyle |
| `data/ilceler.json` | 11 ilçe: fiyat (2019, 2020, 2026), Ankara medyanına göre oran, sınıf, kural, neden, olaylar | `build.py` |
| `data/projeler.json` | 49 proje: raylı, hastane, kurum, AVM, dönüşüm, imar, yol, havalimanı, risk. Durum, tarih, ilçe, geometri, kaynak. | `build.py` |
| `data/build.py` | Seed verisi (fiyatlar, projeler, koordinatlar, ABB bina sayıları) ve v1 sınıflama kuralı (yapı + emsal) | `python3 data/build.py`; hatları her çalıştırmada OSM API'sinden çeker |

## Lisans ve atıf nasıl?

- **Harita verisi:**
  - © OpenStreetMap katkıcıları, ODbL.
  - Uygulamada atıf görünür olmalı.
- **Fiyatlar:**
  - Endeksa (Emlakjet), yayımlanmış rakamlar, atıfla.
  - [Kullanım koşulları](https://www.emlakjet.com/kullanim-kosullari) kazımayı ve ticari veritabanı kullanımını yazılı izin olmadan yasaklıyor.
  - Etkinlik sonrası ürün olacaksa lisans gerekir.
- **Wikipedia:** metin CC BY-SA. Tarih ve koordinat gibi olgular kullanılıyor, metin kopyalanmıyor.
- **ABB açık verisi (Şeffaf Ankara):** [lisans](https://seffaf.ankara.bel.tr/resources/images/hakkimizda/lisans.pdf) atıfla ticari kullanıma izin veriyor.
- **ABB ArcGIS sunucusu:**
  - Kullanım koşulu bulunamadı; Şeffaf Ankara lisansının kapsayıp kapsamadığı belli değil.
  - Toplu çekim ya da ticari kullanımdan önce ABB CBS biriminden yazılı izin alınmalı.
  - Yalnızca plan katmanları yaklaşık 400 bin poligon.
