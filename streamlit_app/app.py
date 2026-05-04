import streamlit as st
import requests
import pandas as pd
import io

# ── Config ────────────────────────────────────────────────────────────────────

API_BASE = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="محلل المشاعر العربي",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg:      #0d0f14;
    --surface: #151820;
    --border:  #252a35;
    --accent:  #4fffb0;
    --neutral: #7b8494;
    --text:    #e8ecf4;
    --pos:     #4fffb0;
    --neg:     #ff4f7b;
}

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1000px; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero h1 { font-size: 3rem; font-weight: 900; letter-spacing: -1px; margin: 0; }
.hero h1 span { color: var(--accent); }
.hero p { color: var(--neutral); font-size: 0.9rem; margin-top: 0.5rem; font-family: 'Space Mono', monospace !important; }

.health-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-left: 6px; vertical-align: middle; }
.dot-green { background: var(--pos); box-shadow: 0 0 6px var(--pos); }
.dot-red   { background: var(--neg); box-shadow: 0 0 6px var(--neg); }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 1rem !important;
    direction: rtl;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(79,255,176,0.15) !important;
}
.stTextInput > div > div > div[data-testid="InputInstructions"],
small, .stTextInput small { display: none !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 4px;
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--neutral);
    border-radius: 6px;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
}
.stTabs [aria-selected="true"] { background: var(--accent) !important; color: #0d0f14 !important; }

.stButton > button {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    width: 100%;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stats-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.stat-box { flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; text-align: center; }
.stat-num { font-family: 'Space Mono', monospace; font-size: 1.8rem; font-weight: 700; }
.stat-label { font-size: 0.8rem; color: var(--neutral); margin-top: 2px; }
.stat-num-pos { color: var(--pos); }
.stat-num-neg { color: var(--neg); }
.stat-num-neu { color: var(--neutral); }

.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    direction: rtl;
    text-align: right;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: var(--accent); }

.badge {
    flex-shrink: 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.badge-positive { background: rgba(79,255,176,0.12); color: var(--pos); border: 1px solid var(--pos); }
.badge-negative { background: rgba(255,79,123,0.12); color: var(--neg); border: 1px solid var(--neg); }
.badge-unknown  { background: rgba(123,132,148,0.12); color: var(--neutral); border: 1px solid var(--neutral); }
.comment-text { flex: 1; font-size: 1rem; line-height: 1.6; }

.single-result {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    margin-top: 1.5rem;
}
.single-result .label { font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--neutral); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.single-result .value { font-size: 2.5rem; font-weight: 900; }
.value-positive { color: var(--pos); }
.value-negative { color: var(--neg); }
.value-unknown  { color: var(--neutral); }

.stDownloadButton > button {
    background: var(--surface) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 8px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    width: 100%;
    margin-top: 1rem;
}

.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=10)
def check_api_health():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        data = r.json()
        return r.ok and data.get("model_loaded") and data.get("vectorizer_loaded")
    except Exception:
        return False

def badge_html(sentiment: str) -> str:
    s = sentiment.lower()
    cls = f"badge-{s}" if s in ("positive", "negative") else "badge-unknown"
    label = {"positive": "إيجابي ✓", "negative": "سلبي ✗"}.get(s, "غير معروف")
    return f'<span class="badge {cls}">{label}</span>'

def render_results(results: list, total: int):
    pos = sum(1 for r in results if r["sentiment"].lower() == "positive")
    neg = sum(1 for r in results if r["sentiment"].lower() == "negative")
    unk = total - pos - neg

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box"><div class="stat-num">{total}</div><div class="stat-label">الإجمالي</div></div>
        <div class="stat-box"><div class="stat-num stat-num-pos">{pos}</div><div class="stat-label">إيجابي</div></div>
        <div class="stat-box"><div class="stat-num stat-num-neg">{neg}</div><div class="stat-label">سلبي</div></div>
        <div class="stat-box"><div class="stat-num stat-num-neu">{unk}</div><div class="stat-label">غير معروف</div></div>
    </div>
    """, unsafe_allow_html=True)

    if total > 0:
        pos_pct = pos / total * 100
        neg_pct = neg / total * 100
        st.markdown(f"""
        <div style="background:var(--border);border-radius:20px;height:8px;margin-bottom:0.5rem;overflow:hidden;display:flex;">
            <div style="width:{pos_pct:.1f}%;height:100%;background:var(--pos);"></div>
            <div style="width:{neg_pct:.1f}%;height:100%;background:var(--neg);"></div>
        </div>
        <p style="color:var(--neutral);font-size:0.8rem;text-align:center;margin-bottom:1.5rem;">
            <span style="color:var(--pos)">■</span> إيجابي {pos_pct:.0f}% &nbsp;&nbsp;
            <span style="color:var(--neg)">■</span> سلبي {neg_pct:.0f}%
        </p>
        """, unsafe_allow_html=True)

    st.markdown("#### النتائج")
    for r in results:
        st.markdown(f"""
        <div class="result-card">
            {badge_html(r['sentiment'])}
            <div class="comment-text">{r['text']}</div>
        </div>
        """, unsafe_allow_html=True)

    df = pd.DataFrame({
        "النص":    [r["text"] for r in results],
        "المشاعر": [r["sentiment"] for r in results],
    })
    st.download_button(
        label="⬇️  تحميل النتائج CSV",
        data=df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="sentiment_results.csv",
        mime="text/csv",
    )


# ── Header ────────────────────────────────────────────────────────────────────

healthy = check_api_health()
dot_cls = "dot-green" if healthy else "dot-red"
api_status = "متصل" if healthy else "غير متصل"

st.markdown(f"""
<div class="hero">
    <h1>محلل المشاعر <span>العربي</span></h1>
    <p>Arabic Sentiment Analyzer &nbsp;·&nbsp; API <span class="health-dot {dot_cls}"></span> {api_status}</p>
</div>
""", unsafe_allow_html=True)

if not healthy:
    st.error("⚠️ لا يمكن الاتصال بـ API. تأكد من تشغيل `uvicorn main:app --reload --port 8001` أولاً.")
    st.stop()


# ── Tabs ──────────────────────────────────────────────────────────────────────

tab_csv, tab_single = st.tabs(["📂  تحليل ملف CSV", "✍️  تحليل نص واحد"])


# ════════════════════════════════════════════════════════════
# TAB 1 — CSV Upload
# ════════════════════════════════════════════════════════════

with tab_csv:
    st.markdown("#### ارفع ملف CSV")
    st.markdown('<p style="color:var(--neutral);font-size:0.9rem;margin-top:-0.5rem;">يجب أن يحتوي الملف على عمود واحد على الأقل يحتوي على النصوص العربية</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "اختر ملف CSV",
        type=["csv"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        # Preview the CSV and let user pick column
        try:
            df_preview = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)  # reset after reading

            st.markdown(f'<p style="color:var(--neutral);font-size:0.85rem;">✓ تم تحميل الملف — {len(df_preview)} صف, {len(df_preview.columns)} عمود</p>', unsafe_allow_html=True)

            # Column selection
            if len(df_preview.columns) == 1:
                selected_col = df_preview.columns[0]
                st.markdown(f'<p style="color:var(--neutral);font-size:0.85rem;">العمود المستخدم: <b style="color:var(--accent)">{selected_col}</b></p>', unsafe_allow_html=True)
            else:
                selected_col = st.selectbox(
                    "اختر العمود الذي يحتوي على النصوص",
                    options=df_preview.columns.tolist(),
                    label_visibility="visible",
                )

            # Preview first 3 rows
            st.markdown(f'<p style="color:var(--neutral);font-size:0.85rem;margin-top:0.5rem;">معاينة أول 3 صفوف:</p>', unsafe_allow_html=True)
            st.dataframe(
                df_preview[[selected_col]].head(3),
                use_container_width=True,
                hide_index=True,
            )

            run_csv = st.button("🔍  تحليل الملف", key="btn_csv")

            if run_csv:
                with st.spinner(f"جاري تحليل {len(df_preview)} نص..."):
                    try:
                        uploaded_file.seek(0)
                        resp = requests.post(
                            f"{API_BASE}/predict/csv",
                            files={"file": (uploaded_file.name, uploaded_file, "text/csv")},
                            params={"column": selected_col},
                            timeout=120,
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            render_results(data["results"], data["total"])
                        else:
                            st.error(f"خطأ من API: {resp.status_code} — {resp.json().get('detail', resp.text)}")
                    except requests.exceptions.Timeout:
                        st.error("انتهت مهلة الطلب. جرب ملفاً أصغر.")
                    except requests.exceptions.ConnectionError:
                        st.error("تعذّر الاتصال بـ API.")
                    except Exception as e:
                        st.error(f"خطأ غير متوقع: {e}")

        except Exception as e:
            st.error(f"تعذّر قراءة الملف: {e}")


# ════════════════════════════════════════════════════════════
# TAB 2 — Single Text
# ════════════════════════════════════════════════════════════

with tab_single:
    st.markdown("#### أدخل النص العربي")
    st.markdown('<p style="color:var(--neutral);font-size:0.9rem;margin-top:-0.5rem;">اكتب أو الصق تعليقاً عربياً لتحليل مشاعره</p>', unsafe_allow_html=True)

    user_text = st.text_area(
        "النص",
        placeholder="اكتب أو الصق النص العربي هنا...",
        height=150,
        label_visibility="collapsed",
    )

    run_single = st.button("🔍  تحليل النص", key="btn_single")

    if run_single:
        if not user_text.strip():
            st.warning("الرجاء إدخال نص للتحليل.")
        else:
            with st.spinner("جاري التحليل..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/predict",
                        json={"text": user_text.strip()},
                        timeout=15,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        sentiment = data["sentiment"]
                        emoji = {"positive": "😊", "negative": "😞"}.get(sentiment.lower(), "❓")
                        val_cls = f"value-{sentiment.lower()}" if sentiment.lower() in ("positive", "negative") else "value-unknown"
                        label_ar = {"positive": "إيجابي", "negative": "سلبي"}.get(sentiment.lower(), "غير معروف")

                        st.markdown(f"""
                        <div class="single-result">
                            <div class="label">نتيجة التحليل</div>
                            <div class="value {val_cls}">{emoji} {label_ar}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    elif resp.status_code == 400:
                        st.warning("النص فارغ أو غير صالح.")
                    else:
                        st.error(f"خطأ من API: {resp.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("تعذّر الاتصال بـ API.")
                except Exception as e:
                    st.error(f"خطأ: {e}")