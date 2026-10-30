#!/bin/bash
O=/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim/dis/rb
mkdir -p $O; cd $O
B=https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info
for m in Rice2020Overfitting Rade2021Helper_R18_ddpm Addepalli2022Efficient_RN18 Sehwag2021Proxy Pang2022Robustness_WRN28_10 Wang2023Better_WRN-28-10 Jia2022LAS-AT_34_10 Debenedetti2022Light_XCiT-S12 Hendrycks2019Using; do
  curl -sL "$B/cifar100/Linf/$m.json" -o c100_$m.json
  python3 -c "import json,sys;d=json.load(open('c100_$m.json'));print('c100',sys.argv[1],d.get('clean_acc'),d.get('autoattack_acc'),d.get('additional_data'))" $m
done
for m in Salman2020Do_R18 Salman2020Do_R50 Salman2020Do_50_2 Engstrom2019Robustness Chen2024Data_WRN_50_2 Peng2023Robust Singh2023Revisiting_ConvNeXt-T-ConvStem Singh2023Revisiting_ViT-S-ConvStem Singh2023Revisiting_ConvNeXt-B-ConvStem Singh2023Revisiting_ViT-B-ConvStem Liu2023Comprehensive_ConvNeXt-B Liu2023Comprehensive_Swin-B Mo2022When_ViT-B Debenedetti2022Light_XCiT-S12 Wong2020Fast; do
  curl -sL "$B/imagenet/Linf/$m.json" -o in_$m.json
  python3 -c "import json,sys;d=json.load(open('in_$m.json'));print('in',sys.argv[1],d.get('clean_acc'),d.get('autoattack_acc'),d.get('additional_data'))" $m
done
