import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models
from tqdm import tqdm
import time
import numpy as np
import random
import os
import sys

# Torchattacks kütüphanesini ekle
sys.path.append('./torchattacks')
from torchattacks import PGD

# Yeniden üretilebilirlik için seed ayarları
seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cudnn.deterministic = True

# GPU kontrolü
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Eğitim cihazı: {device}")

# Dönüşümleri tanımla
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
])

# Veri setlerini yükle
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)

# ResNet18 modelini tanımla
model = models.resnet18(weights=None)
# CIFAR-10 için ilk katmanı modifiye et
model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
model.maxpool = nn.Identity()
model.fc = nn.Linear(model.fc.in_features, 10)

model = model.to(device)

# Önceden eğitilmiş temiz modeli yükle
model.load_state_dict(torch.load('models/resnet/clean/resnet18_cifar10.pth'))
print("Önceden eğitilmiş model yüklendi.")

# Kayıp fonksiyonu ve optimize edici
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=25)

# PGD saldırı parametrelerini tanımla (epsilon=8/255, alpha=2/255, steps=10)
atk = PGD(model, eps=8/255, alpha=2/255, steps=10, random_start=True)

# Adversarial eğitim fonksiyonu
def train_adv(epoch):
    model.train()
    train_loss = 0
    correct = 0
    total = 0
    
    progress_bar = tqdm(trainloader, desc=f"Epoch {epoch+1}/{epochs}")
    
    for i, (inputs, labels) in enumerate(progress_bar):
        inputs, labels = inputs.to(device), labels.to(device)
        
        # Adversarial örnekler oluştur
        adv_inputs = atk(inputs, labels)
        
        optimizer.zero_grad()
        
        # Normal ve adversarial örnekler üzerinde eğitim
        outputs_clean = model(inputs)
        loss_clean = criterion(outputs_clean, labels)
        
        outputs_adv = model(adv_inputs)
        loss_adv = criterion(outputs_adv, labels)
        
        # Toplam kayıp: (Clean + Adversarial) / 2
        loss = (loss_clean + loss_adv) / 2
        
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item()
        _, predicted = outputs_adv.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        progress_bar.set_postfix({
            'loss': train_loss/(i+1),
            'adv_acc': 100.*correct/total
        })

# Test fonksiyonu
def test(epoch, adversarial=False):
    model.eval()
    test_loss = 0
    correct = 0
    total = 0
    
    desc = "Adversarial Test" if adversarial else "Clean Test"
    progress_bar = tqdm(testloader, desc=desc)
    
    for inputs, labels in progress_bar:
        inputs, labels = inputs.to(device), labels.to(device)
        
        if adversarial:
            inputs = atk(inputs, labels)
        
        with torch.no_grad():
            outputs = model(inputs)
            loss = criterion(outputs, labels)
        
        test_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        progress_bar.set_postfix({
            'loss': test_loss/(progress_bar.n+1),
            'acc': 100.*correct/total
        })
    
    acc = 100.*correct/total
    print(f"{desc} doğruluk: {acc:.2f}%")
    return acc

# Modeli eğit
epochs = 25
best_adv_acc = 0
start_time = time.time()

print("Adversarial eğitim başlatılıyor...")

for epoch in range(epochs):
    train_adv(epoch)
    
    clean_acc = test(epoch, adversarial=False)
    adv_acc = test(epoch, adversarial=True)
    
    scheduler.step()
    
    # En iyi adversarial doğruluk oranına sahip modeli kaydet
    if adv_acc > best_adv_acc:
        best_adv_acc = adv_acc
        torch.save(model.state_dict(), 'models/resnet/adv/resnet18_adv_cifar10.pth')
        print(f"En iyi adversarial model kaydedildi! Adv. Doğruluk: {best_adv_acc:.2f}%")

elapsed_time = time.time() - start_time
print(f"Eğitim tamamlandı! Toplam süre: {elapsed_time/60:.2f} dakika")
print(f"En iyi adversarial doğruluk: {best_adv_acc:.2f}%")
