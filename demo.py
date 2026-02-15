import sys
if 'streamlit' not in sys.modules:
  !pip install streamlit
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. DATA INITIALIZATION (Representative 2026 Gazette Data) ---
def load_data():
    # Primary Seat-wise Results (Partial list of 300)
    data = [
        {"Seat": "Panchagarh-1", "Winner": "Mohammad Nawshad Zamir", "Party": "BNP", "Votes": 176169, "Division": "Rangpur"},
        {"Seat": "Thakurgaon-1", "Winner": "Mirza Fakhrul Islam Alamgir", "Party": "BNP", "Votes": 238836, "Division": "Rangpur"},
        {"Seat": "Bogra-6", "Winner": "Tarique Rahman", "Party": "BNP", "Votes": 216284, "Division": "Rajshahi"},
        {"Seat": "Dhaka-8", "Winner": "Mirza Abbas", "Party": "BNP", "Votes": 59366, "Division": "Dhaka"},
        {"Seat": "Dhaka-11", "Winner": "Nahid Islam", "Party": "NCP", "Votes": 42100, "Division": "Dhaka"},
        {"Seat": "Nilphamari-1", "Winner": "Md. Abdus Sattar", "Party": "BJI", "Votes": 150824, "Division": "Rangpur"},
        {"Seat": "Rangpur-3", "Winner": "Md. Mahbubar Rahman", "Party": "BJI", "Votes": 157403, "Division": "Rangpur"},
        {"Seat": "Dhaka-7", "Winner": "Hamidur Rahman", "Party": "BNP", "Votes": 104666, "Division": "Dhaka"},
        {"Seat": "Dinajpur-5", "Winner": "AZM Rezwanul Haque", "Party": "IND", "Votes": 114484, "Division": "Rangpur"},
    ]
    return pd.DataFrame(data)

df = load_data()

# Summary Data for Charts
summary_data = {
    'Party': ['BNP', 'BJI', 'NCP', 'IND', 'Others'],
    'Seats': [209, 68, 6, 7, 7],
    'Colors': ['#204080', '#008000', '#FF4B4B', '#FFFF00', '#A9A9A9']
}
df_sum = pd.DataFrame(summary_data)

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("Election 2026 Navigator")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/f/f9/Flag_of_Bangladesh.svg", width=100)
mode = st.sidebar.radio("Go to:", ["National Summary", "Seat-Wise Lookup", "Regional Analysis"])

# --- 3. PAGE: NATIONAL SUMMARY ---
if mode == "National Summary":
    st.title("🗳️ Bangladesh General Election 2026: Results")

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Winner", "BNP", "Landslide")
    c2.metric("Total Seats (BNP)", "209", "+202 from 2018")
    c3.metric("BJI (Jamaat)", "68", "Record High")
    c4.metric("Voter Turnout", "59.44%", "Official")

    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Parliament Composition")
        fig = px.pie(df_sum, values='Seats', names='Party', color='Party',
                     color_discrete_map=dict(zip(df_sum.Party, df_sum.Colors)), hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Major Party Performance")
        fig2 = px.bar(df_sum, x='Party', y='Seats', color='Party',
                      color_discrete_map=dict(zip(df_sum.Party, df_sum.Colors)))
        st.plotly_chart(fig2, use_container_width=True)

# --- 4. PAGE: SEAT-WISE LOOKUP ---
elif mode == "Seat-Wise Lookup":
    st.title("🔍 Constituency Navigator")
    search = st.text_input("Enter Constituency Name (e.g., Bogra, Dhaka, Thakurgaon)")

    if search:
        results = df[df['Seat'].str.contains(search, case=False)]
        if not results.empty:
            for _, row in results.iterrows():
                with st.expander(f"📍 {row['Seat']} Details"):
                    st.write(f"**Elected MP:** {row['Winner']}")
                    st.write(f"**Political Party:** {row['Party']}")
                    st.write(f"**Total Votes Received:** {row['Votes']:,}")
        else:
            st.error("No matching constituency found.")
    else:
        st.info("Search by constituency name above.")

    st.subheader("Full Gazette Excerpt")
    st.dataframe(df, use_container_width=True)

# --- 5. PAGE: REGIONAL ANALYSIS ---
elif mode == "Regional Analysis":
    st.title("🗺️ Division-wise Breakdown")
    div = st.selectbox("Select Division", df['Division'].unique())
    div_df = df[df['Division'] == div]

    st.write(f"Showing results for **{div}** Division:")
    st.table(div_df)

    st.bar_chart(div_df.set_index('Seat')['Votes'])

# --- 6. FOOTER ---
st.sidebar.divider()
st.sidebar.caption("Data source: Bangladesh Election Commission (Feb 15, 2026)")
