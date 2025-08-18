#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 Генератор фишинговых писем
Образовательный модуль для изучения социальной инженерии

⚠️ ВАЖНО: Использовать только в образовательных целях!
"""

import random
import json
import os
from datetime import datetime, timedelta
import re

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class PhishingGenerator:
    """Генератор фишинговых писем для обучения"""
    
    def __init__(self):
        self.templates = self.load_templates()
        self.target_info = {}
    
    def load_templates(self):
        """Загрузка шаблонов писем"""
        templates = {
            "banking": {
                "subjects": [
                    "🔒 Подтвердите вашу учетную запись",
                    "⚠️ Подозрительная активность на счете",
                    "💳 Ваша карта заблокирована",
                    "📧 Обновите ваши данные",
                    "🚨 Безопасность вашего счета под угрозой"
                ],
                "bodies": [
                    """
Уважаемый клиент {name},

Мы обнаружили подозрительную активность на вашем счете {account_number}.

Для защиты ваших средств, пожалуйста, подтвердите ваши данные по ссылке ниже:
{phishing_link}

Если вы не подтвердите данные в течение 24 часов, ваш счет будет заблокирован.

С уважением,
Служба безопасности {bank_name}
                    """,
                    """
Здравствуйте, {name}!

Ваша банковская карта **** {card_last4} была временно заблокирована из-за подозрительной транзакции на сумму {amount} руб.

Для разблокировки перейдите по ссылке: {phishing_link}

Время действия ссылки: 2 часа

{bank_name} - Ваша безопасность наш приоритет
                    """
                ]
            },
            "social": {
                "subjects": [
                    "🎉 У вас новое сообщение!",
                    "👤 Кто-то посмотрел ваш профиль",
                    "💝 У вас есть подарок!",
                    "🔔 Важное уведомление",
                    "📱 Подтвердите ваш аккаунт"
                ],
                "bodies": [
                    """
Привет {name}!

У вас {message_count} новых сообщений от {friend_name}.

Посмотреть сообщения: {phishing_link}

Не пропустите важные уведомления!

Команда {platform_name}
                    """,
                    """
{name}, ваш профиль очень популярен! 

За последние сутки ваш профиль посмотрели {views} человек.

Посмотреть кто именно: {phishing_link}

Возможно, среди них есть ваши старые друзья!

{platform_name}
                    """
                ]
            },
            "tech_support": {
                "subjects": [
                    "🔧 Требуется обновление системы",
                    "⚠️ Обнаружена уязвимость",
                    "💻 Ваш компьютер заражен",
                    "🛡️ Установите обновление безопасности",
                    "📊 Проверка системы завершена"
                ],
                "bodies": [
                    """
Уважаемый пользователь {name},

Наша система обнаружила {threat_count} угроз на вашем компьютере.

Для немедленной очистки скачайте наш инструмент: {phishing_link}

Если не принять меры в течение {hours} часов, возможна потеря данных.

Служба технической поддержки
                    """,
                    """
Внимание!

Ваша система Windows нуждается в критическом обновлении безопасности.

Обнаружены уязвимости: CVE-2023-{random_cve}

Скачать обновление: {phishing_link}

Microsoft Security Team
                    """
                ]
            },
            "work": {
                "subjects": [
                    "📄 Срочный документ для подписи",
                    "💼 Изменения в трудовом договоре", 
                    "📊 Квартальный отчет",
                    "🎯 Новая задача от руководства",
                    "💰 Бонусная программа"
                ],
                "bodies": [
                    """
{name},

Вам назначена срочная задача от {boss_name}.

Детали и документы: {phishing_link}

Срок выполнения: до {deadline}

Отдел кадров
                    """,
                    """
Сотрудник {name},

В связи с изменениями в трудовом законодательстве требуется обновить ваши данные.

Форма для заполнения: {phishing_link}

Заполните до {deadline}, иначе возможны задержки с зарплатой.

HR-отдел {company}
                    """
                ]
            }
        }
        return templates
    
    def generate_fake_data(self):
        """Генерация поддельных данных"""
        names = ["Александр", "Мария", "Дмитрий", "Анна", "Михаил", "Елена", "Иван", "Ольга"]
        companies = ["Сбербанк", "ВТБ", "Альфа-Банк", "Тинькофф", "Газпромбанк"]
        platforms = ["ВКонтакте", "Одноклассники", "Facebook", "Instagram", "Telegram"]
        
        return {
            "name": random.choice(names),
            "account_number": f"40817810{random.randint(100000000, 999999999)}",
            "card_last4": str(random.randint(1000, 9999)),
            "amount": random.randint(1000, 50000),
            "bank_name": random.choice(companies),
            "platform_name": random.choice(platforms),
            "friend_name": random.choice(names),
            "message_count": random.randint(1, 15),
            "views": random.randint(10, 500),
            "threat_count": random.randint(3, 25),
            "hours": random.randint(2, 24),
            "random_cve": random.randint(10000, 99999),
            "boss_name": random.choice(names),
            "deadline": (datetime.now() + timedelta(days=random.randint(1, 7))).strftime("%d.%m.%Y"),
            "company": random.choice(["ООО Техно", "ИП Сидоров", "АО РосТех", "ЗАО Инновации"]),
            "phishing_link": "https://bit.ly/secure-verify-" + str(random.randint(100000, 999999))
        }
    
    def customize_template(self, category, target_name=None, target_company=None):
        """Настройка шаблона под конкретную цель"""
        print(f"\n{Colors.YELLOW}🎯 Настройка шаблона для категории: {category.upper()}{Colors.END}")
        
        if target_name:
            print(f"👤 Цель: {target_name}")
        if target_company:
            print(f"🏢 Компания: {target_company}")
        
        # Получаем данные
        data = self.generate_fake_data()
        
        if target_name:
            data["name"] = target_name
        if target_company:
            data["company"] = target_company
            data["bank_name"] = target_company
        
        # Выбираем случайный шаблон
        template_data = self.templates[category]
        subject = random.choice(template_data["subjects"])
        body = random.choice(template_data["bodies"])
        
        # Заполняем шаблон
        try:
            formatted_body = body.format(**data)
            formatted_subject = subject.format(**data)
        except KeyError as e:
            formatted_body = body
            formatted_subject = subject
        
        return {
            "subject": formatted_subject,
            "body": formatted_body,
            "category": category,
            "target": target_name or "Не указано",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def advanced_generator(self):
        """Продвинутый генератор с психологическими приемами"""
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🧠 ПРОДВИНУТЫЙ ГЕНЕРАТОР{Colors.END}")
        print(f"{Colors.CYAN}Использует психологические приемы социальной инженерии{Colors.END}")
        
        techniques = {
            "urgency": "⏰ Создание ощущения срочности",
            "authority": "👨‍💼 Апелляция к авторитету", 
            "fear": "😨 Использование страха",
            "curiosity": "🤔 Возбуждение любопытства",
            "greed": "💰 Использование жадности",
            "social_proof": "👥 Социальное доказательство"
        }
        
        print("\nВыберите психологический прием:")
        for key, desc in techniques.items():
            print(f"  {desc}")
        
        technique = input(f"\n{Colors.YELLOW}Введите ключевое слово (urgency/authority/fear/etc): {Colors.END}")
        
        if technique in techniques:
            return self.generate_psychological_email(technique)
        else:
            print(f"{Colors.RED}Неизвестный прием, используется случайный{Colors.END}")
            return self.generate_psychological_email(random.choice(list(techniques.keys())))
    
    def generate_psychological_email(self, technique):
        """Генерация письма с конкретным психологическим приемом"""
        data = self.generate_fake_data()
        
        templates = {
            "urgency": {
                "subject": "🚨 СРОЧНО: Ваш аккаунт будет удален через 1 час!",
                "body": f"""
ВНИМАНИЕ! КРИТИЧЕСКАЯ СИТУАЦИЯ!

Ваш аккаунт {data['name']} будет НАВСЕГДА удален через 1 час из-за подозрительной активности.

ДЛЯ СОХРАНЕНИЯ АККАУНТА немедленно перейдите: {data['phishing_link']}

Время до удаления: 59 минут 32 секунды

Это последнее предупреждение!
                """
            },
            "authority": {
                "subject": "📋 Распоряжение от руководства IT-отдела",
                "body": f"""
По распоряжению директора по информационным технологиям всем сотрудникам необходимо:

1. Пройти обязательную проверку безопасности
2. Обновить корпоративные пароли
3. Подтвердить доступ к системам

Ссылка для прохождения: {data['phishing_link']}

Сотрудники, не прошедшие проверку до {data['deadline']}, будут лишены доступа к корпоративным системам.

С уважением,
Главный администратор безопасности
                """
            },
            "fear": {
                "subject": "⚠️ ВАШИ ДАННЫЕ УКРАДЕНЫ! Срочные меры",
                "body": f"""
ВНИМАНИЕ! УТЕЧКА ДАННЫХ!

Ваша личная информация была скомпрометирована в результате кибератаки:
• Пароли: УКРАДЕНЫ
• Банковские данные: ПОД УГРОЗОЙ  
• Личные фото: ДОСТУПНЫ ЗЛОУМЫШЛЕННИКАМ

Для блокировки доступа злоумышленников СРОЧНО перейдите:
{data['phishing_link']}

КАЖДАЯ СЕКУНДА НА СЧЕТУ!

Служба экстренного реагирования
                """
            },
            "curiosity": {
                "subject": "🤫 Кто-то анонимно оставил вам сообщение...",
                "body": f"""
Здравствуйте, {data['name']}!

Некто, кто знает вас лично, оставил анонимное сообщение.

В нем говорится что-то очень важное о вас...

Прочитать сообщение: {data['phishing_link']}

P.S. Сообщение будет удалено через 24 часа
                """
            },
            "greed": {
                "subject": "💰 Поздравляем! Вы выиграли 500,000 рублей!",
                "body": f"""
🎉 ПОЗДРАВЛЯЕМ, {data['name']}! 🎉

Ваш номер телефона выиграл в лотерее "Миллион"!

Сумма выигрыша: 500,000 рублей

Для получения приза перейдите: {data['phishing_link']}

⏰ Срок получения: до {data['deadline']}

Не упустите свой шанс!

Организационный комитет лотереи
                """
            },
            "social_proof": {
                "subject": "👥 Уже 50,000 человек получили бонус!",
                "body": f"""
{data['name']}, не пропустите!

Более 50,000 пользователей уже получили бонус 10,000 рублей от нашего банка!

"Спасибо за бонус! Очень быстро и просто!" - Мария К.
"Не поверил сначала, но деньги действительно пришли!" - Александр П.
"Всем советую!" - Елена Д.

Получить свой бонус: {data['phishing_link']}

Осталось мест: {random.randint(15, 150)}

Присоединяйтесь к счастливчикам!
                """
            }
        }
        
        template = templates.get(technique, templates["urgency"])
        
        return {
            "subject": template["subject"],
            "body": template["body"],
            "technique": technique,
            "category": "psychological",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def save_email(self, email_data):
        """Сохранение письма в файл"""
        if not os.path.exists("generated_emails"):
            os.makedirs("generated_emails")
        
        filename = f"generated_emails/phishing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("ФИШИНГОВОЕ ПИСЬМО (ОБРАЗОВАТЕЛЬНЫЕ ЦЕЛИ)\n")
            f.write("="*60 + "\n\n")
            f.write(f"Дата создания: {email_data['created']}\n")
            f.write(f"Категория: {email_data.get('category', 'Не указано')}\n")
            f.write(f"Цель: {email_data.get('target', 'Не указано')}\n")
            if 'technique' in email_data:
                f.write(f"Психологический прием: {email_data['technique']}\n")
            f.write("\n" + "-"*40 + "\n")
            f.write(f"ТЕМА: {email_data['subject']}\n")
            f.write("-"*40 + "\n\n")
            f.write(email_data['body'])
            f.write("\n\n" + "="*60 + "\n")
            f.write("⚠️ ВНИМАНИЕ: Данное письмо создано в образовательных целях!\n")
            f.write("Не используйте для реальных атак!\n")
            f.write("="*60 + "\n")
        
        print(f"{Colors.GREEN}✅ Письмо сохранено: {filename}{Colors.END}")
        return filename
    
    def run(self):
        """Запуск генератора"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.CYAN}📧 ГЕНЕРАТОР ФИШИНГОВЫХ ПИСЕМ{Colors.END}")
            print(f"{Colors.RED}⚠️ ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!{Colors.END}\n")
            
            print("Выберите режим:")
            print("1. 🎯 Быстрая генерация по категориям")
            print("2. 🧠 Продвинутый генератор (психологические приемы)")
            print("3. ⚙️ Настраиваемый шаблон")
            print("4. 📁 Просмотр сохраненных писем")
            print("0. ← Назад в главное меню")
            
            choice = input(f"\n{Colors.YELLOW}Выберите опцию: {Colors.END}")
            
            if choice == '1':
                self.quick_generation()
            elif choice == '2':
                email = self.advanced_generator()
                self.display_email(email)
                if input("\nСохранить письмо? (y/n): ").lower() == 'y':
                    self.save_email(email)
            elif choice == '3':
                self.custom_template()
            elif choice == '4':
                self.view_saved_emails()
            elif choice == '0':
                break
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
    
    def quick_generation(self):
        """Быстрая генерация по категориям"""
        print(f"\n{Colors.BOLD}🎯 БЫСТРАЯ ГЕНЕРАЦИЯ{Colors.END}")
        
        categories = {
            "1": ("banking", "🏦 Банковские письма"),
            "2": ("social", "📱 Социальные сети"),
            "3": ("tech_support", "🔧 Техподдержка"),
            "4": ("work", "💼 Рабочие письма")
        }
        
        print("\nКатегории:")
        for key, (_, desc) in categories.items():
            print(f"  {key}. {desc}")
        
        cat_choice = input(f"\n{Colors.YELLOW}Выберите категорию: {Colors.END}")
        
        if cat_choice in categories:
            category = categories[cat_choice][0]
            email = self.customize_template(category)
            self.display_email(email)
            
            if input("\nСохранить письмо? (y/n): ").lower() == 'y':
                self.save_email(email)
        else:
            print(f"{Colors.RED}❌ Неверная категория!{Colors.END}")
    
    def custom_template(self):
        """Настраиваемый шаблон"""
        print(f"\n{Colors.BOLD}⚙️ НАСТРАИВАЕМЫЙ ШАБЛОН{Colors.END}")
        
        target_name = input("Имя цели (или Enter для случайного): ").strip()
        target_company = input("Компания цели (или Enter для случайной): ").strip()
        
        categories = ["banking", "social", "tech_support", "work"]
        print(f"\nДоступные категории: {', '.join(categories)}")
        category = input("Категория (или Enter для случайной): ").strip()
        
        if not category or category not in categories:
            category = random.choice(categories)
        
        email = self.customize_template(
            category,
            target_name if target_name else None,
            target_company if target_company else None
        )
        
        self.display_email(email)
        
        if input("\nСохранить письмо? (y/n): ").lower() == 'y':
            self.save_email(email)
    
    def display_email(self, email_data):
        """Отображение письма"""
        print(f"\n{Colors.BOLD}{Colors.GREEN}📧 СГЕНЕРИРОВАННОЕ ПИСЬМО{Colors.END}")
        print("="*60)
        print(f"{Colors.BOLD}ТЕМА:{Colors.END} {email_data['subject']}")
        print("="*60)
        print(email_data['body'])
        print("="*60)
        
        if 'technique' in email_data:
            print(f"{Colors.PURPLE}🧠 Психологический прием: {email_data['technique']}{Colors.END}")
    
    def view_saved_emails(self):
        """Просмотр сохраненных писем"""
        if not os.path.exists("generated_emails"):
            print(f"{Colors.YELLOW}📁 Папка с письмами не найдена{Colors.END}")
            return
        
        files = [f for f in os.listdir("generated_emails") if f.endswith('.txt')]
        
        if not files:
            print(f"{Colors.YELLOW}📁 Сохраненные письма не найдены{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}📁 СОХРАНЕННЫЕ ПИСЬМА{Colors.END}")
        for i, filename in enumerate(files, 1):
            print(f"  {i}. {filename}")
        
        try:
            choice = int(input(f"\n{Colors.YELLOW}Выберите письмо для просмотра (или 0 для выхода): {Colors.END}"))
            
            if 1 <= choice <= len(files):
                filepath = os.path.join("generated_emails", files[choice-1])
                with open(filepath, 'r', encoding='utf-8') as f:
                    print(f"\n{Colors.CYAN}{f.read()}{Colors.END}")
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
        except (ValueError, IndexError):
            print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")

if __name__ == "__main__":
    generator = PhishingGenerator()
    generator.run()
