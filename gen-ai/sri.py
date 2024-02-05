from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
from langchain.agents import Tool
from ritetag import RiteTagApi
from langchain.prompts import PromptTemplate
import google.generativeai as gen_ai
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.chains import LLMRequestsChain,LLMChain
load_dotenv()





#_Hashtag__data: {'tag': 'nft', 'tweets': 216, 'retweets': 376, 'exposure': 193576, 'links': 0.2314815, 'photos': 0.2314815, 'mentions': 0.5740741, 'color': 3}
def get_trending_hashtags(input=''):
    access_token = '0d2ce29596ea5f73de51a6e7e47799bcff27a78e3988'
    client = RiteTagApi(access_token)
    trending=client.trending_hashtags()
    for hashtag in trending:
        attributes = vars(hashtag)
        for attribute, value in attributes.items():
            trending_hashtags=(f'{attribute}: {value}')
    
    return trending_hashtags
        
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
    feautures =feauture_extraction_llm(final_prompt)
    return feautures


def scraping_hashtags(platform:str):
    scarping_llm=OpenAI(model_name="gpt-3.5-turbo-instruct")
    template="""
    Extract the trending hastags for the following {platform}
    """
    scraping_prompt=PromptTemplate(
        input_variables=["platform"],
        template=template
    )
    chain=LLMRequestsChain(llm_chain=LLMChain(llm=scarping_llm,prompt=scraping_prompt))
    inputs={
        "platform":platform,
        "url":f"https://www.google.com/search?q=trending+hashtags+for+"+platform.replace(" ","+")   
    }
    scraped_hashtags=chain.run(inputs)
    return scraped_hashtags
    





trending_hashtags_tool=Tool(
    name="trending_hashtags",
    func=get_trending_hashtags,
    description="Get the trending hashtags on twitter and their engagement metrics.This tells you how popular a hashtag is on twitter and how much engagement it has.",
    input_variables=[],
    output_variables=["trending_hashtags"]
)

feauture_extraction_tool=Tool(
    name="feauture_extraction",
    func=extract_feautures,
    description="Extract feautures from text.Use this tool to extract feautures from text.Then the extracted feautures can be used to find which hashtag is more relevant to the text.",
    input_variables=["text"],
    output_variables=["feautures"]
)

scraping_hashtags_tool=Tool(
    name="scraping_hashtags",
    func=scraping_hashtags,
    description="Scrape the trending hashtags on a platform. Use this in case the trending hashtags are not available on the platform you are looking for. This tool will scrape the trending hashtags for you. ",
    input_variables=["platform"],
    output_variables=["scraped_hashtags"]
)


tools=[feauture_extraction_tool,scraping_hashtags_tool]
hashtag_llm=OpenAI(model_name="gpt-3.5-turbo-instruct")
hashtag_agent=initialize_agent(
    agent='zero-shot-react-description',
    tools=tools,
    verbose=True,
    name="hashtag_agent",
    max_iterations=8,
    llm=hashtag_llm
    )
print(hashtag_agent.agent.llm_chain.prompt.template)
hashtag_prompt="""
You are the Content Strategist at a company .Your role is to find the most relevant hashtags
 to increase the client's social media engagement.
    """

print(hashtag_agent( {"input":"Im posting a ad for coaching classes on instagram?"}))