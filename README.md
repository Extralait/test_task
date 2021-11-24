# Graphite

### Project run
```
docker build -t web-image Back
docker-compose up
```
### Project update
```
docker-compose up -d --build
docker-compose down
```

### Run script
```
docker-compose exec web {script} 
```

### Swarm
```
docker swarm init --advertise-addr 127.0.0.1:2377
docker stack deploy -c docker-compose.yml  proj
```  
### Remove swarm 
```
docker stack rm proj
docker swarm leave --force
```

# API documentation 

## Правила формирования запросов
### Базовый URL

<i>http://159.89.37.210/api/ </i>

### Сортировка
```sh
# Упорядочить по полю username
http://example.com/api/users?ordering=username

# Упорядочить по полю username в обратном порядке
http://example.com/api/users?ordering=-username
Также можно указать несколько заказов:

# Упорядочить сначала по полю account, а затем по username
http://example.com/api/users?ordering=account,username
```

### Базовые функции поиска
```sh
# Вернет пользователей со значением поля age = 18
http://example.com/api/users?age=18

# Вернет пользователей со значением поля age < 18
http://example.com/api/users?age__lt=18

# Вернет пользователей со значением поля age <= 18
http://example.com/api/users?age__lte=18

# Вернет пользователей со значением поля age > 18
http://example.com/api/users?age__gt=18

# Вернет пользователей со значением поля age =>= 18
http://example.com/api/users?age__gte=18

# Вернет пользователей со значением поля age 5, 10 или 15
http://example.com/api/users?age__in=5,10,15

# Вернет пользователей со значением поля age от 5 до 10
http://example.com/api/users?age__range=5,10

# Вернет пользователей со значением поля name содержащем подстроку foo
http://example.com/api/users?name__incontains=foo

# Вернет пользователей со значением поля name не содержащем подстроку foo
http://example.com/api/users?name__incontains!=foo

```
### Фильтр по вложенным объектам
```sh
# Вернет пользователей, присоединившихся между 2010 и 2015 через связанную модель пользователя (o2m)
example.com/users/?profile__joined__range=2010-01-01,2015-12-31
```
### Сложный фильтр
```sh
# Комбинация нескольких условий в одном запросе
http://example.com/api/users?age__range=5,10&name__incontains=foo&profile__joined__range=2010-01-01,2015-12-31
```

### Кастомный фильтр 
```sh
# Вернет всех пользователей в радиусе 1000 км
http://159.89.37.210/api/users/?distance=1000
``` 


## Конечные точки
### Authorization 
#### Создание пользователя
<i>https://159.89.37.210/api/auth/users/ \
/auth/users/</i>
```sh
# POST ожидает 
    {
    "first_name": <str>,
    "last_name": <str>,
    "gender": <str>, (male|female)
    "avatar": <image>,
    "email": <str(email)>,
    "password": <str>
    }
```
#### Получение JWT токена
<i>https://159.89.37.210/api/auth/jwt/create/ \
/auth/jwt/create</i>
```sh
# POST ожидает
    {
        "email": <str>,
        "password": <str>
    }
    # возвращает
    {
        "refresh": <str>,
        "access": <str> 
    }
```
#### Проверка валидности JWT токена
<i>https://159.89.37.210/api/auth/jwt/verify/ \
/auth/jwt/verify</i>
```sh
# POST ожидает
    {
        "token": <str> 
    }
# При валидном токене возвращает status 200
```
### User
#### Получение текущего пользователя
<i>https://159.89.37.210/api/auth/users/me/ \
/auth/users/me/</i>
```sh
# GET возвращает
    {
        "id": <int>,
        "subscribers_quantity": <int>,
        "subscriptions_quantity": <int>,
        "last_login": <str(datetime)>,
        "is_superuser": true,
        "first_name": <str>,
        "last_name": <str>,
        "is_staff": <bool>,
        "is_active": <bool>,
        "date_joined": <str(datetime)>,
        "email": <str(email)>,
        "gender": <str>, (male|female)
        "avatar": <str(image_path)>,
        "longitude": <str(decimal)>,
        "latitude": <str(decimal)>,
        "updated_at": <str(datetime)>,
        "groups": [],
        "user_permissions": [],
  }
```
#### Получение текущего пользователя
<i>https://159.89.37.210/api/auth/users/me/ \
<i>https://159.89.37.210/api/users/{id}/ \
/auth/users/me/</i>
```sh
# PUT,PATCH принимают
    {
        "id": <int>,
        "is_superuser": <bool>,
        "first_name": <str>,
        "last_name": <str>,
        "is_staff": <bool>,
        "is_active": <bool>,
        "gender": <str>, (male|female)
        "avatar": <image>,
        "longitude": <decimal>,
        "latitude": <decimal>,
        "groups": <array(int)>,
        "user_permissions": <array(int)>,
   }
   # Экстра поля для staff
   {
        "is_active": <bool>,
   }
   # Экстра поля для superuser
   {
        "is_superuser": <bool>,
        "is_staff": <bool>,
        "groups": <array(int)>,
        "user_permissions": <array(int)>
   }
```
#### Подписка на пользователя
<i>http://159.89.37.210/api/users/{id}/match/ \
/users/{id}/match/</i>
```sh
# GET возвращает
    {
        'is_subscribed': <bool>
    }
# POST (без тела) подписывает на пользователя
# DELETE отменяет подписку на пользователя
```

