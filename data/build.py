"""bandl seed -> data/ilceler.json + data/projeler.json

python3 data/mahalle.py && python3 data/build.py

Kaynaklar README.md'de. Koordinatlar 25 Eyl 2026'da OSM Nominatim'den alındı;
raylı hat güzergâhları her çalıştırmada OSM API'sinden çekilir.
Sınıflama kuralı PROJECT.md "Nasıl sınıflıyor?" bölümündeki v1 kuralıdır.
"""
import json, math, statistics, time, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

D = Path(__file__).parent
UA = {"User-Agent": "bandl-seed/0.1 (damummyphus@gmail.com)"}

# --- fiyat: Endeksa TL/m2. 2019 ve 2020 Haziran (Baret tablosu), 2026 Ağustos (Emlakjet ilçe sayfası)
BARET = "https://www.baretdergisi.com/ankarada-konut-fiyatlari-2020-yilinin-ilk-6-ayinda-yuzde-799-artti/20007/"
EJ = "https://www.emlakjet.com/emlak-piyasasi/satilik-konut/ankara-"
ILCE = {  # id: (ad, 2019, 2020, 2026)
    "cankaya": ("Çankaya", 2474, 2869, 66165),
    "golbasi": ("Gölbaşı", 2349, 2739, 73190),
    "yenimahalle": ("Yenimahalle", 2064, 2347, 51607),
    "etimesgut": ("Etimesgut", 1794, 2126, 48878),
    "pursaklar": ("Pursaklar", 1589, 1930, 39268),
    "cubuk": ("Çubuk", 1114, 1375, 36227),
    "kecioren": ("Keçiören", 1511, 1711, 36023),
    "altindag": ("Altındağ", 1508, 1594, 33678),
    "sincan": ("Sincan", 1275, 1487, 33605),
    "mamak": ("Mamak", 1335, 1457, 32010),
    "akyurt": ("Akyurt", 943, 1103, 29042),
}

# --- raylı hatlar: OSM relation id
HAT_OSM = {"A1": 456693, "M1": 456707, "M2": 3604162, "M3": 7878077,
           "M4": 7981739, "B1": 14118633, "M5": 19925415}

# --- noktalar (lat, lng), OSM Nominatim / Wikipedia
P = {
    "gar": (39.9359, 32.8417), "bilkent_sh": (39.9008, 32.7569), "etlik_sh": (39.9642, 32.8289),
    "numune": (39.93341, 32.85803), "diskapi": (39.95546, 32.85868), "ankamall": (39.9511, 32.8317),
    "armada": (39.91155, 32.80819), "optimum": (39.96522, 32.63179), "cepa": (39.91242, 32.77781),
    "panora": (39.84884, 32.83236), "acity": (39.94578, 32.76223), "gordion": (39.90038, 32.69133),
    "kentpark": (39.90986, 32.77627), "atlantis": (39.97004, 32.71555), "nextlevel": (39.91142, 32.81347),
    "taurus": (39.88839, 32.8112), "metromall": (39.98321, 32.61066), "portakal": (39.88794, 32.85166),
    "dikmen_vadisi": (39.8853, 32.8467), "ulus": (39.93922, 32.85067), "hidirliktepe": (39.9466, 32.8638),
    "gultepe": (39.9487, 32.8849), "demetevler": (39.96877, 32.78467), "incek": (39.80754, 32.69755),
    "esenboga": (40.1281, 32.9950), "kulliye": (39.9308, 32.7989), "ankapark": (39.94327, 32.78123),
    "kizilay": (39.9208, 32.8540),
    # durak adı taşıyan mahalle merkezleri (yaklaşık güzergâh için)
    "dikimevi": (39.9323, 32.8775), "abidinpasa": (39.9284, 32.8869), "asikveysel": (39.92402, 32.89542),
    "tuzlucayir": (39.9237, 32.9071), "zekidogan": (39.91677, 32.90617), "fahrikoruturk": (39.90995, 32.9228),
    "cengizhan": (39.90005, 32.92395), "aksemsettin": (39.90707, 32.93501), "natoyolu": (39.8928, 32.9330),
    "demirlibahce": (39.9365, 32.8825), "siteler": (39.9576, 32.9076), "solfasol": (39.9798, 32.9077),
    "pursaklar_merkez": (40.03716, 32.89709), "koru": (39.8876, 32.6870), "yasamkent": (39.85841, 32.64387),
    "baglica": (39.89407, 32.64804),
}

def pt(k): return {"type": "Point", "coordinates": [P[k][1], P[k][0]]}
def ln(*ks): return {"type": "LineString", "coordinates": [[P[k][1], P[k][0]] for k in ks]}

W = "https://en.wikipedia.org/wiki/"
DOGRULA = "https://www.dogrula.org/ekipten/ankara-buyuksehir-belediyesi-rayli-sistem-tarihcesi/"

# geometri: "hat:<kod>" = OSM'den, dict = elle, None = haritada yok (panelde var)
# ilceler: geometri None ise elle; değilse poligon testinden
# buyuk: ilçe ölçeğinde tetikleyici (raylı ve hastane zaten sayılır; dönüşümde 5000+ konut)
PROJELER = [
    # raylı
    dict(id="a1", ad="A1 Ankaray AŞTİ–Dikimevi", tur="rayli", durum="acik", tarih="1996-08-30", geometri="hat:A1", kaynak_url=DOGRULA),
    dict(id="m1", ad="M1 Kızılay–Batıkent", tur="rayli", durum="acik", tarih="1997-12-28", geometri="hat:M1", kaynak_url=DOGRULA, not_="kaynaklar 28 ve 29 Aralık diyor"),
    dict(id="m3", ad="M3 Batıkent–OSB Törekent", tur="rayli", durum="acik", tarih="2014-02-12", geometri="hat:M3", kaynak_url=W+"OSB-Törekent_(Ankara_Metro)", not_="kaynaklar 12 Şubat ve 13 Mart diyor"),
    dict(id="m2", ad="M2 Kızılay–Koru", tur="rayli", durum="acik", tarih="2014-03-13", geometri="hat:M2", kaynak_url=W+"Koru_(Ankara_Metro)"),
    dict(id="gar", ad="Ankara YHT Garı", tur="rayli", durum="acik", tarih="2016-10-29", geometri=pt("gar"), kaynak_url=W+"Ankara_Tren_Gar%C4%B1"),
    dict(id="m4", ad="M4 Şehitler–AKM", tur="rayli", durum="acik", tarih="2017-01-05", geometri="hat:M4", kaynak_url=W+"Ankara_Metro"),
    dict(id="b1", ad="Başkentray Sincan–Kayaş", tur="rayli", durum="acik", tarih="2018-04-12", geometri="hat:B1", kaynak_url="https://www.yenisafak.com/ekonomi/dev-proje-bugun-aciliyor-3224470", not_="Temmuz 2016'da kapatılıp yenilendi"),
    dict(id="m4k", ad="M4 AKM–Gar–Kızılay bağlantısı", tur="rayli", durum="acik", tarih="2023-04-12", geometri=None, ilceler=["kecioren"], kaynak_url=W+"Ankara_Metro", not_="Keçiören hattını Kızılay'a bağladı"),
    dict(id="m5", ad="M5 Kızılay–Dikmen", tur="rayli", durum="planli", tarih="2025-04-30", geometri="hat:M5", yaklasik=True, kaynak_url="https://www.ego.gov.tr/sayfa/2284/m5-kizilaydikmen-hatti", not_="15,45 km; kesin proje 30 Nis 2025; 2026 ulusal yatırım programında değil (ABB proje sayfası 179 'tamamlandı' diyor, yanlış). Güzergâh OSM'deki taslaktan"),
    dict(id="a2", ad="Dikimevi–Natoyolu hafif raylı", tur="rayli", durum="yapimda", tarih="2025-06-13", hedef="2029-01-14", yaklasik=True,
         geometri=ln("dikimevi", "abidinpasa", "asikveysel", "tuzlucayir", "zekidogan", "fahrikoruturk", "cengizhan", "aksemsettin", "natoyolu"),
         kaynak_url="https://www.ego.gov.tr/sayfa/2281/dikimevinatoyolu-ankaray-hafif-rayli-sistem-hatti", not_="temel atma 13 Haz 2025, 8 durak; EBRD+AFD 250 M€ kredisi 22 Haz 2023; ABB 2026 programında bütçesi olan tek raylı hat. Güzergâh durak adlarının mahalle merkezlerinden"),
    dict(id="m6", ad="M6 Çayyolu–Sincan", tur="rayli", durum="planli", tarih="2025-12-08", geometri=None, ilceler=["etimesgut", "sincan"],
         kaynak_url="https://yatirimlar.com/haber/ankara-ya-4-yeni-metro-hatti-toplam-44-kilometrelik-dev-ulasim-hamlesi_249147", not_="Bağlıca–Eryaman YHT, 12,5 km; tasarım onayı 23 Tem 2025; 2026 bütçesinde yok (ABB proje sayfası 258)"),
    dict(id="koru_ext", ad="M2 Koru–Yaşamkent ve Koru–Bağlıca uzatması", tur="rayli", durum="planli", tarih="2026-07", yaklasik=True,
         geometri={"type": "MultiLineString", "coordinates": [ln("koru", "yasamkent")["coordinates"], ln("koru", "baglica")["coordinates"]]},
         kaynak_url="https://www.ankara.bel.tr/proje/x-177", not_="9,36 km; UİP ve NİP onayı 11 Haz 2025, meclis karar 831 (ABB plan/PlanRaporu katmanı); 2026 ulusal yatırım programında (RG 15 Oca 2026); meclis 16 Tem 2026 karar 933 dış borçlanma; ihale sonucu bulunamadı"),
    dict(id="m7", ad="M7 Gar–Esenboğa metrosu", tur="rayli", durum="sozlesmeli", tarih="2026-09", yaklasik=True,
         geometri=ln("gar", "demirlibahce", "siteler", "solfasol", "pursaklar_merkez", "esenboga"),
         kaynak_url="https://www.haberankara.com/ankara/pursaklar-esenboga-metro-ihalesi-tamamlandi-319433",
         not_="36 km, 12 durak; üç paket sözleşmesi Ağu–Eyl 2026 (34,0 + 42,4 + 54,4 mlr TL). Güzergâh durak adlarının mahalle merkezlerinden; Keçiören'deki duraklar bulunamadı"),
    dict(id="m4_forum", ad="M4 Şehitler–Forum uzatması", tur="rayli", durum="planli", tarih="", geometri=None, ilceler=["kecioren"], kaynak_url="https://www.ankara.bel.tr/proje/x-178", not_="7,69 km (depo bağlantısı dahil); 2026 ulusal yatırım programında değil"),
    dict(id="teleferik_ulus", ad="Hacıbayram–Kale–Hıdırlıktepe teleferiği", tur="ulasim", durum="planli", tarih="2026", geometri=pt("ulus"), kaynak_url="https://s.ankara.bel.tr/s3/abb/2026/01/30/91a36f2f-cac5-4b36-9f97-630237507179.pdf", not_="ABB 2026 performans programında"),
    dict(id="ulus_yaya", ad="Ulus yayalaştırma", tur="donusum", durum="yapimda", tarih="", geometri=pt("ulus"), kaynak_url="https://www.ankara.bel.tr/proje/x-240", not_="yaklaşık 30.000 m² meydan, trafik yer altına"),
    dict(id="cubuk_plan", ad="Çubuk merkez imar planı (~165 ha)", tur="imar", durum="onaylandi", tarih="2026-08-11", geometri=None, ilceler=["cubuk"], kaynak_url="https://s.ankara.bel.tr/s3/abb/2026/08/24/0277fdc9-cbc8-4a2c-8a06-961a245b4234.docx", not_="1/25000 ve 1/5000 nazım, 1/1000 uygulama imar planı; meclis karar 1023; askı ve itiraz süreci doğrulanmadı"),
    # hastane ve kurum
    dict(id="bilkent_sh", ad="Bilkent Şehir Hastanesi", tur="hastane", durum="acik", tarih="2019-03-14", geometri=pt("bilkent_sh"), kaynak_url=W+"Ankara_Bilkent_City_Hospital"),
    dict(id="numune", ad="Numune Hastanesi kapandı (Bilkent'e taşındı)", tur="kurum", durum="kapandi", tarih="2019-05-26", geometri=pt("numune"), kaynak_url=W+"Ankara_Bilkent_City_Hospital"),
    dict(id="etlik_sh", ad="Etlik Şehir Hastanesi", tur="hastane", durum="acik", tarih="2022-09-28", geometri=pt("etlik_sh"), kaynak_url=W+"Ankara_Etlik_City_Hospital"),
    dict(id="diskapi", ad="Dışkapı hastaneleri Etlik'e taşındı", tur="kurum", durum="kapandi", tarih="2022-08-17", geometri=pt("diskapi"), kaynak_url=W+"Ankara_Etlik_City_Hospital"),
    dict(id="kulliye", ad="Cumhurbaşkanlığı Külliyesi", tur="kurum", durum="acik", tarih="2014-10-29", geometri=pt("kulliye"), kaynak_url=W+"Presidential_Complex_(Turkey)"),
    # avm
    dict(id="ankamall", ad="ANKAmall", tur="avm", durum="acik", tarih="1999-08-27", geometri=pt("ankamall"), kaynak_url=W+"ANKAmall"),
    dict(id="armada", ad="Armada", tur="avm", durum="acik", tarih="2002-09-28", geometri=pt("armada"), kaynak_url="https://tr.wikipedia.org/wiki/Armada_Al%C4%B1%C5%9Fveri%C5%9F_ve_%C4%B0%C5%9F_Merkezi"),
    dict(id="optimum", ad="Optimum Outlet", tur="avm", durum="acik", tarih="2004-10-29", geometri=pt("optimum"), kaynak_url="https://optimumankara.com/tr/hakkimizda"),
    dict(id="cepa", ad="Cepa", tur="avm", durum="acik", tarih="2007-08-23", geometri=pt("cepa"), kaynak_url="https://cepaavm.com.tr/hakkimizda/"),
    dict(id="panora", ad="Panora", tur="avm", durum="acik", tarih="2007-12-10", geometri=pt("panora"), kaynak_url="https://www.yeniankara.com.tr/ankara/panora-avm-ne-zaman-acildi-nerede-ve-nasil-gidilir-110667"),
    dict(id="acity", ad="Acity", tur="avm", durum="acik", tarih="2008-04-05", geometri=pt("acity"), kaynak_url="https://www.milliyet.com.tr/emlak/acity-outlet-bir-ilkle-aciliyor-66466"),
    dict(id="gordion", ad="Gordion", tur="avm", durum="acik", tarih="2009-09-17", geometri=pt("gordion"), kaynak_url="https://www.hurriyet.com.tr/ekonomi/gordion-avm-17-eylulde-acilacak-12443678"),
    dict(id="kentpark", ad="Kentpark", tur="avm", durum="acik", tarih="2010-02-12", geometri=pt("kentpark"), kaynak_url="https://www.tercihiniyap.net/kentpark-avm-kacta-acilir-kacta-kapanir-calisma-saatleri-nasil-h11234.html", not_="tarih zayıf kaynaktan"),
    dict(id="atlantis", ad="Atlantis", tur="avm", durum="acik", tarih="2011-08-19", geometri=pt("atlantis"), kaynak_url="https://www.aksam.com.tr/ekonomi/atlantis-avm-acildi--63965h/haber-63965"),
    dict(id="nextlevel", ad="Next Level", tur="avm", durum="acik", tarih="2013-10-24", geometri=pt("nextlevel"), kaynak_url="https://www.haberler.com/politika/next-level-avm-nin-acilisi-5212253-haberi/"),
    dict(id="taurus", ad="Taurus", tur="avm", durum="acik", tarih="2013-10", geometri=pt("taurus"), kaynak_url="https://retailturkiye.com/avm/taurus-avm-acildi/"),
    dict(id="metromall", ad="Metromall", tur="avm", durum="acik", tarih="2017-09-28", geometri=pt("metromall"), kaynak_url="https://tr.wikipedia.org/wiki/Metromall_AVM"),
    # kentsel dönüşüm
    dict(id="portakal", ad="Portakal Çiçeği Vadisi dönüşümü", tur="donusum", durum="acik", tarih="1997", geometri=pt("portakal"), kaynak_url="https://kentselstrateji.com/ankara-portakal-cicegi-vadisi-kentsel-donusum-projesi/", not_="konutlar 1994–97"),
    dict(id="dikmen_vadisi", ad="Dikmen Vadisi dönüşümü", tur="donusum", durum="yapimda", tarih="1996", geometri=pt("dikmen_vadisi"), kaynak_url="https://www.ankara.bel.tr/proje/dikmen-vadisi-son-etap-kentsel-donusum-projesi-84", not_="etaplar 1996, 2002, 2009'da bitti; son etap sürüyor"),
    dict(id="kuzey_ankara", ad="Kuzey Ankara Girişi dönüşümü", tur="donusum", durum="belirsiz", tarih="2005-03", geometri=None, ilceler=["altindag", "kecioren"], kaynak_url="https://www.lexpera.com.tr/mevzuat/kanunlar/kuzey-ankara-girisi-kentsel-donusum-projesi-kanunu", not_="5104 sayılı kanun; ~18.000 konut planlandı; güncel durumu doğrulanmadı"),
    dict(id="ulus", ad="Ulus Tarihi Kent Merkezi planı", tur="donusum", durum="belirsiz", tarih="2005-07-15", geometri=pt("ulus"), kaynak_url="https://ankaradergisi.org/jvi.aspx?pdir=jas&plng=tur&un=JAS-44154", not_="207 ha; plan onayı"),
    dict(id="gultepe", ad="Gültepe–Aktaş dönüşümü", tur="donusum", durum="belirsiz", tarih="2006", geometri=pt("gultepe"), kaynak_url="https://www.yapi.com.tr/ankaranin-olayli-mahallesi-cincine-3-bin-210-konut", not_="3.210 TOKİ konutu"),
    dict(id="yeni_mamak", ad="Yeni Mamak dönüşümü", tur="donusum", durum="yapimda", tarih="2008", buyuk=True, geometri=None, ilceler=["mamak"], kaynak_url="https://www.ankara.bel.tr/proje/x-182", not_="8.006 konut; 1.038 teslim, 325'i 2026 1. çeyrekte; Oca 2026'da 56,6 mlr TL ihale; 8 Eyl 2026 meclis kararı 1150 ile 11 etabın uygulama planı revizyonu"),
    dict(id="yamacevler", ad="Yamaçevler dönüşümü", tur="donusum", durum="yapimda", tarih="", geometri=None, ilceler=["yenimahalle"], kaynak_url="https://www.yenimahalle.bel.tr/ProjeDetay/yamacevler-kentsel-donusum-projesi/15", not_="66 ha, ~4.000 konut"),
    dict(id="demetevler", ad="Demetevler dönüşümü", tur="donusum", durum="planli", tarih="", geometri=pt("demetevler"), kaynak_url="https://www.haberturk.com/ankara-haberleri/30530321-yenimahalle-belediyesinden-demetevlerde-kentsel-donusum-cagrisi", not_="öncelikli alan, başlamadı; ABB 2026 performans programında hazırlık işi var"),
    dict(id="hidirliktepe", ad="Hıdırlıktepe–Atıfbey–İsmetpaşa dönüşümü", tur="donusum", durum="yapimda", tarih="2026-01-30", geometri=pt("hidirliktepe"), kaynak_url="https://www.ankara.bel.tr/en/proje/hidirliktepe-atifbey-ismetpasa-kentsel-donusum-ve-gelisim-projesi-305", not_="60 ay"),
    # imar, yol, havalimanı, risk
    dict(id="incek_imar", ad="İncek imar değişikliği", tur="imar", durum="iptal", tarih="2017-02-14", geometri=pt("incek"), kaynak_url="https://www.gazeteduvar.com.tr/yargi-gokcekin-incekteki-imar-plani-degisikligini-iptal-etti-haber-1552615", not_="emsal 0,33'ten 2'ye, konut 25'ten 390'a; mahkeme iptal etti"),
    dict(id="nigde_otoyolu", ad="Ankara–Niğde otoyolu", tur="yol", durum="acik", tarih="2020-12", geometri=None, ilceler=["golbasi"], kaynak_url="https://www.aa.com.tr/tr/turkiye/ankara-nigde-otoyolunun-tamami-hizmete-girdi/2078934", not_="Gölbaşı eşleşmesi doğrulanmadı"),
    dict(id="esenboga", ad="Esenboğa yeni dış hatlar terminali", tur="havalimani", durum="acik", tarih="2006-10-16", geometri=pt("esenboga"), kaynak_url=W+"Esenbo%C4%9Fa_International_Airport"),
    dict(id="ankapark", ad="Ankapark", tur="kurum", durum="kapandi", tarih="2020-02", geometri=pt("ankapark"), kaynak_url="https://www.sozcu.com.tr/750-milyon-dolar-harcanan-ankapark-kapatildi-wp5618555", not_="2019'da açıldı, Şub 2020'de kapandı, Tem 2022'de ABB'ye devredildi"),
    dict(id="golbasi_arz", ad="Gölbaşı–İncek arz fazlası uyarısı", tur="risk", durum="belirsiz", tarih="2026", geometri=None, ilceler=["golbasi"], kaynak_url="https://www.ekonomiankara.com/ankaraya-binlerce-yeni-konut-geliyor-hangi-bolgelerde-arz-yogunlasacak/14501"),
    dict(id="kizilay_cekim", ad="Kızılay'ın çekim kaybı", tur="risk", durum="belirsiz", tarih="", geometri=pt("kizilay"), kaynak_url="https://www.yeniankara.com.tr/ankara/ankarada-eski-populerligini-kaypeden-7-semt-183561", not_="nitel; sayı yok"),
]

# ABB, deprem yönetmeliğine göre toplam bina sayısı (ilçe), 25 Eyl 2026 sorgusu
ABB_BINA_URL = "https://planaski.ankara.bel.tr/webgis/rest/services/deprem/ilceMahalleRapor/MapServer/3"
BINA = {"cankaya": 64446, "golbasi": 37503, "yenimahalle": 59915, "etimesgut": 24564, "pursaklar": 8752,
        "cubuk": 21591, "kecioren": 33839, "altindag": 31411, "sincan": 33483, "mamak": 32116, "akyurt": 7622}
KIZILAY = (32.8540, 39.9208)
CEVRE_KM, YOGUN_BINA_KM2 = 30, 150  # 11 ilçede doğal kırılımlar: 16->21->33 km, 93->143->197 bina/km2

# ilçeye özel, kaynaklı notlar. Kaynak yoksa bunu söyler, uydurmaz.
YEREL = {
    "cankaya": "Bilkent Şehir Hastanesi 2019'da açıldı; beklenenin üstündeki farkla bağı kanıtlanmadı.",
    "golbasi": "Çevreye kayışla uyumlu yükseldi, ama Gölbaşı–İncek için 2026'da arz fazlası uyarısı var.",
    "yenimahalle": "Etlik Şehir Hastanesi 2022'de açıldı; ilçe fiyatı uzaklığa göre beklenen düzeyde kaldı.",
    "pursaklar": "Esenboğa metrosu sözleşmeli. Ankara emsali: Keçiören metrosu 2023'te Kızılay'a bağlandı, ilçenin göreli fiyatı yerinde saydı. Metronun etkisi durak çevresindeki mahallelerde aranmalı; onların fiyat geçmişi elimizde yok.",
    "cubuk": "Esenboğa Havalimanı ve metronun havalimanı ucu burada; 11 Ağu 2026'da merkezde ~165 ha yeni imar planı onaylandı.",
    "kecioren": "M4 2017'de açıldı, 2023'te Kızılay'a bağlandı; göreli fiyat yine de yerinde saydı.",
    "altindag": "Numune (2019) ve Dışkapı hastaneleri (2022) ilçeden taşındı. Esenboğa metrosu ve Hıdırlıktepe dönüşümü geliyor; Keçiören emsali metronun ilçe düzeyinde tek başına yetmediğini gösteriyor.",
    "sincan": "Çevre ilçesi, ama uzaklığa göre beklenenin altında kaldı; nedeni için kaynak bulunamadı.",
    "mamak": "Dikimevi–Natoyolu hattı yapımda (hedef 2029), Yeni Mamak dönüşümü sürüyor. Keçiören emsali metronun ilçe düzeyinde tek başına yetmediğini gösteriyor; durak çevresi mahalleler ayrıca izlenmeli.",
    "akyurt": "Yükselişi açıklayan tek bir proje bulunamadı; çevreye kayışla uyumlu.",
    "etimesgut": "",
}

# --- güçler: "neye göre artar, azalır?" (PROJECT.md "Model"). 26 Eyl 2026 sorguları; ağ çağrısı yok, sabit.
# bina dönemi: ABB ilçe katmanı; plan ve dava: UİP+NİP değişiklik sınırları (ilçe poligonuyla kesişen);
# dönüşüm: kentsel dönüşüm alanları; istasyon: metro+ankaray+başkentray; sel: 2017–2025 su baskını kayıtları;
# okul/park/sağlık: OSM Overpass sayımı.
# ABB'de beşinci bir dönem daha var: "2007 Deprem Yönetmeliği Öncesi" (y2007Oncesi). 1998 öncesi mi sonrası mı ayrılmamış binalar.
# 26 Eyl ölçümü bunu atladı, Çubuk ve Akyurt'u "dönemi girilmemiş" sandı. 27 Eyl'de düzeltildi: 2018 sonrası payı bütün binalar
# üstünden; 1998 öncesi payı, binaların %20'sinden fazlası bu kovadaysa ölçülmedi sayılır.
GUC_HAM = {  # id: (1998 öncesi, 1998–2006, 2007–2017, 2018 sonrası, plan top, plan 2020+, plan davalı, dönüşüm, istasyon, sel, okul, park, sağlık)
    "cankaya": (23276, 31488, 7762, 1920, 3714, 764, 273, 40, 27, 3369, 246, 548, 98),
    "golbasi": (3902, 22708, 3364, 3633, 830, 316, 72, 15, 0, 389, 52, 111, 8),
    "yenimahalle": (17009, 36444, 5335, 1127, 3086, 386, 119, 24, 18, 4149, 151, 391, 53),
    "etimesgut": (4072, 11587, 6899, 2006, 1532, 286, 83, 16, 11, 1753, 130, 344, 31),
    "pursaklar": (1375, 5295, 1585, 497, 450, 83, 16, 3, 0, 140, 38, 301, 8),
    "cubuk": (319, 331, 1387, 410, 383, 104, 8, 0, 0, 186, 41, 92, 6),
    "kecioren": (11448, 14822, 7096, 473, 1332, 206, 66, 11, 12, 3399, 160, 397, 45),
    "altindag": (13237, 12788, 4846, 539, 1311, 257, 51, 12, 11, 1552, 119, 167, 24),
    "sincan": (7872, 17883, 5476, 1463, 898, 289, 32, 6, 6, 2321, 97, 333, 23),
    "mamak": (8004, 16381, 6879, 852, 1338, 297, 69, 18, 7, 2124, 134, 188, 28),
    "akyurt": (318, 194, 1001, 418, 153, 53, 10, 1, 0, 371, 10, 14, 3),
}
ABB = "https://baskentcbs.ankara.bel.tr/server/rest/services/"
OVERPASS = "https://overpass-api.de/api/interpreter"
Y07_ONCESI = {"cubuk": 19137, "akyurt": 5691, "golbasi": 3896, "sincan": 789}  # ABB ilçe katmanı, 27 Eyl 2026 sorgusu
AYRILMAMIS_SINIR = 0.2
GUC_TANIM = [  # id, ad, birim, kaynak
    ("kizilay_km", "Kızılay'a uzaklık", "km", "https://www.openstreetmap.org/"),
    ("bina_km2", "bina yoğunluğu", "bina/km²", ABB_BINA_URL),
    ("yeni_arz", "2018 sonrası bina payı", "%", ABB_BINA_URL),
    ("eski_stok", "1998 öncesi bina payı", "%", ABB_BINA_URL),
    ("plan_2020", "2020'den beri plan değişikliği", "/1000 bina", ABB + "plan/PlanRaporu/MapServer/3"),
    ("dava", "davalı plan değişikliği payı", "%", ABB + "plan/PlanRaporu/MapServer/3"),
    ("donusum", "kentsel dönüşüm alanı", "/10.000 bina", ABB + "plan/PlanRaporu/MapServer/2"),
    ("istasyon", "raylı istasyon", "/10.000 bina", ABB + "kentrehberi/ego_kent_Rehberi/MapServer/4"),
    ("istasyon_km", "raylı istasyona uzaklık (bina ağırlıklı)", "km", ABB + "kentrehberi/ego_kent_Rehberi/MapServer/4"),
    ("kurum", "kurum girişi − çıkışı (2019–2026)", "adet", ""),
    ("sel", "su baskını kaydı (2017–2025)", "/1000 bina", ABB + "hidroloji_analizi/Ankara_Hidroloji_Analizi/MapServer/0"),
    ("okul", "okul", "/1000 bina", OVERPASS),
    ("park", "park", "/1000 bina", OVERPASS),
    ("saglik", "hastane ve klinik", "/1000 bina", OVERPASS),
]
HUKUM = {
    "ana": "2019–2026'da Ankara'da fiyatı en çok bu sürükledi",
    "bagimsiz": "uzaklık sabit tutulunca da fiyatla birlikte hareket etti",
    "golge": "fiyatla birlikte hareket etti ama merkezden uzaklığın yansıması",
    "zayif": "fiyatla ilişkisi zayıf",
    "kararsiz": "tek bir ilçe çıkarılınca yönü değişiyor; kararsız",
    "tutmadi": "fiyatla ilişkisi yok",
}
GUC_NOT = {
    "yeni_arz": "Endeksa ilan tabanlı: yeni binalar çoğaldıkça ortalama m² karışım yüzünden de yükselir. Neden değil, birlikte hareket.",
    "kurum": "hastane açılışı +1, kurum kapanışı −1; kaynaklar olay listesinde.",
    "istasyon_km": "Her mahallenin orta noktasından en yakın açık istasyona, bina sayısıyla ağırlıklı. r pozitif: istasyondan uzak ilçeler 2019–2026'da daha çok yükseldi. Kızılay'a uzaklıkla çok iç içe (r = 0,91); 11 ilçede ikisini ayırmak zor. Birlikte hareket, neden değil.",
}
EMSAL = {  # bekleyen proje türü -> Ankara'nın kendi emsali
    "rayli": "Ankara emsali: Keçiören'in metrosu 2023'te Kızılay'a bağlandı, ilçenin göreli fiyatı yerinde saydı. Etki durak çevresinde aranmalı.",
    "donusum": "Ankara emsali: dönüşüm alanı yoğunluğu 2019–2026 değişimiyle zayıf ve uzaklığın gölgesinde.",
    "hastane": "Ankara emsali: Bilkent Şehir Hastanesi (2019) Çankaya'da beklenenin üstündeki farkla örtüşüyor.",
    "imar": "Ankara'da ölçülmüş emsal yok.",
    "ulasim": "Ankara'da ölçülmüş emsal yok.",
}
GELECEK_DURUM = ("sozlesmeli", "yapimda", "planli", "onaylandi")

def guc_olcu(iid, yapi, projeler):
    y98o, y98, y07, y18, pt, p20, pd, dn, ist, sel, okul, park, sag = GUC_HAM[iid]
    b = BINA[iid]; per = y98o + y98 + y07 + y18 + Y07_ONCESI.get(iid, 0)
    eski = None if Y07_ONCESI.get(iid, 0) / per > AYRILMAMIS_SINIR else y98o / per * 100
    kurum = (sum(1 for p in projeler if iid in p["ilceler"] and p["tur"] == "hastane" and "2019" <= p["tarih"][:4] <= "2026")
             - sum(1 for p in projeler if iid in p["ilceler"] and p["tur"] == "kurum" and p["durum"] == "kapandi" and "2019" <= p["tarih"][:4] <= "2026"))
    return dict(kizilay_km=yapi["kizilay_km"], bina_km2=yapi["bina_km2"], yeni_arz=y18 / per * 100, eski_stok=eski,
                plan_2020=p20 / b * 1000, dava=pd / pt * 100, donusum=dn / b * 10000, istasyon=ist / b * 10000,
                kurum=kurum, sel=sel / b * 1000, okul=okul / b * 1000, park=park / b * 1000, saglik=sag / b * 1000)

def guc_hukum(xs, ys, ds, ana):
    k = [i for i, x in enumerate(xs) if x is not None]  # ölçülemeyen ilçe hükme girmez
    xs, ys, ds = [xs[i] for i in k], [ys[i] for i in k], [ds[i] for i in k]
    n = len(xs)
    r = statistics.correlation(xs, ys)
    loo = [statistics.correlation([xs[i] for i in range(n) if i != j], [ys[i] for i in range(n) if i != j]) for j in range(n)]
    if ana:
        return "ana", r, None, loo
    rd, rx = statistics.correlation(ys, ds), statistics.correlation(xs, ds)
    kismi = (r - rd * rx) / math.sqrt((1 - rd ** 2) * (1 - rx ** 2))
    if min(loo) * max(loo) < 0: h = "kararsiz"
    elif abs(r) < 0.3: h = "tutmadi"
    elif abs(r) < 0.5: h = "zayif"
    elif abs(kismi) >= 0.5: h = "bagimsiz"
    else: h = "golge"
    return h, r, kismi, loo

def osm_hat(rid):
    req = urllib.request.Request(f"https://api.openstreetmap.org/api/0.6/relation/{rid}/full", headers=UA)
    root = ET.fromstring(urllib.request.urlopen(req, timeout=60).read())
    nodes = {n.get("id"): (round(float(n.get("lon")), 5), round(float(n.get("lat")), 5)) for n in root.iter("node")}
    ways = {w.get("id"): [nodes[nd.get("ref")] for nd in w.iter("nd") if nd.get("ref") in nodes] for w in root.iter("way")}
    rel = next(r for r in root.iter("relation") if r.get("id") == str(rid))
    segs = [[list(c) for c in ways[m.get("ref")]] for m in rel.iter("member")
            if m.get("type") == "way" and m.get("ref") in ways and not m.get("role", "").startswith("platform")]
    return {"type": "MultiLineString", "coordinates": segs}

def in_ring(x, y, ring):
    c = False
    for i in range(len(ring)):
        (x1, y1), (x2, y2) = ring[i], ring[(i + 1) % len(ring)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def in_poly(x, y, g):
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in polys)

def alan_merkez(g):
    A = cx = cy = 0
    for ring in [p[0] for p in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]])]:
        for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
            c = x1 * y2 - x2 * y1; A += c; cx += (x1 + x2) * c; cy += (y1 + y2) * c
    cx, cy = cx / (3 * A), cy / (3 * A)
    return abs(A) / 2 * 111.32 * 111.32 * math.cos(math.radians(cy)), cx, cy

def vertices(g):
    t, c = g["type"], g["coordinates"]
    return [c] if t == "Point" else c if t == "LineString" else [v for s in c for v in s]

def main():
    sinirlar = {f["properties"]["id"]: f["geometry"] for f in json.load(open(D / "ilceler.geojson"))["features"]}
    projeler = []
    for p in PROJELER:
        p = dict(p)
        if isinstance(p["geometri"], str):
            p["geometri"] = osm_hat(HAT_OSM[p["geometri"][4:]]); time.sleep(1)
        if p["geometri"] and "ilceler" not in p:
            vs = vertices(p["geometri"])
            p["ilceler"] = [i for i, g in sinirlar.items() if any(in_poly(x, y, g) for x, y in vs)]
        p.setdefault("yaklasik", False)
        if "not_" in p: p["not"] = p.pop("not_")
        projeler.append(p)

    medyan = {y: statistics.median(v[k] for v in ILCE.values()) for k, y in ((1, 2019), (2, 2020), (3, 2026))}
    yapi = {}
    for iid, (ad, f19, f20, f26) in ILCE.items():
        km2, cx, cy = alan_merkez(sinirlar[iid])
        km = math.hypot((cx - KIZILAY[0]) * 111.32 * math.cos(math.radians(KIZILAY[1])), (cy - KIZILAY[1]) * 111.32)
        yapi[iid] = dict(kizilay_km=round(km, 1), bina_km2=round(BINA[iid] / km2), degisim=(f26 / medyan[2026]) / (f19 / medyan[2019]) - 1)
    xs = [v["kizilay_km"] for v in yapi.values()]; ys = [v["degisim"] for v in yapi.values()]
    r = statistics.correlation(xs, ys)
    egim = statistics.covariance(xs, ys) / statistics.variance(xs); kes = statistics.mean(ys) - egim * statistics.mean(xs)
    fmt = lambda x: ("+" if x >= 0 else "−") + f"%{abs(x) * 100:.0f}"
    YAPI = f"Ankara'da 2019'dan beri fiyat merkezden çevreye kaydı: ilçenin Kızılay'a uzaklığı ile göreli fiyat değişimi arasında r = {r:.2f} (11 ilçe).".replace(".", ",", 1).replace("r = 0,", "r = 0,")
    # güçler: her birinin 2019–2026 göreli değişimle ilişkisi, 11 ilçede ölçülür; hüküm sayıdan çıkar, elle yazılmaz
    olcu = {iid: guc_olcu(iid, yapi[iid], projeler) for iid in ILCE}
    mah = json.load(open(D / "mahalleler.json"))["mahalleler"]  # önce: python3 data/mahalle.py
    for iid in ILCE:
        ms = [m for m in mah if m["ilce"] == iid and m["bina"]]
        olcu[iid]["istasyon_km"] = sum(m["bina"] * m["olcu"]["istasyon_km"] for m in ms) / sum(m["bina"] for m in ms)
    ids = list(ILCE); dy = [yapi[i]["degisim"] for i in ids]; dd = [yapi[i]["kizilay_km"] for i in ids]
    hukum = {}
    for gid, gad, birim, kaynak in GUC_TANIM:
        gx = [olcu[i][gid] for i in ids]
        h, gr, gk, loo = guc_hukum(gx, dy, dd, ana=(gid == "kizilay_km"))
        hukum[gid] = dict(hukum=h, r=round(gr, 2), kismi=None if gk is None else round(gk, 2),
                          aralik=[round(min(loo), 2), round(max(loo), 2)], medyan=statistics.median(x for x in gx if x is not None),
                          n=sum(1 for x in gx if x is not None))
    ilceler = []
    for iid, (ad, f19, f20, f26) in ILCE.items():
        goreli = {2019: f19 / medyan[2019], 2020: f20 / medyan[2020], 2026: f26 / medyan[2026]}
        gucler = []
        for gid, gad, birim, kaynak in GUC_TANIM:
            v, H = olcu[iid][gid], hukum[gid]
            sira = None if v is None else 1 + sum(1 for i in ids if olcu[i][gid] is not None and olcu[i][gid] > v)
            yon = None  # yalnızca kanıtı tutan güçte: bu ilçenin değeri medyanın hangi tarafında, Ankara'da o taraf ne yaptı
            if v is not None and H["hukum"] in ("ana", "bagimsiz") and v != H["medyan"]:
                yon = "yukseltir" if (v > H["medyan"]) == (H["r"] > 0) else "dusurur"
            not_ = GUC_NOT.get(gid, "")
            if gid == "eski_stok" and v is None:
                not_ = (f"Bu ilçede binaların %{Y07_ONCESI[iid] / BINA[iid] * 100:.0f}'i ABB'de yalnızca \"2007 öncesi\" diye girilmiş; "
                        "1998 öncesi payı ayrılamıyor, ölçülmedi. " + not_).strip()
            gucler.append(dict(id=gid, ad=gad, deger=None if v is None else round(v, 1), birim=birim, sira=sira, n=H["n"],
                               hukum=H["hukum"], hukum_metin=HUKUM[H["hukum"]], r=H["r"], kismi=H["kismi"], aralik=H["aralik"],
                               yon=yon, not_=not_, kaynak_url=kaynak))
        gelecek = [dict(id=p["id"], baslik=p["ad"], tur=p["tur"], durum=p["durum"], tarih=p["tarih"], hedef=p.get("hedef", ""),
                        emsal=EMSAL.get(p["tur"], "Ankara'da ölçülmüş emsal yok."), kaynak_url=p["kaynak_url"])
                   for p in sorted(projeler, key=lambda p: p["tarih"] or "0", reverse=True)
                   if iid in p["ilceler"] and p["durum"] in GELECEK_DURUM]
        y = yapi[iid]; degisim = y["degisim"]; beklenen = kes + egim * y["kizilay_km"]
        olaylar = sorted([p for p in projeler if iid in p["ilceler"]], key=lambda p: p["tarih"] or "0", reverse=True)
        arz = any(p["tur"] == "risk" and "arz" in p["ad"] for p in olaylar)
        if y["bina_km2"] >= YOGUN_BINA_KM2 and degisim <= 0:
            sinif = "duser"
            kural = f"yoğun merkez ilçesi (≥{YOGUN_BINA_KM2} bina/km²) ve göreli fiyatı 2019'dan beri artmamış"
        elif y["kizilay_km"] >= CEVRE_KM and degisim > 0 and not arz:
            sinif = "degerlenebilir"
            kural = f"çevre ilçesi (Kızılay'a ≥{CEVRE_KM} km), göreli fiyatı 2019'dan beri artmış, arz fazlası uyarısı yok"
        else:
            sinif = "korur"
            kural = "ilk iki kural geçerli değil"
        neden = (f"{YAPI} {ad}: orta noktası Kızılay'a {y['kizilay_km']:.0f} km, {y['bina_km2']} bina/km². "
                 f"Ankara medyanına göre fiyatı {fmt(degisim)}; uzaklığa göre beklenen {fmt(beklenen)}. {YEREL[iid]}").strip()
        ilceler.append(dict(
            id=iid, ad=ad, sinif=sinif, kural=kural, neden=neden,
            goreli={str(k): round(v, 3) for k, v in goreli.items()}, goreli_degisim=round(degisim, 3),
            yapi=dict(kizilay_km=y["kizilay_km"], bina_km2=y["bina_km2"], beklenen=round(beklenen, 3),
                      fark=round(degisim - beklenen, 3), bina_kaynak_url=ABB_BINA_URL),
            fiyat=[dict(yil=2019, ay="Haziran", tl_m2=f19, kaynak="Endeksa (Baret Dergisi)", kaynak_url=BARET),
                   dict(yil=2020, ay="Haziran", tl_m2=f20, kaynak="Endeksa (Baret Dergisi)", kaynak_url=BARET),
                   dict(yil=2026, ay="Ağustos", tl_m2=f26, kaynak="Endeksa (Emlakjet)", kaynak_url=EJ + iid)],
            olaylar=[dict(id=p["id"], tarih=p["tarih"], baslik=p["ad"], tur=p["tur"], durum=p["durum"],
                          not_=p.get("not", ""), kaynak_url=p["kaynak_url"]) for p in olaylar],
            gucler=gucler, gelecek=gelecek,
        ))
    for i in ilceler:
        for o in i["olaylar"] + i["gucler"]: o["not"] = o.pop("not_")
    json.dump(ilceler, open(D / "ilceler.json", "w"), ensure_ascii=False, indent=1)
    json.dump(projeler, open(D / "projeler.json", "w"), ensure_ascii=False, separators=(",", ":"))
    for i in ilceler:
        print(f"{i['ad']:12s} {i['yapi']['kizilay_km']:5.1f}km {i['yapi']['bina_km2']:4d}b/km2  gerçek {i['goreli_degisim']*100:+4.0f}  beklenen {i['yapi']['beklenen']*100:+4.0f}  {i['sinif']}")
    print(f"r = {r:.2f}")
    for gid, H in hukum.items():
        print(f"  {gid:11s} r={H['r']:+.2f} ({H['aralik'][0]:+.2f}…{H['aralik'][1]:+.2f}) kısmi={H['kismi'] if H['kismi'] is not None else '—'}  {H['hukum']}")
    print(len(projeler), "proje;", sum(1 for p in projeler if not p["ilceler"]), "ilçesiz")

if __name__ == "__main__":
    main()
