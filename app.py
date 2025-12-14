import streamlit as st
import backend as bk

# Page Configuration
st.set_page_config(page_title="Customer Feedback Portal")

st.title("Customer Feedback")
st.write("We value your opinion. Please rate your experience below.")

# 1. User Input Section [cite: 46, 47]
stars = st.slider("Rating (1-5)", 1, 5, 5)
review_text = st.text_area("Your Review", placeholder="Please share details about your experience...")

# 2. Submission Logic [cite: 48, 49]
if st.button("Submit Feedback"):
    if review_text:
        with st.spinner("Processing your feedback..."):
            # Generate AI content
            ai_reply = bk.generate_ai_response(stars, review_text)
            analysis = bk.analyze_review_for_admin(stars, review_text)
            
            # Save data to backend
            bk.save_review(stars, review_text, ai_reply, analysis)
            
            # Display confirmation and response [cite: 50]
            st.success("Feedback submitted successfully.")
            st.info(f"Response from Management: {ai_reply}")
    else:
        st.warning("Please enter review text before submitting.")
