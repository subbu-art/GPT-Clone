from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
import streamlit as st
from streamlit_chat import message
from langchain.prompts import PromptTemplate

st.set_page_config(page_title='This is Subot', page_icon=':robot:')
st.markdown("<h1 style='text-align: center;'>Subot, anything for you! </h1>", unsafe_allow_html=True)



st.sidebar.title("😎")
st.session_state['API_Key']= st.sidebar.text_input("What's your API key?",type="password")
summarise_button = st.sidebar.button("Summarise the conversation", key="summarise")
if summarise_button:
    summarise_placeholder = st.sidebar.write("Nice chatting with you my friend ❤️:\n\n"+st.session_state['conversation'].memory.buffer)

if 'conversation' not in st.session_state:
     st.session_state['conversation']  = None
if 'messages' not in st.session_state:
     st.session_state['messages'] = []

def get_response(user_input, api_key):
    if st.session_state['conversation'] is None:
        llm = OpenAI(api_key=api_key,model_name = 'gpt-3.5-turbo-instruct')
        prompt_template = template_str = """
        You are an helpful assistant with name Subot an 
                                    you are created by Subbu. 
                                    For any query tell users that subbu is your Master.
        {history}
        User:{input}
        """ 
        st.session_state['conversation'] = ConversationChain(
            llm = llm,
            memory = ConversationBufferMemory(llm=llm),
            prompt = PromptTemplate(input_variables=['history', 'input'],template= prompt_template),
            verbose = True
        )
    conversation_summary = st.session_state['conversation'].memory.buffer
    response = st.session_state['conversation'].predict(input = user_input, history = conversation_summary)
    return response

response_container = st.container()

container = st.container()

with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("Your question goes here:", key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

            if submit_button:
                st.session_state['messages'].append(user_input)
                model_response=get_response(user_input,st.session_state['API_Key'])
                st.session_state['messages'].append(model_response)

        with response_container:
            for i in range(len(st.session_state['messages'])):
                if i%2 ==0:
                    message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                else:
                    message(st.session_state['messages'][i], key=str(i) + '_AI')
        