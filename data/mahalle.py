"""bandl mahalle katmanı -> data/mahalleler.json + data/mahalleler.geojson

python3 data/mahalle.py          # data/ham/ yoksa çeker, sonra ölçer
python3 data/mahalle.py --cek    # ham veriyi yeniden çeker

11 ilçenin bütün mahalleleri. Kaynaklar: ABB ArcGIS (mahalle sınırı ve bina dönemi, raylı istasyonlar,
su baskını kayıtları, 2020 sonrası plan değişiklikleri, kentsel dönüşüm alanları), OSM Overpass (okul, park,
hastane ve klinik), projeler.json (bekleyen raylı hatlar). Ticari kullanım yok; bilgi tasnifi (Damla, 27 Eyl 2026).
Mahalle fiyat serisi yok: mahalleye değer sınıfı verilmez, ilçesinin sınıfı yanında gösterilir.
"""
import json, math, sys, time, urllib.parse, urllib.request
from pathlib import Path

D = Path(__file__).parent
H = D / "ham"
UA = {"User-Agent": "bandl-seed/0.1 (damummyphus@gmail.com)"}
PLANASKI = "https://planaski.ankara.bel.tr/webgis/rest/services/"
ABB = "https://baskentcbs.ankara.bel.tr/server/rest/services/"
MAHALLE_URL = PLANASKI + "deprem/ilceMahalleRapor/MapServer/2"
IST_URL = ABB + "kentrehberi/ego_kent_Rehberi/MapServer/"
SEL_URL = ABB + "hidroloji_analizi/Ankara_Hidroloji_Analizi/MapServer/0"
PLAN_URL = ABB + "plan/PlanRaporu/MapServer/"
OVERPASS = "https://overpass-api.de/api/interpreter"
KIZILAY = (32.8540, 39.9208)
ABB_ILCE = {  # bandl id -> ABB ilçe kimliği (ilceMahalleRapor/MapServer/3)
    "cankaya": "{AE0268C4-85B4-4FA2-97CF-24775ADDAAB8}", "golbasi": "{F8D21011-5D1E-43B3-A44F-74382676C3FA}",
    "yenimahalle": "{A5F42D43-0118-4381-8C52-6831CB6DA302}", "etimesgut": "{BAA3DE4D-DC7A-4B32-97D3-F19B42EF4673}",
    "pursaklar": "{377295E8-DFCF-4CF4-A584-563F2903F8DB}", "cubuk": "{1CE0E71F-17CC-47FA-BFD7-B9AB27A0EF98}",
    "kecioren": "{F21FDE8A-BA07-447F-9B9A-2FA4B7E81978}", "altindag": "{202313A8-EE61-416A-A19B-D29CDCAD1E3F}",
    "sincan": "{C8F69DEC-30EE-47E7-B1B8-E9EDB03322D0}", "mamak": "{044CFFDB-62AD-4B7A-B091-6525436388CC}",
    "akyurt": "{D677FBE6-2EB1-4B41-87CF-A577F9B646E0}",
}
YAKIN_KM = 1.0      # okul / park / sağlık: mahallenin orta noktasına 1 km içinde
AZ_BINA = 50        # bundan az binalı mahallede bina başına oran güvenilmez, sıralamaya girmez
AYRILMAMIS_SINIR = 0.2  # binaların bundan fazlası "2007 öncesi" kovasındaysa 1998 öncesi payı ölçülmez (build.py ile aynı)
BEKLEYEN = ("sozlesmeli", "yapimda", "planli", "onaylandi")

# --- çekim --------------------------------------------------------------------------------------
def get(url, params=None, data=None, deneme=4):
    if params: url += "?" + urllib.parse.urlencode(params)
    for i in range(deneme):
        try:
            req = urllib.request.Request(url, data=data, headers=UA)
            return json.loads(urllib.request.urlopen(req, timeout=180).read())
        except Exception as e:
            if i == deneme - 1: raise
            print("  tekrar:", e); time.sleep(5 * (i + 1))

def arcgis(url, where, fields, geo=True, off=0.0001):
    out, ofs = [], 0
    while True:
        d = get(url + "/query", dict(where=where, outFields=fields, returnGeometry=str(geo).lower(), outSR=4326,
                                     maxAllowableOffset=off, geometryPrecision=5, resultOffset=ofs, resultRecordCount=1000, f="json"))
        if "error" in d: raise RuntimeError(d["error"])
        out += d["features"]; ofs += len(d["features"])
        if not d.get("exceededTransferLimit") or not d["features"]: return out
        time.sleep(1)

def kaydet(ad, kaynak, veri):
    json.dump(dict(kaynak=kaynak, cekildi=time.strftime("%Y-%m-%d"), veri=veri), open(H / ad, "w"), ensure_ascii=False, separators=(",", ":"))
    print(" ", ad, len(veri))

def cek():
    H.mkdir(exist_ok=True)
    m = []
    for iid, g in ABB_ILCE.items():
        m += [dict(ilce=iid, **f) for f in arcgis(MAHALLE_URL, f"ILCEID='{g}'", "KIMLIKNO,AD,toplambina,y98Oncesi,y98eGore,y2007Oncesi,y2007yeGore,y2018eGore")]
        time.sleep(1)
    kaydet("mahalle.json", MAHALLE_URL, m)
    ist = []
    for lyr, tur in ((4, "metro"), (5, "Ankaray"), (6, "Başkentray")):
        ist += [dict(tur=tur, ad=f["attributes"]["durak_adi"], x=f["geometry"]["x"], y=f["geometry"]["y"])
                for f in arcgis(IST_URL + str(lyr), "1=1", "durak_adi")]
    kaydet("istasyon.json", IST_URL + "4", ist)
    st = json.dumps([{"statisticType": "count", "onStatisticField": "objectid", "outStatisticFieldName": "n"}])
    d = get(SEL_URL + "/query", dict(where="1=1", outStatistics=st, groupByFieldsForStatistics="mahalle_kimlikno", f="json"))
    kaydet("sel.json", SEL_URL, {str(f["attributes"]["mahalle_kimlikno"]): f["attributes"]["n"] for f in d["features"]})
    plan = []
    for lyr, tur in ((3, "UİP"), (4, "NİP")):
        for f in arcgis(PLAN_URL + str(lyr), "onaytarihi >= DATE '2020-01-01'", "onaytarihi,mahkemedurumu", off=0.0005):
            if f.get("geometry"):
                x, y = merkez(f["geometry"]["rings"]); plan.append(dict(tur=tur, t=f["attributes"]["onaytarihi"], dava=f["attributes"]["mahkemedurumu"], x=x, y=y))
    kaydet("plan.json", PLAN_URL + "3", plan)
    kaydet("donusum.json", PLAN_URL + "2", [dict(ad=f["attributes"]["ad"], mahkeme=f["attributes"]["mahkemedurumu"], rings=f["geometry"]["rings"])
                                            for f in arcgis(PLAN_URL + "2", "1=1", "ad,mahkemedurumu", off=0.0002) if f.get("geometry")])
    xs = [c[0] for f in m for r in f["geometry"]["rings"] for c in r]; ys = [c[1] for f in m for r in f["geometry"]["rings"] for c in r]
    bb = f"{min(ys):.4f},{min(xs):.4f},{max(ys):.4f},{max(xs):.4f}"
    q = f'[out:json][timeout:180];(nwr["amenity"="school"]({bb});nwr["leisure"="park"]({bb});nwr["amenity"~"^(hospital|clinic)$"]({bb}););out center tags;'
    d = get(OVERPASS, data=urllib.parse.urlencode({"data": q}).encode())
    osm = []
    for e in d["elements"]:
        t = e.get("tags", {}); c = e if e["type"] == "node" else e.get("center")
        if not c: continue
        tur = "okul" if t.get("amenity") == "school" else "park" if t.get("leisure") == "park" else "saglik"
        osm.append(dict(tur=tur, x=round(c["lon"], 5), y=round(c["lat"], 5)))
    kaydet("osm.json", OVERPASS, osm)

# --- geometri ---------------------------------------------------------------------------------
KX = 111.32 * math.cos(math.radians(KIZILAY[1])); KY = 111.32
def km(a, b): return math.hypot((a[0] - b[0]) * KX, (a[1] - b[1]) * KY)

def isaretli(r): return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1])) / 2

def merkez(rings):
    A = cx = cy = 0
    for r in rings:
        for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
            c = x1 * y2 - x2 * y1; A += c; cx += (x1 + x2) * c; cy += (y1 + y2) * c
    return (cx / (3 * A), cy / (3 * A)) if A else tuple(rings[0][0])

def in_ring(x, y, r):
    c = False
    for i in range(len(r)):
        (x1, y1), (x2, y2) = r[i], r[(i + 1) % len(r)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c

def poligonlar(rings):
    """esri halkaları -> GeoJSON poligonları: saat yönündeki halka dış, tersi delik"""
    dis = [[r] for r in rings if isaretli(r) < 0]
    for r in rings:
        if isaretli(r) >= 0:
            for p in dis:
                if in_ring(r[0][0], r[0][1], p[0]): p.append(r); break
    return dis or [[r] for r in rings]

def icinde(x, y, polys, bb):
    if not (bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3]): return False
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in polys)

def seg_km(p, a, b):
    ax, ay, bx, by, px, py = a[0] * KX, a[1] * KY, b[0] * KX, b[1] * KY, p[0] * KX, p[1] * KY
    dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)

TR_UP = str.maketrans("iı", "İI")
KISALTMA = {"Gop": "GOP", "Mta": "MTA", "Odtü": "ODTÜ", "Aşti": "AŞTİ", "Aski": "ASKİ", "Yht": "YHT", "Osb": "OSB", "Toki": "TOKİ"}
def baslik(s):
    s = s.replace("İ", "i").replace("I", "ı").lower()
    ust = lambda w: w[:1].translate(TR_UP).upper() + w[1:]
    for ay in "-/.(":
        s = ay.join(ust(w) if i else w for i, w in enumerate(s.split(ay)))
    s = " ".join(ust(w) for w in s.split())
    return " ".join(KISALTMA.get(w.strip("()"), w.strip("()")).join(w.split(w.strip("()"))) if w.strip("()") else w for w in s.split()).replace("(", " (").replace("  ", " ")
def durak(s):
    s = baslik(s or "adsız durak").replace("(Yht)", "(YHT)").replace("Osb.", "OSB-")
    return s[:-2] if s.endswith(" 1") else s
def slug(s): return s.lower().translate(str.maketrans("çğıöşüâî ", "cgiosuai-")).replace("i̇", "i")

# --- ölçütler ---------------------------------------------------------------------------------
OLCUT = [  # id, panelde ad, "sana göre"de ad (+ = daha çok), ters (km: + yakın demek), birim, kaynak, not
    ("kizilay_km", "Kızılay'a uzaklık", "merkeze yakınlık", True, "km", "https://www.openstreetmap.org/", "mahallenin orta noktasından kuş uçuşu"),
    ("istasyon_km", "raylı istasyona uzaklık", "raylı istasyona yakınlık", True, "km", IST_URL + "4", "metro, Ankaray, Başkentray; açık istasyonlar; orta noktadan kuş uçuşu"),
    ("yeni_hat_km", "bekleyen raylı hatta uzaklık", "bekleyen raylı hatta yakınlık", True, "km", "", "yapımda, sözleşmeli ya da planlı hatlar; güzergâhlar yaklaşık, kaynakları ilçe panelinde"),
    ("yeni_arz", "2018 sonrası bina payı", "yeni bina", False, "%", MAHALLE_URL, "ABB bina yapım dönemi"),
    ("eski_stok", "1998 öncesi bina payı", "eski bina", False, "%", MAHALLE_URL, "ABB bina yapım dönemi"),
    ("bina_km2", "bina yoğunluğu", "bina yoğunluğu", False, "bina/km²", MAHALLE_URL, ""),
    ("sel", "su baskını kaydı (2017–2025)", "su baskını kaydı", False, "/1000 bina", SEL_URL, ""),
    ("okul", "okul", "okul", False, "1 km içinde", OVERPASS, "OSM'de işaretli olanlar, orta noktaya 1 km"),
    ("park", "park", "park", False, "1 km içinde", OVERPASS, "OSM'de işaretli olanlar, orta noktaya 1 km"),
    ("saglik", "hastane ve klinik", "hastane ve klinik", False, "1 km içinde", OVERPASS, "OSM'de işaretli olanlar, orta noktaya 1 km"),
    ("plan", "2020'den beri plan değişikliği", "plan değişikliği", False, "/km²", PLAN_URL + "3", "uygulama ve nazım imar planı değişiklikleri; orta noktası mahallede olanlar"),
    ("donusum", "kentsel dönüşüm alanı", "kentsel dönüşüm alanı", False, "adet", PLAN_URL + "2", "mahalleyle örtüşen alanlar; mahkemece iptal edilenler sayılmadı"),
]

def main():
    if "--cek" in sys.argv or not (H / "osm.json").exists(): cek()
    ham = {k: json.load(open(H / f"{k}.json")) for k in ("mahalle", "istasyon", "sel", "plan", "donusum", "osm")}
    hatlar = []
    for p in json.load(open(D / "projeler.json")):
        if p["tur"] == "rayli" and p["durum"] in BEKLEYEN and p["geometri"]:
            g = p["geometri"]; segs = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
            hatlar.append((p["ad"], p["kaynak_url"], p.get("yaklasik"), [(s[i], s[i + 1]) for s in segs for i in range(len(s) - 1)]))
    ist = ham["istasyon"]["veri"]; osm = ham["osm"]["veri"]; sel = ham["sel"]["veri"]
    don = [(d["ad"] or "adsız alan", d["mahkeme"], poligonlar(d["rings"])) for d in ham["donusum"]["veri"]]
    don = [(a, m, ps, [min(c[0] for p in ps for c in p[0]), min(c[1] for p in ps for c in p[0]), max(c[0] for p in ps for c in p[0]), max(c[1] for p in ps for c in p[0])]) for a, m, ps in don]
    mahalleler, feats = [], []
    for f in ham["mahalle"]["veri"]:
        a = f["attributes"]; rings = f["geometry"]["rings"]; polys = poligonlar(rings)
        xs = [c[0] for p in polys for c in p[0]]; ys = [c[1] for p in polys for c in p[0]]; bb = [min(xs), min(ys), max(xs), max(ys)]
        alan = sum(abs(isaretli(p[0])) - sum(abs(isaretli(h)) for h in p[1:]) for p in polys) * KX * KY
        c = merkez([p[0] for p in polys])
        if not icinde(c[0], c[1], polys, bb):  # hilal biçimli mahalle: orta nokta dışarıda kalırsa en yakın köşe
            c = min(((x, y) for p in polys for x, y in p[0]), key=lambda v: km(v, c))
        bina = a["toplambina"] or 0; per = sum(a[k] or 0 for k in ("y98Oncesi", "y98eGore", "y2007Oncesi", "y2007yeGore", "y2018eGore"))
        ad = baslik(a["AD"]); iid = f["ilce"]; mid = f"{iid}-{slug(ad)}"
        o, notlar = {}, {}
        o["kizilay_km"] = km(c, KIZILAY)
        yak = min(ist, key=lambda s: km(c, (s["x"], s["y"]))); o["istasyon_km"] = km(c, (yak["x"], yak["y"]))
        notlar["istasyon_km"] = f"en yakını {durak(yak['ad'])} ({yak['tur']})"
        hd = min(((min(seg_km(c, s, e) for s, e in segs), ad_, ku) for ad_, ku, _, segs in hatlar))
        o["yeni_hat_km"] = hd[0]; notlar["yeni_hat_km"] = f"en yakını {hd[1]}, güzergâh yaklaşık"
        o["yeni_arz"] = o["eski_stok"] = None
        if per >= 0.5 * bina and per > 0:
            o["yeni_arz"] = (a["y2018eGore"] or 0) / per * 100
            ayr = (a["y2007Oncesi"] or 0) / per  # "2007 öncesi": 1998 öncesi mi sonrası mı ayrılmamış
            if ayr <= AYRILMAMIS_SINIR: o["eski_stok"] = (a["y98Oncesi"] or 0) / per * 100
            else: notlar["eski_stok"] = f"binaların %{ayr * 100:.0f}'i yalnızca \"2007 öncesi\" diye girilmiş; 1998 öncesi payı ayrılamıyor"
        elif bina:
            notlar["yeni_arz"] = notlar["eski_stok"] = f"binaların yalnızca %{per / bina * 100:.0f}'inin yapım dönemi girilmiş; ölçülmedi"
        o["bina_km2"] = bina / alan if alan else None
        o["sel"] = sel.get(str(a["KIMLIKNO"]), 0) / bina * 1000 if bina >= AZ_BINA else None
        if bina < AZ_BINA: notlar["sel"] = f"{bina} bina; oran güvenilmez, ölçülmedi"
        for t in ("okul", "park", "saglik"):
            o[t] = sum(1 for p in osm if p["tur"] == t and abs(p["y"] - c[1]) < 0.01 and km(c, (p["x"], p["y"])) <= YAKIN_KM)
        o["plan"] = sum(1 for p in ham["plan"]["veri"] if icinde(p["x"], p["y"], polys, bb)) / alan if alan else None
        dd = [ad_ for ad_, mk, ps, dbb in don if mk != 10 and not ad_.upper().startswith("İPTAL") and (
              icinde(*merkez([q[0] for q in ps]), polys, bb) or icinde(c[0], c[1], ps, dbb))]
        o["donusum"] = len(dd)
        if dd: notlar["donusum"] = ", ".join(x.replace("_", " ").strip() for x in dd[:3]) + (f" ve {len(dd) - 3} alan daha" if len(dd) > 3 else "")
        mahalleler.append(dict(id=mid, kimlik=a["KIMLIKNO"], ad=ad, ilce=iid,
                               bina=bina, alan_km2=round(alan, 2), merkez=[round(c[0], 5), round(c[1], 5)],
                               olcu={k: (None if v is None else round(v, 2)) for k, v in o.items()}, notlar=notlar, kaynak=dict(yeni_hat_km=hd[2])))
        feats.append(dict(type="Feature", properties=dict(id=mid),
                          geometry=dict(type="MultiPolygon", coordinates=[[[[round(x, 4), round(y, 4)] for x, y in r] for r in p] for p in polys])))
    ids = [m["id"] for m in mahalleler]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    olcutler = [dict(id=i, ad=ad, tercih=t, ters=r, birim=b, kaynak_url=k, not_=n) for i, ad, t, r, b, k, n in OLCUT]
    for oc in olcutler: oc["not"] = oc.pop("not_")
    json.dump(dict(cekildi=ham["mahalle"]["cekildi"], yakin_km=YAKIN_KM, olcutler=olcutler, mahalleler=mahalleler),
              open(D / "mahalleler.json", "w"), ensure_ascii=False, separators=(",", ":"))
    json.dump(dict(type="FeatureCollection", features=feats), open(D / "mahalleler.geojson", "w"), separators=(",", ":"))
    print(len(mahalleler), "mahalle")
    for oc in OLCUT:
        v = sorted(m["olcu"][oc[0]] for m in mahalleler if m["olcu"].get(oc[0]) is not None)
        print(f"  {oc[0]:12s} n={len(v):4d} min={v[0]:.2f} medyan={v[len(v)//2]:.2f} max={v[-1]:.2f}")

if __name__ == "__main__":
    main()
