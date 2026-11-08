import streamlit as st  # type: ignore[import-not-found]

from scanner import get_website_info
from reputation import check_virustotal

st.set_page_config(
    page_title="WebGuard",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ WebGuard")
st.subheader("OSINT Website Safety Checker")

st.write(
    "Check publicly available website information "
    "and basic security indicators."
)

url = st.text_input(
    "Enter website URL",
    placeholder="https://example.com"
)

if st.button("Analyze Website", type="primary"):

    if not url:
        st.warning("Please enter a website URL.")

    else:
        with st.spinner("Analyzing website..."):

            info = get_website_info(url)

            if "error" in info:
                st.error(info["error"])

            else:
                st.success("Basic analysis completed")

                st.subheader("Website Information")

                st.write("Domain:", info["domain"])
                st.write("IP Addresses:", info["ip_addresses"])
                st.write("Website Status:", info["status"])
                st.write(
                    "HTTPS:",
                    "Enabled" if info["https"] else "Not verified"
                )

                st.divider()

                st.subheader("VirusTotal Reputation")

                reputation = check_virustotal(url)

                if "error" in reputation:
                    st.warning(reputation["error"])
                else:
                    st.json(reputation)

st.divider()

st.caption(
    "WebGuard is an educational OSINT tool. "
    "No warning does not guarantee that a website is safe."
)
