# Beşinci kapı kör: "otoriter" değerleri sabit yazılmış

> 2026-08-25'te B2 yeniden üretimi sırasında ölçüldü. `B2_DURUM.md` §9 yerine
> ayrı dosya, çünkü bu kusur B2'den bağımsızdır ve B2 kapandıktan sonra da
> geçerlidir.

## Kusur

`scripts/bildiri_tutarlilik.py` bildirinin taşıyıcı sayılarını "otoriter
değer"lerle karşılaştırıyor. Ama o otoriter değerler betiğin içine **sabit
yazılmış**:

```python
("protokol alt sinir",  r"...", 4.36),
("protokol ust sinir",  r"...", 14.60),
```

Yani kapı, korumaya çalıştığı sayının bir **kopyasını** taşıyor. Artefakt
değiştiğinde kapı bunu göremez — tam da önlemek için yazıldığı kaymayı.

## Ölçüm

B2 düzeltmesinden sonra CIFAR-10 protokol üst sınırı **14,60 → 19,37** oldu.
Kapı yine "tutuyor" dedi ve **GEÇTİ** verdi. Bildiri hâlâ 14,6 ve "3,3 kat"
taşıyor.

Kapının kendi öz-sınaması (`test_bildiri_tutarlilik.sh`) bunu yakalayamaz:
öz-sınama **bildiriyi** bozup kapının gördüğünü sınıyor, **artefaktı** bozup
gördüğünü değil.

## Yapılacak

1. Otoriter değerler artefaktlardan okunacak, sabit yazılmayacak:
   - protokol sınırları → `results/c1_transfer/c1_transfer_summary.json`
   - AutoAttack → `results/c1_eval_summary.json`
   - Hoyer / hizalanma → `results/rev2_blockA/a3_gradient_paired.json`
2. Öz-sınamaya **üçüncü kol**: artefaktı boz, kapının KALDIĞINI doğrula.
3. "3,3 kat" gibi eş-varlık kontrolleri de sayısal karşılaştırmaya çevrilecek
   (şu an yalnız "bildiride VAR / makalede VAR" diye bakıyor; ikisi birlikte
   eskirse sessiz kalır).

## Aynı sınıftan ikinci bulgu

`verify_manuscript_numbers.py` artefaktlardan okuyor, yani bu kusur onda YOK.
Ama orada **bağlamsız alt dize eşleştirmesi** var: `E6 L2 protokol yayilimi`
kontrolü 10,92 arıyor ve metindeki **CIFAR-100'ün her-ikisi-doğru farkı** olan
10,92'yi bulup "OK" veriyor. Oysa $L_2$ yayılımı metinde 10,91 yazıyordu, yani
kontrol gerçekte KALMASI gerekirken geçti. Bildiri kapısındaki gibi bağlam
deseni burada da gerekli.
