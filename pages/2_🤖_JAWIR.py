from openai import OpenAI
import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv

# ----------------- Load environment -----------------
load_dotenv()

# Initialize OpenAI client once
if "client" not in st.session_state:
    st.session_state["client"] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------- System Prompt -----------------

system_prompt = """
You are JAWIR (Jawa Timur AI for Wellness & Intelligent Responses), 
a healthcare-focused chatbot specialized in Jawa Timur. 

Your goals:
1. Provide clear, trustworthy, and empathetic responses about healthcare.
2. Use Jawa Timur Open Data (rumah sakit, penyakit, fasilitas kesehatan, gizi, vaksinasi, dll.) 
   whenever relevant to ground your answers.
3. If users ask something outside health or Jawa Timur, politely redirect them back to healthcare context.
4. Always answer in Bahasa Indonesia that is easy to understand for the public.
5. Avoid giving medical prescriptions. Instead, provide general health info, data, 
   and advise consulting a professional doctor.
"""


# Store conversation messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
    ]

# ----------------- Page Config -----------------
# Loading Image using PIL
web_icon = Image.open('icon\Only LOGO.png') # Adding Image to web app
st.set_page_config(page_title="JAWIR", layout="wide", initial_sidebar_state="auto", page_icon = web_icon)

# ----------------- Custom Header -----------------
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 56px;
            color: #27AE60;
            margin-bottom: 10px;
            font-weight: bold;
        }

        /* efek hover: tambah tulisan " ChatBot" */
        .main-title:hover::after {
            content: " ChatBot";
            color: #2C3E50;      /* warna teks tambahan */
            font-weight: normal; /* biar kontras sama JAWIR */
        }

        .sub-title {
            text-align: center;
            font-size: 20px;
            color: gray;
            margin-bottom: 40px;
        }
        
        .footer {
            text-align: center;
            color: gray;
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
    <h1 class="main-title">🏥 JAWIR</h1>
    <p class="sub-title">Jawa Timur AI for Wellness & Intelligent Responses</p>
    """,
    unsafe_allow_html=True,
)

# ----------------- Sidebar -----------------
st.sidebar.header("⚙ Model Parameters")
temperature = st.sidebar.slider(
    "Creativity (temperature)",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
    help="Higher values = more creative, lower values = more focused/deterministic."
)
max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value=64,
    max_value=4096,
    value=512,
    step=64,
    help="Controls the maximum length of the response."
)

# Clear chat button
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()

# About JAWIR (pakai expander di sidebar)
with st.sidebar.expander("ℹ️ About JAWIR", expanded=False):
    st.markdown(
        """
        *JAWIR* is a healthcare-focused chatbot powered by AI and 
        connected to *Jawa Timur Open Data*.
        
        ✅ Provides health insights  
        ✅ Uses local healthcare data  
        ✅ Easy-to-use for the public
        """
    )

# ----------------- Chat History -----------------
for msg in st.session_state["messages"]:
    if msg["role"] == "system":
        continue  # jangan tampilkan system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------- User Input -----------------
if prompt := st.chat_input("Ask JAWIR about Jawa Timur healthcare..."):
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Model response
    with st.chat_message("assistant"):
        client = st.session_state["client"]

        # Example of integrating Jawa Timur Open Data in the future
        # Here you could query API endpoints and add context
        # Example (pseudo):
        # jatim_data = get_jatim_health_data(prompt)

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state["messages"].append({"role": "assistant", "content": response})

# ----------------- Footer -----------------
st.markdown(
    """
    <hr>
    <div class="footer">
        Built with ❤ using <b>Streamlit</b> + <b>OpenAI</b> | Powered by Jawa Timur Open Data
    </div>
    """,
    unsafe_allow_html=True,
)