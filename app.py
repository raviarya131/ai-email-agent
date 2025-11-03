import streamlit as st
import google.generativeai as genai
import os
import pyperclip  # For copy-to-clipboard functionality

# --- Configuration ---
api_key = None

# 1. Try to get API key from Streamlit secrets (for deployment)
try:
    api_key = st.secrets.get("GOOGLE_API_KEY")
except Exception:
    pass  # This exception is fine, means secrets.toml likely not present

# 2. If not found in secrets, try environment variable (for local dev)
if not api_key:
    try:
        api_key = os.environ['GOOGLE_API_KEY']
    except KeyError:
        st.error(
            "GOOGLE_API_KEY not found in environment variables. "
            "Please set it in your terminal/PyCharm before running."
        )
        st.stop()

# 3. If we still don't have a key (e.g., it was empty), stop.
if not api_key:
    st.error("API Key configuration failed. Please check your setup.")
    st.stop()

# Configure the generative AI model
try:
    genai.configure(api_key=api_key)
    # --- MODEL NAME UPDATED ---
    model = genai.GenerativeModel('gemini-2.5-pro')
except Exception as e:
    st.error(f"Error configuring AI model with provided key: {e}")
    st.stop()


# --- The Master Prompt Template (UPDATED for Subject/Body/Guide) ---
def get_prompt(recipient, goal, points, sender_name, sender_id, sender_course, tone):
    """
    Creates the structured prompt, now asking for Subject, Body, and a Guide separately.
    """
    return f"""
    You are an AI agent designed to help university students. Your task is to draft a professional email.
    You MUST follow this 'Reason, Plan, Execute, Guide' process and output your response in the
    exact multi-part format specified below.

    **User Input:**
    * To: {recipient}
    * My Goal: {goal}
    * Key Points to Include: {points}
    * Desired Tone: {tone}
    * Sender Name: {sender_name if sender_name else 'Student'}
    * Sender Student ID: {sender_id if sender_id else 'N/A'}
    * Sender Course: {sender_course if sender_course else 'N/A'}

    ---

    **Your Process:**

    1.  **🧠 Reasoning:** Analyze the user's goal, context, desired tone, and sender details.
    2.  **📝 Plan:** Create a step-by-step outline for the email's structure and content.
    3.  **📧 Execute Draft:** Write the final email, splitting it into a Subject line and a Body.
    4.  **💡 Analysis & Guide:** After writing the draft, analyze it. Note any placeholders (like `[Insert Date]` or `[Professor's Office Location]`) that the user must replace. If no changes are needed, state that the draft is "Ready to send."

    **Output:**

    ---
    **🧠 Reasoning:**
    [Your reasoning here]
    ---
    **📝 Plan:**
    [Your plan here]
    ---
    **📬 Subject:**
    [Your generated subject line here. DO NOT include "Subject:"]
    ---
    **📧 Body:**
    [Your email draft body here. Start with "Dear {recipient}," and end with your sender's name.]
    ---
    **💡 Guide:**
    [Your analysis and guide here. For example: "This draft is ready to send," or "Please replace `[placeholder]` with the correct information."]
    ---
    """


# --- Helper Function to Call AI and Parse Response (UPDATED for 5 Parts) ---
def get_agent_response(recipient, goal, points, sender_name, sender_id, sender_course, tone):
    """
    Calls the LLM, gets the response, and parses it into FIVE parts.
    """
    prompt_text = get_prompt(recipient, goal, points, sender_name, sender_id, sender_course, tone)

    try:
        response = model.generate_content(prompt_text)
        full_response_text = response.text

        # New parsing logic based on 5 sections
        parts = full_response_text.split("---")

        if len(parts) >= 6:  # Expecting 5 content parts + 1 empty string at start
            reasoning = parts[1].replace("**🧠 Reasoning:**", "").strip()
            plan = parts[2].replace("**📝 Plan:**", "").strip()
            subject = parts[3].replace("**📬 Subject:**", "").strip()
            body = parts[4].replace("**📧 Body:**", "").strip()
            guide = parts[5].replace("**💡 Guide:**", "").strip()

            return reasoning, plan, subject, body, guide
        else:
            # Fallback for if the AI fails to follow the 5-part format
            st.warning("Agent response was not in the expected 5-part format. Attempting fallback parse...")
            # Try to just get the reasoning, plan, and full draft
            parts = full_response_text.split("---")
            if len(parts) >= 4:
                reasoning = parts[1].replace("**🧠 Reasoning:**", "").strip()
                plan = parts[2].replace("**📝 Plan:**", "").strip()
                draft = parts[3].replace("**📧 Executed Draft:**", "").strip()  # Old format
                return reasoning, plan, "Check Body for Subject", draft, "Could not parse guide."
            else:
                st.error("Failed to parse agent response. Displaying raw output.")
                return "Error", "Error", "Error", full_response_text, "Error"

    except Exception as e:
        st.error(f"Error communicating with the AI: {e}. Check your prompt and API key.")
        return None, None, None, None, None


# --- Streamlit User Interface (UI) ---
st.set_page_config(layout="wide", page_title="AI Email Drafter Agent")
st.title("🎓 AI University Email Agent")
st.markdown(
    "Draft professional university emails instantly with AI assistance. Tell the agent your goal, key points, desired tone, and your details.")

# Use a form for user input
with st.form("email_form"):
    st.subheader("📝 1. Your Email Request")

    # Use columns for better layout of primary inputs
    col1_form, col2_form = st.columns(2)

    with col1_form:
        recipient = st.text_input("To (e.g., Professor Smith, TA Jane)", placeholder="Professor Jane Doe")
        goal = st.text_input("My Goal (e.g., Ask for an extension)",
                             placeholder="Request an extension for Assignment 3")

    with col2_form:
        # NEW FEATURE: Tone selection
        tone = st.selectbox("Desired Tone",
                            options=["Formal", "Polite", "Direct", "Concise", "Empathetic"],
                            index=0,
                            help="Choose the overall tone for your email.")
        st.text("")  # Spacer

    points = st.text_area("Key Points to Include",
                          placeholder="I was sick last week; I will catch up quickly; My current grade in the course is A-",
                          height=100)

    st.subheader("👤 2. Your Details (for a ready-to-send email)")
    # NEW FEATURE: Sender Details
    col3_form, col4_form, col5_form = st.columns(3)
    with col3_form:
        sender_name = st.text_input("Your Full Name", placeholder="John Doe")
    with col4_form:
        sender_id = st.text_input("Your Student ID", placeholder="12345678")
    with col5_form:
        sender_course = st.text_input("Your Course Code (e.g., CS101)", placeholder="CS101")

    st.markdown("---")  # Visual separator
    submit_button = st.form_submit_button("🚀 Run AI Agent")

# This block executes ONLY when the submit button is pressed
if submit_button:
    if not recipient or not goal or not points:
        st.error("Please fill out 'To', 'My Goal', and 'Key Points to Include'.")
    else:
        with st.spinner("🧠 Agent is reasoning, planning, and executing the draft..."):

            # --- UPDATED FUNCTION CALL ---
            # Pass all new parameters to the agent
            # NOW EXPECTING 5 RETURN VALUES
            reasoning, plan, subject, body, guide = get_agent_response(
                recipient, goal, points,
                sender_name, sender_id, sender_course, tone
            )

            if reasoning and body:  # Check if we got valid reasoning and body
                st.divider()
                st.subheader("✅ Agent Executed Successfully")

                # NEW LAYOUT: Use columns for side-by-side view (1/3 and 2/3)
                col1, col2 = st.columns([1, 2])

                with col1:
                    # --- AGENT'S INTERNAL PROCESS (Left Side) ---
                    st.subheader("Agent's Internal Process")
                    st.info("Monitoring the agent's reasoning and plan (Bonus Feature).")
                    st.markdown("---")
                    st.markdown("**🧠 Reasoning:**")
                    st.write(reasoning)  # st.write automatically wraps text
                    st.markdown("---")
                    st.markdown("**📝 Plan:**")
                    st.write(plan)  # st.write automatically wraps text

                with col2:
                    # --- FINAL EMAIL DRAFT (Right Side) ---
                    st.subheader("Your Ready-to-Send Email")

                    # --- NEW GUIDE BOX ---
                    st.markdown("**💡 Guide & Analysis**")
                    st.info(guide)  # The .info() box is perfect for this

                    # --- NEW SUBJECT BOX ---
                    st.markdown("**📬 Subject**")
                    st.code(subject, language='text')

                    # --- EMAIL BODY BOX (with text-wrap fix) ---
                    st.markdown("**📧 Email Body**")
                    with st.container(border=True):
                        st.write(body)

                        # --- UPDATED COPY BUTTON ---
                    # Create the full email text for the copy button
                    full_email_text = f"Subject: {subject}\n\n{body}"

                    if st.button("📋 Copy Full Email (Subject + Body)"):
                        try:
                            pyperclip.copy(full_email_text)
                            st.success("Full email (Subject + Body) copied to clipboard!")
                        except pyperclip.PyperclipException:
                            st.warning("Could not copy to clipboard automatically. Please copy the text manually.")
                            st.info(
                                "You might need to install a copy/paste backend for pyperclip (e.g., 'pip install xclip' on Linux).")