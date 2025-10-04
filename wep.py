import streamlit as st
import requests

# ====== Telegram Bot ======
BOT_TOKEN = "توكن البوت هنا"
CHAT_ID = "شات آي دي هنا"

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
        background-color: #FFF8F0;
    }
    [data-testid="stHeader"], [data-testid="stSidebar"] {
        background: rgba(0,0,0,0);
    }
    h1 {
        color: #2E4053;
    }
    .green-btn {
        font-size:20px;
        padding:10px 25px;
        background-color:#28A745;
        color:white;
        border:none;
        border-radius:10px;
        cursor:pointer;
    }
    .green-btn:hover {
        background-color:#218838;
        color:#fff;
    }
    .gray-btn {
        font-size:20px;
        padding:10px 25px;
        background-color:#D3D3D3;
        color:black;
        border:none;
        border-radius:10px;
        cursor:pointer;
    }
    .gray-btn:hover {
        background-color:#BEBEBE;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ====== Session ======
query_params = st.query_params
if "page" not in query_params:
    query_params["page"] = "1"

page_str = query_params["page"]
if not page_str.isdigit():
    page_str = "1"
page = int(page_str)

# ====== الصفحة الرئيسية ======
if page == 1:
    st.markdown("<h1 style='text-align: center;'>كنيسة الشهيدة دميانة</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style='text-align: center; margin-top:200px;'>
            <a href="?page=2" target="_self">
                <button class='green-btn'>التالي</button>
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
    with col3:
        with st.expander("📋 الافتقاد"):
            st.markdown(
            """
            <div style='text-align: left; margin-top:0px;'>
                <a href="?page=3" target="_self">
                    <button class='gray-btn'>ميخائيل</button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col1:
        st.markdown(
        """
        <div style='text-align: left; margin-top:300px;'>
            <a href="?page=1" target="_self">
                <button style='font-size:20px; padding:10px 25px; background-color:#FF0000; color:white; border:none; border-radius:8px; cursor:pointer;'>
                    رجوع
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# ====== صفحة الشخص ======
elif page == 3:
    person = "ميخائيل"
    st.markdown(f"<h1 style='text-align: center;'>افتقاد - {person}</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col2:
        nermine = st.checkbox("نرمين")
        irene = st.checkbox("إيريني")
        notes = st.text_area("📝 ملاحظات إضافية", "")

        if st.button("Submit"):
            if nermine and irene:
                msg = f"{person}\nتم اختيار في الافتقاد: نرمين و إيريني"
            elif nermine:
                msg = f"{person}\nتم اختيار في الافتقاد: نرمين فقط"
            elif irene:
                msg = f"{person}\nتم اختيار في الافتقاد: إيريني فقط"
            else:
                msg = f"{person}\nلم يتم اختيار أي شخص في الافتقاد"

            if notes.strip():
                msg += f"\n📝 ملاحظات: {notes}"

            send_to_telegram(msg)
            st.success("✅ تم إرسال الرسالة على التلجرام")
