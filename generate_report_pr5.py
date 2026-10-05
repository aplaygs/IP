"""Генератор официального отчета по Практической работе № 5 (ПР5) в формате ГОСТ.

Студент: Мишуков Владислав Романович
Группа: ЭФБО-11-24
Преподаватель: Ящун Татьяна Викторовна
Тема 433: Сервис регистрации продавцов на ярмарку (FairVendor)
"""

import os
import pymupdf
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

LOGO_PATH = os.path.join(os.path.dirname(__file__), "mirea_logo.jpg")


class GostNumberedCanvas(canvas.Canvas):
    """Холст с ГОСТ-нумерацией (титул без номера, со 2-й страницы по центру)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times", 11)
        self.setFillColor(colors.black)
        self.drawCentredString(A4[0] / 2.0, 12 * mm, str(self._pageNumber))
        self.restoreState()


def create_gost_report_pr5(output_pdf_path: str):
    """Создает официальный отчет по ПР5 строго по требованиям ГОСТ 7.32."""
    font_dir = "/System/Library/Fonts/Supplemental"
    pdfmetrics.registerFont(
        TTFont("Times", os.path.join(font_dir, "Times New Roman.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("Times-Bold", os.path.join(font_dir, "Times New Roman Bold.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont(
            "Times-Italic", os.path.join(font_dir, "Times New Roman Italic.ttf")
        )
    )
    pdfmetrics.registerFont(
        TTFont(
            "Times-BoldItalic",
            os.path.join(font_dir, "Times New Roman Bold Italic.ttf"),
        )
    )

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=30 * mm,
        rightMargin=15 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    style_univ = ParagraphStyle(
        "UnivTitle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_univ_bold = ParagraphStyle(
        "UnivTitleBold",
        parent=style_univ,
        fontName="Times-Bold",
        fontSize=10.5,
        leading=13.5,
    )

    style_doc_title = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=15,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_doc_subtitle = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_theme = ParagraphStyle(
        "ThemeStyle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_sign = ParagraphStyle(
        "SignStyle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=11,
        leading=14,
        textColor=colors.black,
    )

    style_sign_sub = ParagraphStyle(
        "SignSubStyle",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=8.5,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_h1 = ParagraphStyle(
        "GostH1",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=12.5,
        leading=15.5,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )

    style_body = ParagraphStyle(
        "GostBody",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=10,
        leading=13.5,
        alignment=TA_JUSTIFY,
        firstLineIndent=12.5 * mm,
        textColor=colors.black,
        spaceAfter=2,
    )

    style_bullet = ParagraphStyle(
        "GostBullet",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=10,
        leading=13.2,
        alignment=TA_JUSTIFY,
        leftIndent=10 * mm,
        firstLineIndent=-5 * mm,
        textColor=colors.black,
        spaceAfter=2,
    )

    style_table_text = ParagraphStyle(
        "TableText",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=9.5,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    style_table_header = ParagraphStyle(
        "TableHeader",
        parent=style_table_text,
        fontName="Times-Bold",
        alignment=TA_CENTER,
    )

    style_center = ParagraphStyle(
        "GostCenter",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    story = []

    # =========================================================================
    # СТРАНИЦА 1: ТИТУЛЬНЫЙ ЛИСТ (С ГЕРБОМ РТУ МИРЭА)
    # =========================================================================
    if os.path.exists(LOGO_PATH):
        logo_img = Image(LOGO_PATH, width=24 * mm, height=27.2 * mm)
        logo_img.hAlign = "CENTER"
        story.append(logo_img)
        story.append(Spacer(1, 2.5 * mm))

    story.append(Paragraph("МИНОБРНАУКИ РОССИИ", style_univ))
    story.append(
        Paragraph(
            "Федеральное государственное бюджетное образовательное учреждение<br/>"
            "высшего образования<br/>"
            "<b>«МИРЭА – Российский технологический университет»</b>",
            style_univ,
        )
    )
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("РТУ МИРЭА", style_univ_bold))
    story.append(Spacer(1, 2 * mm))

    story.append(
        HRFlowable(
            width="100%", thickness=2, color=colors.black, spaceAfter=18 * mm
        )
    )

    story.append(Paragraph("Практическая работа № 5", style_doc_title))
    story.append(Spacer(1, 2.5 * mm))
    story.append(
        Paragraph(
            "по дисциплине «Технологии разработки приложений на базе фреймворков»",
            style_doc_subtitle,
        )
    )
    story.append(Spacer(1, 6 * mm))

    story.append(
        Paragraph(
            "<b>Тема работы:</b> Django, HTTP и основы веб-разработки",
            style_theme,
        )
    )
    story.append(Spacer(1, 28 * mm))

    sign_table_data = [
        [
            Paragraph("Выполнил:", style_sign),
            Paragraph("студент группы ЭФБО-11-24", style_sign),
            Paragraph("", style_sign),
            Paragraph("Мишуков В.Р.", style_sign),
        ],
        [
            Paragraph("", style_sign_sub),
            Paragraph("(группа)", style_sign_sub),
            Paragraph("(подпись)", style_sign_sub),
            Paragraph("(Фамилия И.О.)", style_sign_sub),
        ],
        [
            Paragraph("", style_sign),
            Paragraph("", style_sign),
            Paragraph("", style_sign),
            Paragraph("", style_sign),
        ],
        [
            Paragraph("Принял:", style_sign),
            Paragraph("доц.", style_sign),
            Paragraph("", style_sign),
            Paragraph("Ящун Т.В.", style_sign),
        ],
        [
            Paragraph("", style_sign_sub),
            Paragraph("(должность)", style_sign_sub),
            Paragraph("(подпись)", style_sign_sub),
            Paragraph("(Фамилия И.О.)", style_sign_sub),
        ],
    ]

    t_sign = Table(
        sign_table_data,
        colWidths=[24 * mm, 62 * mm, 32 * mm, 47 * mm],
    )
    t_sign.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ("LINEBELOW", (2, 0), (2, 0), 0.75, colors.black),
                ("LINEBELOW", (2, 3), (2, 3), 0.75, colors.black),
            ]
        )
    )
    story.append(t_sign)

    story.append(Spacer(1, 24 * mm))
    story.append(Paragraph("Москва", style_center))
    story.append(Paragraph("2026", style_center))

    # =========================================================================
    # СТРАНИЦА 2: РАЗДЕЛЫ 1, 2 И 3 (ОБЩИЕ СВЕДЕНИЯ, КУРС, ДОРАБОТКА ПРОЕКТА)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("1. Общие сведения", style_h1))
    story.append(
        Paragraph(
            "• <b>Название работы:</b> Практическая работа № 5 «Django, HTTP и основы веб-разработки».",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>ФИО студента:</b> Мишуков Владислав Романович.",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>Учебная группа:</b> ЭФБО-11-24.",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>Название индивидуального проекта:</b> Сервис регистрации продавцов на ярмарку (FairVendor), вариант темы № 433.",
            style_bullet,
        )
    )

    story.append(
        Paragraph("2. Выполненные материалы Яндекс Практикума", style_h1)
    )
    yp_table_data = [
        [
            Paragraph("Раздел курса", style_table_header),
            Paragraph("Выполненная тема", style_table_header),
        ],
        [
            Paragraph(
                "Раздел 04. «Основы веб-разработки»", style_table_text
            ),
            Paragraph(
                "«Создание проекта», «Пути и view-функции», «Вёрстка для бэкендера»",
                style_table_text,
            ),
        ],
    ]
    t_yp = Table(yp_table_data, colWidths=[65 * mm, 100 * mm])
    t_yp.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.93, 0.93, 0.93)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(t_yp)
    story.append(Spacer(1, 2 * mm))

    story.append(
        Paragraph("3. Доработка индивидуального проекта", style_h1)
    )
    story.append(
        Paragraph(
            "• <b>Название проекта:</b> Сервис регистрации продавцов на ярмарку (FairVendor).",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>Созданный Django-проект:</b> <code>fairvendor</code> (корневой файл <code>manage.py</code>, "
            "пакет конфигурации <code>fairvendor/</code>: <code>settings.py</code>, <code>urls.py</code>, "
            "<code>wsgi.py</code>, <code>asgi.py</code>). Настроены параметры локализации: <code>LANGUAGE_CODE = 'ru-RU'</code>, "
            "<code>TIME_ZONE = 'Europe/Moscow'</code>, <code>USE_TZ = True</code>.",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>Созданные Django-приложения:</b><br/>"
            "&nbsp;&nbsp;1. <code>homepage</code> — точка входа в проект, базовый HTML-каркас <code>page()</code>, главная страница и обработчик 404;<br/>"
            "&nbsp;&nbsp;2. <code>fairs</code> — работа с ярмарочными площадками (сущность <code>Fair</code> из ПР3);<br/>"
            "&nbsp;&nbsp;3. <code>applications</code> — работа с заявками участников (сущность <code>Application</code> из ПР3).",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>Реализованные URL и страницы веб-интерфейса:</b>",
            style_bullet,
        )
    )

    url_table_data = [
        [
            Paragraph("URL", style_table_header),
            Paragraph("View-функция", style_table_header),
            Paragraph("Назначение страницы", style_table_header),
        ],
        [
            Paragraph("<code>/</code>", style_table_text),
            Paragraph("<code>homepage.views.index</code>", style_table_text),
            Paragraph("Главная страница: описание сервиса, навигационные кнопки", style_table_text),
        ],
        [
            Paragraph("<code>/fairs/</code>", style_table_text),
            Paragraph("<code>fairs.views.fairs</code>", style_table_text),
            Paragraph("Реестр ярмарок из <code>data/fairs.json</code> (список Bootstrap)", style_table_text),
        ],
        [
            Paragraph("<code>/fairs/&lt;int:fair_id&gt;/</code>", style_table_text),
            Paragraph("<code>fairs.views.fair_detail</code>", style_table_text),
            Paragraph("Карточка ярмарки, лимит площади, статус доступности мест", style_table_text),
        ],
        [
            Paragraph("<code>/applications/</code>", style_table_text),
            Paragraph("<code>applications.views.applications</code>", style_table_text),
            Paragraph("Реестр заявок участников из <code>data/applications.json</code>", style_table_text),
        ],
        [
            Paragraph("<code>/applications/&lt;int:application_id&gt;/</code>", style_table_text),
            Paragraph("<code>applications.views.application_detail</code>", style_table_text),
            Paragraph("Карточка заявки, продавец, ставка, сбор, статус-бейдж", style_table_text),
        ],
    ]
    t_url = Table(url_table_data, colWidths=[38 * mm, 52 * mm, 75 * mm])
    t_url.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.93, 0.93, 0.93)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(t_url)
    story.append(Spacer(1, 2 * mm))

    story.append(
        Paragraph(
            "• <b>Краткое описание выполненной работы:</b> выполнена интеграция фреймворка Django 5.2 в репозиторий проекта "
            "с сохранением полной работоспособности объектной модели ПР3 (классы <code>Fair</code>, <code>Vendor</code>, <code>Application</code>) "
            "и консольного интерфейса (<code>main.py</code>). Настроена двухуровневая маршрутизация с функцией <code>include()</code> и конвертерами "
            "путей <code>&lt;int:fair_id&gt;</code>, <code>&lt;int:application_id&gt;</code>. В модуль <code>models/applications.py</code> "
            "добавлена функция <code>find_application_by_id()</code>. Реализован единый каркас <code>page()</code> с адаптивным дизайном Bootstrap 5.3 CDN. "
            "Настроен кастомный обработчик <code>handler404 = 'homepage.views.page_not_found'</code>, возвращающий стилизованную страницу ошибки 404.",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>Ссылка на Git-репозиторий:</b> https://github.com/aplaygs/IP.git",
            style_bullet,
        )
    )

    # =========================================================================
    # СТРАНИЦА 3: РАЗДЕЛ 4 (РЕЗУЛЬТАТ РАБОТЫ) И РАЗДЕЛ 5 (ВЫВОД)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("4. Результат работы", style_h1))
    story.append(
        Paragraph(
            "В результате выполнения практической работы № 5 (ПР5):",
            style_body,
        )
    )

    story.append(
        Paragraph(
            "• <b>созданы три Django-приложения:</b> <code>homepage</code> (главная страница и глобальный обработчик 404), "
            "<code>fairs</code> (каталог ярмарок и расчет доступности торговых мест) и <code>applications</code> "
            "(реестр заявок участников); все приложения зарегистрированы в <code>INSTALLED_APPS</code> проекта <code>fairvendor</code>;",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>настроена двухуровневая маршрутизация URL:</b> корневой конфигурационный файл <code>fairvendor/urls.py</code> "
            "делегирует обработку путей приложениям с помощью <code>include()</code>, а приложения содержат собственные локальные файлы <code>urls.py</code> "
            "с типизированными конвертерами <code>&lt;int:fair_id&gt;</code> и <code>&lt;int:application_id&gt;</code>;",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>реализованы view-функции:</b> <code>index()</code>, <code>fairs()</code>, <code>fair_detail()</code>, "
            "<code>applications()</code>, <code>application_detail()</code> и <code>page_not_found()</code>, формирующие корректные HTTP-ответы "
            "<code>HttpResponse</code> с кодами статусов 200 OK и 404 Not Found;",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>создан адаптивный веб-интерфейс:</b> реализована вспомогательная функция <code>page()</code>, формирующая валидный HTML5-документ "
            "с метатегом <code>viewport</code>, верхней навигационной панелью и подключением стилей фреймворка Bootstrap 5.3 через CDN;",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>реализованы основные страницы проекта:</b> главная витрина сервиса, интерактивный список ярмарок, детальная карточка ярмарки "
            "с расчетом остатка свободной площади (<code>is_space_available()</code>), реестр заявок участников и карточка бронирования со связанными объектами;",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>настроена навигация между страницами:</b> все веб-страницы связаны сквозными ссылками навигации и кнопками быстрого возврата "
            "(«← к списку ярмарок», «← к списку заявок», «На главную»);",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>использованы компоненты Bootstrap 5.3:</b> контейнеры <code>container</code>, списки <code>list-group</code>, "
            "карточки <code>card</code>, кнопки <code>btn-primary</code>/<code>btn-secondary</code>, цветные бейджи статусов "
            "<code>bg-success</code> (активно/доступно), <code>bg-secondary</code> (отменено) и <code>bg-danger</code> (мест нет);",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>сохранена предметная область индивидуального проекта:</b> веб-слой использует классы предметной модели ПР3 "
            "(<code>Fair</code>, <code>Vendor</code>, <code>Application</code>) и функции загрузки данных JSON из <code>storage.py</code>; "
            "консольная версия <code>main.py</code> и автоматизированные тесты продолжают успешно функционировать;",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>разработан и выполнен комплекс автоматизированных тестов:</b> создан тестовый модуль <code>tests/test_views.py</code>, "
            "проверяющий все маршруты (200 и 404), структуру HTML и обработку несуществующих ресурсов. "
            "Все 42 теста в проекте успешно пройдены;",
            style_bullet,
        )
    )
    story.append(
        Paragraph(
            "• <b>обеспечено качество кода:</b> выполнена проверка линтером <code>flake8</code>, проект на 100% соответствует требованиям PEP 8 (0 замечаний); "
            "обновлена документация <code>README.md</code> и сформированы коммиты Git с префиксом <code>PR5:</code>.",
            style_bullet,
        )
    )

    story.append(Paragraph("5. Вывод", style_h1))
    story.append(
        Paragraph(
            "В ходе выполнения практической работы № 5 были всесторонне изучены архитектура и базовые механизмы веб-фреймворка Django 5.2, "
            "стандарт взаимодействия HTTP по циклу «запрос – ответ» (Request – Response), принципы двухуровневой маршрутизации URL с "
            "использованием конвертеров параметров пути, а также основы адаптивной верстки веб-интерфейсов с применением HTML5, CSS и фреймворка Bootstrap 5.3. "
            "Консольный проект «Сервис регистрации продавцов на ярмарку (FairVendor)» был успешно переведен на начальный этап веб-разработки: "
            "создан Django-проект, выделены три специализированных Django-приложения, разработаны обработчики запросов (view-функции), обеспечивающие "
            "динамическое формирование страниц на основе существующей объектной модели и JSON-хранилища. Реализована обработка ошибок 404 со стилизованным интерфейсом. "
            "Комплекс тестов из 42 проверок подтвердил надежность архитектуры и готовность проекта к переходу на Django ORM, шаблоны и веб-формы на последующих этапах.",
            style_body,
        )
    )

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Москва", style_center))
    story.append(Paragraph("2026", style_center))

    doc.build(story, canvasmaker=GostNumberedCanvas)
    print(
        f"Итоговый отчет по ГОСТ (ПР5) успешно сгенерирован: {output_pdf_path}"
    )


def verify_pdf_pages(pdf_path: str):
    """Проверяет точное количество страниц в сгенерированном PDF-документе."""
    doc = pymupdf.open(pdf_path)
    page_count = len(doc)
    print(f"Проверка PDF: файл '{pdf_path}' содержит {page_count} страниц.")
    return page_count


if __name__ == "__main__":
    pdf_filename = "Отчет_Практическая_работа_5_Мишуков_В_Р.pdf"
    create_gost_report_pr5(pdf_filename)
    pages = verify_pdf_pages(pdf_filename)
    if pages != 3:
        print(f"ВНИМАНИЕ: Ожидалось ровно 3 страницы, получено: {pages}")
    else:
        print("УСПЕХ: Отчет строго соответствует стандарту (ровно 3 страницы)!")
