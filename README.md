# System Design: AI University Email Agent

## 1. System Architecture

The system is a single-page web application that uses a simple, serverless-style "agent-on-demand" architecture.

* **Frontend (UI):** A web interface built and served by **Streamlit**. It provides form-based inputs for the user and displays the structured output in a 1/3 + 2/3 column layout.
* **Backend:** The **Streamlit server** itself acts as the backend. It runs the Python script, receives form data, and handles all application logic.
* **AI Agent:** The "agent" is not a persistent service but is instantiated on-demand via a call to the **Google Gemini API** (using the `gemini-2.5-pro` model). The agent's "reason, plan, execute" logic is enforced by a highly-structured prompt.



## 2. Data Design

The application is stateless (it does not use a database). Data flows as follows:

* **Input Data:** The system takes seven unstructured text strings from the Streamlit form:
    1.  `recipient`
    2.  `goal`
    3.  `points`
    4.  `tone`
    5.  `sender_name`
    6.  `sender_id`
    7.  `sender_course`
* **Process Data:** The core of the system is the **master prompt** in the `get_prompt` function. This prompt formats the user's input and instructs the LLM to return a structured response separated by `---` markers.
* **Output Data:** The LLM returns a single string. The `get_agent_response` function parses this string by splitting it `---` to extract five distinct pieces of data:
    1.  `Reasoning` (for the monitoring UI)
    2.  `Plan` (for the monitoring UI)
    3.  `Subject` (for the output)
    4.  `Body` (for the output)
    5.  `Guide` (for the output)

## 3. Component Breakdown

The entire prototype is contained in `app.py`:

* **`get_prompt(...)`:** A function that takes all user inputs and constructs the large, detailed master prompt string. This prompt is the core of the "agent's" logic.
* **`get_agent_response(...)`:** This function handles the "external integration."
    1.  It calls `get_prompt` to get the formatted request.
    2.  It sends the request to the Gemini API.
    3.  It receives the raw text response.
    4.  It parses the text into the five required parts (Reasoning, Plan, Subject, Body, Guide) and returns them.
* **Streamlit UI (Main Body):**
    1.  Renders the title and input form (`st.form`).
    2.  Uses `st.columns` to organize the input fields.
    3.  On `st.form_submit_button` click, it runs the spinner and calls `get_agent_response`.
    4.  **Output Rendering:**
        * It creates a 1/3 + 2/3 column layout using `st.columns([1, 2])`.
        * **Left Column (1/3):** Displays the `reasoning` and `plan` (fulfilling the "UI for monitoring" bonus).
        * **Right Column (2/3):** Displays the `guide` (in `st.info`), `subject` (in `st.code`), and `body` (in `st.container(border=True)` to ensure text wrapping).
    5.  It uses the `pyperclip` library for the "Copy to Clipboard" button.

## 4. Chosen Technologies & Justification

* **Python:** Chosen as the primary language due to its dominance in the AI/LLM space and its rich ecosystem of libraries.
* **Streamlit:** Chosen for **extreme rapid prototyping speed**. It allowed us to build and deploy a functional, data-driven web UI and backend in a single file, which is essential for a short-deadline project. It perfectly met the "user interface" requirement.
* **Google Gemini API (`gemini-2.5-pro`):** Chosen as the external integration to fulfill the "reason, plan, and execute" requirement. By instructing the LLM to output its own reasoning and plan, we satisfy the core and bonus requirements without building a complex, from-scratch agent framework.
* **`pyperclip`:** A small utility library chosen to improve the user experience (UX) by adding a functional "Copy to Clipboard" button.

## 5. Originality & Social Impact

The system automates a common, high-friction task for university students: professional communication. Many students struggle with "email anxiety" or finding the correct tone when writing to professors. This agent acts as a co-pilot, not only drafting the email (execution) but also showing its thought process (reasoning & plan). This transparency can help educate the user on *how* to write such emails, providing a positive social impact by improving communication skills and reducing anxiety.
