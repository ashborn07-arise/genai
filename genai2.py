import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# Configure Gemini API Key
genai.configure(api_key="AIzaSyA1SfkZ1wx8D10zby2R9vKRL7ad2rdaw7Y")

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize session state for chat and message history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.message = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot with PDF", page_icon="🤖")
st.title("🤖 Gemini AI Chatbot with PDF Training")

# File uploader for PDF
uploaded_pdf = st.file_uploader("Upload your PDF", type="pdf")

# Extract text from uploaded PDF
if uploaded_pdf is not None:
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pdf_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pdf_text += page.get_text()

    st.session_state.pdf_text = pdf_text  # Save to session state

    st.write("📄 Preview of extracted PDF text:")
    st.write(pdf_text[:1000] + "...")  # Show a sample of text

# Display chat messages from history
for msg in st.session_state.message:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Ask a question related to the PDF...")

# Process user query
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.message.append({"role": "user", "content": user_input})

    # Use a portion of the PDF text as context (limit to first 2000 characters)
    pdf_context = st.session_state.pdf_text[:2000]
    input_text = f"{pdf_context}\n\nUser query: {user_input}"

    try:
        response = st.session_state.chat.send_message(input_text)
        answer = response.text
    except Exception as e:
        answer = f"Error: {e}"

    st.chat_message("assistant").markdown(answer)
    st.session_state.message.append({"role": "assistant", "content": answer})
