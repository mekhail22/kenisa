
import streamlit as st
import requests

# ====== Telegram Bot ======
BOT_TOKEN = "7517001841:AAFZZQM1hiprXxhPhK4GMfFwu-eP-DkOdMU"
CHAT_ID = "8108209758"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# ====== إعداد الصفحة ======
st.set_page_config(page_title="كنيسة الشهيدة دميانة", page_icon="✝️", layout="wide")

# ====== CSS للألوان والخلفية ======
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFF8F0; /* خلفية هادية */
    }
    [data-testid="stHeader"], [data-testid="stSidebar"] {
        background: rgba(0,0,0,0);
    }
    h1 {
        color: #2E4053; /* لون العنوان */
    }
    .stButton button {
        background-color: #32CD32; 
        color: white;
        font-size: 20px;
        border-radius: 10px;
        padding: 10px 25px;
        border: none;
        
    }
    
    .stCheckbox label {
        color: #1A5276; /* لون نص الشيكبوكس */
        font-size: 18px;
    }
    .stTextArea textarea {
        background-color: #FDEBD0; /* لون صندوق الملاحظات */
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ====== Session ======
query_params = st.query_params
if "page" not in query_params:
    query_params["page"] = "1"

# تأمين القيمة
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
                <button style='font-size:25px; padding:10px 40px; background-color:#32CD32; color:white; border:none; border-radius:12px; cursor:pointer;'>
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


    st.markdown(
                f"""
                <div style='text-align: left; position:relative; top:10px; margin-left:0;'>
                    <a href="?page=1" target="_self">
                        <button style='font-size:20px; padding:10px 25px; background-color:#FF0000; color:black; border:none; border-radius:8px; cursor:pointer;'>
                            رجوع
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col1:
        with st.expander("📌 الغياب"):
            st.write("✅ ميخائيل")
            st.write("✅ ميكي")
            st.write("✅ قريني")

    with col3:
        with st.expander("📋 الافتقاد"):
            st.markdown(
                f"""
                <div style='text-align: center; position:relative; top:-10px; margin-left:-250px;'>
                    <a href="?page=3" target="_self">
                        <button style='font-size:20px; padding:10px 25px; background-color:#D3D3D3; color:black; border:none; border-radius:8px; cursor:pointer;'>
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

    col1, col2, col3 = st.columns(3)
    with col2:
        nermine = st.checkbox("نرمين")
        irene = st.checkbox("إيريني")
        notes = st.text_area("📝 ملاحظات إضافية", "")

        # الأزرار جنب بعض
        col_btn1, col_btn2 = st.columns([1,1])
        with col_btn1:
            if st.button("Submit", type="primary"):
                if nermine and irene:
                    msg = f"{person}\nتم اختيار في الافتقاد: نرمين و إيريني"
                elif nermine and not irene:
                    msg = f"{person}\nتم اختيار في الافتقاد: نرمين فقط"
                elif irene and not nermine:
                    msg = f"{person}\nتم اختيار في الافتقاد: إيريني فقط"
                else:
                    msg = f"{person}\nلم يتم اختيار أي شخص في الافتقاد"

                if notes.strip():
                    msg += f"\n📝 ملاحظات: {notes}"

                send_to_telegram(msg)
                st.success("✅ تم إرسال الرسالة على التلجرام")

        with col_btn2:
            st.markdown(
                """
                <a href="?page=2" target="_self">
                    <button style='font-size: 20px;padding: 10px 25px; background-color:#FF0000; color:white; border:none; border-radius: 10px; cursor:pointer;'>
                        رجوع
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
