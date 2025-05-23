import streamlit as st
import time
from langchain_ollama import OllamaLLM

# =======================
# Page Configuration
# =======================
st.set_page_config(
    page_title="Zeejay Labs AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# Session State for Chat History
# =======================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

# =======================
# Sidebar
# =======================
with st.sidebar:
    st.title("Zeejay Labs")
    st.markdown("🤖 Local AI Assistant")
    st.markdown("⚡ Powered by Llama 3")
    st.markdown("🔒 Privacy First")

    st.markdown("---")
    st.subheader("System Status")
    st.markdown(f"💬 **Total Messages:** {st.session_state.total_messages}")
    st.markdown(f"📝 **Current Session:** {len(st.session_state.messages)} messages")

    st.markdown("---")
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")
        time.sleep(1)
        st.rerun()

    st.markdown("---")
    st.subheader("💡 Tips")
    st.info("• Ask complex questions\n• Request code examples\n• Get explanations\n• Brainstorm ideas")

    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit + LangChain + Ollama")

# =======================
# Main App Content
# =======================
st.title("Zeejay's AI Assistant")

if len(st.session_state.messages) == 0:
    st.markdown(
        """
👋 **Welcome to your Personal AI Assistant!**

I'm powered by Llama 3 and running locally on your machine. Ask me anything—from coding help to creative writing, analysis, or just casual conversation!

**🚀 Ready to get started? Type your message below!**
        """
    )

# =======================
# Initialize Ollama LLM
# =======================
@st.cache_resource
def load_llm():
    try:
        return OllamaLLM(model="llama3")
    except Exception as e:
        st.error(f"Error loading AI model: {str(e)}")
        st.info("Make sure Ollama is running and the llama3 model is installed.")
        return None

llm = load_llm()

# =======================
# Chat History
# =======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🧠"):
        st.markdown(msg["content"])

# =======================
# Chat Input
# =======================
if llm is not None:
    prompt = st.chat_input("💭 Ask me anything... (Press Enter to send)")

    if prompt:
        st.session_state.total_messages += 1
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = llm.invoke(prompt)
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}"
                    st.error(response)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()
else:
    st.error("⚠️ AI Model not available. Please check your Ollama installation.")
    st.info(
        """
To fix this issue:
1. Make sure Ollama is installed and running
2. Run: `ollama pull llama3`
3. Restart this application
        """
    )
