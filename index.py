import tweepy
import json
from collections import OrderedDict
import googletrans
import telegram
from dotenv import load_dotenv
import os


load_dotenv()
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('CHAT_ID')
CONSUMER_TOKEN = os.environ.get('CONSUMER_TOKEN')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.environ.get('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')



translator = googletrans.Translator()

auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
bot = telegram.Bot(token = BOT_TOKEN)



# tweepy.StreamClient 클래스를 상속받는 클래스
class TwitterStream(tweepy.StreamingClient):
    def on_data(self, raw_data):
        tweetData = json.loads(raw_data)
        print(tweetData)
        tweetId = tweetData['data']['id']
        tweetText = tweetData['data']['text']
        korText = translator.translate(tweetText, src="en", dest='ko').text
        #get_tweet user by id
        responseUser = userClient.get_tweet(tweetId, expansions=["author_id"])
        print(responseUser.includes['users'][0].name)
        
        bot.sendMessage(
            chat_id = chat_id, 
            text = responseUser.includes['users'][0].name+ " : " + korText + "\n\n" + tweetText + "\n\n"
         + "https://twitter.com/twitter/statuses/"+tweetId)
        print('전송완료 : ' + korText)
        
        
# 규칙 제거 함수
def delete_all_rules(rules):
    # 규칙 값이 없는 경우 None 으로 들어온다.
    if rules is None or rules.data is None:
        return None
    stream_rules = rules.data
    ids = list(map(lambda rule: rule.id, stream_rules))
    client.delete_rules(ids=ids)

# 스트림 클라이언트 인스터턴스 생성
client = TwitterStream(BEARER_TOKEN)

# 글 작성자 가져오기 위한 인스턴스 생성
userClient = tweepy.Client(BEARER_TOKEN)


# 모든 규칙 불러오기 - id값을 지정하지 않으면 모든 규칙을 불러옴
rules = client.get_rules()

# 모든 규칙 제거
delete_all_rules(rules)

# 스트림 규칙 추가
client.add_rules(tweepy.StreamRule(value="write here to stream sentence you want"+" from:"+targetIntTweetId))

# 스트림 시작
client.filter()