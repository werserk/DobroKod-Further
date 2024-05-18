class Charity_Information:
    def __init__(self, info_type, file, name):
        self.info_type = info_type  # текстовое название типа информации
        self.file = file  # файл
        self.name = name  # название

    def __str__(self):
        return f"Information(type={self.info_type}, file={self.file}, name={self.name})"

CHARITY_ANSWERS = {
    'как сохранить здоровье груди': Charity_Information('..\document', 'data/Posobie_2021_33_page_WEB_020221 (2).pdf', None),
    'как узнать свой риск': Charity_Information('link', None, 'https://www.dalshefond.ru/check/'),
    'как рак груди лечится':Charity_Information('link', None, 'https://vmesteplus.ru/distance-programs/oncologist-course/'),
    'навигатор для пациента': Charity_Information('link', None, 'https://vmesteplus.ru/first-hand/articles/rak-grudi-putevoditel/'),
    'соедините меня с сотрудником фонда' : Charity_Information('link', None, 'почта info@dalshefond.ru, тел. 8-800-707-44-03'),
    'подозрение на рак' : Charity_Information('link', None, 'https://vmesteplus.ru/personal/personalized-help/oncologist/'),

    #'Вопрос онкологу' ,
    # 'Вопрос лимфологу',
    # 'Вопрос эндокринологу',
    # 'Вопрос диетологу',
    # 'Вопрос дерматологу',

    # 'Хочу поделиться своим опытом',
    # 'Хочу оставить отзыв',
    # 'Оцените работу Фонда по шкале от 1 до 10',
    # 'Помочь по-другому',

    # 'Как попасть к онкологу',
    # 'Где пройти обследования',
    # 'Где получить лечение',
    # 'Где пройти реабилитацию',
    # 'Где пройти контрольные обследования',

     'консультация психолога' : Charity_Information('link', None, 'Зарегистрируйтесь на сайте https://vmesteplus.ru/ , ' +
                                                                  'выберите в личном кабинете раздел Получить индивидуальную помощь, ' +
                                                                  'а затем выберите консультацию'),
     'консультация онколога' : Charity_Information('link', None, 'Зарегистрируйтесь на сайте https://vmesteplus.ru/ , ' +
                                                                  'выберите в личном кабинете раздел Получить индивидуальную помощь, ' +
                                                                  'а затем выберите консультацию'),
     'консультация медицинского юриста' : Charity_Information('link', None, 'Зарегистрируйтесь на сайте https://vmesteplus.ru/ , ' +
                                                                  'выберите в личном кабинете раздел Получить индивидуальную помощь, ' +
                                                                  'а затем выберите консультацию'),

     'бесплатное такси к месту лечения' : Charity_Information('link', None, 'https://vmesteplus.ru/support/how/targeted-assistance/'),
     'скачать пособие для пациентов' : Charity_Information('document', '..\data/Posobie_final (3).pdf', None),
     'группы поддержки': Charity_Information('link', None, 'https://vmesteplus.ru/support/support-groups/'),
    'психологические тренинги' : Charity_Information('link', None, 'https://vmesteplus.ru/support/online-classes/'),
    'написать руководителю' : Charity_Information('link', None, 'Директор фонда Оксана Молдованова moldovanova@dalshefond.ru'),
    'юридическое лицо' : Charity_Information('link', None, 'https://dalshefond.ru/donate/'),
    'частное лицо' : Charity_Information('link', None, 'https://dalshefond.ru/donate/'),
     'отправить ссылку другу или в соц. сети' : Charity_Information('link', None, 'https://vmesteplus.ru'),
     'сделать пожертвование' : Charity_Information('link', None, 'https://dalshefond.ru/donate/'),
    'связаться с руководителем' : Charity_Information('link', None, 'Директор фонда Оксана Молдованова moldovanova@dalshefond.ru'),
}
