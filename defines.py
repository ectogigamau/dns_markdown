

UPDATE_DATABASE = True
ALWAYS_REINIT_CATEGORY = True

DB_FILE_NAME = "DnsCatalog.db"

MAX_DAY_SAVE = 5

CATALOG_HEAD_URL = 'https://www.dns-shop.ru/catalog/markdown/'

def url_from_tag(tag):
    return 'http://www.dns-shop.ru/catalog/markdown/?category=' + tag
