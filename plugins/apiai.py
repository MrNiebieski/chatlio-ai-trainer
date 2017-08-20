from rtmbot.core import Plugin
import apiai
import yaml
import os.path
import sys, traceback

from .models import chatlioDataModel, apiResponseModel

dir_name = os.path.dirname(__file__)
config_file = os.path.join(dir_name, '../rtmbot.conf')

config = yaml.load(open(config_file, 'r'))
API_API_TOKEN = config.get("API_API_TOKEN", None)
if API_API_TOKEN is None or not API_API_TOKEN:
    raise Exception("No api.ai token provided")

BOT_ID = config.get("BOT_ID", None)

ai = apiai.ApiAI(API_API_TOKEN)


class TrainerPlugin(Plugin):

    def process_message(self, payload):
        try:
            data = chatlioDataModel(payload, BOT_ID)

            if data.is_chatlio_client():
                sessionId = data.build_session()

                request = ai.text_request()
                request.query = data.text
                if sessionId is not None:
                    request.session_id = sessionId

                response = apiResponseModel(request.getresponse())

                if response.should_reply():
                    response.delay()
                    self.outputs.append(
                        [data.channel, response.speech]
                    )
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exc(file=sys.stdout)
            print(e)

