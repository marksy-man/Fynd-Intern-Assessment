import streamlit as st
import backend as bk

# Page Configuration
st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("Feedback Administration Console")

# Load existing data [cite: 60]
df = bk.load_data()

if not df.empty:
    # 1. Key Metrics [cite: 59]
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reviews", len(df))
    col2.metric("Average Rating", f"{df['Rating'].mean():.2f}")
    col3.metric("Negative Reviews", len(df[df['Sentiment'] == "Negative"]))

    st.markdown("---")

    # 2. Detailed Review List [cite: 53]
    st.subheader("Recent Submissions")
    
    # Display the dataframe with relevant columns
    display_columns = ["Date", "Rating", "Review", "Summary", "Action", "Sentiment"]
    
    # Show newest reviews first
    st.dataframe(
        df[display_columns].iloc[::-1],
        use_container_width=True,
        hide_index=True
    )

    # 3. Data Export Option
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False),
        file_name="feedback_data.csv",
        mime="text/csv"
    )

else:
    st.info("No data available. Waiting for user submissions.")
