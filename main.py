from app.logic.functions import create_user, get_user, get_all_markets, get_market_by_id, search_markets_by_location, add_review, delete_review

def main_menu():

    while True:
        print("Добро пожаловать в приложение просмотра фермерских рынков.")

        print("1. Просмотреть рынки")
        print("2. Поиск по городу/штату/индексу")
        print("3. Посмотреть подробности о рынке")
        print("4. Добавить отзыв")
        print("5. Удалить отзыв")
        print("0. Выйти")