def clear_phone(phone: str):
    """
    Очищаем телефон от посторонних символов.
    """
    new_phone = filter(str.isdigit, phone)
    return "".join(new_phone)
