# bandl — şu an ne doğru?

- Ankara ilçe değer haritası. Spec ve Lovable promptları: PROJECT.md. Kaynaklar ve varlıklar: README.md.
- Uydurma veri yok. Her sayı ve olay kaynak URL'li. Kaynak yoksa "kaynak bulunamadı" yazılır.
- Nominal TL ile sınıflama yapılmaz. Ölçü: ilçe m² fiyatının 11 ilçe medyanına oranı.
- Sınıflama v1 = yapı (Kızılay'a uzaklık, r=0,85) + Ankara emsalleri + kural. v0 ("metro geliyorsa değerlenebilir") Keçiören emsaliyle çürüdü, geri getirme.
- Veri tek yerden üretilir: `python3 data/build.py`. Seed ve sınıflama kuralı o dosyada.
- Uygulama Lovable'da. Lovable mevcut repoyu içeri alamaz, kendi reposunu açar.
  Bu repo spec ve veriyi tutar; `data/` Lovable reposuna `src/data/` olarak basılır.
- Fiyatlar Endeksa'nın yayımlanmış rakamları. Emlakjet kazımayı yasaklıyor; otomatik çekme yazılmaz.
- 26 Eyl 2026: GarajX "Ship in Ankara", bina süresi ~2 sa 15 dk.
