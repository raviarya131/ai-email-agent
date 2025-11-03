# 🎓 AI University Email Agent

**Submitted by: Ravi Kumar, BS Economics, IIT Kanpur**

A prototype AI agent built for a university assignment (SDE Role). This tool helps students automate the task of drafting professional emails by leveraging a Large Language Model (LLM) to reason, plan, and execute the draft.

---

##  Demo

Here is a brief demonstration of the application, showing the user input and the side-by-side output of the agent's reasoning and the final email draft.

![Demo](demo.gif)

---

##  core Features

* **Task Automation:** Automates the manual task of drafting professional university emails.
* **AI-Powered Logic:** The agent follows a "Reason, Plan, Execute, Guide" model to generate drafts.
* **Intuitive UI:** Built with Streamlit for a clean, form-based user interface.
* **Personalization:** Allows users to input their personal details (name, course, etc.) and desired tone for a ready-to-send email.
* **Separated Outputs:** The final draft is split into a **Guide**, **Subject**, and **Body** for clarity and ease of use.

## ✨ Bonus Features Implemented

* **External Integration:** Integrates with the Google Gemini API (`gemini-2.5-pro`) to act as the agent's "brain."
* **UI for Monitoring:** The app provides a dedicated side-panel to monitor the agent's internal **Reasoning** and **Plan**, fulfilling the bonus requirement.

## 🚀 How to Run Locally

This project was built in Python using Streamlit.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install streamlit google-generativeai pyperclip
    ```

4.  **Set your API Key:**
    You must set your Google AI API key as an environment variable.
    * **On Mac/Linux:** `export GOOGLE_API_KEY='YOUR_API_KEY_HERE'`
    * **On Windows:** `set GOOGLE_API_KEY=YOUR_API_KEY_HERE`

5.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

## 🛠️ Technologies Used

* **Python**
* **Streamlit** (for the UI and web server)
* **Google Gemini API** (for the AI agent logic)
* **Pyperclip** (for the "Copy to Clipboard" feature)
