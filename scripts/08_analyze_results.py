import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from glob import glob

# Sonuç klasörünü kontrol et
os.makedirs('results', exist_ok=True)

# Tüm sonuç CSV'lerini içe aktar
result_files = glob('results/*.csv')

if len(result_files) == 0:
    print("Henüz sonuç dosyası bulunamadı. Lütfen önce değerlendirme scriptlerini çalıştırın.")
    exit(0)

# Tüm sonuçları birleştir
all_results = []
for file in result_files:
    df = pd.read_csv(file)
    all_results.append(df)

results_df = pd.concat(all_results)

# Eksik değerleri NaN ile doldur
results_df = results_df.fillna('N/A')

# Veri çerçevesini temizle
# Epsilon değerlerini string'e çevir (grafik gösterimi için)
results_df['Epsilon_str'] = results_df['Epsilon'].apply(lambda x: 'Clean' if x == 0 or x == '0' or x == 'N/A' else f"ε={x}")

# Savunma stratejisini ayarla
results_df['Defense'] = results_df['Defense'].fillna('None')

# Modellerin temiz ve adversarial eğitimli karşılaştırması
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Clean vs PGD8 karşılaştırma
comparison = results_df[
    ((results_df['Attack'] == 'None') & (results_df['Defense'] == 'None')) | 
    ((results_df['Attack'] == 'PGD') & (results_df['Epsilon'] == 8/255) & (results_df['Defense'] == 'None'))
]

sns.barplot(x='Model', y='Accuracy', hue='Attack', data=comparison)
plt.title('Clean vs PGD-8/255 Accuracy by Model and Training')
plt.ylim(0, 100)
plt.savefig('results/clean_vs_pgd_comparison.png')
plt.close()

# Farklı saldırılarla doğruluk karşılaştırması
attacks_to_compare = results_df[
    (results_df['Defense'] == 'None') & 
    (results_df['Attack'].isin(['None', 'FGSM', 'PGD']))
]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for i, model_type in enumerate(['resnet', 'vit']):
    model_results = attacks_to_compare[attacks_to_compare['Model'] == model_type]
    
    # Pivot tablo oluştur
    pivot = pd.pivot_table(
        model_results,
        values='Accuracy',
        index=['Training'],
        columns=['Attack', 'Epsilon_str']
    ).reset_index()
    
    # Daha iyi gösterim için sütunları yeniden düzenle
    column_order = []
    for attack in ['None', 'FGSM', 'PGD']:
        if attack == 'None':
            column_order.append(('None', 'Clean'))
        else:
            for eps in ['ε=0.00784314', 'ε=0.03137255']:
                column_order.append((attack, eps))
    
    # Mevcut sütunları kes (hatalı olabilir)
    try:
        pivot = pivot.loc[:, ['Training'] + column_order]
    except:
        pass  # Tüm sütunlar olmayabilir
    
    # Bar plot çiz
    pivot.plot(x='Training', kind='bar', ax=axes[i])
    axes[i].set_title(f'{model_type.upper()} Model Performance')
    axes[i].set_xlabel('Training Method')
    axes[i].set_ylabel('Accuracy (%)')
    axes[i].legend(title='Attack')
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/attack_comparison_by_model.png')
plt.close()

# Test-Time Augmentation karşılaştırması
if 'TTA' in results_df['Defense'].unique():
    tta_results = results_df[results_df['Defense'].isin(['None', 'TTA'])]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    for i, model_type in enumerate(['resnet', 'vit']):
        for j, training_type in enumerate(['clean', 'adv']):
            model_train_results = tta_results[
                (tta_results['Model'] == model_type) & 
                (tta_results['Training'] == training_type)
            ]
            
            model_train_pivot = pd.pivot_table(
                model_train_results,
                values='Accuracy',
                index=['Attack', 'Epsilon_str'],
                columns=['Defense']
            ).reset_index()
            
            # Bar plot çiz
            sns.barplot(x='Attack', y='None', data=model_train_pivot, color='skyblue', ax=axes[i][j])
            sns.barplot(x='Attack', y='TTA', data=model_train_pivot, color='orange', ax=axes[i][j])
            
            axes[i][j].set_title(f'{model_type.upper()} ({training_type.capitalize()} Training)')
            axes[i][j].set_xlabel('Attack')
            axes[i][j].set_ylabel('Accuracy (%)')
            axes[i][j].legend(['Standard', 'TTA'])
            axes[i][j].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/tta_defense_comparison.png')
    plt.close()

# Adversarial eğitim ve TTA'nın birleşik etkisi
if 'adv' in results_df['Training'].unique() and 'TTA' in results_df['Defense'].unique():
    combined_results = results_df[
        (results_df['Attack'].isin(['None', 'PGD'])) & 
        (results_df['Attack'] == 'None' or results_df['Epsilon'] == 8/255)
    ]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for i, model_type in enumerate(['resnet', 'vit']):
        model_results = combined_results[combined_results['Model'] == model_type]
        
        # Pivot tablo oluştur
        pivot = pd.pivot_table(
            model_results,
            values='Accuracy',
            index=['Training', 'Defense'],
            columns=['Attack', 'Epsilon_str'],
            aggfunc='first'
        ).reset_index()
        
        # Bar plot çiz
        pivot.plot(x='Training', kind='bar', ax=axes[i])
        axes[i].set_title(f'{model_type.upper()} - Combined Defense Effects')
        axes[i].set_xlabel('Training and Defense Combination')
        axes[i].set_ylabel('Accuracy (%)')
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/combined_defense_effects.png')
    plt.close()

# Ana karşılaştırma tablosunu oluştur
print("Ana karşılaştırma tablosu hazırlanıyor...")

# Modeller arası karşılaştırma tablosu (makale için)
comparison_table = pd.pivot_table(
    results_df[(results_df['Defense'] == 'None') | (results_df['Defense'] == 'TTA')],
    values='Accuracy',
    index=['Model', 'Training'],
    columns=['Attack', 'Epsilon_str', 'Defense'],
    aggfunc='first'
).round(2)

# LaTeX formatında tablo olarak kaydet
os.makedirs('paper', exist_ok=True)
with open('paper/comparison_table.tex', 'w') as f:
    f.write(comparison_table.to_latex())

print(f"Sonuç analizi tamamlandı. Grafikler 'results/' klasörüne kaydedildi.")
print(f"Karşılaştırma tablosu 'paper/comparison_table.tex' dosyasına kaydedildi.")

# Kapsamlı sonuç özeti
print("\n============= KAPSAMLI SONUÇ ÖZETİ =============")
for model_type in ['resnet', 'vit']:
    for training_type in ['clean', 'adv']:
        model_df = results_df[
            (results_df['Model'] == model_type) & 
            (results_df['Training'] == training_type)
        ]
        
        # Temiz doğruluk
        clean_acc = model_df[(model_df['Attack'] == 'None') & (model_df['Defense'] == 'None')]['Accuracy'].values[0]
        
        # PGD-8 doğruluk
        pgd8_acc = model_df[
            (model_df['Attack'] == 'PGD') & 
            (model_df['Epsilon'] == 8/255) & 
            (model_df['Defense'] == 'None')
        ]['Accuracy'].values[0] if len(model_df[
            (model_df['Attack'] == 'PGD') & 
            (model_df['Epsilon'] == 8/255) & 
            (model_df['Defense'] == 'None')
        ]) > 0 else "N/A"
        
        # TTA ile PGD-8 doğruluk
        tta_pgd8_acc = model_df[
            (model_df['Attack'] == 'PGD') & 
            (model_df['Epsilon'] == 8/255) & 
            (model_df['Defense'] == 'TTA')
        ]['Accuracy'].values[0] if len(model_df[
            (model_df['Attack'] == 'PGD') & 
            (model_df['Epsilon'] == 8/255) & 
            (model_df['Defense'] == 'TTA')
        ]) > 0 else "N/A"
        
        print(f"\n{model_type.upper()} ({training_type.capitalize()} Eğitimli):")
        print(f"- Temiz doğruluk: {clean_acc:.2f}%")
        print(f"- PGD-8 doğruluk: {pgd8_acc}")
        print(f"- TTA+PGD-8 doğruluk: {tta_pgd8_acc}")
        
        if str(pgd8_acc) != "N/A" and str(tta_pgd8_acc) != "N/A":
            improvement = float(tta_pgd8_acc) - float(pgd8_acc)
            print(f"- TTA iyileştirme: {improvement:.2f}%")
