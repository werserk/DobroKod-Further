class CharityInformation:
    def __init__(self, info_type, file, name):
        self.info_type = info_type  # текстовое название типа информации
        self.file = file  # файл
        self.name = name  # название

    def __str__(self):
        return f"Information(type={self.info_type}, file={self.file}, name={self.name})"


CHARITY_ANSWERS = {
    "как сохранить здоровье груди": CharityInformation(
        "document", "../data/Posobie_2021_33_page_WEB_020221 (2).pdf", None
    ),
    "как узнать свой риск": CharityInformation(
        "link", None, "https://www.dalshefond.ru/check/"
    ),
    "как рак груди лечится": CharityInformation(
        "link", None, "https://vmesteplus.ru/distance-programs/oncologist-course/"
    ),
    "навигатор для пациента": CharityInformation(
        "link", None, "https://vmesteplus.ru/first-hand/articles/rak-grudi-putevoditel/"
    ),
    "соедините меня с сотрудником фонда": CharityInformation(
        "link", None, "почта info@dalshefond.ru, тел. 8-800-707-44-03"
    ),
    "подозрение на рак": CharityInformation(
        "link", None, "https://vmesteplus.ru/personal/personalized-help/oncologist/"
    ),
    # 'Оцените работу Фонда по шкале от 1 до 10',
    # 'Как попасть к онкологу',
    # 'Где пройти обследования',
    # 'Где получить лечение',
    # 'Где пройти реабилитацию',
    # 'Где пройти контрольные обследования',
    "консультация психолога": CharityInformation(
        "link",
        None,
        "Зарегистрируйтесь на сайте https://vmesteplus.ru/ , "
        + "выберите в личном кабинете раздел Получить индивидуальную помощь, "
        + "а затем выберите консультацию",
    ),
    "консультация онколога": CharityInformation(
        "link",
        None,
        "Зарегистрируйтесь на сайте https://vmesteplus.ru/ , "
        + "выберите в личном кабинете раздел Получить индивидуальную помощь, "
        + "а затем выберите консультацию",
    ),
    "консультация медицинского юриста": CharityInformation(
        "link",
        None,
        "Зарегистрируйтесь на сайте https://vmesteplus.ru/ , "
        + "выберите в личном кабинете раздел Получить индивидуальную помощь, "
        + "а затем выберите консультацию",
    ),
    "бесплатное такси к месту лечения": CharityInformation(
        "link", None, "https://vmesteplus.ru/support/how/targeted-assistance/"
    ),
    "скачать пособие для пациентов": CharityInformation(
        "document", "../data/Posobie_final (3).pdf", None
    ),
    "группы поддержки": CharityInformation(
        "link", None, "https://vmesteplus.ru/support/support-groups/"
    ),
    "психологические тренинги": CharityInformation(
        "link", None, "https://vmesteplus.ru/support/online-classes/"
    ),
    "написать руководителю": CharityInformation(
        "link", None, "Директор фонда Оксана Молдованова moldovanova@dalshefond.ru"
    ),
    "юридическое лицо": CharityInformation(
        "link", None, "https://dalshefond.ru/donate/"
    ),
    "частное лицо": CharityInformation("link", None, "https://dalshefond.ru/donate/"),
    "отправить ссылку другу или в соц. сети": CharityInformation(
        "link", None, "https://vmesteplus.ru"
    ),
    "сделать пожертвование": CharityInformation(
        "link", None, "https://dalshefond.ru/donate/"
    ),
    "связаться с руководителем": CharityInformation(
        "link", None, "Директор фонда Оксана Молдованова moldovanova@dalshefond.ru"
    ),
}
