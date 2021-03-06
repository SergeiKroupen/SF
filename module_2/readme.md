Проект 2 
Анализ данных по успеваемости учеников по программе UNICEF

По заданию необходимо будет прогнозировать риски не сдачи теста по математике. К сожалению, не ясно, какой балл на тесте является риском. Но, возможно, это станет настраиваемым параметром для повышения или понижения порога этого риска. Что лично меня удивило, в данных я не обнаружил признаков того, что кто-то получил оценки ниже 20 балоов. Анализ распределения показывает обычную "нормальную"кривую, но не от 0 а от 20 баллов. То есть, нули в датасете - это такое же событие как и пропуски. Я исключил не только пропуски, но и нули. Это стало первым этапом работы с базой.

Далее я проанализировал номинативные переменные. Многие из них содержали пропуски значений. Для некоторых из перменных я предположил логическое объясненеиие пропускам и создал дубликаты оригинальных столбцов, но с заполнением пропусков по предложенной логике. Сказать, что это улучшило результат (колрреляцию или тест Стьюдента) - не могу. Но верю, что я делал правильно. 

Оставшиеся количественные переменные показали не высокие результаты корреляции. Правда, я одно значение исправил, обнаружив, как мне кажется, причину ошибочности: поля стоят по пордяку друг за другом, и в первом поставили 385,в а во втором - 85. Это исправление существенно улучшило корреляцию между данными.

Меня удивило, что характер корреляции больше у обратно-зависимых переменных от целевого парметра. Как будто задание построено от результата, когда рост каких-то признаков негативно влияет на тест по математике. Как раз тот самый риск! 
    
Много времени и сил занял анализ номинативных перменных. Возможно надо будет научится лучше использовать объектно-оринтированны подход, чтобы автоматизировать такой анализ. С другой стороны, все равно нужно смотреть на каждую переменную отдельно. Также не совсем понятным для меня является анализ важности переменной по графикам "boxplot". Возможно, нужно еще больше изучить вопрос и потренироваться. Тоже касается и теста Стюдента.

Одна переменная оказалась дубликатом столбца, я думаю, замаскированной ошибкой, которую нужно было найти. И это меня порадоволо!

Что несомненно полезно, я узнал и применил на практике (териновочной) комплексный анализ взаимное влияния данных. Можно сказать, я сделал первый шаг в область, которая была для меня новой. Надеюсь, теперь она станет моим местом жизни.

Визуализация данных - один из важнейших инструментов в работе. По-этому я планирую особенно плотно изучить возможности, которые дают продвинутые библиотеки, так как стандартные, расмотренные и примененные, все же - это далеко не то, что нужно. С этим мы "слона не продадим"...
