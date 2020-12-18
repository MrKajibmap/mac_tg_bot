from telegram import Bot, Update
from echo.config import DATABASELINK_POSTGRES, DATABASELINK_ETL

import dj_database_url
import psycopg2
# for send wolf pictures
# import requests
# from json import loads
# from bs4 import BeautifulSoup

def button_help_handler(bot: Bot, update: Update):
    txt = '<b>HELP:</b>\n'
    txt += '<b>/start</b> Ну че, народ, погнали?!\n'
    txt += '<b>/request_rtp</b> Показать последнюю сводку по краткосрочному прогнозу\n'
    txt += '<b>/request_vf</b> Показать последюю сводку по долгосрочному прогнозу\n'
    txt += '<b>/request</b> Показать ошибки с начала цикла (17:00)\n'
    txt += '<b>/request_etl</b> Отображение общей сводки в системе\n'
    txt += '<b> INFO </b> Бот создан для получения запросов к базе данных Postgresql проекта Macdonalds\n'
    bot.send_message(update.message.chat.id, txt, parse_mode='HTML')


def button_request_errors_handler(bot: Bot, update: Update):
    db_info = dj_database_url.config(default=DATABASELINK_ETL)
    connection = psycopg2.connect(database=db_info.get('NAME'),
                                  user=db_info.get('USER'),
                                  password=db_info.get('PASSWORD'),
                                  host=db_info.get('HOST'),
                                  port=db_info.get('PORT'))
    cursor = connection.cursor()
    update.message.reply_text(
        text='Я отправил реквест в базу данных для извлечения статистики ошибок в системе за сегодня, ждите!',
    )

    cursor.execute(""" select t1.* from 
    (
    select cast(lower(process_nm) as varchar(32)) as process_nm,
    				case when status_description='' and end_dttm is null then 'In progress' 
					when status_description='' and end_dttm is not null then 'Success' 
    				else cast(status_description as varchar(50)) 
    				end as status_description
    				,cast(start_dttm + interval'8 hour' as timestamp (0)) as start_dttm
    				, cast(end_dttm + interval'8 hour' as timestamp (0)) as end_dttm
    				, case when end_dttm is null then cast(current_timestamp as timestamp (0)) - cast(start_dttm as timestamp (0)) 
    					else cast(end_dttm as timestamp (0)) - cast(start_dttm as timestamp (0))
    					end as exec_tm
    				, cast(user_nm as varchar(15)) as user
    				from etl_cfg.cfg_log_event 
    				where cast(current_date as timestamp (0)) - interval'8 hour' <= start_dttm + interval'8 hour'
    				and status_cd=1
    				order by start_dttm desc 
    				limit 40
    				) t1 
			order by start_dttm
    				""")

    query_results = cursor.fetchall()
    #print(query_results)
    text = '\n\n'.join([', '.join(map(str, x)) for x in query_results])
    #print(text)
    bot.send_message(
        chat_id=update.message.chat.id,
        text=text
    )

    update.message.reply_text(
        text='Ответ отправлен',
    )

def button_request_status_handler(bot: Bot, update: Update):
    db_info = dj_database_url.config(default=DATABASELINK_ETL)
    connection = psycopg2.connect(database=db_info.get('NAME'),
                                  user=db_info.get('USER'),
                                  password=db_info.get('PASSWORD'),
                                  host=db_info.get('HOST'),
                                  port=db_info.get('PORT'))
    cursor = connection.cursor()
    update.message.reply_text(
        text='Я отправлю реквест в базу данных для извлечения свежей статистики в системе за сегодня (ограничение = '
             '30 записей), ждите!',
    )

    cursor.execute(""" select t1.* from 
        (
        select cast(lower(process_nm) as varchar(32)) as process_nm,
        				case when status_description='' and end_dttm is null then 'In progress' 
    					when status_description='' and end_dttm is not null then 'Success' 
        				else cast(status_description as varchar(50)) 
        				end as status_description
        				,cast(start_dttm + interval'8 hour' as timestamp (0)) as start_dttm
        				, cast(end_dttm + interval'8 hour' as timestamp (0)) as end_dttm
        				, case when end_dttm is null then cast(current_timestamp as timestamp (0)) - cast(start_dttm as timestamp (0)) 
        					else cast(end_dttm as timestamp (0)) - cast(start_dttm as timestamp (0))
        					end as exec_tm
        				, cast(user_nm as varchar(15)) as user
        				from etl_cfg.cfg_log_event 
        				where cast(current_date as timestamp (0)) - interval'8 hour' <= start_dttm + interval'8 hour'
        				order by start_dttm desc 
        				limit 40
        				) t1 
    			order by start_dttm
        				""")

    query_results = cursor.fetchall()
    #print(query_results)
    text = '\n\n'.join([', '.join(map(str, x)) for x in query_results])
    #print(text)
    bot.send_message(
        chat_id=update.message.chat.id,
        text=text
    )

    update.message.reply_text(
        text='Ответ отправлен',
    )

def button_request_rtp_handler(bot: Bot, update: Update):
    db_info = dj_database_url.config(default=DATABASELINK_ETL)
    connection = psycopg2.connect(database=db_info.get('NAME'),
                                  user=db_info.get('USER'),
                                  password=db_info.get('PASSWORD'),
                                  host=db_info.get('HOST'),
                                  port=db_info.get('PORT'))
    cursor = connection.cursor()
    update.message.reply_text(
        text='Я отправлю реквест в базу данных для извлечения свежей статистики по краткосрочному процессу за сегодня '
             '(ограничение = '
             '30 записей), ждите!',
    )

    cursor.execute("""select t1.* from
(
select cast(lower(process_nm) as varchar(32)) as process_nm,
    				case when status_description='' and end_dttm is null then 'In progress' 
					when status_description='' and end_dttm is not null then 'Success' 
    				else cast(status_description as varchar(50)) 
    				end as status_description
    				,cast(start_dttm + interval'8 hour' as timestamp (0)) as start_dttm
    				, cast(end_dttm + interval'8 hour' as timestamp (0)) as end_dttm
    				, case when end_dttm is null then cast(current_timestamp as timestamp (0)) - cast(start_dttm as timestamp (0)) 
    					else cast(end_dttm as timestamp (0)) - cast(start_dttm as timestamp (0))
    					end as exec_tm
    				, cast(user_nm as varchar(15)) as user
    				from etl_cfg.cfg_log_event 
    				where cast(current_date as timestamp (0)) - interval'8 hour' <= start_dttm + interval'8 hour'
 					and lower(process_nm) like 'rtp_%'
    				order by start_dttm desc 
    				limit 30
	) t1 order by start_dttm """)

    query_results = cursor.fetchall()
    #print(query_results)
    text = '\n\n'.join([', '.join(map(str, x)) for x in query_results])
    #print(text)
    bot.send_message(
        chat_id=update.message.chat.id,
        text=text
    )

    update.message.reply_text(
        text='Ответ отправлен',
    )

def button_request_vf_handler(bot: Bot, update: Update):
    db_info = dj_database_url.config(default=DATABASELINK_ETL)
    connection = psycopg2.connect(database=db_info.get('NAME'),
                                  user=db_info.get('USER'),
                                  password=db_info.get('PASSWORD'),
                                  host=db_info.get('HOST'),
                                  port=db_info.get('PORT'))
    cursor = connection.cursor()
    update.message.reply_text(
        text='Я отправляю реквест в базу данных для извлечения свежей статистики по долгосрочному процессу за сегодня '
             '(ограничение = '
             '30 записей), ждите!',
    )

    cursor.execute("""select t1.* from
(
select cast(lower(process_nm) as varchar(32)) as process_nm,
    				case when status_description='' and end_dttm is null then 'In progress' 
					when status_description='' and end_dttm is not null then 'Success' 
    				else cast(status_description as varchar(50)) 
    				end as status_description
    				,cast(start_dttm + interval'8 hour' as timestamp (0)) as start_dttm
    				, cast(end_dttm + interval'8 hour' as timestamp (0)) as end_dttm
    				, case when end_dttm is null then cast(current_timestamp as timestamp (0)) - cast(start_dttm as timestamp (0)) 
    					else cast(end_dttm as timestamp (0)) - cast(start_dttm as timestamp (0))
    					end as exec_tm
    				, cast(user_nm as varchar(15)) as user
    				from etl_cfg.cfg_log_event 
    				where cast(current_date as timestamp (0)) - interval'8 hour' <= start_dttm + interval'8 hour'
 					and lower(process_nm) like 'vf_%'
    				order by start_dttm desc 
    				limit 30
	) t1 order by start_dttm """)

    query_results = cursor.fetchall()
    #print(query_results)
    text = '\n\n'.join([', '.join(map(str, x)) for x in query_results])
    #print(text)
    bot.send_message(
        chat_id=update.message.chat.id,
        text=text
    )

    update.message.reply_text(
        text='Ответ отправлен',
    )

# def button_send_wolf_handler(bot: Bot, update: Update):
#     s = requests.session()
#     s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'})
#
#     r = s.get('https://www.google.ru/search?q=яблоко&tbm=isch')
#
#     soup = BeautifulSoup(r.text, "html.parser")
#
#     for text in soup.findAll(attrs={'class': 'rg_meta notranslate'}):
#         text = loads(text.text)
#         print(text["ou"])