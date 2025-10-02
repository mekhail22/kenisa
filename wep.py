import streamlit as st
import requests
import base64

# ====== Telegram Bot ======
BOT_TOKEN = "7517001841:AAFZZQM1hiprXxhPhK4GMfFwu-eP-DkOdMU"
CHAT_ID = "8108209758"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# ====== إعداد الخلفية ======
def img_to_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img = img_to_base64("mgma8.png")  # غيّر اسم الصورة حسب اللي عندك

st.set_page_config(page_title="كنيسة الشهيدة دميانة", layout="wide")

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/png;base64,{bg_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ====== Session ======
query_params = st.query_params
if "page" not in query_params:
    query_params["page"] = "1"

# تأمين القيمة علشان لو مش رقم
page_str = query_params["page"]
if not page_str.isdigit():
    page_str = "1"

page = int(page_str)

# ====== الصفحة الرئيسية ======
if page == 1:
    st.markdown("<h1 style='text-align: center;'>كنيسة الشهيدة دميانة</h1>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='text-align: center; position:relative; top:240px;'>
            <a href="?page=2" target="_self">
                <button style='font-size:25px; padding:10px 40px; background-color:#4CAF50; color:black; border:none; border-radius:8px; cursor:pointer;'>
                    التالي
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# ====== صفحة القائمة ======
elif page == 2:
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("📌 الغياب"):
            st.write("✅ ميخائيل")
            st.write("✅ ميكي")
            st.write("✅ قريني")

    with col2:
        with st.expander("🎶 الترانيم"):
            st.write("🎵 ترنيمة 1")
            st.write("🎵 ترنيمة 2")
            st.write("🎵 ترنيمة 3")

    with col3:
        with st.expander("📋 الافتقاد"):
            st.markdown(
                f"""
                <div style='text-align: center; position:relative; top:-10px; margin-left:-330px;'>
                    <a href="?page=3" target="_self">
                        <button style='font-size:20px; padding:10px 25px; background-color:none; color:black; border:none; border-radius:8px; cursor:pointer;'>
                            ميخائيل
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

# ====== صفحة الشخص ======
elif page == 3:
    person = "ميخائيل"

    st.markdown("<h1 style='text-align: center;'>افتقاد - ميخائيل</h1>", unsafe_allow_html=True)

    # checkboxes في النص
    col1, col2, col3 = st.columns(3)
    with col2:
        nermine = st.checkbox("نرمين")
        irene = st.checkbox("إيريني")

        if st.button("Submit"):
            if nermine and irene:
                msg = f"{person}\nتم اختيار في الافتقاد: نرمين و إيريني"
            elif nermine and not irene:
                msg = f"{person}\nتم اختيار في الافتقاد: نرمين فقط"
            elif irene and not nermine:
                msg = f"{person}\nتم اختيار في الافتقاد: إيريني فقط"
            else:
                msg = f"{person}\nلم يتم اختيار أي شخص في الافتقاد"

            send_to_telegram(msg)
            st.success("✅ تم إرسال الرسالة على التلجرام")
