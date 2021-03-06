# Varya_Choice_Prize

Техническое задание

1.	Цель проекта
Цель проекта – создание ПО для розыгрыша призов среди клиентов компании. Функционал ПО предусматривает создание базы данных (далее – БД) для хранения списка клиентов, призов и ранжирование клиентов и призов на разные диапазоны в зависимости от оборота. 

2.	База данных
База данных разбита на три таблицы:
1)	Клиенты
2)	Призы
3)	Диапазоны

2.1. Клиент
Клиентская база содержит в себе следующую информацию: 
1)	Наименование клиента: текст с именем/наименованием клиента;
2)	Уникальный код идентификации клиента: x-разрядное число, позволяющее идентифицировать клиента без указания его имени/наименования;
3)	Приз: связь с призом, который выиграл этот клиент. Поле может оставаться пустым, если розыгрыш еще не состоялся;
4)	Диапазон: связь с диапазоном, к которому данный клиент принадлежит.

2.2.	Призы
База призов содержит в себе следующую информацию:
1)	Наименование приза: короткий текст, позволяющий идентифицировать приз;
2)	Текст при выигрыше: текст, всплывающий при получении данного приза клиентом;
3)	Количество доступных призов: целое число, указывающее на количество доступных для розыгрыша призов этого типа;
4)	Диапазон: связь с диапазоном, к которому данный клиент принадлежит.

2.3.	Диапазоны
База диапазонов содержит в себе следующую информацию:
1)	Наименование диапазона: произвольный текст.

3.	Интерфейс
Интерфейс ПО разбит на три основных части: 
1)	Главное меню;
2)	Окно розыгрыша;
3)	Окно взаимодействия с БД.

3.1.	Главное меню
Главное меню содержит две кнопки, открывающие окно розыгрыша и окно взаимодействия с БД.

3.2.	Окно розыгрыша
Окно розыгрыша содержит в себе два элемента: поле ввода уникального идентификатора клиента и кнопка розыгрыша. Розыгрыш призов происходит следующим образом: система проверяет, привязан ли какой-либо приз к данному клиенту. Если клиент еще не участвовал в розыгрыше, то ПО открывает другое окно, в котором выведен текст «Поздравляем! Мы дарим Вам:» и текст, соответствующий полученному призу. После этого ПО добавляет в БД запись о том, что данный клиент выиграл данный приз и уменьшает количество доступных подарков этого типа на 1.
В случае, если клиент уже получил приз, ПО открывает окно с предупреждением о том, что данный клиент уже участвовал в розыгрыше.

3.3.	Окно взаимодействия с БД
Данное окно защищено паролем (без возможности изменения) – «112233». В данном окне пользователь имеет возможность ознакомиться со всеми записями в БД о гостях, призах и диапазонах, а также удалить или добавить эти записи. В рамках окна отображена следующая информация:
1)	Клиент – имя, уникальный код идентификации клиента, диапазон и подарок (если клиент участвовал в розыгрыше)
2)	Приз – название, количество, диапазон
3)	Диапазон: название
Также в этом окне расположен элемент (кнопка), активация которого позволит динамически пересчитать количество подарков для приведения этого количества в соответствие с количеством клиентов. Такой пересчет с максимальной точностью, возможной для целых чисел, должен сохранять пропорциональное соотношение имеющихся подарков при этом количество подарков не может быть меньше одного.  

4.	Требование к дизайну
По должно отображаться в разрешении 1920х1080

