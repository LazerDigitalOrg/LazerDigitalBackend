from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from database.models import *
from database.database import async_session
from src.dependencies import get_async_session


async def generate_date():
    session = async_session()
    try:
        categories = [
            Category(title="Приборы полного вращения",
                     category_slug="0-moving-heads",
                     hint="Martin, Clay Paky, High End Systems и др.",
                     photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340/cat1.png",
                     description=f"""Прокатный парк компании Лазер-Кинетикс имеет огромное количество интеллектуальных световых приборов полного вращения. Приборы этого типа как правило составляют основное количество всего светового оборудования на мероприятиях. Световые приборы полного вращения позволяют реализовывать динамические красочные проекты и предоставляют неограниченные возможности художникам для создания оригинальных и неповторимых световых шоу.В эту категорию светового оборудования входят самые разные приборы:LED-приборы, такие как Mac 301, Mac Aura, A7; Приборы заливного света, такие как Vari Lite и Mac 2000 Wash Приборы рисующего света, такие как Showgun, Mac III Profile, Mac Viper Profile Световые приборы полного вращения каждого подтипа решают определенные задачи при создании световых проектов, а в совокупности они полностью закрывают все базовые потребности в световом оформлении. У нашей компании более 1000 единиц световых приборов полного вращения и мы можем одновременно работать как с крупными проектами так и с небольшими. Наш опыт работы на самых разных площадках позволяет предложить наиболее полные комплекты светового оборудования за лучшую цену."""),
            Category(title="Приборы заливного света1",
                     category_slug="1-fill-light",

                     hint="Thomas Chomolech и др.",
                     photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340/cat2.png",
                     description=f"""Прокатный парк компании Лазер-Кинетикс имеет огромное количество интеллектуальных световых приборов полного вращения. Приборы этого типа как правило составляют основное количество всего светового оборудования на мероприятиях. Световые приборы полного вращения позволяют реализовывать динамические красочные проекты и предоставляют неограниченные возможности художникам для создания оригинальных и неповторимых световых шоу. В эту категорию светового оборудования входят самые разные приборы: LED-приборы, такие как Mac 301, Mac Aura, A7; Приборы заливного света, такие как Vari Lite и Mac 2000 Wash Приборы рисующего света, такие как Showgun, Mac III Profile, Mac Viper Profile Световые приборы полного вращения каждого подтипа решают определенные задачи при создании световых проектов, а в совокупности они полностью закрывают все базовые потребности в световом оформлении. У нашей компании более 1000 единиц световых приборов полного вращения и мы можем одновременно работать как с крупными проектами так и с небольшими. Наш опыт работы на самых разных площадках позволяет предложить наиболее полные комплекты светового оборудования за лучшую цену."""),
            Category(title="Световые пульты",
                     category_slug="2-consoles",

                     hint="Martin, ChamSys, GrandMA, Flying Pig Systems",
                     photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340/cat3.png",

                     description=f"""Световые пульты являются незаменимым оборудованием каждого светового шоу. Всё управление, все эффекты и импровизации выполняются именно на световых консолях. Отчасти от уровня пульта управления зависит качество всего светового оформления на мероприятии. В настоящее время производителей качественных, удобных пультов много, и художники по свету выбирают световой пульт под себя. Чтобы удовлетворить потребность большинства художников наша компания располагает большим ассортиментом профессиональных пультов управления светом. Для больших мероприятий возможностей одного отдельного пульта может не хватать. Компания Лазер-Кинетикс имеет возможность предоставить необходимое число крыльев расширения, чтобы расширить возможности пульта до необходимого уровня и предоставить полный фиизический контроль над световым шоу."""),
            Category(title="Приборы следящего света",
                     category_slug="3-follow-spots",
                     hint="Robert Juliat: Flo, Aramis, Lanсelot и др.",
                     photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340/cat4.png",
                     description=f"""Приборы следящего света - необходимый элемент любового концертного шоу. Компания Лазер-Кинетикс имеет в своем распоряжении несколько типов прожекторов следящего света различной мощности и с различным углом зумирования. Такой широкий ряд этих приборов позволяет подобрать оборудование для абсолютно любых мероприятий. У нас есть мощные 4000 Вт прожекторы, которые позволяют работать на огромных площадках, как правило открытых и ряд прожекторов мощностью 1200, 1800, 2500 Вт.Каждый прибор следящего света  управляется одним оператором."""),
            Category(title="Другое световое оборудование",
                     category_slug="4-etc-light",

                     hint="Martin, Griven, Coemar, Chroma-Q",
                     photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340/cat5.png",
                     description=f"""Компания Лазер-Кинетикс предоставляет большой ассортимент светодиодного оборудования, студийного света и света для архитектурной подсветки. Всё световое оборудование из этой категории позволяет  дополнить и расширить возможности штатного оборудования. Хоть оно статично, и имеет возможность только возможность смены цвета, но каждый тип приборов имеет свои преимущества и особенности, которые делают его незаменимыми при решении определенных художественных задач. Для концертных выступлений рок групп очень востребован стобоскоп Atomic 3000, а для архитектурной подсветки или заливки различных поверхностей и баннеров незаменим Kolorado."""),
            Category(title="Вспомогательное оборудование",
                     category_slug="5-rig",

                     hint="Фермы, Лебедки, Дым машины и др.",
                     photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340/cat6.png",
                     description=f"""Для проведения любой шоу программы с использованием мультимедийного и светового оборудования необходимо использование вспомогательного оборудования, начиная от простой защиты кабелей и заканчивая сложными подвесными конструктивами из ферм и лебедок. Мы имеем в своем распоряжении большое количество риггингового оборудования и достаточное количество ферм, чтобы самостоятельно провести любые монтажные работы по обеспечению подвеса под световое оборудование. Несмотря на то, что на рынке есть множество компаний специализирующихся на составлении  сложных металлоконструкций, мы также имеем возможность реализовывать интересные подвесные проекты."""),

        ]
        session.add_all(categories)
        await session.flush()
        # Создаем бренды
        brands = [
            Brand(title="AXCOR", description="Производитель светового оборудования"),
            Brand(title="Clay-Paky", description="Производитель светового оборудования"),
            Brand(title="Martin", description="Лидер в своей области"),
            Brand(title="AYRTON", description="Лидер в своей области"),
            Brand(title="GLP", description="Лидер в своей области"),
            Brand(title="Chromlech", description="Лидер в своей области"),
            Brand(title="JARAG", description="Лидер в своей области"),
            Brand(title="MA Lightning", description="Лидер в своей области"),
            Brand(title="High End Systems", description="Лидер в своей области"),
            Brand(title="Robe", description="Лидер в своей области"),
            Brand(title="Martin", description="Лидер в своей области"),
            Brand(title="Thomas", description="Лидер в своей области")

        ]
        session.add_all(brands)
        await session.flush()
        # Создаем оборудование
        equipments = [

            Equipment(
                title="Axcor Beam 300",
                rental_price=4000,
                brand_id=brands[0].id,
                category_id=categories[0].id,
                category_slug="0-moving-heads",
                power="110 Вт",
                producer="Италия",
                characteristics={"Производитель": "Clay Paky / Италия", "Тип прибора": "BEAM",
                                 "Кол-во источников света": 1, "Цветовая температура": "7600K",
                                 "Угол Вращения PAN": "540°", "Угол Вращения TILT": " 270°", "Мощность": "110 Вт",
                                 "Яркость": "1800 лм", "Zoom": " 2°"},
                weight=8,
                available_quantity=10,
                description="""Axcor Beam 300 - компактная вращающаяся голова типа BEAM, размером чуть более 500 мм. В качестве источника светового луча выступает белый светодиод мощностью 110 Вт с цветовой температурой 7600К.Axcor Spot 300 имеет в своем арсенале 17 гобо и способен излучать яркий плотный луч с минимальным углом менее 2°.Изобилие и качество цветовых эффектов, электронный фокус, 140 мм диаметра фронтальной линзы позволяет Axcor Beam 300 соперничать с легендарным Clay Paky Sharpy.""",
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/axcorbeam300_1_2.png",
                quantity=10
            ),
            Equipment(
                title="HY B-EYE K25",
                rental_price=3500,
                brand_id=brands[1].id,
                category_id=categories[0].id,
                category_slug="0-moving-heads",
                power="110 Вт",
                producer="Италия",
                characteristics={"Производитель": "Clay Paky / Италия", "Тип прибора": "WASH",
                                 "Кол-во источников света": 1, "Цветовая температура": "7600K",
                                 "Угол Вращения PAN": "540°", "Угол Вращения TILT": " 210°", "Мощность": "110 Вт",
                                 "Яркость": "1800 лм", "Zoom": " 2°"},
                weight=12,
                available_quantity=10,
                description="""HY B-EYE K25 Изменит ваше представление о диодных световых приборах. HY B-EYE K25 является доработанной и более мощной версией прибора B-EYE. Поворотная голова HY B-EYE K25 от CLAYPAKY оснащена 40-ваттнымидиодными модулями ORSAM STAR RGBW, которые вдвое мощнее чем у предшественника, в световой поток с новыми чипами ORSAM STAR стал в полтора раза сильнее. Прибор имеет три режима работы: Wash, Beam и FX, что позволяет использовать его как для заливного, статичного и динамического света, так и для создания световых эффектов, «вихревого» мульти лучевого света и прочих художественных замыслов.Так же прибор поддерживает пиксель-мэппинг, что позволяет использовать его в качестве необычного диодного экрана и выводить графические изображения на группе приборов. Усовершенствованная и компактная система охлаждения, спроектированная инженерами компании CLAYPAKY гарантирует бесперебойную работу прибора HT B-EYE K25 даже на самых жарких мероприятиях и выводит яркие цвета любых оттенков без риска перегрева""",
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/hy_b-eye_k25_main.png",
                quantity=10
            ),
            Equipment(
                title="Ayrton Dreampanel Twin",
                rental_price=10000,
                brand_id=brands[3].id,
                category_id=categories[0].id,
                category_slug="0-moving-heads",
                producer="SoundMaster GmbH",
                characteristics={"Общая мощность": "900 Вт", "Производитель": "Ayrton / Франция"},
                weight=12,
                available_quantity=5,
                description="""Этот гибридный прибор объединил в себе уже знакомый многим световой прибор MagicPanel и новую разработку французской компании - видео панель DreamPanel Shift. Объединенный в одном корпусе этот прибор благодаря свободному вращению по пану и тилту позволяет создавать невероятные эффекты позволяя создать шоу, в которых видео интегрировано в световую концепцию. Прибор MagicPanel Twin можно использовать как гибридный прибор, так и отдельно только световую часть.""",
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/01.png",
                quantity=8
            ),
            Equipment(
                title="Mac Viper Profile",
                rental_price=12000,
                brand_id=brands[9].id,
                category_id=categories[0].id,
                category_slug="0-moving-heads",
                power="1200 Вт",
                producer="Martin/Дания",
                characteristics={"Производитель": "Martin / Дания", "Яркость": "26000 Лм", "Общая мощность": "1200 Вт", "Zoom": "10° - 44°"},
                description="""MAC Viper Profile – мощный и яркий световой прибор, предлагающий пользователям массу функциональных преимуществ. Этот новый прибор оснащен высокоэффективной оптической системой, благодаря которой он с легкостью превосходит любые, даже лучшие профильные приборы, работающие на 1200 Вт лампе. Используя последние технические разработки и самые современные методы производства, инженерам компании Martin удалось достичь новых высот и создать более компактное, более быстрое и одновременно более яркое устройство. Новый прибор потребляет гораздо меньше энергии, а его световой выход эффективнее почти на 50%, чем у светильников на 1200 Вт лампе, которым собственно, он и приходит на замену.""",
                weight=8,
                available_quantity=10,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/1.jpg",
                quantity=10
            ),
            Equipment(
                title="Mac III Profile",
                rental_price=12000,
                brand_id=brands[9].id,
                category_id=categories[0].id,
                category_slug="0-moving-heads",
                power="1200 Вт",
                producer="Martin/Дания",
                characteristics={"Мощность": "1500 Вт", "Яркость": "33900 лм", "Цветовая температура": "3000K"},
                description="""MAC III Profile предлагает совершенный баланс между превосходными характеристиками, инновационными идеями и их окончательной реализацией. Этот высокомощный профильный прибор сочетает в себе технологически новую лампу 1500 Вт, непревзойденную оптическую систему и новую конструкцию. Он определяет новый уровень развития приборов с полным вращением.""",
                weight=8,
                available_quantity=10,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/1.jpg",
                quantity=10
            ),
            Equipment(
                title="Mac 2000 WASH",
                rental_price=12000,
                brand_id=brands[9].id,
                category_id=categories[0].id,
                category_slug="0-moving-heads",
                power="1200 Вт",
                producer="Martin/Дания",
                characteristics={"Производитель": "Martin / Дания", "Мощность": "1200 Вт", "Яркость": "33900 лм",
                                 "Цветовая температура": "3000K"},
                description="""MAC 2000 Wash XB на сегодняшний день является одним из лучших приборов заливного света. Световой выход устройства превышает 60000 люмен. Проверенная временем конструкция, прочный корпус, компактный для такой мощности формат, высокая степень надежности – все эти факторы позволяют прибору считаться лидером индустрии.""",
                weight=8,
                available_quantity=10,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/big/1_2.png",
                quantity=10
            ),
            Equipment(
                title="ROBE BMFL FollowSpot",
                rental_price=5000,
                brand_id=brands[8].id,
                category_id=categories[3].id,
                category_slug="3-follow-spots",
                power="40 Вт",
                producer="Чешская республика",
                characteristics={"Производитель": "Robe / Чешская Республика", "Мощность": "2000 Вт",
                                 "Общая мощность": "2000 Вт", "Цветовая температура": "6000К",
                                 "Угол Вращения PAN": "540°", "Угол Вращения TILT": " 270°"},
                description="""Следящий прожектор BMFL FollowSpot позволяет держать артистов в луче света без необходимости оборудования места оператора под потолком. Дистанционное управление за сценой значительно облегчает работу с фронтовыми лучами, а возможности самого прибора помогают добиться того, что невозможно осуществить с классическими приборами.BMFL FollowSpot от Чешской фирмы Robe имеет фронтальную линзу диаметром 160 mm и лампу с высоким CRI мощностью 1700W. Мощность светового потока составляет 251 000 lux на расстоянии 5 метров. Угол раскрытия луча с высокоточной фокусировкой варьируется от 5° до 45°.Управляемые вручную или дистанционно функции включают в себя плавное смешивание цветов и СТО, два колеса цвета, множество фрост-фильтров, фокусировку, зум и ирис с быстрой пульсацией. Управлять устройством можно и с помощью опционального внешнего программируемого блока для приборов следящего света LightMaster.""",

                weight=12,
                available_quantity=10,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/followspot-lt-1.png",
                quantity=10
            ),
            Equipment(
                title="GLP KNV ARC",
                rental_price=5000,
                brand_id=brands[8].id,
                category_id=categories[3].id,
                category_slug="4-etc-light",
                power="2000 Вт",
                producer="Чешская республика",
                characteristics={"Производитель": "GLP / Германия", "Мощность": "2000 Вт",
                                 "Общая мощность": "2000 Вт", "Количество диодов": "25 (5x5)",
                                 "Тип прибора": "Диоды"},
                description="""GLP KNV ARC - Стробоскоп подходящий как для одиночного, бесшовного подвеса из нескольких приборов. Благодаря 25 мощным пикселям формата RGBW мощностью 50000 люмен достигается качественна и мощная вспышка. Защита IP54 дает возможность использовать стробоскоп GLP KNV ARC даже в самых агресссивных погодных условиях. Рекомендовано совместное использование с GLP KNV Cube""",
                weight=12,
                available_quantity=10,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/glp-knv-arc-1.png",
                quantity=10
            ),
            Equipment(
                title="GLP KNV Cube",
                rental_price=5000,
                brand_id=brands[8].id,
                category_id=categories[3].id,
                category_slug="4-etc-light",
                power="750 Вт",
                producer="Германия",
                characteristics={"Производитель": "GLP / Германия", "Мощность": "750 Вт",
                                 "Общая мощность": "750 Вт",
                                 "Количество диодов": "25 (5x5)",
                                 "Тип прибора": "Диоды"},
                description="""GLP KNV Cube - Стробоскоп подходящий как для подеса, так и для установки на повеохностях. Имеется возможность использоания как одиночного прибора, так и связку на бесшовном каркасе. Благодаря 25 мощным пикселям формата RGBW мощностью 50000 люмен достигается качественна и мощная вспышка. Защита IP54 дает возможность использовать стробоскоп GLP KNV Cube даже в самых агресссивных погодных условиях.""",
                weight=12,
                available_quantity=10,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/glp-knv-cube-1.png",
                quantity=10
            ),

            Equipment(
                title="GLP X4 Atom",
                rental_price=5000,
                brand_id=brands[4].id,
                category_id=categories[1].id,
                category_slug="1-fill-light",
                producer="GLP/Германия",
                weight=50,
                power="40 Вт",
                characteristics={"Производитель": "GLP / Германия", "Мощность": "40 Вт", "Zoom": "3,5° - 34°"},
                available_quantity=12,
                description="""GLP X4 Atom Разработан для придания максимальной индивидуальности вашему шоу. Благодаря компактному корпусу, спроектированному для монтажа в максимально узких местах, он обеспечивает ровный свет как для концертов, так и для телевизионных и кино съемок.За счет защиты IP 65, X4 Atom можно использовать вне помещений и под проливным дождем, а инновационная система крепежа дает возможность легко соединять прибороы между собой.X4 Atom оснащен мощным RGBW диодом, что позволяет не терять в качестве при компактных габаритах.""",
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/1_11.png",
                quantity=8
            ),
            Equipment(
                title="JARAG-Line PAR30",
                rental_price=5000,
                brand_id=brands[6].id,
                category_id=categories[1].id,
                category_slug="1-fill-light",
                producer="Chromlech/Франция",
                characteristics={"Производитель": "Chromlech / Франция", "Общая мощность:": "375 Вт",
                                 "Мощность": "375 Вт"},
                weight=50,
                power="375 Вт",
                total_power="375 Вт",
                available_quantity=12,
                description="""Jarag Line позволяет создавать световые рисунки, как его "собрат" Jarag 5. Но в виду уменьшенных размеров одного отдельного модуля есть возможность значительно расширить разнообразие собираемых конструкций.""",
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/02.png",
                quantity=8
            ),
            Equipment(
                title="JARAG 5 PAR30",
                rental_price=7000,
                brand_id=brands[6].id,
                category_id=categories[1].id,
                category_slug="1-fill-light",
                producer="JARAG/Франция",
                characteristics={"Производитель": "Chromlech / Франция", "Общая мощность:": "1875  Вт",
                                 "Мощность": "1875 Вт"},
                power="1875 Вт",
                weight=12,
                total_power="1875 Вт",
                description="""Jarag-5 Par 30 представляет слияние проверенных временем технологий и новых разработок. Этот прибор позволяет создавать конструкции оригинальных форм для осуществления любых художественных задумок. Jarag имеет модульную конструкцию состоящую из блоков с индивидуальным контролем ламп. Объединяя модули можно создать целую стену света и отображать на них различные световые узоры.""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/02_2.png",
                quantity=8
            ),
            Equipment(
                title="2-lite Blinder",
                rental_price=7000,
                brand_id=brands[11].id,
                category_id=categories[1].id,
                category_slug="1-fill-light",
                producer="Thomas / Англия",
                characteristics={"Производитель": "Thomas / Англия", "Мощность": "1300  Вт",
                                 "Цветовая система": "DWE", "Общая мощность": "1300 Вт"},
                power="1300 Вт",
                weight=12,
                total_power="1300 Вт",
                description="""2-lite blinder состоит из двух мощных ламп по 650 Вт. Совокупная мощность небольшого количества таких приборов позволяет добавлять в шоу сильные, контрастные вставки. При этом прибор компактен и подходит как для небольших площадок, так и для крупных проектов.""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/02_3.png",
                quantity=8
            ),
            Equipment(
                title="8-lite Blinder",
                rental_price=3500,
                brand_id=brands[11].id,
                category_id=categories[1].id,
                category_slug="1-fill-light",
                producer="Thomas / Англия",
                characteristics={"Производитель": "Thomas / Англия", "Общая мощность:": "5200 Вт",
                                 "Мощность": "5200 Вт", "Тип лампы": "DWE"},
                power="5200 Вт",
                weight=12,
                total_power="5200 Вт",
                description="""8-lite blinder состоит из восьми мощных ламп по 650 Вт. Общая мощность одного прибора поражает воображение - 5200 Вт. Правильная геометрическая форма этого светового прибора позволяет составлять различные орнаменты и фигуры, а колоссальная мощность делает этот прибор эффектным не только в больших помещениях, но и на открытых площадках.""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/big/02_4.png",
                quantity=8
            ),
            Equipment(
                title="PAR-64 single",
                rental_price=1000,
                brand_id=brands[11].id,
                category_id=categories[1].id,
                category_slug="1-fill-light",
                producer="Thomas / Англия",
                characteristics={"Производитель": "Thomas / Англия", "Общая мощность:": "1 кВт",
                                 "Мощность": "1 кВт"},
                power="1000 Вт",
                weight=12,
                total_power="1875 Вт",
                description="""""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/02_5.png",
                quantity=8
            ),
            Equipment(
                title="6-lamp Bar PAR-64",
                rental_price=1000,
                brand_id=brands[11].id,
                category_id=categories[1].id,
                category_slug="1-fill-light",
                producer="Thomas / Англия",
                characteristics={"Производитель": "Thomas / Англия", "Общая мощность:": "6 кВт",
                                 "Мощность": "6 кВт"},
                power="6 кВт",
                weight=12,
                total_power="6 кВт",
                description="""""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/02_6.png",
                quantity=8
            ),
            Equipment(
                title="Grand MA2 Light",
                rental_price=12000,
                brand_id=brands[7].id,
                category_id=categories[2].id,
                category_slug="2-consoler",
                producer="MA Lighting/Германия",
                characteristics={"1": "6 выходов DMX", "2": "1 встроенный программируемый экран",
                                 "3": "2 встроенных сенсорных монитора",
                                 "4": "2 внешних монитора",
                                 "5": "15 приводных фейдеров",
                                 "6": "2 входа etherCON",
                                 "7": "Встроенная клавиатура",
                                 "8": "Моторизованное мониторное крыло"},
                power="1875 Вт",
                total_power="1875 Вт",
                description="""Пульт GrandMA2 light – является компактной версией grandMA2 full-size. Имеет на борту 15 приводных фейдеров, 2 сенсорных дисплея и возможность работы с 4096 HTP/LTP-параметрами. Во всем остальном идентичен полной версии. Пульт grandMA2 light идеально подходит для любых мероприятий. Способен управлять всеми видами приборов: статическими, динамическими, светодиодными, видео и медиасерверами. Пульт поддерживает различные стили интуитивно понятного и удобного управления всеми подключенными приборами и каналами. Программировать на grandMA2 light легко и просто. К услугам программиста практически бесконечное число пресетов, световых картин, страниц, секвенций и эффектов. Пульт grandMA2 light – отличная поддержка пульту grandMA2 full-size. Он так же полностью совместим с шоу-файлами Series 1 и dot2""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/01_2.png",
                quantity=8,
                weight=30,

            ),
            Equipment(
                title="WholeHOG IV",
                rental_price=12000,
                brand_id=brands[7].id,
                category_id=categories[2].id,
                category_slug="2-consoler",
                producer="High End Systems/США",
                characteristics={"1": "2 Ethernet порта", "2": "2 сенсерных экрана",
                                 "3": "Подключение до 3 внешних мониторов",
                                 "4": "12 LCD дисплея фейдеров",
                                 "5": "Процессор DMX 8000"},
                power="1875 Вт",
                total_power="1875 Вт",
                weight=12,

                description="""WholeHOG IV - новейший пульт для управления светом от компании High End Systems.""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/01_2.png",
                quantity=8
            ),
            Equipment(
                title="WholeHOG Playback Wing 4",
                rental_price=20000,
                brand_id=brands[7].id,
                category_id=categories[2].id,
                category_slug="2-consoler",
                producer="High End Systems/США",
                characteristics={"Производитель":"High End Systems / США", "Общая мощность":"1875 Вт"},
                weight=12,
                power="1875 Вт",
                total_power="1875 Вт",
                description="""Это крыло позволяет расширять возможности световых пультов Flying Pig Systems последнего поколения. Playback wing 4 предоставляет оператору 10 моторизированных мастеров и сенсерный экран размером 15.6".""",
                available_quantity=12,
                photo_url="https://laserkinetics.ru/uploadedFiles/eshopimages/icons/340x340_cropped/02_9.png",
                quantity=8
            ),

        ]
        session.add_all(equipments)
        await session.flush()

        for equipment in equipments:
            equipment.equipment_slug = f"{equipment.id}-{equipment.title.lower().replace(' ', '-')}"

        roles = [
            Role(
                title="Admim"
            ),
            Role(
                title="customer"
            ),
        ]
        user_last_name: Mapped[str] = mapped_column(String)
        user_first_name: Mapped[str] = mapped_column(String)
        user_middle_name: Mapped[str] = mapped_column(String, nullable=True)
        user_phone_number: Mapped[str] = mapped_column(String(12))
        avatar_url: Mapped[str] = mapped_column(String, nullable=True)
        user_email_address: Mapped[str] = mapped_column(String)
        role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

        users = [
            User(user_last_name="Test",
                 user_first_name="Test",
                 user_middle_name="Test",
                 user_phone_number="89162964845",
                 user_email_address="test@gmail.com",
                 avatar_url="https://avatars.mds.yandex.net/i?id=ecf30915047a57f9f10570d7e39490f43be4a697-4854935-images-thumbs&n=13",
                 role_id=roles[1].id),
            User(user_last_name="Admin",
                 user_first_name="Admin",
                 user_middle_name="Admin",
                 user_phone_number="89162964845",
                 user_email_address="admin@gmail.com",

                 avatar_url="https://avatars.mds.yandex.net/i?id=ecf30915047a57f9f10570d7e39490f43be4a697-4854935-images-thumbs&n=13",
                 role_id=roles[1].id)
        ]
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e


import asyncio

asyncio.run(generate_date())
