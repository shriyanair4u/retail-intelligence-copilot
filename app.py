import streamlit as st

from router import route_question
from rag.rag_chain import ask_question
from sql.sql_agent import agent


# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Retail Intelligence Copilot",
    page_icon="🛍️",
    layout="wide"
)


# ---------------------------------
# SESSION STATE
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------
# HEADER
# ---------------------------------

st.title("🛍️ Retail Intelligence Copilot")

st.write(
    "Ask questions about sales, inventory, "
    "customer reviews, and product performance."
)


# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.header("Retail Copilot")

    st.write(
        "This application uses:"
    )

    st.write("📚 RAG + ChromaDB")
    st.write("🗄️ SQL Agent + PostgreSQL")
    st.write("🤖 LLM Router")

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ---------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ---------------------------------
# USER INPUT
# ---------------------------------

question = st.chat_input(
    "Ask a retail business question..."
)


# ---------------------------------
# PROCESS QUESTION
# ---------------------------------

if question:

    # Display user question

    with st.chat_message("user"):

        st.write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # Assistant response

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing your question..."
        ):

            try:

                # -----------------------------
                # ROUTER
                # -----------------------------

                route = route_question(question)

                st.caption(
                    f"Detected route: {route}"
                )


                # -----------------------------
                # RAG
                # -----------------------------

                if route == "RAG":

                    answer, sources = ask_question(
                        question
                    )

                    st.subheader("Answer")

                    st.write(answer)

                    st.subheader(
                        "📚 Review Sources"
                    )

                    for document in sources:

                        with st.expander(
                            f"Review "
                            f"{document.metadata.get('review_id')}"
                        ):

                            st.write(
                                f"**Product ID:** "
                                f"{document.metadata.get('product_id')}"
                            )

                            st.write(
                                f"**Rating:** "
                                f"{document.metadata.get('rating')}"
                            )

                            st.write(
                                f"**Review:** "
                                f"{document.page_content}"
                            )


                # -----------------------------
                # SQL
                # -----------------------------

                elif route == "SQL":

                    response = agent.invoke({
                        "input": question
                    })

                    answer = response["output"]

                    st.subheader("Answer")

                    st.write(answer)


                # -----------------------------
                # BOTH
                # -----------------------------

                elif route == "BOTH":

                    sql_response = agent.invoke({
                        "input": question
                    })

                    sql_answer = (
                        sql_response["output"]
                    )

                    rag_answer, sources = (
                        ask_question(question)
                    )

                    st.subheader(
                        "📊 Business Analysis"
                    )

                    st.write(sql_answer)

                    st.subheader(
                        "📚 Customer Review Insights"
                    )

                    st.write(rag_answer)

                    st.subheader(
                        "Review Sources"
                    )

                    for document in sources:

                        with st.expander(
                            f"Review "
                            f"{document.metadata.get('review_id')}"
                        ):

                            st.write(
                                f"**Product ID:** "
                                f"{document.metadata.get('product_id')}"
                            )

                            st.write(
                                f"**Rating:** "
                                f"{document.metadata.get('rating')}"
                            )

                            st.write(
                                f"**Review:** "
                                f"{document.page_content}"
                            )

                    answer = (
                        f"Business Analysis:\n\n"
                        f"{sql_answer}\n\n"
                        f"Customer Review Insights:\n\n"
                        f"{rag_answer}"
                    )


                else:

                    answer = (
                        "I could not determine the "
                        "appropriate analysis route."
                    )

                    st.warning(answer)


                # ---------------------------------
                # SAVE ASSISTANT RESPONSE
                # ---------------------------------

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })


            except Exception as e:

                error_message = (
                    "Sorry, I encountered an error "
                    "while processing your question."
                )

                st.error(error_message)

                st.caption(
                    f"Technical details: {str(e)}"
                )