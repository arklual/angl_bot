START_MESSAGES_RU = [
'Привет! Я Скилбадди – ваш репетитор английского языка, созданный на модели chatGPT. Пожалуйста, не стесняйтесь спрашивать меня о своих грамматике и произношении. Я помогу вам с практикой, или мы можем просто поговорить на английском. ',
'Здравствуйте, я Скилбадди. Я ваш личный репетитор по английскому языку. Вы можете говорить, тренироваться и проверять свои грамматические навыки вместе со мной. Также я могу проверить ваше произношение и сказать, правильное ли оно. С чего начнём?',
'Привет! Я Скилбадди. Я буду вашим личным носителем английского языка. Вы можете говорить со мной на любую тему. Давайте общаться и развлекаться!',
'Рад познакомиться! Я Скилбадди - ваш репетитор по английскому языку, разработанный на основе модели chatGPT. Вы можете общаться со мной как с приятелем-носителем языка. Пожалуйста, скажите мне, что вы хотите обсудить, и желаете ли, чтобы я проверил ваши знания английского языка.',
'Привет, как дела? Я Скилбадди, искусственный интеллект в роли носителя английского языка. Я  буду распознавать ваш устный и письменный английский и давать советы по грамматике и навыкам произношения. '
]


START_MESSAGES_EN = [
    "Hi there! I am Skillbuddy, your English tutor, built on chatGPT model. Please do not hesitate to ask me tips about grammar & pronunciation. I will help you with practice, or we can just talk in English!",
    "Hello, this is Skillbuddy. I am your personal tutor of English. You can speak, train and check your grammar skills with me. I can also check your pronunciation and tell you, if it is correct. Where do we start?",
    "Hi! I am Skillbuddy. I`ll be your personal English native speaker. You can speak with me on any topic. Let`s communicate and have fun!",
    "Nice to meet you! I`m Skillbuddy, your chatGPT-designed English tutor. You can chat with me as with a native speaker buddy. Please tell me, what you want to discuss and if you want me to check your English skills. ",
    "Hey, how are you? I am Skillbuddy, an Artificial Intelligence in the role of a native English speaker. I will recognize your verbal and written English and give advice on grammar & pronunciation skills."
]

HELP_MESSAGE_RU_1 = '''
Справочное меню:
Меню пользователя – информация о вашей подписке на использование Скилбадди. 
Справочное меню - информация обо всех режимах и командах бота. 
Как пользоваться – инструкция по практическому использованию бота с примерами, показывающая скрытые возможности Скилбадди. 
Режим "Грамматика" – режим тренировки навыков письменного английского (грамматика, синтаксис, правописание, пунктуация). 
Режим "Разговор" – режим тренировки навыков разговорного английского (режим бота по умолчанию), в котором вы можете построить диалог с Бадди на любую тему текстом или голосом. 
Режим "Фонетика" – режим тренировки навыков устного английского (транскрипция, слогообразование, ударения) с 2-х этапным фонетическим анализом текста. 
Смена голоса - выбор мужского или женского вариантов голоса Бадди для каждого из режимов. 
Смена языка - выбор русского или английского языка для всех описаний и меню. 
'''
HELP_MESSAGE_RU_2 = '''
Команды, доступные в боте:
/start - экран приветствия с описанием бота
/menu - основное меню
/help – справочное меню
/talk - переход в режим “Разговор“ (тренировка разговорного английского) 
/grammar - переход в режим “Грамматика“
(тренировка письменного английского) /phonetics - переход в режим “Фонетика“ (тренировка устного английского)
/tutorial – переход к инструкции, как пользоваться ботом, с наглядными  практическим примерами
/reset – удалить контекст (начать новую сессию)
/subscribe – информация о подписке
/voice - переход в режим голосового меню
'''

HELP_MESSAGE_EN_1 = '''
Help menu:
User menu – information about your Skillbuddy subscription. 
Help menu - information about all modes and commands of the bot.
Tutorial – a manual for the practical use of the bot with examples, showing hidden capabilities of Skillbuddy. 
"Grammar" mode – written English train mode (grammar, syntax, spelling, punctuation). 
"Talk" mode - conversational English train mode (the default bot mode), in which you can build a dialogue with Buddy on any topic by text or voice. 
"Phonetics" mode - verbal English train mode (transcription, syllable formation, stress) with a 2-stage phonetic analysis of the text. 
Voice menu - select male or female versions of Buddy's voice for each of the modes. 
Language menu - select Russian or English for all descriptions and menus. 
'''
HELP_MESSAGE_EN_2 = '''
Commands available in the bot:
/start - welcome screen with a description of the bot 
/menu - main menu
/help - help menu
/talk – switch to the "Talk" mode (conversational English trainer)
/grammar - switch to "Grammar" mode
(written English trainer)
/phonetics – switch to "Phonetics" mode (verbal English trainer). 
/tutorial – instruction on how to use the bot, with illustrative practical examples. 
/reset – clear context (start a new session)
/subscribe - subscription details. 
/voice - switch to voice menu mode. 
'''

def get_ref_link_text(n, url):
    return [f'Будущее уже здесь 🤙 Тренируй свой английский со Skillbuddy! Попробовать бесплатно: {url}',                                          
    f'Попробуй бесплатного ИИ-репетитора 🇬🇧, с которым изучение английского превращается в игру двух интеллектов: {url}',                                                                                                          
    f'Узнай много нового в интерактивном диалоге с chatGPT-на английском языке. Skillbuddy повысит твой скилл общения на English 💪 {url}',                                                                                      
    f'Skillbuddy (chatGPT) - тренер английского нового поколения, помогающий общаться на одном языке с 🤖 в удовольствие. Попробуй: {url}',                                                                                    
    f'Раскрой языковой потенциал нейросети chatGPT со Skillbuddy! Английский язык ещё никогда не был столь увлекательным 👍 {url}',                                                          
    f'Тренируй свой английский 🇬🇧, расширяй кругозор 🏝, развивай вербальный интеллект вместе со Skillbuddy 👧! Поговорить с репетитором на базе chatGPT бесплатно: {url}',
    f'Новый вербальный носитель 🇬🇧 - Skillbuddy. Твой лучший друг в тренировке навыков английского. Пробуй: {url}',
    f'Разговори свой English cо Skillbuddy! Попробуй поговорить с опытным носителем в непринужденной беседе ⛱: {url}',
    f'Не знаешь с кем поговорить на английском 🤷‍♀️? Как насчёт искусственного интеллекта? Прокачай свой English c chatGPT: {url}',
    f'Собираешься поехать за границу 😎? Потренируй свой английский со Skillbuddy, это бесплатно: {url}. Он использует 🇬🇧 на базе chatGPT и поможет освоиться в любой языковой среде🤙'][n]