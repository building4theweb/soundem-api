import dotenv


dotenv.read_dotenv()

from soundem import app

if __name__ == '__main__':
    app.run()
