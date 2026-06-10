from dotenv import load_dotenv
from pathlib import Path

load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)

from langfuse import get_client

langfuse = get_client()

print("Client:", langfuse)

try:
    result = langfuse.auth_check()
    print("Auth:", result)
except Exception as e:
    print("Error:", e)