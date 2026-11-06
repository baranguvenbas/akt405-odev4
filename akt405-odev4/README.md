# AKT405 - Aktüeryal Yazılımlar Ödev 4

Bu çalışma, altın, Sabancı Holding ve tahvil ETF'i fiyatlarını Python ile Yahoo Finance üzerinden
inceleyen bir yatırım portföyü defteridir.

## Seçilen varlıklar

| Varlık | Yahoo Finance sembolü | Tür | Açıklama |
|---|---|---|---|
| Altın | `GC=F` | Emtia | COMEX altın vadeli işlem kontratı |
| Sabancı Holding | `SAHOL.IS` | Hisse | Sabancı Holding A.Ş. |
| Tahvil ETF'i | `TLT` | Hisse dışı | ABD uzun vadeli Hazine tahvili ETF'i |

Semboller, ödev kapsamındaki sitelerden kontrol edilmiştir. `TLT`, doğrudan tahvil yerine tahvil
piyasasına ETF yoluyla yatırım yapar.

## Veri aralığı

Fiyat verileri **2021-01-01 - 2025-12-31** tarihleri arasındadır. Çekim uc tarih olarak
2026-01-01'i kullanır; veri bir gün öncesi dahil olacak şekilde sınırlandırılır. Her sembol için
ortak işlem günleri tutulmuş; ortak veri **1205 gün** içerir.

## Çalıştırma sırası

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python veri_cek.py
python analiz.py
```

Çalıştırma sonunda `kapanis.csv`, yıllık getiri/volatilite tablosu, korelasyon matrisi ve
`fiyatlar.png` oluşturulur.

## Çeşitlendirme yorumu

Korelasyon matrisi altın, hisse ve tahvil ETF'i arasındaki gerçek hareketleri gösterir. En düşük
korelasyona sahip iki varlık portföy riskini birlikte daha iyi azaltma potansiyeline sahiptir;
Bu veride Sabancı Holding ile tahvil ETF'i (`TLT`) arasında korelasyon yaklaşık **-0.0726** olduğu
için, bu çift birlikte daha güçlü bir çeşitlendirme sağlayabilir. Altın ile Sabancı Holding arasındaki
korelasyon da çok düşük (-0.0015) olup, düşüş dönemlerinde dengeleme etkisi yaratabilir.

## Yapay zekâ kullanımı

Proje dosyalarının oluşturulması, Yahoo Finance sembol doğrulaması, veri işleme ve grafik kodunun
hazırlanmasında yapay zekâ asistanı kullanılmıştır. Hesaplamalar ve çalışma çıktıları yerel olarak
doğrulanmıştır.

## Veri çekim tarihi

Veri bu çalışma kapsamında 2026-11-06 tarihinde çekilmek üzere hazırlanmıştır.

## Yahoo Finance çalışma durumu

Yerel Python 3.15 sanal ortamında bazı denemelerde `yfinance` için `curl_cffi/certifi` katmanından
`error adding trust anchors` SSL hatası oluşmuştur. Bu nedenle `veri_cek.py`, `yfinance` başarısız
olursa Yahoo Finance'ın `query2.finance.yahoo.com/v8/finance/chart` uç noktasını kullanarak veriyi
güvenli şekilde çeker. Bu çalışma tarihinde veri çekimi başarıyla tamamlanmıştır.
