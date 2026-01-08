# Docker + VSCode + GPU + Claude Code Kurulum Rehberi

> Bu rehber, Windows WSL2 üzerinde Docker container içinden VSCode çalıştırarak GPU destekli geliştirme ortamı kurmayı anlatır.

---

## 1. ÖN KOŞULLAR

### Windows Tarafı
- [ ] Windows 10/11 (Build 19041+)
- [ ] WSL2 etkin
- [ ] Docker Desktop kurulu (WSL2 backend)
- [ ] NVIDIA GPU Driver (Windows tarafında, 570+ önerilir)

### Kurulum Kontrolleri
```powershell
# PowerShell'de çalıştır
wsl --version          # WSL2 olmalı
docker --version       # Docker Desktop
nvidia-smi             # GPU görünmeli
```

---

## 2. NVIDIA CONTAINER TOOLKIT (WSL2 İçinde)

```bash
# WSL2 terminal'de çalıştır
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Test
```bash
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

---

## 3. PROJE YAPISI

```
my-project/
├── .devcontainer/
│   ├── devcontainer.json    # VSCode Dev Container config
│   └── docker-compose.yml   # Docker Compose config
├── src/
├── requirements.txt
└── ...
```

---

## 4. DEVCONTAINER DOSYALARI

### 4.1 devcontainer.json

```json
{
    "name": "Project Name",
    "dockerComposeFile": "docker-compose.yml",
    "service": "dev-container",
    "workspaceFolder": "/workspace/project-name",
    "customizations": {
        "vscode": {
            "extensions": [
                "anthropic.claude-code",
                "ms-python.python",
                "ms-toolsai.jupyter"
            ]
        }
    }
}
```

**Önemli alanlar:**
- `service`: docker-compose.yml'deki servis adı
- `workspaceFolder`: Container içindeki çalışma dizini
- `extensions`: Otomatik kurulacak VSCode eklentileri

### 4.2 docker-compose.yml (GPU Destekli)

```yaml
version: '3.8'
services:
  dev-container:
    image: nvcr.io/nvidia/pytorch:25.01-py3
    working_dir: /workspace/project-name
    volumes:
      - ..:/workspace/project-name:cached
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    stdin_open: true
    tty: true
```

**Önemli alanlar:**
- `image`: NVIDIA NGC container (PyTorch, TensorFlow, vb.)
- `volumes`: Proje dizinini container'a bağla
- `deploy.resources`: GPU reservation

---

## 5. NVIDIA NGC CONTAINER SEÇENEKLERİ

| İhtiyaç | Image | Boyut |
|---------|-------|-------|
| PyTorch | `nvcr.io/nvidia/pytorch:25.01-py3` | ~15GB |
| TensorFlow | `nvcr.io/nvidia/tensorflow:25.01-tf2-py3` | ~15GB |
| CUDA Only | `nvcr.io/nvidia/cuda:12.8.0-devel-ubuntu24.04` | ~5GB |
| JAX | `nvcr.io/nvidia/jax:25.01-py3` | ~12GB |

> Not: NGC container'ları her ay güncellenir (25.01 = 2025 Ocak)

---

## 6. VSCODE İLE AÇMA

### Yöntem 1: Command Palette
1. VSCode aç
2. `Ctrl+Shift+P` → "Dev Containers: Open Folder in Container"
3. Proje klasörünü seç
4. Container build edilir ve açılır

### Yöntem 2: Sol Alt Köşe
1. VSCode sol alt köşedeki yeşil `><` ikonuna tıkla
2. "Reopen in Container" seç

### İlk Açılışta
- Container image indirilir (~15GB, ilk seferde)
- Extension'lar kurulur
- Claude Code extension aktif olur

---

## 7. CLAUDE CODE EXTENSION

### Kurulum
Container açıldıktan sonra otomatik kurulur (`devcontainer.json`'da tanımlı).

### Manuel Aktivasyon
```bash
# Container terminal'de
claude  # veya extension panelinden
```

### Özellikler
- Doğrudan GPU erişimi var
- PyTorch/CUDA kullanabilir
- Model eğitimi çalıştırabilir
- Dosya okuma/yazma tam yetki

---

## 8. MEVCUT ORTAM BİLGİLERİ

Bu proje şu ortamda çalışıyor:

| Bileşen | Versiyon |
|---------|----------|
| Base Image | `nvcr.io/nvidia/pytorch:25.01-py3` |
| Ubuntu | 24.04.1 LTS |
| Python | 3.12.3 |
| PyTorch | 2.6.0 (CUDA 12.8) |
| CUDA | 12.8.0 |
| GPU | RTX 5060 Ti (16GB) |
| Driver | 591.44 |

### Önemli Environment Variables
```bash
CUDA_VERSION=12.8.0.038
CUDA_HOME=/usr/local/cuda
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility,video
```

---

## 9. SORUN GİDERME

### GPU Görünmüyor
```bash
# WSL2'de docker daemon'ı yeniden başlat
sudo service docker restart

# Windows'ta Docker Desktop'ı yeniden başlat
```

### Permission Denied
```yaml
# docker-compose.yml'e ekle:
user: root  # veya "1000:1000"
```

### Container Açılmıyor
```bash
# Manuel build dene
cd .devcontainer
docker-compose build
docker-compose up -d
```

### Extension Kurulmuyor
```json
// devcontainer.json'a ekle:
"postCreateCommand": "pip install -r requirements.txt"
```

---

## 10. YENİ PROJE OLUŞTURMA (TEMPLATE)

Yeni proje için bu adımları takip et:

```bash
# 1. Proje klasörü oluştur
mkdir my-new-project && cd my-new-project

# 2. .devcontainer klasörü oluştur
mkdir .devcontainer

# 3. Dosyaları kopyala
# devcontainer.json ve docker-compose.yml dosyalarını yukarıdaki örneklerden kopyala

# 4. Proje adını güncelle
# - devcontainer.json: "name" ve "workspaceFolder"
# - docker-compose.yml: "working_dir" ve volumes

# 5. VSCode ile aç
code .
# Sonra "Reopen in Container"
```

---

## 11. FAYDALI KOMUTLAR

```bash
# GPU durumu
nvidia-smi

# PyTorch GPU testi
python -c "import torch; print(torch.cuda.is_available())"

# CUDA versiyonu
nvcc --version

# Container içinden host'a erişim
# (genelde gerek yok, volume mount kullan)
```

---

## 12. İPUÇLARI

1. **İlk indirme uzun sürer**: NGC image'ları ~15GB, sabırlı ol
2. **Volume cache**: `:cached` flag'i performansı artırır
3. **Extension sync**: GitHub account ile extension'ları senkronla
4. **Git credentials**: Container içinde git config gerekebilir
5. **Persist data**: Volume mount olmayan veriler container silinince kaybolur

---

## 13. ÖRNEK: SIFIRDAN PROJE

```bash
# Terminal'de
mkdir awesome-ml-project
cd awesome-ml-project
mkdir -p .devcontainer

# devcontainer.json oluştur
cat > .devcontainer/devcontainer.json << 'EOF'
{
    "name": "Awesome ML",
    "dockerComposeFile": "docker-compose.yml",
    "service": "ml-dev",
    "workspaceFolder": "/workspace/awesome-ml-project",
    "customizations": {
        "vscode": {
            "extensions": [
                "anthropic.claude-code",
                "ms-python.python"
            ]
        }
    }
}
EOF

# docker-compose.yml oluştur
cat > .devcontainer/docker-compose.yml << 'EOF'
version: '3.8'
services:
  ml-dev:
    image: nvcr.io/nvidia/pytorch:25.01-py3
    working_dir: /workspace/awesome-ml-project
    volumes:
      - ..:/workspace/awesome-ml-project:cached
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    stdin_open: true
    tty: true
EOF

# VSCode ile aç
code .
```

Sonra VSCode'da "Reopen in Container" yap ve hazırsın!

---

> **Not**: Bu rehber 2026-01-05 tarihinde oluşturulmuştur. NGC container versiyonları güncellendikçe image tag'lerini kontrol et.
