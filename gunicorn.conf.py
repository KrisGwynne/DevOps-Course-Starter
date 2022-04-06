from dotenv import load_dotenv, find_dotenv

# Load environment variables when running the app through gunicorn
load_dotenv(find_dotenv('.env'))