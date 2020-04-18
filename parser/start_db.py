# insert into film_app_genre (genre) values
# ('Аниме'),
# ('Биографии'),
# ('Боевики'),
# ('Вестерны'),
# ('Военные'),
# ('Детективы'),
# ('Документальные'),
# ('Драмы'),
# ('Исторические'),
# ('Комедии'),
# ('Криминал'),
# ('Мелодрамы'),
# ('Мультфильмы'),
# ('Мюзиклы'),
# ('Приключения'),
# ('Семейные'),
# ('Триллеры'),
# ('Ужасы'),
# ('Фантастика'),
# ('Фэнтези')


# insert into film_app_film (title, url, description, poster, year, duration) values
# ('Джей и Молчаливый Боб: Перезагрузка (2019)', 'http://kinogo-net.org/ru/1779-dzhey-i-molchalivyy-bob-perezagruzka-2019.html', 'Неугомонные приятели Джей и Молчаливый Боб попадаются на незаконном выращивании марихуаны и предстают перед судом, /''
#                        ''но невесть откуда взявшийся адвокат умудряется снять с них все обвинения, ловко подсунув бумаги на подпись. /''
#                        ''Зато теперь друзья не имеют права называться своими знаменитыми именами, потому что права на них принадлежат голливудской...', 'http://kinogo-net.org/ru/uploads/posts/2020-03/1584270413-1962305457.jpg', '2019', '105 мин. / 01:45' )

#
# insert into film_app_screenshots (film_id, screenshot) values
# (1, 'http://kinogo-net.org/ru/uploads/posts/2020-03/thumbs/1584270481-734688292-1.jpg' ),
# (1, 'http://kinogo-net.org/ru/uploads/posts/2020-03/thumbs/1584270484-493532112-2.jpg'),
# (1,'http://kinogo-net.org/ru/uploads/posts/2020-03/thumbs/1584270482-1959934958-3.jpg')


#insert into film_app_review (film_id, date, text, is_deleted, user_id) values
#(1, '2020-03-18', 'test description for 1st film', FALSE, 2 )

# insert into film_app_reviewlike (review_id, user_id) values
# (1, 3)