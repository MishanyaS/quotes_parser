from parser import get_quotes, write_to_excel, write_to_db

if __name__ == '__main__':
    write_to_excel(get_quotes)
    write_to_db(get_quotes)