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

# AI Robustness Platform'u ekle
sys.path.append('./robustness')
from autoattack import AutoAttack

# Argüman ayrıştırıcısı
parser = argparse.ArgumentParser(description='AutoAttack ile model değerlendirmesi')
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
# AutoAttack yavaş olduğu için subset kullan
subset_size = 1000
subset_indices = np.random.choice(len(testset), subset_size, replace=False)
subset = torch.utils.data.Subset(testset, subset_indices)
testloader = torch.utils.data.DataLoader(subset, batch_size=100, shuffle=False, num_workers=2)

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

# AutoAttack için model wrapper sınıfı
class ModelWrapper(nn.Module):
    def __init__(self, model):
        super(ModelWrapper, self).__init__()
        self.model = model
        self.num_classes = 10
        
    def forward(self, x):
        return self.model(x)

model_wrapped = ModelWrapper(model)

# Temiz doğruluk değerlendirme
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

# Temiz doğruluk ölç
clean_acc = evaluate_clean()

# AutoAttack değerlendirme
epsilons = [2/255, 4/255, 8/255]
results = []

# Temiz sonucu ekle
results.append({
    'Model': model_type,
    'Training': training_type,
    'Attack': 'None',
    'Epsilon': 0,
    'Accuracy': clean_acc
})

# Her epsilon değeri için AutoAttack değerlendirmesi
for eps in epsilons:
    print(f"\nAutoAttack değerlendirmesi başlatılıyor (ε={eps})...")
    
    # AutoAttack örneği oluştur
    adversary = AutoAttack(model_wrapped, norm='Linf', eps=eps, version='standard')
    
    # Tüm test setini topla
    x_test = []
    y_test = []
    
    for inputs, targets in testloader:
        x_test.append(inputs)
        y_test.append(targets)
    
    x_test = torch.cat(x_test).to(device)
    y_test = torch.cat(y_test).to(device)
    
    # AutoAttack'i çalıştır
    start_time = time.time()
    x_adv = adversary.run_standard_evaluation(x_test, y_test, bs=100)
    elapsed_time = time.time() - start_time
    
    # Adversarial örneklerle doğruluğu değerlendir
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        outputs = model(x_adv)
        _, predicted = outputs.max(1)
        total = y_test.size(0)
        correct = predicted.eq(y_test).sum().item()
    
    adv_acc = 100. * correct / total
    print(f"AutoAttack (ε={eps}) doğruluk: {adv_acc:.2f}%")
    print(f"Süre: {elapsed_time/60:.2f} dakika")
    
    # Sonuçları ekle
    results.append({
        'Model': model_type,
        'Training': training_type,
        'Attack': 'AutoAttack',
        'Epsilon': eps,
        'Accuracy': adv_acc
    })

# Sonuçları DataFrame'e dönüştür
results_df = pd.DataFrame(results)

# Sonuçları CSV'ye kaydet
os.makedirs('results', exist_ok=True)
csv_path = f'results/{model_type}_{training_type}_autoattack_results.csv'
results_df.to_csv(csv_path, index=False)
print(f"Sonuçlar kaydedildi: {csv_path}")
