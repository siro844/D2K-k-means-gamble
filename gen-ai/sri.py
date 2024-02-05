from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.agents import Tool
from ritetag import RiteTagApi
load_dotenv()

model=ChatOpenAI(
    temperature=0.3,
    model_name="gpt-3.5-turbo",
)


access_token = '0d2ce29596ea5f73de51a6e7e47799bcff27a78e3988'
client = RiteTagApi(access_token)

#_Hashtag__data: {'tag': 'nft', 'tweets': 216, 'retweets': 376, 'exposure': 193576, 'links': 0.2314815, 'photos': 0.2314815, 'mentions': 0.5740741, 'color': 3}
def get_trending_hashtags():
     trending=client.trending_hashtags()
     for hashtag in trending:
        attributes = vars(hashtag)
        for attribute, value in attributes.items():
            print(f'{attribute}: {value}')
        
               
