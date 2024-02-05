from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.agents import Tool
from ritetag import RiteTagApi
from langchain.prompts import PromptTemplate
import google.generativeai as gen_ai
from langchain.tools import load_tools
from langchain.agents import initialize_agent
load_dotenv()



access_token = '0d2ce29596ea5f73de51a6e7e47799bcff27a78e3988'
client = RiteTagApi(access_token)

#_Hashtag__data: {'tag': 'nft', 'tweets': 216, 'retweets': 376, 'exposure': 193576, 'links': 0.2314815, 'photos': 0.2314815, 'mentions': 0.5740741, 'color': 3}
def get_trending_hashtags():
     trending=client.trending_hashtags()
     for hashtag in trending:
        attributes = vars(hashtag)
        for attribute, value in attributes.items():
            print(f'{attribute}: {value}')
        
def extract_feautures(text):
    feauture_extraction_llm=OpenAI(model_name="gpt-3.5-turbo-instruct")
    our_prompt = """
    
    {query}
    You are a capable AI, who is able to accuractely extract feautures from text,Extract feautures from the text above.
    """ 
    prompt =PromptTemplate(
    input_variables=["query"],
    template=our_prompt,
    )
    
    final_prompt=prompt.format(query=text)
    print(final_prompt)
    print(feauture_extraction_llm(final_prompt))
    

extract_feautures("I am a data scientist who is passionate about machine learning and artificial intelligence")
