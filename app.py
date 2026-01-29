import streamlit as st

st.set_page_config(page_title="Proxy Filter Tool", layout="centered")

st.title("🔌 Proxy Filter & Export Tool")
st.write("Upload a TXT file containing mixed proxies. The app will auto-split them into HTTP, SOCKS4, and SOCKS5 files.")

uploaded_file = st.file_uploader("Upload proxy TXT file", type=["txt"])

def clean_proxy(line):
    return (
        line.replace("http://", "")
            .replace("https://", "")
            .replace("socks4://", "")
            .replace("socks5://", "")
            .strip()
    )

if uploaded_file:
    raw_lines = uploaded_file.read().decode("utf-8", errors="ignore").splitlines()

    http_proxies = []
    socks4_proxies = []
    socks5_proxies = []

    for line in raw_lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("http://") or line.startswith("https://"):
            http_proxies.append(clean_proxy(line))
        elif line.startswith("socks4://"):
            socks4_proxies.append(clean_proxy(line))
        elif line.startswith("socks5://"):
            socks5_proxies.append(clean_proxy(line))

    st.success("✅ Proxies processed successfully")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("HTTP", len(http_proxies))
        if http_proxies:
            st.download_button(
                "⬇ Download HTTP",
                "\n".join(http_proxies),
                file_name="http.txt",
                mime="text/plain"
            )

    with col2:
        st.metric("SOCKS4", len(socks4_proxies))
        if socks4_proxies:
            st.download_button(
                "⬇ Download SOCKS4",
                "\n".join(socks4_proxies),
                file_name="socks4.txt",
                mime="text/plain"
            )

    with col3:
        st.metric("SOCKS5", len(socks5_proxies))
        if socks5_proxies:
            st.download_button(
                "⬇ Download SOCKS5",
                "\n".join(socks5_proxies),
                file_name="socks5.txt",
                mime="text/plain"
            )
