# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os

from dotenv import load_dotenv


class ConfigManager:
    def __init__(self):
        load_dotenv()

        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')

    def set_openai_api_key(self, api_key):
        self.openai_api_key = api_key
        os.environ['OPENAI_API_KEY'] = api_key

    def has_openai_api_key(self):
        return bool(self.openai_api_key)


config = ConfigManager()
