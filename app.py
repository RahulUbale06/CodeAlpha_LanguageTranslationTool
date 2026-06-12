import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import datetime

# --- Configuration & State ---
st.set_page_config(page_title="Linguify Pro", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

LANGUAGES = {
    "English": "en", "Hindi": "hi", "German": "de", "French": "fr", 
    "Spanish": "es", "Italian": "it", "Japanese": "ja", "Chinese": "zh-CN", 
    "Russian": "ru", "Arabic": "ar", "Portuguese": "pt", "Korean": "ko"
}
LANG_LIST = list(LANGUAGES.keys())

# Initialize Session States for dynamic UI updates
if 'history' not in st.session_state:
    st.session_state.history = []
if 'src_text' not in st.session_state:
    st.session_state.src_text = ""
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'src_lang' not in st.session_state:
    st.session_state.src_lang = LANG_LIST.index("English")
if 'tgt_lang' not in st.session_state:
    st.session_state.tgt_lang = LANG_LIST.index("Spanish")

def inject_custom_css():
    """Injects advanced CSS for animations, glassmorphism, and the signature footer."""
    st.markdown("""
        <style>
        /* Animated Gradient Header */
        .hero-container {
            background: linear-gradient(-45deg, #6e8efb, #a777e3, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient-bg 10s ease infinite;
            border-radius: 20px;
            padding: 30px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        @keyframes gradient-bg {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Fade-in animation for main elements */
        .stTextArea, .stSelectbox {
            animation: fadeIn 0.8s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Glassmorphism Inputs */
        .stTextArea textarea {
            border-radius: 12px !important;
            border: 2px solid #f0f2f6 !important;
            transition: all 0.3s ease !important;
            font-size: 1.1rem !important;
            padding: 15px !important;
        }
        .stTextArea textarea:focus {
            border-color: #a777e3 !important;
            box-shadow: 0 0 15px rgba(167, 119, 227, 0.3) !important;
        }

        /* Primary Button Glow & Scale */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #6e8efb, #a777e3) !important;
            border: none !important;
            color: white !important;
            border-radius: 10px !important;
            font-size: 1.2rem !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            padding: 0.75rem !important;
        }
        .stButton>button[kind="primary"]:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 8px 20px rgba(167, 119, 227, 0.4) !important;
        }

        /* Premium Credits Footer Styling */
        .pro-footer {
            text-align: center;
            padding: 25px 10px;
            margin-top: 60px;
            border-top: 1px solid #e0e0e0;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .footer-text {
            font-size: 1rem;
            color: #666666;
            letter-spacing: 1px;
        }
        .designer-glow {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            animation: text-pulse 2s infinite alternate;
        }
        @keyframes text-pulse {
            from { filter: drop-shadow(0 0 2px rgba(110,142,251,0.2)); }
            to { filter: drop-shadow(0 0 8px rgba(167,119,227,0.6)); }
        }
        </style>
    """, unsafe_allow_html=True)

def swap_languages():
    """Swaps the source and target languages/text."""
    st.session_state.src_lang, st.session_state.tgt_lang = st.session_state.tgt_lang, st.session_state.src_lang
    st.session_state.src_text, st.session_state.translated_text = st.session_state.translated_text, st.session_state.src_text

def generate_audio(text: str, lang_code: str) -> BytesIO:
    """Generates TTS audio entirely in-memory."""
    tts = gTTS(text=text, lang=lang_code.split("-")[0])
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp
def get_learning_tip(source_lang, target_lang, original, translated):
    tips = {
        ("English", "German"): {
            "pronunciation": translated,
            "fact": "German nouns are always capitalized. For example, House becomes Haus and School becomes Schule."
        },
        ("English", "French"): {
            "pronunciation": translated,
            "fact": "French pronunciation often differs greatly from spelling."
        },
        ("English", "Spanish"): {
            "pronunciation": translated,
            "fact": "Spanish is spoken in over 20 countries."
        },
        ("English", "Hindi"): {
            "pronunciation": translated,
            "fact": "Hindi uses the Devanagari script."
        }
    }

    return tips.get(
        (source_lang, target_lang),
        {
            "pronunciation": translated,
            "fact": f"{target_lang} is a fascinating language to learn."
        }
    )
def main():
    inject_custom_css()

    # --- Sidebar History ---
    with st.sidebar:
        st.markdown("### 🕒 Translation History")
        if not st.session_state.history:
            st.info("Your translations will appear here.")
        else:
            for item in reversed(st.session_state.history[-5:]): # Show last 5
                st.markdown(f"**{item['src']} ➔ {item['tgt']}**")
                st.caption(f"*From:* {item['original']}")
                st.success(f"*To:* {item['translated']}")
                st.divider()

    # --- Animated Header ---
    st.markdown("""
        <div class="hero-container">
            <h1 style="margin:0; font-size: 3rem; font-weight: 800;">✨ Linguify Pro</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">Next-Generation Language Translation</p>
        </div>
    """, unsafe_allow_html=True)

    # --- Main Interface ---
    col1, col_swap, col2 = st.columns([10, 2, 10], gap="small")

    with col1:
        st.selectbox("Translate From", LANG_LIST, index=st.session_state.src_lang, key="src_lang_select")
        source_text = st.text_area("Source", height=200, placeholder="Type something beautifully...", key="src_text", label_visibility="collapsed")
        st.caption(f"Characters: {len(source_text)}")

    with col_swap:
        st.markdown("<br><br>", unsafe_allow_html=True) # Vertical spacing
        st.button("⇆", on_click=swap_languages, help="Swap Languages", use_container_width=True)

    with col2:
        st.selectbox("Translate To", LANG_LIST, index=st.session_state.tgt_lang, key="tgt_lang_select")
        st.text_area("Target", height=200, value=st.session_state.translated_text, label_visibility="collapsed", disabled=True)

    # --- Action Buttons ---
    st.write("")
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])

    with btn_col2:
        if st.button("🚀 Translate Text", type="primary", use_container_width=True):
            if not source_text.strip():
                st.toast("Please enter some text first!", icon="⚠️")
            elif st.session_state.src_lang_select == st.session_state.tgt_lang_select:
                st.toast("Source and Target languages must be different.", icon="🛑")
            else:
                with st.spinner("Decoding language matrix..."):
                    try:
                        # Translate
                        translator = GoogleTranslator(
                            source=LANGUAGES[st.session_state.src_lang_select],
                            target=LANGUAGES[st.session_state.tgt_lang_select]
                        )
                        result = translator.translate(source_text)
                        
                        # Update State
                        st.session_state.translated_text = result
                        st.session_state.src_lang = LANG_LIST.index(st.session_state.src_lang_select)
                        st.session_state.tgt_lang = LANG_LIST.index(st.session_state.tgt_lang_select)
                        
                        # Save to History
                        st.session_state.history.append({
                            "src": st.session_state.src_lang_select,
                            "tgt": st.session_state.tgt_lang_select,
                            "original": source_text[:30] + ("..." if len(source_text) > 30 else ""),
                            "translated": result[:30] + ("..." if len(result) > 30 else "")
                        })

                        st.toast("Translation Successful!", icon="✅")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- Post-Translation Tools (Audio & Download) ---
    if st.session_state.translated_text:
        learning = get_learning_tip(
        st.session_state.src_lang_select,
        st.session_state.tgt_lang_select,
        st.session_state.src_text,
        st.session_state.translated_text
    )
        
    st.markdown("### 🧠 Learn From This Translation")

    with st.expander("Show Learning Insights"):

        st.write(
            f"**Translation:** {st.session_state.translated_text}"
        )

        st.write(
            f"**Pronunciation Hint:** {learning['pronunciation']}"
        )

        st.info(
            learning["fact"]
        )
        st.divider()
        st.markdown("### 🛠️ Actions")
        action1, action2, action3 = st.columns([1, 1, 2])
        
        with action1:
            st.download_button(
                "📥 Download TXT", 
                data=st.session_state.translated_text, 
                file_name=f"linguify_{datetime.datetime.now().strftime('%H%M%S')}.txt",
                use_container_width=True
            )
            
        with action2:
            if st.button("🔊 Play Audio", use_container_width=True):
                with st.spinner("Synthesizing audio..."):
                    audio_fp = generate_audio(st.session_state.translated_text, LANGUAGES[st.session_state.tgt_lang_select])
                    st.audio(audio_fp, format="audio/mp3")

    # --- Premium Signature Footer ---
    st.markdown(f"""
        <div class="pro-footer">
            <p class="footer-text">
                Designed & Engineered with ⚡ by 
                <span class="designer-glow">Rahul</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()