import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models
import os
import time
from tqdm import tqdm
import numpy as np
import random

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
# CIFAR-10 için ilk katmanı modifiye et (224x224 yerine 32x32)
model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
model.maxpool = nn.Identity()  # Maksimum havuzlama katmanını kaldır
model.fc = nn.Linear(model.fc.in_features, 10)  # 10 sınıf için çıkış katmanı

model = model.to(device)

# Kayıp fonksiyonu ve optimize edici
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)

# Modeli eğit
epochs = 50
best_acc = 0

# Zaman takibi
start_time = time.time()

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    progress_bar = tqdm(trainloader, desc=f"Epoch {epoch+1}/{epochs}")
    
    for i, (inputs, labels) in enumerate(progress_bar):
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        progress_bar.set_postfix({
            'loss': running_loss/(i+1),
            'acc': 100.*correct/total
        })
    
    scheduler.step()
    
    # Test et
    model.eval()
    test_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in testloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            test_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    acc = 100.*correct/total
    print(f"Epoch {epoch+1}/{epochs} - Test Doğruluk: {acc:.2f}%")
    
    # En iyi modeli kaydet
    if acc > best_acc:
        best_acc = acc
        torch.save(model.state_dict(), 'models/resnet/clean/resnet18_cifar10.pth')
        print(f"En iyi model kaydedildi! Doğruluk: {best_acc:.2f}%")

elapsed_time = time.time() - start_time
print(f"Eğitim tamamlandı! Toplam süre: {elapsed_time/60:.2f} dakika")
print(f"En iyi test doğruluğu: {best_acc:.2f}%")
