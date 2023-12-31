import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
 You are a marketing copywriter with 20 years of experience. You are analyzing customer's background to write personalized product description that only this customer will receive; 
    PRODUCT input text: {content};
    CUSTOMER age group (y): {agegroup};
    CUSTOMER activity level: {activity};
    TASK: Write a product description that is tailored into this customer's Age group and activity level. Use age group specific slang.;
    FORMAT: Present the result in the following order: (PRODUCT DESCRIPTION), (BENEFITS), (USE CASE);
    PRODUCT DESCRIPTION: describe the product in 5 sentences;
    BENEFITS: describe in 3 sentences why this product is perfect considering customers age group and activity level;
    USE CASE: write a story in 5 sentences, of an example weekend activity taking into account activity level {activity} and age {agegroup}, write a story in first person, example "I started my Saturday morning with ...";
"""

prompt = PromptTemplate(
    input_variables=["agegroup", "activity", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(model_name='gpt-4', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Otstarve: tootetutvustustekstide personaliseerimine igale kliendile või kliendigruppidele; väljundtekst on kohandatud kliendi a) vanuserühmaga ja b) aktiivsustasemega; sisendtekstiks on neutraalses vormis tootekirjeldus. \
    \n\n Kasutusjuhend: 1) valmista ette tootekirjeldus (sisendtekst). 2) määra tarbijasegemendid lähtuvalt vanuserühma ja aktiivsustaseme kombinatsioonidest. 3) sisesta ükshaaval tarbijasegmentide lõikes eeltoodud info äpi kasutajaliideses, saada ära. \
    4) kopeeri ükshaaval tarbijasegmentide lõikes äpi väljundteksti kõnealuse toote tutvustuslehele.")

with col2:
    st.image(image='companylogo.jpg', caption='Our company motto')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_agegroup = st.selectbox(
        'Which age group would you like your content to target?',
        ('9-15', '16-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-100'))
    
with col2:
    option_activity = st.selectbox(
        'What activity level you like your content to target?',
        ('Sedentary lifestyle', 'Slightly active', 'Moderatly active', 'Active lifestyle', 'Very active lifestyle'))

def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "white watch, I would like it to count steps"

st.button("*See An Example*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(agegroup=option_agegroup, activity=option_activity, content=content_input)

    formatted_content = llm(prompt_with_content)

    st.write(formatted_content)
