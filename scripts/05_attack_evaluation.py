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
import matplotlib.pyplot as plt

# Torchattacks kütüphanesini ekle
sys.path.append('./torchattacks')
from torchattacks import FGSM, PGD, CW

# Argüman ayrıştırıcısı
parser = argparse.ArgumentParser(description='Model saldırı değerlendirmesi')
parser.add_argument('--model', type=str, choices=['resnet', 'vit'], required=True, help='Değerlendirilecek model türü')
parser.add_argument('--training', type=str, choices=['clean', 'adv'], required=True, help='Eğitim türü')
args = parser.parse_args()

# Model ve eğitim türünü ayarla
model_type = args.model
training_type = args.training

# GPU kontrolü
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Değerlendirme cihazı: {device}")

# Dönüşümleri tanımla - model türüne göre
if model_type == 'vit':
    transform_test = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
    ])
else:
    transform_test = transforms.Compose([
        transforms.ToTensor(),
    ])

# Test veri setini yükle
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)

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

# Kayıp fonksiyonu
criterion = nn.CrossEntropyLoss()

# Temiz doğruluk değerlendirme fonksiyonu
def evaluate_clean():
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, targets in tqdm(testloader, desc="Temiz değerlendirme"):
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    clean_acc = 100. * correct / total
    print(f"Temiz doğruluk: {clean_acc:.2f}%")
    return clean_acc

# Saldırı doğruluk değerlendirme fonksiyonu
def evaluate_attack(attack, attack_name, epsilon):
    correct = 0
    total = 0
    
    for inputs, targets in tqdm(testloader, desc=f"{attack_name} değerlendirme (ε={epsilon})"):
        inputs, targets = inputs.to(device), targets.to(device)
        adv_inputs = attack(inputs, targets)
        
        with torch.no_grad():
            outputs = model(adv_inputs)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    adv_acc = 100. * correct / total
    print(f"{attack_name} (ε={epsilon}) doğruluk: {adv_acc:.2f}%")
    return adv_acc

# Sonuçları saklamak için DataFrame
results = []

# Temiz doğruluk değerlendir
clean_acc = evaluate_clean()
results.append({
    'Model': model_type,
    'Training': training_type,
    'Attack': 'None',
    'Epsilon': 0,
    'Accuracy': clean_acc
})

# Saldırı parametreleri
epsilons = [2/255, 4/255, 8/255]
attack_types = ['FGSM', 'PGD']

# Farklı saldırıları değerlendir
for attack_type in attack_types:
    for eps in epsilons:
        if attack_type == 'FGSM':
            attack = FGSM(model, eps=eps)
        elif attack_type == 'PGD':
            attack = PGD(model, eps=eps, alpha=eps/4, steps=10)
        
        # Saldırıyı değerlendir
        adv_acc = evaluate_attack(attack, attack_type, eps)
        
        # Sonuçları ekle
        results.append({
            'Model': model_type,
            'Training': training_type,
            'Attack': attack_type,
            'Epsilon': eps,
            'Accuracy': adv_acc
        })

# CW saldırısı özel bir durum (epsilon parametresi yok)
if model_type == 'resnet':  # CW saldırısı ViT için çok uzun sürebilir
    attack = CW(model, c=1.0, lr=0.01, steps=50)
    attack_type = 'CW'
    
    # Saldırıyı değerlendir (subset üzerinde)
    subset_size = 1000  # CW çok yavaş olduğu için 1000 örnekle sınırla
    
    subset_loader = torch.utils.data.DataLoader(
        torch.utils.data.Subset(testset, list(range(subset_size))),
        batch_size=100, shuffle=False
    )
    
    correct = 0
    total = 0
    
    for inputs, targets in tqdm(subset_loader, desc="CW değerlendirme"):
        inputs, targets = inputs.to(device), targets.to(device)
        adv_inputs = attack(inputs, targets)
        
        with torch.no_grad():
            outputs = model(adv_inputs)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    adv_acc = 100. * correct / total
    print(f"CW doğruluk: {adv_acc:.2f}% (subset={subset_size})")
    
    results.append({
        'Model': model_type,
        'Training': training_type,
        'Attack': attack_type,
        'Epsilon': 'N/A',
        'Accuracy': adv_acc
    })

# Sonuçları DataFrame'e dönüştür
results_df = pd.DataFrame(results)

# Sonuçları CSV'ye kaydet
os.makedirs('results', exist_ok=True)
csv_path = f'results/{model_type}_{training_type}_attack_results.csv'
results_df.to_csv(csv_path, index=False)
print(f"Sonuçlar kaydedildi: {csv_path}")

# Sonuçları bar grafiği olarak göster
plt.figure(figsize=(10, 6))

# FGSM ve PGD saldırıları için epsilon değerlerini ayrı göster
fgsm_results = results_df[results_df['Attack'] == 'FGSM']
pgd_results = results_df[results_df['Attack'] == 'PGD']

plt.bar(range(len(results)), [r['Accuracy'] for r in results], color='skyblue')
plt.xticks(range(len(results)), [f"{r['Attack']} (ε={r['Epsilon']})" for r in results], rotation=45)
plt.ylabel('Accuracy (%)')
plt.title(f'{model_type.upper()} Model ({training_type.capitalize()} Training) - Attack Evaluation')
plt.tight_layout()

# Grafiği kaydet
plt.savefig(f'results/{model_type}_{training_type}_attack_results.png')
print(f"Grafik kaydedildi: results/{model_type}_{training_type}_attack_results.png")
