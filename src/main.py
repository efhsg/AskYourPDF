import os
import re
import decimal
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from openai import InvalidRequestError
from langchain.callbacks import get_openai_callback

def main():
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    st.set_page_config(page_title="Ask you PDF")
    st.header("Ask your pdf :speech_balloon:")

    pdf = st.file_uploader("Upload your pdf", type="pdf")
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        st.write("Parsing " + str(len(pdf_reader.pages)) + " pages")
        for page in pdf_reader.pages:
            text += page.extract_text()
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        )
        chunks = text_splitter.split_text(text)

        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        user_question = st.text_input("Ask a question about your PDF:")
        if user_question:
            user_question = "From the context." + user_question
            print(user_question)
            docs = knowledge_base.similarity_search(user_question, 3)
            try:
                response = run_chain(5, 1000, model_name, docs, user_question)
            except InvalidRequestError as e:
                if "maximum context length" in str(e):
                    print("============== MAX =======================")
                    print(e)
                    print("==========================================")
                    response = run_chain(2, 500, model_name, docs, user_question)
                else:
                    raise e

            st.write(response)
            st.balloons()


def run_chain(k, max_tokens, model_name, docs, user_question):
    llm = ChatOpenAI(model_name=model_name, temperature=0, max_tokens=max_tokens)
    chain = load_qa_chain(llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs[:k], question=user_question)
        print(cb)
        rounded_cost = extract_and_round_cost(cb)
        st.write("Using " + model_name + ", " + f"${rounded_cost}")
        st.write("---")        
    return response


def extract_and_round_cost(cb):
    cb_str = str(cb)
    cost_line = re.search(r"Total Cost \(USD\): \$(.+)", cb_str)

    if cost_line:
        cost_str = cost_line.group(1)
        cost = decimal.Decimal(cost_str)
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        rounded_cost = round(cost, 3)
        return float(rounded_cost)

load_dotenv()
if __name__ == "__main__":
    main()
