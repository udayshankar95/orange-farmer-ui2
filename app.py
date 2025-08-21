import streamlit as st
import requests
from datetime import date
import pandas as pd
import re

# -----------------------
# CONFIG
# -----------------------
API_URL = "https://udayshankar3008.app.n8n.cloud/webhook/farmer/account"
API_KEY = "abcdefghijk123456789"  # Keep in .env or secrets file ideally

# -----------------------
# UI HEADER
# -----------------------
st.set_page_config(page_title="Farmer Visit Assistant", page_icon="👨‍🌾", layout="centered")
st.title("👨‍🌾 Farmer Visit Assistant")
st.caption("Orange Health Labs • Pilot UI — select your name to fetch today's visits")

# -----------------------
# INPUT FORM
# -----------------------
farmer_name = st.selectbox(
    "Select your name",
    ["pragati.pandey", "ajay.kumar", "neha.sharma"]  # example names
)

today = date.today().strftime("%d/%m/%Y")
st.write(f"**Date (auto):** {today}")

if st.button("🔍 Fetch my visits"):
    with st.spinner("Fetching visit summary..."):
        try:
            response = requests.get(
                API_URL,
                headers={"x-api-key": API_KEY},
                params={"name": farmer_name, "date": today},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            # -----------------------
            # UI OUTPUT
            # -----------------------
            st.subheader("📋 Visit Summary")

            summary_text = data.get("summary", "")

            if not summary_text:
                st.info("No visit summary available for today.")
            else:
                # --- Short Summary ---
                short_match = re.search(r"Short Summary.*?:\s*(.+)", summary_text, re.DOTALL)
                short_summary = short_match.group(1).strip() if short_match else "No short summary found."

                st.subheader("⚡ Quick Summary")
                st.success(short_summary)

                # --- Monthly Orders & Revenue ---
                # st.subheader("📊 Recent 6 Months Performance")
                # month_section_match = re.search(r"Recent 6 Months.*?\n(.*?)\n\n", summary_text, re.DOTALL)
                # month_lines = []
                # if month_section_match:
                #     lines = month_section_match.group(1).split("\n")
                #     for line in lines:
                #         parts = re.split(r"\s+", line.strip())
                #         if len(parts) >= 3:
                #             month, orders, revenue = parts[0], parts[1], parts[2]
                #             month_lines.append({"Month": month, "Orders": orders, "Revenue": revenue})

                # if month_lines:
                #     df = pd.DataFrame(month_lines)
                #     st.table(df)
                # else:
                #     st.info("No monthly order/revenue breakdown found.")

                # --- Full Narrative ---
                st.subheader("📝 Detailed Insights")
                st.write(summary_text.replace("\\n", "\n"))

        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
