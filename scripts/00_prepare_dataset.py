import torch
import torchvision
import torchvision.transforms as transforms
import os

print("CIFAR-10 veri seti indiriliyor ve hazırlanıyor...")

# Dönüşümleri tanımla
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
])

# Eğitim setini indir
trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform_train)

# Test setini indir
testset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform_test)

print(f"Eğitim seti boyutu: {len(trainset)}")
print(f"Test seti boyutu: {len(testset)}")

# Sınıf isimlerini kontrol et
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
print(f"Sınıflar: {classes}")

print("CIFAR-10 veri seti başarıyla hazırlandı!")
