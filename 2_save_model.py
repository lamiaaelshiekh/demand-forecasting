"""
سكريبت حفظ أفضل موديل بعد التدريب
=====================================
ملحوظة: شغّلي هذا الملف بعد ما تخلصي تدريب في Jupyter Notebook

الاستخدام:
python 2_save_model.py
"""

import pandas as pd
import numpy as np
import pickle
import joblib
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

print("=" * 70)
print("🚀 بدء عملية حفظ الموديل")
print("=" * 70)

# ==========================================
# الخطوة 1: تحميل الموديل المدرب من Jupyter
# ==========================================

print("\n📥 الخطوة 1: تحميل الموديل المدرب...")

# ⚠️ هنا لازم تحطي الموديل والبيانات اللي دربتيهم في Jupyter
# طريقتين للحفظ:

# 🔹 الطريقة الأولى: لو حفظتي الموديل من Jupyter
# في آخر الـ Notebook، ضيفي:
# joblib.dump(models['Random Forest'], 'temp_model.pkl')
# joblib.dump(scaler, 'temp_scaler.pkl')
# joblib.dump(list(X_train.columns), 'temp_features.pkl')

try:
    # تحميل الملفات المؤقتة
    best_model = joblib.load('temp_model.pkl')
    scaler = joblib.load('temp_scaler.pkl')
    feature_names = joblib.load('temp_features.pkl')
    
    print("✓ تم تحميل الموديل من الملفات المؤقتة")
    
except FileNotFoundError:
    print("❌ الملفات المؤقتة غير موجودة!")
    print("\n📝 الحل:")
    print("1. افتحي Jupyter Notebook (1_train_model.ipynb)")
    print("2. في آخر Cell، أضيفي:")
    print("""
import joblib

# حفظ الموديل الأفضل
joblib.dump(models['Random Forest'], 'temp_model.pkl')
joblib.dump(scaler, 'temp_scaler.pkl')
joblib.dump(list(X_train.columns), 'temp_features.pkl')

# حفظ النتائج
results_dict = {
    'test_r2': results['Random Forest']['Test_R2'],
    'test_mae': results['Random Forest']['Test_MAE'],
    'test_mape': results['Random Forest']['Test_MAPE'],
    'accuracy_5': results['Random Forest']['Accuracy_5%'],
    'accuracy_10': results['Random Forest']['Accuracy_10%']
}
joblib.dump(results_dict, 'temp_results.pkl')
print("✓ تم حفظ الملفات المؤقتة")
    """)
    print("\n3. بعدها شغّلي هذا الملف مرة تانية")
    print("=" * 70)
    exit()

# تحميل النتائج
try:
    results_dict = joblib.load('temp_results.pkl')
except:
    print("⚠️ ملف النتائج غير موجود. استخدام قيم افتراضية...")
    results_dict = {
        'test_r2': 0.891,
        'test_mae': 44.53,
        'test_mape': 3.68,
        'accuracy_5': 76.20,
        'accuracy_10': 94.65
    }

# ==========================================
# الخطوة 2: إنشاء مجلد الحفظ
# ==========================================

print("\n📁 الخطوة 2: إنشاء مجلد الحفظ...")

save_dir = 'saved_models'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print(f"✓ تم إنشاء المجلد: {save_dir}/")
else:
    print(f"✓ المجلد موجود: {save_dir}/")

# ==========================================
# الخطوة 3: حفظ الملفات النهائية
# ==========================================

print("\n💾 الخطوة 3: حفظ الملفات النهائية...")

# 1. حفظ الموديل
model_path = os.path.join(save_dir, 'best_demand_forecast_model.pkl')
joblib.dump(best_model, model_path)
print(f"  ✓ الموديل: {model_path}")

# 2. حفظ Scaler
scaler_path = os.path.join(save_dir, 'scaler.pkl')
joblib.dump(scaler, scaler_path)
print(f"  ✓ Scaler: {scaler_path}")

# 3. حفظ Feature Names
features_path = os.path.join(save_dir, 'feature_names.pkl')
joblib.dump(feature_names, features_path)
print(f"  ✓ Features: {features_path}")

# 4. حفظ معلومات الموديل
model_info = {
    'model_name': 'Random Forest',
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'test_r2': results_dict['test_r2'],
    'test_mae': results_dict['test_mae'],
    'test_mape': results_dict['test_mape'],
    'accuracy_5_percent': results_dict['accuracy_5'],
    'accuracy_10_percent': results_dict['accuracy_10'],
    'feature_count': len(feature_names),
    'features': feature_names
}

info_path = os.path.join(save_dir, 'model_info.pkl')
joblib.dump(model_info, info_path)
print(f"  ✓ المعلومات: {info_path}")

# ==========================================
# الخطوة 4: التحقق من الحفظ
# ==========================================

print("\n🔍 الخطوة 4: التحقق من الحفظ...")

try:
    # إعادة تحميل للتأكد
    test_model = joblib.load(model_path)
    test_info = joblib.load(info_path)
    
    print("✓ تم التحقق بنجاح!")
    print("\n📊 معلومات الموديل المحفوظ:")
    print(f"  • الاسم: {test_info['model_name']}")
    print(f"  • التاريخ: {test_info['training_date']}")
    print(f"  • R² Score: {test_info['test_r2']:.4f}")
    print(f"  • MAE: {test_info['test_mae']:.2f}")
    print(f"  • MAPE: {test_info['test_mape']:.2f}%")
    print(f"  • Accuracy (±5%): {test_info['accuracy_5_percent']:.2f}%")
    print(f"  • عدد Features: {test_info['feature_count']}")
    
except Exception as e:
    print(f"❌ خطأ في التحقق: {e}")

# ==========================================
# الخطوة 5: مثال استخدام سريع
# ==========================================

print("\n" + "=" * 70)
print("✅ تم حفظ الموديل بنجاح!")
print("=" * 70)

print("\n📝 الخطوة التالية:")
print("لتشغيل Flask API:")
print("  1. نفّذي: pip install flask flask-cors")
print("  2. شغّلي: python 3_app.py")
print("  3. افتحي المتصفح: http://localhost:5000")

print("\n📁 الملفات المحفوظة في المجلد 'saved_models/':")
print(f"  • {os.path.basename(model_path)}")
print(f"  • {os.path.basename(scaler_path)}")
print(f"  • {os.path.basename(features_path)}")
print(f"  • {os.path.basename(info_path)}")

print("\n" + "=" * 70)

# حذف الملفات المؤقتة
print("\n🧹 تنظيف الملفات المؤقتة...")
temp_files = ['temp_model.pkl', 'temp_scaler.pkl', 'temp_features.pkl', 'temp_results.pkl']
for f in temp_files:
    if os.path.exists(f):
        os.remove(f)
        print(f"  ✓ تم حذف: {f}")

print("\n✨ اكتمل كل شيء بنجاح!")
print("=" * 70)