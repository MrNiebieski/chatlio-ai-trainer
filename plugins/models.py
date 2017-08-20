import json
import time

DEBUG = True


class chatlioDataModel(object):
    def __init__(self, data, chatlio_bot_id = None):
        self.data = data
        if DEBUG:
            print("chatlio payload "+"*"*30)
            print(json.dumps(data,
                indent=2, separators=(',', ': ')))
        self.chatlio_bot_id = chatlio_bot_id
        self.parse()

    def parse(self):
        self.team = self.data.get('team')
        self.channel = self.data.get('channel')
        self.text = self.data.get('text')
        self.bot_id = self.data.get('bot_id')
        if self.bot_id is not None:
            self.chatlio_client = (
                    self.bot_id == self.chatlio_bot_id
                )
        else:
            self.chatlio_client = False

    def build_session(self):
        return "{}-{}".format(self.bot_id, self.channel)

    def is_chatlio_client(self):
        return self.chatlio_client



class apiResponseModel(object):
    def __init__(self, resp):
        self.data = json.loads(resp.read().decode("utf-8"))
        self.result = self.data.get('result', {})
        self.fulfillment = self.result.get('fulfillment', {})
        self.speech = self.fulfillment.get('speech', None)
        self.sessionId = self.result.get('sessionId', None)

        if DEBUG:
            print("api.ai response "+"="*30)
            print(json.dumps(self.data,
                indent=2, separators=(',', ': ')))
            print("speech:\n{}".format(self.speech))

    def should_reply(self):
        """
        custom logic
        """
        return False
        # return True

    def delay(self):
        """
        artifical delay in reply
        """
        time.sleep(1)