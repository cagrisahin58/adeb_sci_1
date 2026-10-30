# Denetci: ImageNet modelleri icin get_preprocessing cagrisinin agirlik yuklemeden calisip calismadigi.
import timm, robustbench
from robustbench.data import get_preprocessing
from robustbench.model_zoo.enums import BenchmarkDataset, ThreatModel
import robustbench.model_zoo.imagenet  # kayit
adlar = ["Salman2020Do_R18", "Salman2020Do_R50", "Salman2020Do_50_2", "Engstrom2019Robustness", "Chen2024Data_WRN_50_2",
         "Peng2023Robust", "Singh2023Revisiting_ConvNeXt-T-ConvStem", "Singh2023Revisiting_ViT-S-ConvStem",
         "Singh2023Revisiting_ConvNeXt-B-ConvStem", "Singh2023Revisiting_ViT-B-ConvStem", "Liu2023Comprehensive_ConvNeXt-B",
         "Liu2023Comprehensive_Swin-B", "Mo2022When_ViT-B", "Debenedetti2022Light_XCiT-S12", "Wong2020Fast"]
for ad in adlar:
    tn = f"{ad.lower().replace('-', '_')}_imagenet_linf"
    try:
        tf = get_preprocessing(BenchmarkDataset("imagenet"), ThreatModel("Linf"), ad, None)
        print("OK ", ad, "timm_adi_kayitli=", timm.is_model(tn), "|", repr(tf).replace("\n", " ")[:170])
    except Exception as e:
        print("HATA", ad, type(e).__name__, e)
print("timm xcit kayitlari:", [m for m in timm.list_models("*debenedetti*")][:10])
