import os

import dotenv

# TODO: more elaborate credential management
dotenv.load_dotenv()

ALPHAVANTAGE_API_KEY=os.getenv("ALPHAVANTAGE_API_KEY")