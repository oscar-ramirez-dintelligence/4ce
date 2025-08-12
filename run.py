from cotizador import create_app
from dotenv import load_dotenv

# Load environment variables from .env file,
# so they are available before the app is created.
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # The host and port are now configured inside create_app,
    # but this is the entry point for local development.
    app.run()
