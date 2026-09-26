# bandl

Ankara'nın ilçelerini **değerlenebilir / değer korur / değeri düşer** diye sınıflayan
ve bu sınıfın nedenini, haritada gösterilen projelere ve tarihte olanlara kaynaklı olarak
bağlayan harita. MVP Ankara; sonra Türkiye, sonra dünya.

Yapım: `bandl-app` reposu, tek dosya Leaflet (Lovable 26 Eyl'de denendi, bırakıldı). İlk sahne: 26 Eyl 2026, GarajX "Ship in Ankara", yapıldı.

---

## Sonraki ürün: ne olacak?

**Damla, 25 Eyl 2026 gece:** "maps + sahibinden + hürriyet emlak karışımı ama üstüne yatırım
tavsiyeli, remax / fine estate gibi, ama 10-20m'a ev alabilecek insanlar için".

Yani:
- haritada ilan (sahibinden / Hürriyet Emlak gibi)
- üstünde bandl'ın yatırım katmanı: sınıf, neden, emsal
- premium aracı duruşu (RE/MAX, Fine Estate)
- hedef: 10–20 milyon TL bütçeli alıcı

Etkinlik MVP'si bunun ilk parçası (yatırım katmanı).

**Karar (Damla, 25 Eyl 2026 gece):** "almayacağım sadece ürün çıkartıyorum". Komisyon yok, aracılık yok.
- Emlakçı yetki belgesi gerekmiyor, fiziksel ofis gerekmiyor.
- İlan gösterildiği an bandl hukuken "ilan platformu" oluyor (TTY m.12/2). O zaman EİDS entegrasyonu zorunlu.
- EİDS kodunu Bakanlık "ilanlara elektronik ortam sağlayan gerçek veya tüzel kişilere" veriyor (entegrasyon dokümanı v2.2). Yani şirket şartı yazmıyor. Başvuru yolu da yazmıyor: eids@ticaret.gov.tr.

### Plan: ürün ne, veri nereden?

| Ekranda | Veri | Bugün durum |
|---|---|---|
| Harita: premium aks mahalleleri | ABB: bina yaşı, plan değişikliği, dava, dönüşüm alanı; raylı hatlar | 18 mahalle çekildi. Ticari kullanım için ABB'den yazılı izin şart. |
| İlan pinleri ve ilan kartı (fiyat, m², mahalle) | EİDS'ten sonra: ofislerin sahibinden anahtarı, RE/MAX API'si, malikin kendi ilanı | EİDS yok, ilan yok |
| İlan kartında "bu parselin çevresinde ne değişti?" | İlandaki ada/parsel (EİDS'te zorunlu) + ABB imar adası, plan değişikliği, dava | İlan gelince birleşir. Kimse göstermiyor; Emlakjet'in skorunda bunlar yok. |
| Mahalle sınıfı (değerlenebilir / korur / düşer) | Mahalle fiyat geçmişi | Yok. Endeksa ya da REIDIN lisansı gerek. Platformun kendi ilan fiyatları zamanla seri olur (sahibinden API koşulu buna izin veriyor mu (D)). |

**Sıra:**
1. ✅ **26 Eyl, GarajX:** ilçe MVP'si canlı (bandl.noseydewdrop.com, repo `bandl-app`, Leaflet). Demo yapıldı. Lovable kullanılmadı.
2. **Mahalle katmanı:**
   - Ben: 18 premium mahalle verisini `data/`ya kaynaklı yazarım, Lovable promptunu hazırlarım.
   - Sen: ABB CBS birimine izin e-postası gönderirsin; taslağı ben yazarım.
3. **EİDS:** eids@ticaret.gov.tr'ye "gerçek kişi olarak entegre olabilir miyim, şartlar ne?" diye sorulur. Taslağı ben, göndereni sen.
4. **İlk ilanlar:** sahibinden API'si ofis ofis çalışıyor, her ofis bandl'a kendi anahtarını vermeli.
   - Hedef mahallelerdeki ofislerle görüşülür: RE/MAX'in Ankara'da 47 ofisi var, Oran ve Dikmen'de yok.
   - RE/MAX API formu doldurulur.
5. **Fiyat:** Endeksa ve REIDIN'e lisans fiyatı sorulur.

**10–20 milyon TL ne alır?** Endeksa, Ağu 2026 m² fiyatlarıyla:

| Yer | TL/m² | 10–20 mn TL ile |
|---|---|---|
| Bahçelievler | 119.654 | 84–167 m² |
| Oran | 116.714 | 86–171 m² |
| Beytepe | 108.311 | 92–185 m² |
| Çayyolu | 106.950 | 94–187 m² |
| Ümitköy | 96.246 | 104–208 m² |
| Yukarı Dikmen | 95.846 | 104–209 m² |
| Çukurambar | 83.292 | 120–240 m² |
| Yaşamkent | 82.932 | 121–241 m² |
| İncek | 80.177 | 125–249 m² |
| Gölbaşı (ilçe) | 73.190 | 137–273 m² |
| Çankaya (ilçe) | 66.165 | 151–302 m² |
| Ankara ortalaması | 39.478 | 253–507 m² |

**Sonuç:**
- Bu bütçe premium mahallelerde 3+1 / 4+1 alan aile alıcısı. Batı ve güney aksı: Çankaya
  batısı, Çayyolu–Ümitköy–Yaşamkent, Oran–Dikmen, Gölbaşı–İncek.
- v1'in ilçe düzeyinde "değerlenebilir" dediği yerler (Çubuk, Akyurt, Sincan) bu alıcının baktığı yer değil.
- **Bu ürün mahalle düzeyinde, premium aksta analiz ister.** Sıradaki asıl iş bu.

### Model: neye göre artar, neye göre azalır?

**Damla, 26 Eyl 2026:** "progresif ve geçmişle birleşik"; "neye göre artar azalır diyeceksin".
Örnekleri: "Beytepe hep arttı ama bence artmayacak", "Yaşamkent artacak, metro onayı geldi",
"Çukurambar elit diye bin tane bina yapılınca bunaltıcı oldu".
Kuralı Damla ya da ben yazmıyoruz; sistem veriden buluyor.

**Güçler.** Her biri 1.437 mahallenin hepsi için, her yıl, ücretsiz veriden ölçülür:

| Güç | Nasıl ölçülür | Veri | Durum |
|---|---|---|---|
| Merkezden çevreye kayış | Kızılay'a uzaklık | OSM | ilçe düzeyinde ölçüldü, r = +0,85 |
| Yapılaşma baskısı (Çukurambar) | plana göre izinli inşaat alanı/km², yıllık plan değişikliği, yeni bina payı | ABB plan adası (emsal, kat), PlanRaporu, bina dönemi | 18 mahallede çekildi |
| Erişim | raylı durağa uzaklık ve aşama (plan / ihale / yapım / açık) | ABB istasyonlar, EGO, OSM | ilçede istasyon yoğunluğu ölçüldü; durağa mesafe hesaplanmadı |
| Kurum girişi ve çıkışı | hastane, üniversite, bakanlık açılışı ve kapanışı | `projeler.json` | ilçe düzeyinde örtüşme var (Altındağ −8, Çankaya +12) |
| Stok yaşı ve dönüşüm | 1998 öncesi bina payı, dönüşüm alanı | ABB | 18 mahallede çekildi |
| Hukuki risk | plan iptali, yürütmeyi durdurma | ABB PlanRaporu | 18 mahallede çekildi |
| Doğal risk | diri fay, sel, zemin | ABB deprem ve jeoloji katmanları | ilçe düzeyinde ölçüldü (aşağıda) |
| Donatı | okul, park, sağlık tesisi sayısı | OSM | ilçe düzeyinde ölçüldü (aşağıda) |

**Ağırlıkları kim veriyor?**
- Ankara'nın kendi geçmişi. Her mahallenin yıllara göre göreli fiyat değişimi bu güçlerle karşılaştırılır. Sistem, hangi gücün Ankara'da ne kadar etki ettiğini böyle öğrenir.
- Sonra "şu anda" her mahalleye bir yön verir ve her gücün o yöne katkısını gösterir.
- Engel: bunun için yıllara yayılmış mahalle fiyat serisi gerekiyor.
  - 2014 metro açılışlarını kapsayan tek seri REIDIN (2007'den beri).
  - Endeksa 2020'de başlıyor.
  - Güçler ücretsiz; ağırlıklar lisansa bağlı.

**İlçe düzeyinde ölçüldü (26 Eyl 2026 gecesi, 11 ilçe, 2019–2026 göreli değişim). MVP'ye giren budur.**
- Hüküm sayıdan çıkıyor, elle yazılmıyor (`build.py`, `guc_hukum`).
- Hüküm kuralı:
  - Tek bir ilçe çıkarılınca r'nin işareti değişiyorsa: **kararsız**
  - |r| < 0,3 ise: **tutmadı**; |r| < 0,5 ise: **zayıf**
  - Uzaklık sabit tutulunca |r| ≥ 0,5 kalıyorsa: **uzaklıktan bağımsız**; kalmıyorsa: **uzaklığın yansıması**

| Güç | r | Bir ilçe çıkarılınca | Uzaklık sabitken | Hüküm |
|---|---|---|---|---|
| Kızılay'a uzaklık | +0,85 | +0,78 … +0,91 | — | ana güç |
| 2018 sonrası bina payı | +0,87 | +0,83 … +0,92 | +0,66 | uzaklıktan bağımsız |
| bina yoğunluğu | −0,72 | −0,78 … −0,67 | −0,14 | uzaklığın yansıması |
| 1998 öncesi bina payı | −0,74 | −0,84 … −0,66 | −0,29 | uzaklığın yansıması |
| raylı istasyon (/10.000 bina) | −0,60 | −0,75 … −0,51 | +0,10 | uzaklığın yansıması |
| su baskını kaydı 2017–2025 | −0,58 | −0,74 … −0,43 | −0,21 | uzaklığın yansıması |
| okul (/1000 bina) | −0,72 | −0,85 … −0,65 | −0,33 | uzaklığın yansıması |
| hastane ve klinik (/1000 bina) | −0,62 | −0,74 … −0,51 | +0,20 | uzaklığın yansıması |
| kentsel dönüşüm alanı | −0,47 | −0,56 … −0,20 | +0,39 | zayıf |
| park | −0,37 | −0,49 … −0,29 | −0,30 | zayıf |
| 2020'den beri plan değişikliği | −0,25 | −0,39 … +0,08 | +0,23 | kararsız |
| davalı plan payı | +0,25 | −0,04 … +0,75 | +0,58 | kararsız |
| kurum girişi − çıkışı | +0,38 | −0,05 … +0,44 | +0,55 | kararsız |
| diri fay | — | — | — | ayırt etmiyor: 11 ilçenin hiçbirinde yok, en yakını Kızılay'a 39,5 km |
| yerleşime uygunluk | — | — | — | ölçülemedi: ABB jeolojik etüt katmanı çoğu ilçede boş ya da hata veriyor |

**Okuma:**
- 2019–2026'da Ankara'yı iki güç sürükledi: merkezden uzaklık ve yeni yapı.
- Metro, okul, sel, eski stok fiyatla birlikte hareket ediyor, ama bu merkez–çevre farkının yansıması.
- Yeni yapı payının sonucu Damla'nın Çukurambar sezgisinin (çok bina → düşüş) tersi. Ama iki uyarıyla:
  - Endeksa ilan tabanlı; yeni binalar arttıkça ortalama karışım yüzünden de yükselir.
  - Çubuk ve Akyurt'ta binaların yalnızca %11 ve %25'inin dönemi girilmiş. Bu iki ilçe çıkarılınca r +0,86, uzaklık sabitken +0,68.
- Mahalle düzeyinde, bugünkü fiyat seviyesinde tersi görüldü (yeni bina payı ~ fiyat r = −0,51, 9 mahalle). Değişim ölçülmedi.

**Sınıf kuralı değişmedi (v1).** Güçler panelde "neye göre" olarak görünüyor.
- Her ilçede her gücün değeri ve 11 ilçe içindeki sırası var.
- Hüküm "ana" ya da "bağımsız" ise bir yön de var: bu ilçenin değeri medyanın hangi tarafında ve Ankara'da o taraf ne yaptı.
- "Gelecek" listesi: bekleyen her proje, türüne göre Ankara emsaliyle.

**İlk ölçüm (mahalle): yapılaşma baskısı.**
- Ölçü: plan adası başına alan × emsal, toplamı mahalle km²'sine bölünerek. 25–26 Eyl 2026'da 18 mahalle ölçüldü.
- Sonuçlar (plana göre izinli inşaat alanı, m²/km²):

  | Mahalle | m²/km² |
  |---|---|
  | Kızılırmak | 1.124.776 |
  | Beytepe | 919.055 |
  | Çukurambar | 710.794 |
  | Söğütözü | 697.097 |
  | Yukarı Dikmen | 486.492 |
  | Yaşamkent | 468.198 |
  | Çayyolu | 290.970 |
  | Ümit | 223.637 |
  | Oran | 54.537 |

- **Bu ölçüde Beytepe, Çukurambar'dan yüksek.**
- Zayıf yanlar:
  - Adaların yalnızca yaklaşık yarısında emsal girilmiş. Bahçelievler ve Gaziosmanpaşa'da neredeyse hiç yok; o ikisi ölçülemedi.
  - Kullanım (konut / kampüs / ticaret) ayrılmadı.
  - Tek örnek kanıt değil.

### Blokörler: ne bulundu? (25 Eyl 2026 gece)

(D) = doğrulanmadı. TTY = Taşınmaz Ticareti Hakkında Yönetmelik, güncel metin 29 Nis 2026 değişikliğine kadar.
Kaynak linkleri README'de, "Sonraki ürün araştırması" bölümünde.

**1. Referanslar: RE/MAX ve "Fine Estate" ne sunuyor?**
- **"Fine Estate" adlı bir Türk şirketi bulunamadı.**
  - Alan adları çözülmüyor, LinkedIn sayfaları 404 veriyor.
  - Ada en yakın aday Fine & Country; Türkiye'de ofisi yok.
  - Türkiye Sotheby's Realty İstanbul, Bodrum ve Antalya'da; Ankara'da yok.
  - Hangisinin kastedildiği belirsiz.
- **RE/MAX Türkiye:**
  - Master franchise (Enrichers A.Ş.), 311 ofis. Ankara'da 47 ofis, 1.025 kişi.
  - Hedef mahallelerde ofisi var: Çayyolu, Ümit, Konutkent, Alacaatlı, Beytepe, Yaşamkent, İncek. Oran ve Dikmen'de yok.
  - remax.com.tr'de olanlar: harita araması, EİDS rozeti, Hepsiemlak'tan alınan endeks, EvSkor mahalle yorumu.
  - Olmayanlar: fiyat geçmişi, yatırım skoru. Değerleme ve yatırım tavsiyesini açıkça reddediyor.
- **İlanın üstüne yatırım skoru koyan zaten var: Emlakjet + Endeksa.**
  - İlanlar yatırım skoruna, geri dönüş süresine ve kira gelirine göre sıralanabiliyor.
  - Çayyolu örneği: 106.950 TL/m², yıllık +%41,2 nominal, geri dönüş 20 yıl.
  - Skorun girdileri: fiyat, bölge, konum, yapı, risk (sel, heyelan, enerji hattı).
  - Plan değişikliği, meclis kararı ve dava girdi değil.
- **Çayyolu'ndaki butik TRUEMAX** kaynaksız "yıllık +%50" rakamı ve "garanti" dili kullanıyor (bkz. madde 4).

**2. İlanlar nereden gelir?**
- **Başkasının ilanını gösteren site hukuken "ilan platformu"** (TTY m.12/2).
  - EİDS entegrasyonu zorunlu: kimlik doğrulaması ve malik/yetki doğrulaması.
  - Platformdan yetki belgesi istenmiyor.
- **EİDS'e entegre 257 firma var** (Bakanlık listesi, 17 Eyl 2026).
  - Listede Emlakjet, Hepsiemlak ve sahibinden'in yanında Remax, Century21, Turyap, Endeksa var.
  - Tokur Emlak gibi küçük bir Ankara ofisi de var. Yani küçük oyuncu da entegre olabiliyor.
- **sahibinden API'si:** Rekabet Kurulu kararıyla açıldı (2023; uyum tespiti 26 Haz 2025).
  - Yalnızca EİDS'e entegre ilan platformlarına açık.
  - Her ofisin kendi anahtarını vermesi gerekiyor; toplu ya da bölge bazlı veri yok.
  - İlan yalnızca o platformda ilan olarak yayınlanabilir.
- **RE/MAX'in "API Erişim Talebi" formu var** (site kodunda doğrulandı).
  - Kapsam: yalnızca yayındaki ilanlar ve sitede herkese açık görünen bilgiler.
  - Koşulları görülmedi (D).
- **Diğer portallar:**
  - Hepsiemlak'ın geliştirici portalı ilan yüklemek için (akış ofis → portal); dışarıya veri vermiyor (D).
  - Emlakjet'in dışarıya API'si bulunamadı.
  - Zingat kapandı. Hürriyet Emlak artık Hepsiemlak (301 yönlendirme).
- **Türkiye'de açık bir MLS yok.** Yalnızca kapalı havuzlar var: RE-OS MLS, Emlakjet Portföy Paylaşımı.
- **EİDS ilanında il, ilçe, ada ve parsel değiştirilemez şekilde yazılı.** İlan parsel düzeyinde haritaya ve ABB imar adasına bağlanabilir.

**3. Aracılık ve yetki belgesi**

| Ürün şekli | Ne gerekiyor | Ceza (2026) |
|---|---|---|
| Sadece analiz | Yetki belgesi isteyen hüküm bulunamadı. Reklam ve tüketici kuralları, KVKK, İYS geçerli. | internet reklamı 1,08–10,8 mn TL |
| Analiz + başka sitedeki ilana link | "Platform" sayılıp sayılmadığı belirsiz (D). Bakanlık EİDS'siz ilanlar yüzünden Meta'ya 5 mn TL ceza kesti (13 Haz 2026). | 28.620–286.206 TL/aykırılık |
| İlan platformu | EİDS; üye ofisin yetki belgesini kontrol; müşteri hizmeti; kayıtları 10 yıl saklama. Platformun kendisine yetki belgesi gerekmiyor. | aynı |
| Aracı (emlak ofisi) | Yetki belgesi (aşağıda) | 28.620–858.620 TL/aykırılık, belge iptali |

- **Yetki belgesi şartları:**
  - oda ve vergi kaydı
  - MYK Seviye 5 belgeli sorumlu danışman, 100 saat eğitim
  - ayrı işyeri: ev olamaz, aynı yerde başka ticari iş yapılamaz
  - yıllık harç: Ankara'nın merkez ilçelerinde 40.000 TL
  - komisyon üst sınırı: toplam %4 + KDV
- **Lead ya da referans ücreti:**
  - Mevzuatta bu ifadeler geçmiyor.
  - TBK m.520 simsarlığı "sözleşme fırsatını göstermek" diye geniş tanımlıyor (Yargıtay 3. HD, 2026).
  - Satışa bağlı ücret aracılık sayılabilir (D). Doğrudan karar bulunamadı.

**4. "Yatırım tavsiyesi" dili**
- **Konut sermaye piyasası aracı değil.** Konut için SPK yatırım danışmanlığı lisansı gerekmiyor.
  - GYO, GYF ya da gayrimenkul sertifikası önerilirse gerekir. İzinsiz faaliyetin cezası 2–5 yıl hapis.
- **Asıl risk reklam hukuku.** İddiayı ispat yükü iddia edende (6502 m.61/6).
  - Reklam Kurulu "Metafor Ankara ile Güvenli Gelir, Karlı Yatırım" reklamına 863.580 TL ceza kesti (13 Oca 2026).
  - Rakamlar gerçek bir fonun verisiydi. Ceza, açıklama ana mesajda yer almadığı ve reklam "kesin kazanç" algısı yarattığı için verildi.
  - Arsavev'in "%40 getiri" iddiası ispatsız bulundu; 1,08 mn TL ceza.
- **"Yatırım tavsiyesi değildir" dipnotu ana mesajdaki vaadi ortadan kaldırmaz** (Reklam Yönetmeliği m.18/6).
- **1 Ağu 2026'dan beri:** yapay zekâ tüketicinin ekonomik kararını önemli ölçüde etkiliyorsa bu açıkça belirtilmeli (m.18/8).
- **Kaynaklı sayı bu rejimde savunma, süs değil.**

**5. Mahalle fiyat geçmişi**
- **Açık, işlem tabanlı bir mahalle serisi yok.**
- **Endeksa:**
  - Mahalle düzeyinde, 2020'den beri; sitede 4 yıl geriye gösteriliyor. Model tabanlı.
  - Lisans fiyatı yayımlanmamış. Kazıma ve ticari kullanım yazılı izne bağlı.
- **REIDIN:**
  - Kapsam 1.255 mahalleye çıkmış (81 il, Ağu 2026 raporu). Haz 2007'den beri, ilan tabanlı.
  - Ücretli; fiyat ancak demo talebiyle öğrenilebiliyor. Ankara'daki mahalle listesi bulunamadı.
- **İşlem ve değerleme tabanlı mahalle verisi** iki yerde duruyor: TCMB (konut kredisi değerlemeleri) ve MKK GABİM (değerleme raporları; mahalle, ada, koordinat). İkisi de fiyatı dışarıya vermiyor.
- **TKGM Değer Bilgi Merkezi:** parsel düzeyinde resmî değer. Takvime göre Ankara'ya 2027 ortasında gelecek.
  - Gölbaşı'nda toplu değerleme pilotu yapılmış, sonucu yayımlanmamış.
- **Akademik kaynak:** Çankaya'da mahalle m² fiyatları 2020–2024, Endeksa'dan elle toplanmış (Hacı Bayram Veli Ü., Eyl 2025).
  - Tablo yayımlanmamış.
  - Bulgu: 2024'te Yaşamkent ve Konutkent yüksek fiyat kümesinden çıkmış.

**Tarih uyarısı:** 1 Ekim 2026'dan itibaren nakit, havale ya da EFT ile ödenen her taşınmaz satışı Güvenli Ödeme Sistemi'nden geçiyor (TTY Ek m.1; Bakanlık duyurusu 26 Haz 2026).

### Premium aks: ABB'de mahalle düzeyinde ne var?

25 Eyl 2026'da 18 mahalle için hedefli sorgu yapıldı; toplu çekim yapılmadı. Kaynaklar:
- bina yaşı: `planaski…/deprem/ilceMahalleRapor/MapServer/2`
- plan değişikliği: `baskentcbs…/plan/PlanRaporu/MapServer/3` (UİP) ve `/4` (NİP). Sayıma, orta noktası mahallenin içinde kalan değişiklikler alındı.
- dönüşüm alanı: `/2`

| Mahalle | Bina | 1998 öncesi | 2018 sonrası | UİP değişikliği (2025+) | Dönüşüm alanı (içinde) |
|---|---|---|---|---|---|
| Alacaatlı | 4.480 | %9 | %7 | 256 (14) | 4 (biri iptal) |
| Beytepe | 2.465 | %23 | %13 | 147 (12) | 3 (biri iptal) |
| İncek | 1.706 | %11 | **%27** | 91 (11) | Taşpınar–Kızılcaşar–İncek (2005) |
| Yaşamkent | 1.468 | %5 | %18 | 119 (4) | — |
| Çayyolu | 1.495 | %21 | %0 | 81 (5) | — |
| Ümit (Ümitköy) | 891 | %24 | %2 | 127 (0) | — |
| Yukarı Dikmen | 673 | %23 | %3 | 54 (5); 9'u mahkemece iptal | — |
| Oran | 471 | %47 | %1 | 33 (4) | — |
| Bahçelievler | 659 | %66 | %4 | 7 (0) | — |

**Somut olaylar (ABB plan katmanı):**
- **Koru–Yaşamkent/Bağlıca uzatması:** UİP ve NİP onayı 11 Haz 2025, meclis kararı 831.
- **Çayyolu'nda rezerv yapı alanı planı (16 Şub 2026):** meclis karar numarası yok, yani bakanlık planı.
  - Haberlere göre alan eski askerî bölge, proje Emlak Konut'un 25 lüks konutu.
  - Mahkeme planı iptal etmiş; bakanlık 18 Ara 2025'te alanı yeniden rezerv yapı alanı ilan etmiş (D: tek haber kaynağı).
- **Çayyolu'nda itfaiye alanı ticarete çevrildi:** 43376 ada, meclis kararı 226, 10 Şub 2026.

**Veriyle test (9 mahalle, Endeksa Ağu 2026, yalnızca bugünkü fiyat):**
- 1998 öncesi bina payı ile m² fiyatı arasında r = +0,86. Kızılay'a uzaklık sabit tutulunca da +0,84 kalıyor.
- 2018 sonrası bina payı ile fiyat arasında r = −0,51. En çok yeni arz ve en düşük fiyat İncek'te.
- Bu, fiyat seviyesi; değişim değil. Değişimi ölçmek için mahalle fiyat geçmişi lazım (madde 5).
- Nokta sayısı 9, korelasyon neden göstermez.

Kararı Damla verir.

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
- Mahalle düzeyinde 2007'den geriye giden tek seri REIDIN'de (ücretli, ilan tabanlı; Ağu 2026 raporunda 1.255 mahalle).

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
   - neye göre: Kızılay'a uzaklık düşürür (7/11), 2018 sonrası bina payı düşürür (11/11)
   - gelecek: M4 Şehitler–Forum uzatması, altında Keçiören emsali
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
  olaylar: [{ id, tarih, baslik, tur, durum, not, kaynak_url }],
  gucler: [{ id, ad, deger, birim, sira, n, hukum: "ana"|"bagimsiz"|"golge"|"zayif"|
    "kararsiz"|"tutmadi", hukum_metin, r, kismi, aralik, yon: "yukseltir"|"dusurur"|null,
    not, kaynak_url }],
  gelecek: [{ id, baslik, tur, durum, tarih, hedef, emsal, kaynak_url }] }]
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
5) "neye göre" (field "gucler"). First the items whose hukum is "ana" or
   "bagimsiz", one row each: ad; deger + birim; "{sira}/{n}"; and yon as a word:
   "yükseltir" in #2b5cad or "düşürür" in #c8602a (nothing if null). Under the row,
   hukum_metin in secondary color, "not" in smaller text if not empty, source link.
   Then a plain text toggle "diğer güçler" that expands the rest in two groups:
   hukum "golge" under "uzaklığın yansıması"; "zayif", "kararsiz", "tutmadi" under
   "kanıtı tutmayanlar". Same row without yon. Last line, small: "11 ilçe,
   2019–2026. birlikte hareket etmek neden olmak değildir."
6) "gelecek" (field "gelecek"): baslik, status label, tarih and hedef if present,
   "emsal" in smaller text, source link. If empty: "bekleyen kaynaklı proje yok".
7) "geçmiş" (field "olaylar", skipping items whose id is in "gelecek"): sorted
   by date, newest first: date, title, type, status label, "not" in smaller text,
   source link. If empty: "bu ilçe için kaynaklı olay bulunamadı".
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
