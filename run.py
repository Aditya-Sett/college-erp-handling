# Entry Point

from app import create_app
import os
#from dotenv import load_dotenv
#load_dotenv()

app = create_app()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False
    )

