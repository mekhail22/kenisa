import streamlit as st
from datetime import datetime, timedelta, timezone
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import arabic_reshaper
from bidi.algorithm import get_display
import os

# 🕌 تحميل الخط العربي تلقائيًا لو مش موجود
FONT_PATH = "NotoNaskhArabic-Regular.ttf"
if not os.path.exists(FONT_PATH):
    st.warning("⏳ بيتم تحميل الخط العربي لأول مرة... استنى ثواني بس.")
    url = "https://github.com/googlefonts/noto-fonts/blob/main/hinted/ttf/NotoNaskhArabic/NotoNaskhArabic-Regular.ttf?raw=true"
    r = requests.get(url)
    with open(FONT_PATH, "wb") as f:
        f.write(r.content)
    st.success("✅ تم تحميل الخط العربي بنجاح!")

# تسجيل الخط العربي
pdfmetrics.registerFont(TTFont('Arabic', FONT_PATH))

# 🔧 إعدادات Firebase و Telegram
PATH_TO_SERVICE_ACCOUNT = "attendance-streamlit-app-c3aa8-firebase-adminsdk-fbsvc-198eef2acc.json"
TELEGRAM_BOT_TOKEN = "7517001841:AAFZZQM1hiprXxhPhK4GMfFwu-eP-DkOdMU"
TELEGRAM_CHAT_ID = "8108209758"

# 🔥 تهيئة Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(PATH_TO_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ✉️ إرسال إشعار لتليجرام
def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

# 💾 تسجيل الغياب في Firebase
def record_absence(student_name, teacher_name):
    egypt_time = datetime.now(timezone.utc) + timedelta(hours=2)
    date_str = egypt_time.strftime("%d/%m/%Y")
    doc = {
        "name": student_name.strip(),
        "class": "6/C",
        "status": "غايب",
        "teacher": teacher_name.strip(),
        "date": date_str,
    }
    db.collection("attendance").add(doc)

# 📊 إحضار جدول الغياب لطالب
def get_student_absences_table(student_name):
    query = db.collection("attendance").where("name", "==", student_name.strip()).stream()
    rows = []
    for d in query:
        data = d.to_dict()
        rows.append({
            "المرة": None,
            "الطالب": data.get("name", ""),
            "التاريخ": data.get("date", ""),
            "المدرس": data.get("teacher", "غير معروف"),
            "الحالة": data.get("status", "غايب"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="التاريخ", ascending=True).reset_index(drop=True)
        df["المرة"] = df.index + 1
    return df

# ✉️ إشعار المدرس
def notify_teacher_action(teacher_name, absent_students):
    egypt_time = datetime.now(timezone.utc) + timedelta(hours=2)
    date_str = egypt_time.strftime("%d/%m/%Y")
    msg = (
        f"📢 تقرير غياب جديد\n"
        f"👨‍🏫 المدرس: {teacher_name}\n"
        f"🏫 الفصل: 6/C\n"
        f"📅 التاريخ: {date_str}\n\n"
        f"🚫 الطلاب الغائبين:\n" + "\n".join([f"- {s}" for s in absent_students])
    )
    send_telegram_message(msg)

# 🔤 تهيئة اللغة العربية في النصوص
def reshape_arabic_text(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

# 🧾 توليد PDF بالعربي مضبوط (RTL)
def generate_pdf(student_name, df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []

    styles = getSampleStyleSheet()
    arabic_style = ParagraphStyle(name='Arabic', fontName='Arabic', fontSize=12, alignment=2)
    title_style = ParagraphStyle(name='ArabicTitle', fontName='Arabic', fontSize=16, alignment=1, spaceAfter=14)

    # العنوان الرئيسي
    elements.append(Paragraph(reshape_arabic_text("تقرير غياب الطالب"), title_style))
    elements.append(Spacer(1, 12))

    # بيانات الطالب
    elements.append(Paragraph(reshape_arabic_text(f"الاسم: {student_name}"), arabic_style))
    elements.append(Paragraph(reshape_arabic_text("الفصل: 6/C"), arabic_style))
    elements.append(Paragraph(reshape_arabic_text(f"عدد مرات الغياب: {len(df)}"), arabic_style))
    elements.append(Spacer(1, 12))

    # جدول الغياب
    data = [list(df.columns)] + df.values.tolist()
    data = [[reshape_arabic_text(str(cell)) for cell in row] for row in data]

    table = Table(data, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Arabic'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # التاريخ
    today = datetime.now(timezone.utc) + timedelta(hours=2)
    elements.append(Paragraph(reshape_arabic_text(f"تاريخ إصدار التقرير: {today.strftime('%d/%m/%Y')}"), arabic_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# 🌟 إعداد الصفحة
st.set_page_config(page_title="نظام غياب الفصل", layout="centered")

st.title("📘 نظام غياب الفصل")
page = st.radio("اختار نوع الدخول:", ["-- اختر --", "👨‍🎓 طالب", "👨‍🏫 مدرس"])

# 👨‍🎓 واجهة الطالب
if page == "👨‍🎓 طالب":
    st.header("🔍 البحث عن الغياب")
    student_name = st.text_input("اكتب اسمك الثلاثي:")
    if student_name:
        df = get_student_absences_table(student_name)
        if df.empty:
            st.info("✅ لا يوجد غياب مسجل لهذا الطالب.")
        else:
            st.dataframe(df, use_container_width=True)
            pdf_buffer = generate_pdf(student_name, df)
            st.download_button(
                label="📄 تحميل تقرير PDF",
                data=pdf_buffer,
                file_name=f"{student_name}_تقرير_الغياب.pdf",
                mime="application/pdf",
            )

# 👨‍🏫 واجهة المدرس
elif page == "👨‍🏫 مدرس":
    st.header("🧑‍🏫 تسجيل غياب الطلاب")

    teachers = ["مينا سمير", "فادي حبيب"]
    students = [
        "ميخائيل صابر فوزي",
        "مينا ريمون خيري",
        "توني هاني نصرالله",
        "يوسف شادي كمال",
        "ادم مايكل فوزي",
        "مارك نادر فؤاد",
        "بيشوي عاطف فايز",
        "جورج مينا نجيب",
        "كيرلس فادي صادق",
        "يوستينا مجدي فادي",
    ]

    teacher_name = st.selectbox("اختار اسمك:", teachers)
    st.markdown("### ✅ علم على الطلاب الغايبين:")

    absent_students = []
    cols = st.columns(2)
    for i, student in enumerate(students):
        with cols[i % 2]:
            if st.checkbox(student, key=f"student_{i}"):
                absent_students.append(student)

    st.markdown("---")
    submit = st.button("📋 تسجيل الغياب", use_container_width=True)

    if submit:
        if not absent_students:
            st.warning("من فضلك علم على الطلاب الغايبين قبل التسجيل.")
        else:
            for s in absent_students:
                record_absence(s, teacher_name)
            notify_teacher_action(teacher_name, absent_students)
            st.success(f"✅ تم تسجيل غياب {len(absent_students)} طالب وإرسال إشعار لتليجرام.")
