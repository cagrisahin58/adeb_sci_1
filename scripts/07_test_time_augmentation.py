import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models
import timm
import sys
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import argparse

# Torchattacks kütüphanesini ekle
sys.path.append('./torchattacks')
from torchattacks import FGSM, PGD

# Argüman ayrıştırıcısı
parser = argparse.ArgumentParser(description='Test-Time Augmentation savunması')
parser.add_argument('--model', type=str, choices=['resnet', 'vit'], required=True, help='Değerlendirilecek model türü')
parser.add_argument('--training', type=str, choices=['clean', 'adv'], required=True, help='Eğitim türü')
args = parser.parse_args()

# Model ve eğitim türünü ayarla
model_type = args.model
training_type = args.training

# GPU kontrolü
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Değerlendirme cihazı: {device}")

# Temel dönüşümleri tanımla - model türüne göre
if model_type == 'vit':
    base_transform = transforms.Resize(224)
    img_size = 224
else:
    base_transform = transforms.Lambda(lambda x: x)  # kimlik fonksiyonu
    img_size = 32

# Test-Time Augmentation için 10-crop dönüşümleri
tta_transforms = transforms.Compose([
    base_transform,
    transforms.TenCrop(size=img_size),
    transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops]))
])

# Normal test için dönüşümler
normal_transform = transforms.Compose([
    base_transform,
    transforms.ToTensor()
])

# Veri setleri
testset_normal = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=normal_transform)
testset_tta = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=tta_transforms)

# Dataloaders
testloader_normal = torch.utils.data.DataLoader(testset_normal, batch_size=100, shuffle=False, num_workers=2)
testloader_tta = torch.utils.data.DataLoader(testset_tta, batch_size=10, shuffle=False, num_workers=2)

# Model türüne göre modeli yükle
if model_type == 'resnet':
    model = models.resnet18(weights=None)
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()
    model.fc = nn.Linear(model.fc.in_features, 10)
    
    # Eğitim türüne göre model checkpoint'i yükle
    if training_type == 'clean':
        model_path = 'models/resnet/clean/resnet18_cifar10.pth'
    else:
        model_path = 'models/resnet/adv/resnet18_adv_cifar10.pth'
else:
    model = timm.create_model('vit_tiny_patch16_224', pretrained=False, num_classes=10)
    
    # Eğitim türüne göre model checkpoint'i yükle
    if training_type == 'clean':
        model_path = 'models/vit/clean/vit_tiny_cifar10.pth'
    else:
        model_path = 'models/vit/adv/vit_tiny_adv_cifar10.pth'

# Modeli yükle
model.load_state_dict(torch.load(model_path))
model = model.to(device)
model.eval()

print(f"Model yüklendi: {model_path}")

# Normal değerlendirme (TTA olmadan)
def evaluate_normal(attack=None):
    correct = 0
    total = 0
    
    desc = "Normal değerlendirme" if attack is None else f"Normal değerlendirme ({attack.name})"
    
    for inputs, targets in tqdm(testloader_normal, desc=desc):
        inputs, targets = inputs.to(device), targets.to(device)
        
        if attack is not None:
            inputs = attack(inputs, targets)
        
        with torch.no_grad():
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    acc = 100. * correct / total
    print(f"{desc} doğruluk: {acc:.2f}%")
    return acc

# Test-Time Augmentation değerlendirmesi
def evaluate_tta(attack=None):
    correct = 0
    total = 0
    
    desc = "TTA değerlendirme" if attack is None else f"TTA değerlendirme ({attack.name})"
    
    for inputs, targets in tqdm(testloader_tta, desc=desc):
        batch_size, n_crops, c, h, w = inputs.size()
        
        # TTA olarak gelen input, [batch_size, n_crops, channels, height, width] boyutunda
        # Modele girmesi için [batch_size * n_crops, channels, height, width] boyutuna çevir
        inputs = inputs.view(-1, c, h, w).to(device)
        targets = targets.to(device)
        
        if attack is not None:
            # 10 crop için saldırılar oluştur
            targets_expanded = torch.repeat_interleave(targets, n_crops)
            inputs = attack(inputs, targets_expanded)
        
        with torch.no_grad():
            # Model çıktılarını hesapla
            outputs = model(inputs)
            
            # Çıktıları [batch_size, n_crops, n_classes] şekline çevir
            outputs = outputs.view(batch_size, n_crops, -1)
            
            # Tüm crop'ların tahminlerinin ortalamasını al
            outputs = outputs.mean(1)
            
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    acc = 100. * correct / total
    print(f"{desc} doğruluk: {acc:.2f}%")
    return acc

# Saldırı parametrelerini tanımla
epsilons = [2/255, 8/255]

# Sonuçları sakla
results = []

# Temiz değerlendirme
normal_clean = evaluate_normal()
tta_clean = evaluate_tta()

# Temiz sonuçları ekle
results.append({
    'Model': model_type,
    'Training': training_type,
    'Attack': 'None',
    'Epsilon': 0,
    'Defense': 'None',
    'Accuracy': normal_clean
})

results.append({
    'Model': model_type,
    'Training': training_type,
    'Attack': 'None',
    'Epsilon': 0,
    'Defense': 'TTA',
    'Accuracy': tta_clean
})

# Saldırılar için değerlendir
for eps in epsilons:
    # FGSM saldırısı
    fgsm_attack = FGSM(model, eps=eps)
    fgsm_attack.name = f"FGSM (ε={eps})"
    
    normal_fgsm = evaluate_normal(fgsm_attack)
    tta_fgsm = evaluate_tta(fgsm_attack)
    
    results.append({
        'Model': model_type,
        'Training': training_type,
        'Attack': 'FGSM',
        'Epsilon': eps,
        'Defense': 'None',
        'Accuracy': normal_fgsm
    })
    
    results.append({
        'Model': model_type,
        'Training': training_type,
        'Attack': 'FGSM',
        'Epsilon': eps,
        'Defense': 'TTA',
        'Accuracy': tta_fgsm
    })
    
    # PGD saldırısı
    pgd_attack = PGD(model, eps=eps, alpha=eps/4, steps=10)
    pgd_attack.name = f"PGD (ε={eps})"
    
    normal_pgd = evaluate_normal(pgd_attack)
    tta_pgd = evaluate_tta(pgd_attack)
    
    results.append({
        'Model': model_type,
        'Training': training_type,
        'Attack': 'PGD',
        'Epsilon': eps,
        'Defense': 'None',
        'Accuracy': normal_pgd
    })
    
    results.append({
        'Model': model_type,
        'Training': training_type,
        'Attack': 'PGD',
        'Epsilon': eps,
        'Defense': 'TTA',
        'Accuracy': tta_pgd
    })

# Sonuçları DataFrame'e çevir ve kaydet
results_df = pd.DataFrame(results)
os.makedirs('results', exist_ok=True)
csv_path = f'results/{model_type}_{training_type}_tta_defense.csv'
results_df.to_csv(csv_path, index=False)

print(f"Sonuçlar kaydedildi: {csv_path}")

# Sonuç analizi
tta_improvement = {}
for attack in ['None', 'FGSM', 'PGD']:
    for eps in [0] if attack == 'None' else epsilons:
        normal_acc = results_df[(results_df['Attack'] == attack) & 
                               (results_df['Epsilon'] == eps) & 
                               (results_df['Defense'] == 'None')]['Accuracy'].values[0]
        
        tta_acc = results_df[(results_df['Attack'] == attack) & 
                            (results_df['Epsilon'] == eps) & 
                            (results_df['Defense'] == 'TTA')]['Accuracy'].values[0]
        
        improvement = tta_acc - normal_acc
        if attack == 'None':
            attack_name = 'Clean'
            eps_str = ''
        else:
            attack_name = attack
            eps_str = f" (ε={eps})"
        
        key = f"{attack_name}{eps_str}"
        tta_improvement[key] = improvement
        print(f"TTA iyileştirme - {key}: {improvement:.2f}%")

# Savunma etkinliği özeti
print("\n--- SAVUNMA ETKİNLİĞİ ÖZETİ ---")
if training_type == 'adv':
    print(f"Model: {model_type.upper()} (Adversarial Eğitimli)")
else:
    print(f"Model: {model_type.upper()} (Temiz Eğitimli)")

print(f"Temiz doğruluk: {normal_clean:.2f}%")
print(f"TTA doğruluk: {tta_clean:.2f}%")

for attack_name in ['FGSM', 'PGD']:
    for eps in epsilons:
        normal_acc = results_df[(results_df['Attack'] == attack_name) & 
                               (results_df['Epsilon'] == eps) & 
                               (results_df['Defense'] == 'None')]['Accuracy'].values[0]
        
        tta_acc = results_df[(results_df['Attack'] == attack_name) & 
                            (results_df['Epsilon'] == eps) & 
                            (results_df['Defense'] == 'TTA')]['Accuracy'].values[0]
        
        print(f"{attack_name} (ε={eps}): {normal_acc:.2f}% → {tta_acc:.2f}% (TTA: +{tta_acc-normal_acc:.2f}%)")
