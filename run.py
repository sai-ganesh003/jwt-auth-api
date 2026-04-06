import os
from dotenv import load_dotenv
load_dotenv(override=False)
print("DATABASE_URL:", os.environ.get('DATABASE_URL'))

from app import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)