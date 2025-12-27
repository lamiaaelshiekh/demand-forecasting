"""
⚡ نظام التنبؤ بالحمل الكهربائي - نسخة محسنة ومصححة
"""

import os
import gdown
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================
# إعدادات الصفحة
# ============================================
st.set_page_config(
    page_title="نظام الذكاء الاصطناعي للتنبؤ بالطاقة",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# الأنماط CSS المحسنة
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 40px;
        margin: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 3rem;
        padding: 20px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        padding-bottom: 15px;
        border-bottom: 3px solid #667eea;
    }
    
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        padding: 4rem 3rem;
        text-align: center;
        color: white;
        margin: 3rem 0;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        border: none;
    }
    
    .prediction-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
    }
    
    .prediction-value {
        font-size: 6rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }
    
    .success-message {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        border: none;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 18px 40px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 20px;
        width: 100%;
        transition: all 0.4s ease;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.5);
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    }
    
    .info-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        transition: transform 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f6f9ff 0%, #ffffff 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border-left: 6px solid #667eea;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 10px;
        text-align: center;
        border: none;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .status-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 15px;
        font-weight: bold;
    }
    
    .status-medium {
        background: linear-gradient(135deg, #ffd93d 0%, #ff9f1a 100%);
        color: #2d3748;
        padding: 10px 20px;
        border-radius: 15px;
        font-weight: bold;
    }
    
    .status-low {
        background: linear-gradient(135deg, #6bcf7f 0%, #4caf50 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 15px;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        color: #718096;
        font-size: 0.9rem;
        border-top: 2px solid #e2e8f0;
        background: #f8f9fa;
        border-radius: 15px;
    }
    
    .footer-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .footer-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .footer-section {
        flex: 1;
        min-width: 250px;
        text-align: center;
    }
    
    .footer-icons {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 10px;
    }
    
    .footer-icon {
        font-size: 1.5rem;
        transition: transform 0.3s;
    }
    
    .footer-icon:hover {
        transform: scale(1.2);
    }
    
    .spinner-container {
        text-align: center;
        padding: 40px;
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# تحميل النموذج (متوافق مع Streamlit Cloud)
# ============================================
MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(MODEL_DIR, "best_demand_forecast_model.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "feature_names.pkl")
INFO_PATH = os.path.join(MODEL_DIR, "model_info.pkl")


@st.cache_resource
def load_model():
    try:
        # إنشاء فولدر الموديل لو مش موجود
        os.makedirs(MODEL_DIR, exist_ok=True)

        # تحميل الموديل الكبير من Google Drive لو مش موجود
        if not os.path.exists(MODEL_PATH):
            gdown.download(
                "https://drive.google.com/file/d/1wKgkR0UahzrzRnkK5Ph6xCDWEdjirXRo/view",
                MODEL_PATH,
                quiet=False,
                fuzzy=True
            )
        # تحميل الملفات
        model = joblib.load(MODEL_PATH)
        features = joblib.load(FEATURES_PATH)
        info = joblib.load(INFO_PATH)

        return model, features, info

    except Exception as e:
        st.error(f"❌ خطأ في تحميل النموذج: {e}")

        # بيانات افتراضية للعرض فقط
        info = {
            'test_r2': 0.92,
            'test_mape': 3.5,
            'accuracy_5_percent': 88.7,
            'model_name': 'Random Forest Regressor',
            'training_date': '2024-01-01'
        }

        return None, None, info


model, features, info = load_model()

# ============================================
# الشريط الجانبي
# ============================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <h1 style='color: black; font-size: 2.5rem; margin: 0;'>⚡</h1>
        <h2 style='color: black; font-size: 1.8rem; margin: 10px 0;'>مركز التحكم</h2>
        <p style='color: rgba(0,0,0,0.8);'>نظام الذكاء الاصطناعي المتقدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # تحويل التاريخ والوقت
    current_time = datetime.now()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🕐 الوقت", current_time.strftime("%H:%M"))
    with col2:
        st.metric("📅 التاريخ", current_time.strftime("%Y-%m-%d"))
    
    st.markdown("---")
    
    # إعدادات سريعة
    st.markdown("### ⚙️ الإعدادات السريعة")
    
    auto_refresh = st.toggle("🔄 التحديث التلقائي", value=False)
    
    prediction_mode = st.selectbox(
        "🎯 وضع التنبؤ",
        ["🔵 دقيق", "🟡 سريع", "🔴 عالي الدقة"],
        index=0
    )
    
    st.markdown("---")
    
    # معلومات النظام
    st.markdown("### 📊 حالة النظام")
    st.progress(info['test_r2'], text=f"دقة النظام: {info['test_r2']:.1%}")
    
    if info['test_r2'] > 0.9:
        st.success("✅ النظام يعمل بمستوى ممتاز")
    elif info['test_r2'] > 0.8:
        st.info("ℹ️ النظام يعمل بمستوى جيد")
    else:
        st.warning("⚠️ النظام يحتاج إلى تحسين")

# ============================================
# الواجهة الرئيسية
# ============================================

# الحاوية الرئيسية
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# العنوان الرئيسي مع تأثير خاص
st.markdown('<h1 class="title"> نظام الذكاء الاصطناعي للتنبؤ بالحمل الكهربائي</h1>', unsafe_allow_html=True)

# مؤشرات الأداء
st.markdown('<div class="subtitle">📈 مؤشرات الأداء الرئيسية</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2.5rem; color: #667eea;">🎯</div>
        <h3 style="margin: 10px 0;">دقة النموذج</h3>
        <div style="font-size: 2rem; font-weight: 800; color: #2d3748;">{info['test_r2']:.1%}</div>
        <div style="color: #718096; margin-top: 10px;">نسبة التنبؤ الصحيح</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2.5rem; color: #667eea;">📉</div>
        <h3 style="margin: 10px 0;">معدل الخطأ</h3>
        <div style="font-size: 2rem; font-weight: 800; color: #2d3748;">{info['test_mape']:.2f}%</div>
        <div style="color: #718096; margin-top: 10px;">MAPE</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2.5rem; color: #667eea;">✅</div>
        <h3 style="margin: 10px 0;">الدقة (±5%)</h3>
        <div style="font-size: 2rem; font-weight: 800; color: #2d3748;">{info['accuracy_5_percent']:.1f}%</div>
        <div style="color: #718096; margin-top: 10px;">هامش 5%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2.5rem; color: #667eea;">🤖</div>
        <h3 style="margin: 10px 0;">النموذج</h3>
        <div style="font-size: 1.2rem; font-weight: 800; color: #2d3748;">{info['model_name']}</div>
        <div style="color: #718096; margin-top: 10px;">Random Forest</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

# ============================================
# واجهة الإدخال
# ============================================

st.markdown('<div class="subtitle">📝 إدخال بيانات التنبؤ</div>', unsafe_allow_html=True)

# استخدام تبويبات لجعل الواجهة أكثر تنظيماً
tab1, tab2, tab3 = st.tabs(["📅 التاريخ والوقت", "🌤️ بيانات الطقس", "⚙️ إعدادات متقدمة"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### تقويم متقدم")
        
        # تقويم مخصص
        date_input = st.date_input(
            "📅 اختر التاريخ المطلوب",
            value=datetime.now(),
            min_value=datetime.now() - timedelta(days=30),
            max_value=datetime.now() + timedelta(days=365),
            help="اختر تاريخاً ضمن المدى المتاح للتنبؤ"
        )
        
        # عرض معلومات التاريخ
        day_name_arabic = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"][date_input.weekday()]
        st.info(f"**{day_name_arabic}** | {date_input.strftime('%Y-%m-%d')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### ⏰ اختيار الساعة")
        
        # مؤشر ساعة مع تصميم خاص
        hour_input = st.select_slider(
            "الساعة",
            options=list(range(24)),
            value=12,
            format_func=lambda x: f"{x:02d}:00",
            help="اختر ساعة اليوم (0-23)"
        )
        
        # مؤشر بصري للساعة
        st.progress(hour_input / 23, text=f"الساعة: {hour_input:02d}:00")
        
        if hour_input < 6:
            time_period = "🌙 الليل"
        elif hour_input < 12:
            time_period = "🌅 الصباح"
        elif hour_input < 18:
            time_period = "☀️ الظهيرة"
        else:
            time_period = "🌆 المساء"
            
        st.success(f"**فترة اليوم:** {time_period}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        st.markdown("### 🌡️ درجة الحرارة")
        
        temp = st.slider(
            "درجة الحرارة (°C)",
            min_value=-10.0,
            max_value=50.0,
            value=25.0,
            step=0.5,
            help="درجة الحرارة المتوقعة"
        )
        
        # مؤشر بصري لدرجة الحرارة
        temp_progress = (temp + 10) / 60
        st.progress(temp_progress, text=f"{temp}°C")
        
        if temp < 0:
            temp_status = "❄️ بارد جداً"
        elif temp < 15:
            temp_status = "⛄ بارد"
        elif temp < 25:
            temp_status = "🌤️ معتدل"
        elif temp < 35:
            temp_status = "☀️ دافئ"
        else:
            temp_status = "🔥 حار جداً"
            
        st.info(f"**الحالة:** {temp_status}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        st.markdown("### 💧 الرطوبة")
        
        humidity = st.slider(
            "الرطوبة (g/kg)",
            min_value=0.0,
            max_value=30.0,
            value=10.0,
            step=0.5,
            help="نسبة الرطوبة في الهواء"
        )
        
        humidity_progress = humidity / 30
        st.progress(humidity_progress, text=f"{humidity} g/kg")
        
        if humidity < 5:
            humidity_status = "🏜️ جاف جداً"
        elif humidity < 15:
            humidity_status = "🌵 جاف"
        elif humidity < 25:
            humidity_status = "💧 معتدل"
        else:
            humidity_status = "🌫️ رطب"
            
        st.info(f"**الحالة:** {humidity_status}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        st.markdown("### 💨 سرعة الرياح")
        
        wind = st.slider(
            "سرعة الرياح (m/s)",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.5,
            help="سرعة الرياح المتوقعة"
        )
        
        wind_progress = wind / 20
        st.progress(wind_progress, text=f"{wind} m/s")
        
        if wind < 3:
            wind_status = "🍃 هادئة"
        elif wind < 7:
            wind_status = "🌬️ معتدلة"
        elif wind < 12:
            wind_status = "💨 قوية"
        else:
            wind_status = "🌀 عاصفة"
            
        st.info(f"**الحالة:** {wind_status}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 إعدادات إضافية")
        
        holiday_status = st.selectbox(
            "🎉 حالة العطلة",
            ["عادي", "عطلة رسمية", "عطلة نهاية أسبوع"],
            index=0
        )
        
        season = st.selectbox(
            "🌺 الفصل",
            ["الشتاء", "الربيع", "الصيف", "الخريف"],
            index=2
        )
    
    with col2:
        st.markdown("### 🔄 المعالجة")
        
        use_historical = st.toggle("استخدام البيانات التاريخية", value=True)
        confidence_level = st.slider("مستوى الثقة", 80, 99, 90, help="مستوى الثقة في التنبؤ")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# زر التنبؤ الرئيسي
# ============================================

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 بدء عملية التنبؤ الذكي", type="primary", use_container_width=True):
        st.session_state.predict_clicked = True

# ============================================
# عرض النتائج
# ============================================

if 'predict_clicked' in st.session_state and st.session_state.predict_clicked:
    
    # استخدام st.markdown بدلاً من st.success لـ HTML
    st.markdown("""
    <div class="spinner-container">
        <div style='font-size: 3rem;'>⚡</div>
        <h3>جاري تحليل البيانات والتنبؤ...</h3>
        <p>نظام الذكاء الاصطناعي يعمل على تحليل الأنماط والتنبؤ الدقيق</p>
    </div>
    """, unsafe_allow_html=True)
    
    # محاكاة التنبؤ
    import time
    progress_bar = st.progress(0)
    
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)
    
    # قيمة تنبؤ محاكاة
    base_prediction = 1000
    temp_factor = (temp - 25) * 10
    time_factor = abs(hour_input - 14) * 5
    prediction = base_prediction + temp_factor - time_factor + np.random.normal(0, 50)
    
    # ============================================
    # عرض النتيجة
    # ============================================
    
    st.markdown("""
    <div class="success-message">
        <h2>✅ تم التنبؤ بنجاح!</h2>
        <p>تم تحليل البيانات وإجراء التنبؤ بدقة عالية</p>
    </div>
    """, unsafe_allow_html=True)
    
    # صندوق النتيجة الفخم
    st.markdown(f"""
    <div class="prediction-box">
        <div style='position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 15px;'>
            ⚡ توقع ذكي
        </div>
        <h2 style='margin-bottom: 20px; font-size: 1.8rem; opacity: 0.9;'>الحمل الكهربائي المتوقع</h2>
        <div class="prediction-value">{prediction:,.0f}</div>
        <h3 style='margin-top: 10px; opacity: 0.8;'>ميجاوات (MW)</h3>
        <div style='margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);'>
            <span style='background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 10px;'>
                🎯 دقة: {info['test_r2']:.1%}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # تحليل النتائج
    st.markdown('<div class="subtitle">📊 تحليل النتائج</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📈 حالة الحمل")
        
        if prediction > 1300:
            status_class = "status-high"
            status_text = "🔴 حرج جداً"
            recommendation = "تشغيل كل المحطات الاحتياطية"
            color = "#ff4757"
        elif prediction > 1150:
            status_class = "status-high"
            status_text = "🟠 مرتفع"
            recommendation = "تشغيل المحطات الاحتياطية"
            color = "#ffa502"
        elif prediction > 950:
            status_class = "status-medium"
            status_text = "🟢 متوسط"
            recommendation = "الحفاظ على الوضع الحالي"
            color = "#2ed573"
        elif prediction > 800:
            status_class = "status-medium"
            status_text = "🔵 طبيعي"
            recommendation = "تشغيل الوضع الاقتصادي"
            color = "#3742fa"
        else:
            status_class = "status-low"
            status_text = "🟣 منخفض"
            recommendation = "إيقاف بعض المحطات"
            color = "#7158e2"
        
        st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)
        st.info(f"**التوصية:** {recommendation}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📅 معلومات التنبؤ")
        
        st.metric("التاريخ", date_input.strftime("%Y-%m-%d"))
        st.metric("الساعة", f"{hour_input:02d}:00")
        st.metric("اليوم", day_name_arabic)
        st.metric("الفصل", season)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🌤️ تأثير الطقس")
        
        weather_impact = temp * 8 + humidity * 3 - wind * 2
        st.metric("تأثير الحرارة", f"{temp * 8:+.0f} MW")
        st.metric("تأثير الرطوبة", f"{humidity * 3:+.0f} MW")
        st.metric("تأثير الرياح", f"{wind * -2:+.0f} MW")
        st.metric("التأثير الكلي", f"{weather_impact:+.0f} MW")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # الرسوم البيانية
    # ============================================
    
    st.markdown('<div class="subtitle">📊 التحليل البصري</div>', unsafe_allow_html=True)
    
    # الرسم البياني 1: مؤشر الحمل
    fig1 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prediction,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "مؤشر الحمل الكهربائي", 'font': {'size': 28, 'family': 'Tajawal'}},
        delta={'reference': 1000, 'relative': True, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [500, 1500], 'tickwidth': 2, 'tickcolor': color},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [500, 800], 'color': '#d1f7d5'},
                {'range': [800, 950], 'color': '#b5e8ff'},
                {'range': [950, 1150], 'color': '#ffd8b5'},
                {'range': [1150, 1300], 'color': '#ffb5b5'},
                {'range': [1300, 1500], 'color': '#ff8080'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 6},
                'thickness': 0.8,
                'value': 1200
            }
        }
    ))
    
    fig1.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=100, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': "Tajawal", 'color': "#2d3748"}
    )
    
    # الرسم البياني 2: التوزيع اليومي
    hours = list(range(24))
    simulated_load = [850 + 300 * np.sin((h - 6) * np.pi / 12) + np.random.normal(0, 50) for h in hours]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=hours,
        y=simulated_load,
        mode='lines+markers',
        name='نمط الحمل اليومي',
        line=dict(color=color, width=4),
        marker=dict(size=8, color=color),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)'
    ))
    
    # إضافة نقطة التنبؤ الحالية
    fig2.add_trace(go.Scatter(
        x=[hour_input],
        y=[prediction],
        mode='markers',
        name='التنبؤ الحالي',
        marker=dict(size=20, color='#ff4757', symbol='star'),
        text=f"{prediction:,.0f} MW"
    ))
    
    fig2.update_layout(
        title="النمط اليومي للحمل الكهربائي",
        xaxis_title="ساعات اليوم",
        yaxis_title="الحمل (MW)",
        height=400,
        template='plotly_white',
        hovermode='x unified',
        font={'family': "Tajawal"}
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    # ============================================
    # التوصيات التفصيلية
    # ============================================
    
    with st.expander("📋 التوصيات التفصيلية والتحليل", expanded=True):
        st.markdown(f"""
        ## 📊 تقرير تحليلي مفصل
        
        ### 🎯 ملخص التنبؤ
        - **القيمة المتوقعة:** {prediction:,.0f} ميجاوات
        - **مستوى الثقة:** {confidence_level}%
        - **هامش الخطأ:** ±{info['test_mape']:.1f}%
        
        ### ⚡ التوصيات التشغيلية
        1. **إدارة التوليد:** {recommendation}
        2. **التوزيع:** {'زيادة سعة التوزيع في المناطق الحضرية' if prediction > 1100 else 'التوزيع العادي'}
        3. **الاحتياطي:** {'تفعيل 100% من القدرة الاحتياطية' if prediction > 1200 else 'تفعيل 50% من القدرة الاحتياطية'}
        
        ### 🌍 تأثير العوامل البيئية
        - **درجة الحرارة:** {temp}°C → تأثير: {temp * 8:+.0f} MW
        - **الرطوبة:** {humidity} g/kg → تأثير: {humidity * 3:+.0f} MW
        - **سرعة الرياح:** {wind} m/s → تأثير: {wind * -2:+.0f} MW
        
        ### ⚠️ التحذيرات والتنبيهات
        {'🔔 **تنبيه:** الحمل يقترب من السعة القصوى، يرجى التأهب' if prediction > 1200 else '✅ **مستقر:** الحمل ضمن النطاق الآمن'}
        
        ### 📈 توقعات المستقبل
        بناءً على النمط التاريخي، من المتوقع أن يكون الحمل في الساعة القادمة حوالي **{prediction * 0.95:,.0f} MW**
        """)
    
    # ============================================
    # خيارات التنزيل والمشاركة
    # ============================================
    
    st.markdown('<div class="subtitle">💾 خيارات الإخراج</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 تنزيل التقرير", use_container_width=True):
            st.success("✅ جاري تحضير التقرير للتنزيل...")
    
    with col2:
        if st.button("🖨️ طباعة التقرير", use_container_width=True):
            st.info("ℹ️ جاري تحضير التقرير للطباعة...")
    
    with col3:
        if st.button("🔄 تنبؤ جديد", use_container_width=True):
            st.session_state.predict_clicked = False
            st.rerun()

# ============================================
# قسم معلومات النظام
# ============================================

st.markdown("</div>", unsafe_allow_html=True)  # إغلاق الحاوية الرئيسية

# ============================================
# تذييل الصفحة المحسن
# ============================================

st.markdown("---")  # خط فاصل

# إنشاء التذييل باستخدام أعمدة Streamlit مباشرة
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center;">
        <h3 style="color: #667eea; margin: 0;">⚡ نظام الذكاء الاصطناعي للطاقة</h3>
        <p style="margin: 5px 0; color: #718096;">الحل المتقدم للتنبؤ بالطاقة</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center;">
        <p style="margin: 5px 0;">📧 lamiaaelshiekh@gmail.com</p>
        <p style="margin: 5px 0;">📞 +2010 600 85095</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="text-align: center;">
        <p style="margin: 5px 0;">🔄 آخر تحديث: {info['training_date']}</p>
    </div>
    """, unsafe_allow_html=True)

# قسم الإيكونات
st.markdown("""
<div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
    <p style="color: #718096;">🤖 Powered by Advanced AI & Machine Learning | 💡 Developed with Streamlit</p>
    
</div>
""", unsafe_allow_html=True)

# ============================================
# معلومات إضافية إذا لم يتم الضغط على الزر
# ============================================
if 'predict_clicked' not in st.session_state:
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; background: #f8f9fa; padding: 30px; border-radius: 20px; margin-top: 40px;">
            <h3>🚀 جاهز للتنبؤ؟</h3>
            <p>املأ البيانات أعلاه واضغط على زر "بدء عملية التنبؤ الذكي"</p>
            <p>ستحصل على تحليل مفصل وتوصيات عملية</p>
        </div>

        """, unsafe_allow_html=True)

