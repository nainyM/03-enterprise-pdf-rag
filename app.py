import streamlit as st

from rag import ROLE_ACCESS, answer, require_api_key

st.set_page_config(page_title="Enterprise PDF RAG", page_icon="📄", layout="centered")

st.title("Enterprise PDF RAG")
st.caption("Answers come only from the documents this role can access. Every claim is cited.")

with st.sidebar:
    st.header("About")
    st.write(
        "Synthetic Kestrel Logistics documents. Each document has an access tag, "
        "and superseded versions are hidden from search."
    )
    role = st.selectbox("Role", list(ROLE_ACCESS), help="Controls which access tags are searchable.")
    st.caption("Searchable tags: " + ", ".join(ROLE_ACCESS[role]))

question = st.text_input("Ask a question", placeholder="e.g. What is the meal allowance for domestic travel?")

if st.button("Ask", type="primary", disabled=not question.strip()):
    try:
        require_api_key()
        with st.spinner("Searching the documents..."):
            result = answer(question.strip(), role)
    except SystemExit as exc:
        st.error(str(exc))
        st.stop()

    if result.refused:
        st.warning(result.text)
    else:
        st.success(result.text)

    if result.citations:
        st.markdown("**Cited:** " + ", ".join(f"`{c}`" for c in result.citations))

    st.caption(
        f"Retrieval {result.retrieval_ms:.0f} ms · generation {result.generation_ms:.0f} ms · "
        f"{result.input_tokens} input / {result.output_tokens} output tokens"
    )

    with st.expander("Retrieved chunks"):
        for hit in result.retrieved:
            st.markdown(f"**{hit.ref}** · {hit.section} · distance {hit.distance:.3f}")
            st.text(hit.text)
