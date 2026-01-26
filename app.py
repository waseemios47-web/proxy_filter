import streamlit as st
import requests

# -----------------------------
# USPTO Trademark Search
# -----------------------------
def search_trademark(keyword):
    url = "https://developer.uspto.gov/ibd-api/v1/trademark/application/publications"

    params = {
        "searchText": keyword,
        "rows": 20
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def analyze_results(data, keyword):
    results = data.get("results", [])
    matches = []

    for item in results:
        mark = item.get("markIdentification", "")
        status = item.get("statusCode", "UNKNOWN")
        owner = item.get("partyName", "Unknown")
        classes = item.get("internationalClasses", [])

        if keyword.lower() in mark.lower():
            matches.append({
                "mark": mark,
                "status": status,
                "owner": owner,
                "classes": classes
            })

    return matches


def risk_level(matches):
    for m in matches:
        if m["status"] == "LIVE":
            # Class 9 = Games/Software | Class 41 = Entertainment/Games
            if any(cls in [9, 41] for cls in m["classes"]):
                return "❌ HIGH RISK — Live trademark exists in Games category"

    if matches:
        return "⚠ MEDIUM RISK — Similar or inactive trademarks found"

    return "✅ LOW RISK — No relevant trademarks found"


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
    "Check whether a **game name or keyword** is trademarked in the **United States (USPTO)**.\n\n"
    "**Note:** Single words and names cannot be copyrighted — this tool checks **trademarks only**."
)

keyword = st.text_input(
    "Enter game name / keyword",
    placeholder="e.g. Cookingdom"
)

if st.button("Check Trademark"):
    if not keyword.strip():
        st.warning("Please enter a keyword")
    else:
        with st.spinner("Searching USPTO trademark database..."):
            try:
                data = search_trademark(keyword.strip())
                matches = analyze_results(data, keyword.strip())
                verdict = risk_level(matches)

                st.subheader("Result")
                st.success(verdict) if "LOW" in verdict else st.warning(verdict) if "MEDIUM" in verdict else st.error(verdict)

                if matches:
                    st.subheader("Trademark Matches")
                    for m in matches:
                        st.markdown(
                            f"""
                            **Mark Name:** {m['mark']}  
                            **Status:** {m['status']}  
                            **Owner:** {m['owner']}  
                            **Classes:** {', '.join(map(str, m['classes'])) if m['classes'] else 'N/A'}
                            ---
                            """
                        )
                else:
                    st.info("No trademark records found for this keyword.")

            except Exception as e:
                st.error("Something went wrong while checking trademarks.")
                st.code(str(e))


st.markdown("---")
st.caption(
    "⚠ This tool provides **preliminary trademark screening only**. "
    "For legal certainty, consult a trademark attorney."
)
