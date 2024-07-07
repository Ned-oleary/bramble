from dotenv import load_dotenv
import os

load_dotenv()

POSTGRID_API_KEY = os.getenv("POSTGRID_TEST_KEY")
# POSTGRID_API_KEY = os.getenv("POSTGRID_PRODUCTION_KEY")

THANKS_IO_HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ os.getenv("THANKS_IO_TOKEN")}
THANKS_IO_SEND_URL = "https://api.thanks.io/api/v2/send/postcard"