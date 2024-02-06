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


def generate_captions(text:str):
    caption_llm=OpenAI(model_name="gpt-3.5-turbo-instruct")
    template="""
    Generate a caption for the following {text}.
    Create the caption depending on the context and the tone should be relevant to the platform to its being posted on.
    i.e tone should be professional for linkedin and casual for instagram,twitter and others.
    """
    caption_prompt=PromptTemplate(
        input_variables=["text"],
        template=template
    )
    chain=LLMChain(llm=caption_llm,prompt=caption_prompt)
    inputs={
        "text":text
    }
    caption=chain.run(inputs)
    return caption
    
# SCRAPE WITH FEAUTURES TO AVOID  INFINITE LOOP 




trending_hashtags_tool=Tool(
    name="trending_hashtags",
    func=get_trending_hashtags,
    description="""
    Only use this when platform is twitter and always use this in combination with the feauture_extraction tool and the scraping_hashtags tool.
    Get the trending hashtags on twitter and their engagement metrics.This tells you how popular a hashtag is on twitter and how much engagement it has.
            Get multiple hashtags for the given text and then use the engagement metrics to find the most relevant hashtags for the text.""",
    input_variables=[],
    output_variables=["trending_hashtags"]
)

feauture_extraction_tool=Tool(
    name="feauture_extraction",
    func=extract_feautures,
    description="""
    You are a content strategist at a company.
    You are responsible to find relevant hashtags for the content that is being posted on social media and catchy captions for it.
    For every good performance, you will be rewarded with a bonus.
    In the same way you are punished for bad performance.
    Use all tools provided to you to give the best results.
    Always use this in combination with the trending_hashtags tool and the scraping_hashtags tool.
    Use this tool to extract feautures from text.Then the extracted feautures can be used to find which hashtag is more relevant to the text.""",
    input_variables=["text"],
    output_variables=["feautures"]
)

scraping_hashtags_tool=Tool(
    name="scraping_hashtags",
    func=scraping_hashtags,
    description="""
    Always use this in combination with the feauture_extraction tool.
    Scrape the trending hashtags on a platform. Use this in case the trending hashtags are not available on the platform you are looking for. This tool will scrape the trending hashtags for you. """,
    input_variables=["platform"],
    output_variables=["scraped_hashtags"]
)


hashtag_tools=[feauture_extraction_tool,scraping_hashtags_tool]
hashtag_llm=OpenAI(
    model_name="gpt-3.5-turbo-instruct",
    )
hashtag_agent=initialize_agent(
    agent='zero-shot-react-description',
    tools=hashtag_tools,
    verbose=True,
    name="hashtag_agent",
    max_iterations=8,
    llm=hashtag_llm
    )

# hashtag_agent.run("I am trying to find a job as software dev on linkedin")

caption_tool=Tool(
    name="caption",
    func=generate_captions,
    description="""
    This tool helps you to generate the best caption for a given text. The caption is generated depending on the context and the tone is relevant to the platform to its being posted on.
    Always use this tool in combination with feauture extraction tool.
    .""",
    input_variables=["text"],
    output_variables=["caption"]
)

caption_llm=OpenAI(
    model_name="gpt-3.5-turbo-instruct",
    )
caption_tools=[feauture_extraction_tool,caption_tool]
caption_agent=initialize_agent(
    agent='zero-shot-react-description',
    tools=caption_tools,
    verbose=True,
    name="caption_agent",
    max_iterations=8,
    llm=hashtag_llm
    )
# caption_agent.run("I am trying to find a job as software dev on linkedin")