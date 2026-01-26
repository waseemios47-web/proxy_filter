import streamlit as st
import requests

# -----------------------------
# USPTO Trademark Search (Working Endpoint)
# -----------------------------
def search_trademark(keyword):
    url = "https://tsdrapi.uspto.gov/ts/cd/casestatus/sn"

    # USPTO does NOT allow text search directly here,
    # so we use a broader name search endpoint instead
    search_url = "https://tmsearch.uspto.gov/bin/showfield"

    params = {
        "f": "toc",
        "p_search": "search",
        "p_L": 50,
        "p_s_PARA1": keyword,
        "p_s_PARA2": "ALL"
    }

    response = requests.get(search_url, params=params, timeout=15)
    response.raise_for_status()
    return response.text.lower()


def analyze_results(html_text, keyword):
    keyword = keyword.lower()

    if keyword in html_text:
        return True
    return False


def risk_level(found):
    if found:
        return "❌ HIGH RISK — Trademark with this name likely exists in the US"
    return "✅ LOW RISK — No obvious trademark found"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Game Name Trademark Checker",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 Game Name Trademark Checker (US)")
st.write(
    "Check whether a **game name or keyword** is already trademarked in the **United States (USPTO)**.\n\n"
    "**Note:** This is a preliminary screening tool, not legal advice."
)

keyword = st.text_input(
    "Enter game name / keyword",
    placeholder="e.g. The Secret Garden"
)

if st.button("Check Trademark"):
    if not keyword.strip():
        st.warning("Please enter a keyword")
    else:
        with st.spinner("Searching USPTO trademark database..."):
            try:
                html = search_trademark(keyword.strip())
                found = analyze_results(html, keyword.strip())
                verdict = risk_level(found)

                st.subheader("Result")
                if "LOW" in verdict:
                    st.success(verdict)
                else:
                    st.error(verdict)

                if found:
                    st.info(
                        "A similar trademark name appears in USPTO search results. "
                        "Manual verification is recommended."
                    )
                else:
                    st.info("No matching trademark name detected.")

            except Exception as e:
                st.error("USPTO search failed.")
                st.code(str(e))

st.markdown("---")
st.caption(
    "⚠ This tool provides **preliminary trademark screening only**. "
    "Always verify manually or consult a trademark attorney."
)
