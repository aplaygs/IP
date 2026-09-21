"""Генератор официального отчета по Практической работе № 3 (ПР3) в формате ГОСТ.

Студент: Мишуков Владислав Романович
Группа: ЭФБО-11-24
Преподаватель: Ящун Татьяна Викторовна
Тема 433: Сервис регистрации продавцов на ярмарку (FairVendor)
"""

import base64
import io
import os
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

from generate_report import MIREA_LOGO_B64


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
        # Номер страницы по центру внизу листа по ГОСТ 7.32
        self.drawCentredString(A4[0] / 2.0, 12 * mm, str(self._pageNumber))
        self.restoreState()


def create_gost_report_pr3(output_pdf_path: str):
    # Регистрация шрифтов Times New Roman
    font_dir = "/System/Library/Fonts/Supplemental"
    pdfmetrics.registerFont(
        TTFont("Times", os.path.join(font_dir, "Times New Roman.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("Times-Bold", os.path.join(font_dir, "Times New Roman Bold.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("Times-Italic",
               os.path.join(font_dir, "Times New Roman Italic.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("Times-BoldItalic",
               os.path.join(font_dir, "Times New Roman Bold Italic.ttf"))
    )

    # Поля страницы по ГОСТ 7.32: левое 30 мм, правое 15 мм, верх/низ 20 мм
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=30 * mm,
        rightMargin=15 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    # Стили по ГОСТ (строго черный цвет, гарнитура Times New Roman)
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
        fontSize=13,
        leading=16.5,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    style_body = ParagraphStyle(
        "GostBody",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=10.5,
        leading=14,
        alignment=TA_JUSTIFY,
        firstLineIndent=12.5 * mm,
        textColor=colors.black,
        spaceAfter=2,
    )

    style_bullet = ParagraphStyle(
        "GostBullet",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=10.5,
        leading=13.8,
        alignment=TA_JUSTIFY,
        leftIndent=12.5 * mm,
        firstLineIndent=-6 * mm,
        textColor=colors.black,
        spaceAfter=2,
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
    logo_bytes = base64.b64decode(MIREA_LOGO_B64)
    logo_img = Image(io.BytesIO(logo_bytes), width=24 * mm, height=27.2 * mm)
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

    # Горизонтальная разделительная черта по ширине листа
    story.append(
        HRFlowable(
            width="100%", thickness=2, color=colors.black, spaceAfter=18 * mm
        )
    )

    # Название практической работы
    story.append(Paragraph("Практическая работа № 3", style_doc_title))
    story.append(Spacer(1, 2.5 * mm))
    story.append(
        Paragraph(
            "по дисциплине «Технологии разработки приложений на базе фреймворков»",
            style_doc_subtitle,
        )
    )
    story.append(Spacer(1, 7 * mm))

    # Тема работы строго по методическим указаниям ПР3
    story.append(
        Paragraph(
            "<b>Тема работы:</b> Объектно-ориентированное программирование на Python",
            style_theme,
        )
    )
    story.append(Spacer(1, 28 * mm))

    # Блок подписей (таблица)
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
    # СТРАНИЦА 2: РАЗДЕЛ 1 (ИНДИВИДУАЛЬНЫЙ ПРОЕКТ)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("1. Индивидуальный проект", style_h1))

    story.append(
        Paragraph(
            "• <b>Название проекта:</b> Сервис регистрации продавцов на ярмарку (FairVendor), тема № 433.",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• <b>Перечень классов и функционала, реализованных на этапе ПР3 (ООП):</b><br/>"
            "&nbsp;&nbsp;1. <code>models/fairs.py</code> (класс <code>Fair</code>): представление ярмарочного мероприятия. "
            "Атрибуты: <code>id</code>, <code>name</code>, <code>location</code>, <code>date</code>, <code>base_rate</code>, <code>total_space</code>. "
            "Методы: <code>is_space_available()</code> (проверка вместимости стенда), <code>get_free_space()</code> (расчет остатка площади), "
            "<code>__str__()</code>, <code>to_dict()</code>, <code>from_dict()</code>, а также функция поиска <code>find_fair_by_id()</code>;<br/>"
            "&nbsp;&nbsp;2. <code>models/vendors.py</code> (иерархия классов продавцов): базовый класс <code>Vendor</code> "
            "с инкапсулированной валидацией реквизитов (ID, наименование, 10/12-значный ИНН, документы, стаж). "
            "Специализированные подклассы с полиморфным переопределением тарифного коэффициента <code>get_category_coefficient()</code> "
            "и строкового вывода: <code>CraftVendor</code> (льготный тариф 1.0), <code>FoodVendor</code> (повышенный тариф 1.3), "
            "<code>SouvenirVendor</code> (тариф 1.1). Фабричный метод <code>Vendor.from_dict()</code>, генератор <code>filter_vendors_by_category()</code>, "
            "сортировка через <code>lambda</code> в <code>sort_vendors()</code>;<br/>"
            "&nbsp;&nbsp;3. <code>models/applications.py</code> (класс <code>Application</code>): связывает продавца и мероприятие "
            "через прямые объектные ссылки: <code>app.vendor: Vendor</code> и <code>app.fair: Fair</code>. Атрибуты: <code>requested_space</code>, "
            "<code>fee</code>, <code>status</code>, <code>is_cancelled</code>. Методы: <code>calculate_fee()</code> (вычисление стоимости "
            "на основе базовой ставки ярмарки, площади и полиморфного коэффициента продавца со скидкой 15% новичкам), "
            "<code>cancel()</code> (инкапсулированный отзыв брони), <code>generate_card()</code> (официальная карточка), "
            "<code>get_occupied_space()</code>, <code>create_application()</code>, <code>calculate_fair_statistics()</code>;<br/>"
            "&nbsp;&nbsp;4. <code>storage.py</code>: объектная сериализация/десериализация JSON (<code>load_fairs</code>, <code>save_fairs</code>, "
            "<code>load_vendors</code>, <code>save_vendors</code>, <code>load_applications</code>, <code>save_applications</code>) "
            "с автоматическим восстановлением связей объектов по идентификаторам и обработкой исключений;<br/>"
            "&nbsp;&nbsp;5. <code>main.py</code>: консольный интерфейс на 10 пунктов меню и автоматический демонстрационный сценарий (<code>--demo</code>).",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• <b>Структура модулей проекта:</b> архитектура реорганизована в модульный пакет <code>models/</code>:<br/>"
            "&nbsp;&nbsp;— <code>models/__init__.py</code> — централизованный экспорт доменных моделей (<code>Fair</code>, <code>Vendor</code>, <code>Application</code>);<br/>"
            "&nbsp;&nbsp;— <code>models/fairs.py</code> — доменная модель ярмарочных площадок;<br/>"
            "&nbsp;&nbsp;— <code>models/vendors.py</code> — иерархия классов продавцов с полиморфизмом тарифов;<br/>"
            "&nbsp;&nbsp;— <code>models/applications.py</code> — объектная модель заявок и аналитика площадки;<br/>"
            "&nbsp;&nbsp;— <code>storage.py</code> — персистентное JSON-хранилище со связыванием объектов;<br/>"
            "&nbsp;&nbsp;— <code>main.py</code>, <code>fairs.py</code>, <code>vendors.py</code>, <code>applications.py</code>, <code>utils.py</code> — "
            "интерфейсный слой и слой обратной совместимости;<br/>"
            "&nbsp;&nbsp;— <code>data/</code> — каталог с файлами постоянного хранения (<code>fairs.json</code>, <code>vendors.json</code>, <code>applications.json</code>);<br/>"
            "&nbsp;&nbsp;— <code>tests/</code> — каталог модульных тестов (<code>test_fairs.py</code>, <code>test_vendors.py</code>, <code>test_applications.py</code>).",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• <b>Формат хранения данных:</b> персистентное хранение организовано в формате JSON в каталоге <code>data/</code>. "
            "В файлах сохраняются нормализованные идентификаторы (<code>vendor_id</code>, <code>fair_id</code>), "
            "а при загрузке функция <code>load_applications()</code> автоматически восстанавливает объектную модель, "
            "связывая каждую заявку с соответствующими объектами <code>Vendor</code> и <code>Fair</code>.",
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
    # СТРАНИЦА 3: РАЗДЕЛ 2 (РЕЗУЛЬТАТ РАБОТЫ) И РАЗДЕЛ 3 (ВЫВОД)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("2. Результат работы", style_h1))
    story.append(
        Paragraph(
            "В результате выполнения практической работы № 3 (ПР3):",
            style_body,
        )
    )

    story.append(
        Paragraph(
            "• осуществлен переход от процедурно-коллекционной модели (ПР2) к полноценной объектно-ориентированной архитектуре (ООП): "
            "создан доменный пакет <code>models/</code> с классами <code>Fair</code>, <code>Vendor</code>, <code>Application</code>;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• реализован принцип инкапсуляции: валидация реквизитов участников, площадей и ставок вынесена в конструкторы <code>__init__</code>, "
            "а управление состоянием заявки реализовано через защищенные методы (<code>app.cancel()</code>);",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• построена иерархия наследования: от базового класса <code>Vendor</code> унаследованы специализированные классы "
            "<code>CraftVendor</code>, <code>FoodVendor</code> и <code>SouvenirVendor</code>;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• продемонстрирован динамический полиморфизм: каждый подкласс переопределяет метод <code>get_category_coefficient()</code> "
            "(ставки 1.0, 1.3, 1.1) и строковое представление <code>__str__()</code>, обеспечивая расчет сборов без ветвлений <code>if/elif</code>;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• реализована объектная ассоциация в классе <code>Application</code>, хранящем прямые ссылки на объекты "
            "<code>vendor: Vendor</code> и <code>fair: Fair</code>, что обеспечивает прозрачный доступ к свойствам связанных сущностей;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• разработан механизм сериализации и десериализации (<code>to_dict()</code>, <code>from_dict()</code>) "
            "с сохранением связей в JSON и автоматическим связыванием объектов при загрузке в <code>storage.py</code>;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• обеспечена полная обратная совместимость через методы <code>__getitem__</code> и <code>__contains__</code>, "
            "позволяющая бесшовно использовать существующие алгоритмы и тесты;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• реализован комплекс автоматизированных тестов <code>pytest</code> в каталоге <code>tests/</code> "
            "(модули <code>test_fairs.py</code>, <code>test_vendors.py</code>, <code>test_applications.py</code>, <code>test_main.py</code>) — "
            "все 33 теста успешно пройдены;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• код проверен линтером <code>flake8</code>: строгое соблюдение PEP 8 (длина строк, структура импортов, форматирование), 0 замечаний;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• обновлена документация <code>README.md</code>, зафиксирован единый итоговый коммит «Практика 3» в репозитории GitHub.",
            style_bullet,
        )
    )

    story.append(Paragraph("3. Вывод", style_h1))
    story.append(
        Paragraph(
            "В ходе выполнения практической работы № 3 были глубоко изучены и успешно применены на практике ключевые концепции "
            "объектно-ориентированного программирования на языке Python: классы, объекты, инкапсуляция, наследование, динамический полиморфизм "
            "и ассоциация сущностей. Проект «Сервис регистрации продавцов на ярмарку» был успешно переведен с функциональной парадигмы на "
            "профессиональную объектную архитектуру. Выделение доменных моделей <code>Fair</code>, <code>Vendor</code> и <code>Application</code> "
            "существенно повысило модульность, расширяемость и сопровождаемость системы, исключило дублирование логики и обеспечило строгое "
            "соблюдение бизнес-правил. Созданный автоматизированный тестовый набор из 33 тестов и безупречное соответствие PEP 8 подтверждают высокое качество "
            "реализации и готовность проекта к интеграции с веб-фреймворком Django на следующем этапе (ПР4).",
            style_body,
        )
    )

    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Москва", style_center))
    story.append(Paragraph("2026", style_center))

    doc.build(story, canvasmaker=GostNumberedCanvas)
    print(
        f"Итоговый отчет по ГОСТ (ПР3) успешно сгенерирован: {output_pdf_path}"
    )


if __name__ == "__main__":
    pdf_filename = "Отчет_Практическая_работа_3_Мишуков_В_Р.pdf"
    create_gost_report_pr3(pdf_filename)
