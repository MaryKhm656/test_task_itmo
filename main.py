from app.db.database import SessionLocal
from app.logic.functions import create_user, get_user, get_all_markets, get_market_by_id, search_markets_by_location, add_review, delete_review

def main():
    while True:
        print("\n=== Меню ===")
        print("1. Создать пользователя")
        print("2. Посмотреть список рынков")
        print("3. Поиск рынков по городу / штату / ZIP")
        print("4. Посмотреть подробности о рынке")
        print("5. Оставить отзыв")
        print("6. Удалить отзыв")
        print("0. Выход")

        choice = input("Выберите пункт меню: ")

        match choice:
            case "1":
                try:
                    with SessionLocal() as db:
                        username = input("Username: ")
                        first_name = input("Имя: ")
                        last_name = input("Фамилия (необязательно): ") or None
                        user = create_user(db, username, first_name, last_name)
                        print(f"✅ Пользователь {user.username} создан.")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            case "2":
                page = 1
                per_page = 5
                while True:
                    try:
                        with SessionLocal() as db:
                            markets, total_pages = get_all_markets(db, page, per_page)
                            print(f"\n📄 Страница {page}/{total_pages}")
                            for market in markets:
                                print(f"{market.id}. {market.name} (ZIP: {market.zip})")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                        break

                    nav = input("← P | N → | Enter — выход: ").lower()
                    if nav == "n" and page < total_pages:
                        page += 1
                    elif nav == "p" and page > 1:
                        page -= 1
                    else:
                        break

            case "3":
                try:
                    with SessionLocal() as db:
                        city = input("Город (можно пропустить): ") or None
                        state = input("Штат (можно пропустить): ") or None
                        zip_code = input("ZIP (можно пропустить): ")
                        zip_code = zip_code if zip_code else None

                        results = search_markets_by_location(db, city, state, zip_code)
                        print(f"\n🔍 Найдено: {len(results)}")
                        for m in results:
                            print(f"{m.id}. {m.name} (ZIP: {m.zip})")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            case "4":
                try:
                    market_id = int(input("Введите ID рынка: "))
                    with SessionLocal() as db:
                        market = get_market_by_id(db, market_id)
                        print(f"\n🏪 {market.name}")
                        print(f"Адрес: {market.street}, ZIP: {market.zip}")
                        if market.reviews:
                            print("Отзывы:")
                            for r in market.reviews:
                                print(f"{r.rating}⭐️ от {r.user.username}: {r.review_text}")
                        else:
                            print("Нет отзывов.")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            case "5":
                try:
                    with SessionLocal() as db:
                        market_id = int(input("ID рынка: "))
                        username = input("Username: ")
                        rating = int(input("Оценка (1–5): "))
                        text = input("Текст отзыва (можно оставить пустым): ")
                        review = add_review(db, market_id, username, rating, text)
                        print(f"✅ Отзыв добавлен (ID: {review.id})")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            case "6":
                try:
                    with SessionLocal() as db:
                        review_id = int(input("Введите ID отзыва для удаления: "))
                        delete_review(db, review_id)
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            case "0":
                print("👋 До свидания!")
                break

            case _:
                print("❗️ Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()