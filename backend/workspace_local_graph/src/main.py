from src.config import DATABASE_URL

def get_database_url():
    return DATABASE_URL

if __name__ == '__main__':
    print(get_database_url())
