
## Базовая структура приложения

3 основных блока:
* package main - название пакета, в котором находится данный файл. Должен быть объявлен на первой строке. Пакет main - неотъемлемая часть проекта, без него проект не запустится.
* import "<название библиотеки>" (Пример import "fmt", пакет из стандартной библиотеки) - импортирует пакет и позволяет использовать его методы/функции.
* func main() - функция main. Основная функция (обязательно должна быть). По сути - является точкой входа в приложении.

Пример 
```go
package main

import "fmt"


func main() {
	fmt.Println("Hello world!")
}
```

**В go для строк используются только двойные кавычки!**
## Команды
Запуск: `go run main.go`

Сделать бинарный файл: `go build main.go`


## Переменные/константы
В go существуют разные способы объявления переменных. Самый простой
```go
message := "Hello world!"
```
**Примечание**. В Go не позволяет создавать переменную, которая нигде не используется! 

Конструкция `:=` используется только при объявлении переменной. В случае если мы хотим изменить переменную можно использовать просто `=`.
```go
message := "Hello world!"
message = 'Hi world!'
```

Второй метод создания переменных.

```go
var <название переменной> <тип переменной>
```
или с неизменяемым значением.
```go
const <название переменной> <тип переменной> = <Значение>
```

Пример
```go
var message string
const book string = 'Гарри Поттер'
```

**Примечание**. Можно также не прописывать тип используемой переменной. Go может определить его самостоятельно в случае, если мы сразу даём значение переменной.
```go
var message = 'Hello world!'
```

В случае, если тип указан неверно, то мы получим ошибку (так как язык статически типизированный).

Пример:
```go
var message int;
message = 'Hello world!'
```

Комментарии в Go задаются при помощи `//`.

Для определения типа используется метод `TypeOf` из стандартной библиотеки `reflect`
Пример
```go
package main

  

import (
	"fmt"
	"reflect"
)

func main() {
	message := "Hello world!"
	fmt.Println(message)
	fmt.Println(reflect.TypeOf(message))
}
```

Также в Go существует концепция **Нулевого значения**. Например для string нулевое значение - пустая строка, для типа int - 0. Присвается в том случае, если для переменной не задано значение

Например Данный код выведет ноль и пустую строку.
```go
package main

import "fmt"

func main() {
	var num int
	var message string
	fmt.Println(num)
	fmt.Println(message)
}
```

Также Go поддерживает **множественное присвоение.** Когда в одной строке мы присваиваем несколько значений.
```go
package main


import "fmt"

func main() {
	var a,b,c int = 1,2,3
	a, b = 4, 5
	fmt.Println(a,b,c)
}
```

Аналогично с Python можно использовать и фиктивные переменные
```go
package main


import "fmt"

func main() {
	var a,b,c int = 1,2,3
	a, _, b = 4, 5, 6
	fmt.Println(a,b,c)
}
```

## Типы
### Целочисленные типы

Ряд типов представляют целые числа:

- int8: представляет целое число от -128 до 127 и занимает в памяти 1 байт (8 бит)
    
- int16: представляет целое число от -32768 до 32767 и занимает в памяти 2 байта (16 бит)
    
- int32: представляет целое число от -2147483648 до 2147483647 и занимает 4 байта (32 бита)
    
- int64: представляет целое число от –9 223 372 036 854 775 808 до 9 223 372 036 854 775 807 и занимает 8 байт (64 бита)
    
- uint8: представляет целое число от 0 до 255 и занимает 1 байт
    
- uint16: представляет целое число от 0 до 65535 и занимает 2 байта
    
- uint32: представляет целое число от 0 до 4294967295 и занимает 4 байта
    
- uint64: представляет целое число от 0 до 18 446 744 073 709 551 615 и занимает 8 байт
    
- byte: синоним типа `uint8`, представляет целое число от 0 до 255 и занимает 1 байт
    
- rune: синоним типа `int32`, представляет целое число от -2147483648 до 2147483647 и занимает 4 байта
    
- int: представляет целое число со знаком, которое в зависимости о платформы может занимать либо 4 байта, либо 8 байт. То есть соответствовать либо int32, либо int64.
    
- uint: представляет целое беззнаковое число только без знака, которое, аналогично типу int, в зависимости о платформы может занимать либо 4 байта, либо 8 байт. То есть соответствовать либо uint32, либо uint64.
### Числа с плавающей точкой

Для представления дробных чисел есть два типа:

- float32: представляет число с плавающей точкой от 1.4*10-45 до 3.4*1038(для положительных). Занимает в памяти 4 байта (32 бита)
    
- float64: представляет число с плавающей точкой от 4.9*10-324 до 1.8*10308 (для положительных) и занимает 8 байт.
### Комплексные числа

Существуют отдельные типы для представления комплексных чисел:

- complex64: комплексное число, где вещественная и мнимая части представляют числа float32
    
- complex128: комплексное число, где вещественная и мнимая части представляют числа float64
### Тип bool

Логический тип или тип bool может иметь одно из двух значений: true (истина) или false (ложь).

### Строки

Строки представлены типом string. В Go строке соответствует строковый литерал - последовательность символов, заключенная в двойные кавычки

## Арифметические операции
Основные арифметические операции в Go

1. Сложение: `+`
2. Вычитание: `-`
3. Умножение: `*`
4. Деление: `/`
5. Остаток от деления (modulo): `%` (в этой операции могут принимать участие только целочисленные операнды)
6. Постфиксный инкремент (x++). Увеличивает значение переменной на единицу
7. Постфиксный декремент (x--). Уменьшает значение переменной на единицу

Аналогично с Python можно использовать +=, -= и т.д.
## Операции сравнения
1. Равенство: `==`
2. Неравенство: `!=`
3. Больше: `>`
4. Меньше: `<`
5. Больше или равно: `>=`
6. Меньше или равно: `<=`

## Логические операции
1. И (логическое И): `&&`
2. Или (логическое ИЛИ): `||`
3. Отрицание (логическое НЕ): `!`
## Функции

По сути - кусок кода, который можно использовать неограниченное количество раз в разных частях кода.

Пример
```go
package main

import "fmt"

func main() {
	print()
	print()
	print()
}


func print() {
	fmt.Println("Вызов print()")
}
```

В функции существуют ещё две концепции:
* Передаваемые значения - значения (аргументы), которые принимает функция при её вызове. Аргумент указывается с типом. Аргументы могут быть обязательными и не обязательными.
Пример
```go
package main


import "fmt"


func main() {
	print("a")
	print("b")
	print("c")
}

  

func print (message string) {
	fmt.Println(message)
}
```

* Возвращаемое значение - то значение, которое вернётся из функции после её выполнения. В случае наличия возвращаемого значения его тип тоже обязательно указывается.
Пример
```go
package main

import "fmt"


func main() {
	var message = sayHello("Mark", 23)
	// message := sayHello("Mark") так тоже можно
	print(message)
}


func print (message string) {
	fmt.Println(message)
}


func sayHello (name string, age int) string {
	return fmt.Sprintf("Привет %s! Тебе %d", name, age)
}```

**Примечание**. В Go форматирование строк осуществляется при помощи метода `fmt.Sprintf()`. Для каждого типа свой "символ" для подстановки. Для строки - %s, а для числа %d.

Также Go позволяет передавать неограниченное количество аргументов. 
Пример
```go
package main


import "fmt"


func main() {
	printNumbers(1,2,3,4,5)
}


func printNumbers(numbers ...int) {
	fmt.Println(numbers)
}
```

Также в Go есть возможность использовать анонимные функции. При запуске программы произойдёт вызов функции `func()`. На практике обычно используется для горутин и замыканий.
```go
package main

import "fmt"


func main() {
	func(){
		fmt.Println("123")
	}()
}
```

## Условные операторы
В Go для условных операторов используются кодовые слова:
* if
* else if
* else
Пример
```go
package main

import "fmt"


func main() {
	message, flag := enterTheClub(18)
	fmt.Println(message, flag)
}


func enterTheClub (age int) (string, bool) {
	if age >= 18 && age < 45 {
		return "Можно", true
	} else if age >= 45{
		return "Вам точно это надо?", true
	} else {
		return "Нельзя", false
	}
	// return "Нельзя", false -> можно без else. Такой вариант предпочтительнее.
}
```

Если в коде есть количество практически одинаковых условий, то можно использовать конструкцию `switch/case/default`. Она позволяет нам проверять значение одной переменной. Так длинную цепь условий читать намного удобнее.
Если ни одно значение не проходит, то можно задать дефолтное значение, которое вернётся в случае, если ни одно значение не прошло.

Пример
```go
package main

  
import (
	"errors"
	"fmt"
	"log"
)

func main() {
	day, err := calendar("пн")
	if err != nil {
		log.Fatal(err)
	}
	
	fmt.Println(day)
} 


func calendar(dayOfWeek string) (int, error) {
	switch dayOfWeek {
		case "пн":
			return 1, nil
		
		case "вт":
			return 2, nil
		
		case "ср":
			return 3, nil
		
		case "чт":
			return 4, nil
		
		case "пт":
			return 5, nil
		
		case "сб":
			return 6, nil
		
		case "вс":
			return 7, nil
		
		default:
			return 0, errors.New("not valid day")
	}
}
```
## Обработка ошибок. Тип error

В Go есть специальный тип для ошибок. При помощи него мы можем например вернуть ошибку из функции). Нулевым типов для типа `error` является `nil`. Для создания ошибок нужно использовать встроенную библиотеку `errors`, туда же можно написать свой текст. По правилам Go текст должен быть написан на английском с маленькой буквы, быть достаточно коротким и информативным. **Ошибка всегда принимается последним аргументом**. Далее ошибка при вызове функции обрабатывается.

Пример
```go
package main

  

import (
	"errors"
	"fmt"
	"log"
)

func main() {
	message, err := enterTheClub(1 )
	if err != nil {
		log.Fatal(err)
		return
	}

	fmt.Println(message)
}

func enterTheClub (age int) (string, error) {
	if age >= 18 && age < 45 {
		return "Можно", nil
	} else if age >= 45{
		return "Вам точно это надо?", nil
	}
 
	return "Нельзя", errors.New("you so young")
}
```
**Примечание**. В примере используется встроенная библиотека `log`. Она позволяет логировать какие-либо данные. По сути аналог `fmt` с некоторыми особенностями для логов.

## Массивы

Массивы в Go представляют собой последовательность элементов определённого типа. var numbers <число элементов> <тип элементов>
Пример (массив из пяти элементов)
```go
var number[5]int
```
При таком определении все значения массива равны 0.

Пример с указанием элементов массива
```go
var numbers [5]int = [5]int{1,2,3,4,5}
```

Также при инициализации массива можно указать только несколько элементов, недостающие заменятся нулями.

```go
var numbers [5]int = [5]int{1,2}
```

Если в квадратных скобках вместо количества элементов указывается троеточие, то количество элементов массива будет исходить из количества переданного в него значений.

```go
var numbers =[...]int{1,2,3,4,5}
```

**Примечание**. Длина массива является частью его типа. И, к примеру, следующие два массива представляют разные типы данных, хотя они и хранят данные одного типа

Пример
```go
package main

import "fmt"


func main() {
	var numbers = [5]int{1,2,3,4,5}
	var numbers2 = [4]int{1,2,3,4}	
	numbers=numbers2
	fmt.Println(numbers)	
	fmt.Println(numbers2)
}

// Ошибка.cannot use numbers2 (variable of type [4]int) as [5]int value in assignment
```

Для получения значения из массива в Go используются индексы - номер элемента (начинается с нуля). Для обращения по индексу используется `<массив>[индекс]`.

Пример
```go
package main


import "fmt"


func main() {
	var numbers = [5]int{1,2,3,4,5}
	fmt.Println(numbers[1])
}
```

При этом можно задать свои, "кастомные" индексы. Которые будут выступать в роли ключей. Они могу распологаться в любом порядке, но не должны выходить за рамки длины массива (для массива из двух элементов максимальный индекс - 1).

Пример:
```go
package main

import "fmt"


func main() {
	var numbers = [2]string{1: "a", 0: "b"}
	fmt.Println(numbers[1])
}
```

Также каждый элемент в массиве можно изменить, обратившись к нему по индексу.

Пример:
```go
package main

import "fmt"


func main() {
	messages := [5]int{1,2,3,4,5}	
	messages[1] = 10
	fmt.Println(messages[1]) // 10
}
```

Массив также может использовать как аргумент функции 
```go
package main

import (
	"errors"
	"fmt"
)


func main() {
	messages := [5]int{1,2,3,4,5}
	printMessages(messages)
}

  

func printMessages(messages [5]int) error {
	if len(messages) == 0 {
		errors.New("empty array")
	}

	fmt.Println(messages)
	return nil
}
```

**ВАЖНО**. Массивы с разной длиной - разные типы.


## Слайсы

Слайсы - по сути обёртка над массивами. По сути массив без указания длины. Инициализация слайса:
```go
messages := []int{1,2,3}
```

При изменении значения слайса (по индексу) в другой функции меняется и исходных массив. При передаче в функцию не копируется значение, а передаётся ссылка.
Пример 
```go
package main


import (
	"fmt"
)


func main() {
	messages := []int{1,2}
	chnageMessages(messages)
	fmt.Println(messages)
}


func chnageMessages(messages []int) {	
	messages[1] = 3
	fmt.Println(messages)
}
```

**По сути мы перезаписали значение в массиве, на который ссылается данный слайс.**

Нулевое значение слайса - пустой слайс (`[]`)

В случае расширения слайса (массива) возникает так называемая **паника** (о ней ниже).

```go
var messages []string
messages[0] = "a"
// Компилятор не покажет ошибку, но при запуске она возникнет
```

Также слайс можо инициализировать при помощи команды `make`.
```go
messages := make([]string, 5)
```

Слайс можно расширить при помощи команды `append`. Принимает массив и элементы для добавления **МАССИВ ТАКИМ ОБРАЗОМ УВЕЛИЧИТЬ НЕЛЬЗЯ**
```go
package main

import (
	"fmt"
)


func main() {
	messages := make([]int, 5)
	messages = append(messages, 1, 2)
	fmt.Println(len(messages)) // 7
}
```

Также третьим параметром можно указать так называемый `capacity` (можно перевести как ёмкость). Без указания равна длине массива. При добавлении нового элемента (расширении слайса), происходит переалакация, т.е. увеличивается capacity (в два раза от текущего значения при меньших значениях). По сути под капотом копируется массив в новый массив в два раза большей ёмкости. Для просмотра его ёмкости можно использовать функцию `cap`. Операция не самая дешёвая, однако поэтому go и увеличивает capacity с запасом. 

При больших значениях увеличивает уже не в два раза, а меньше (см. документацию).

Пример
```go
func main() {
	messages := make([]int, 5)
	fmt.Println(len(messages)) // 5
	fmt.Println(cap(messages)) // 5
	
	messages = append(messages, 1, 2)
	fmt.Println(len(messages)) // 7
	fmt.Println(cap(messages)) // 10
}
```


Двумерные массивы и слайсы задаются следующим образом

Массив
```go
matrix := [][]int{10}
```

Слайс
```go
matrix := make([][]int, 10)
```

## Замыкание

Функция, которая ссылается на свободные/независимые переменные. Другими словами функция при замыкании запоминает состояние, при котором она была создана.

Пример
```go
package main

import "fmt"


func main() {
	inc := increment()
	inc()
	inc()
	inc()
	val := inc()
	
	fmt.Println(val)
}

  

func increment() func() int {
	count := 0
	
	return func() int {
		count ++
		return count	
	}

}
```

Пояснение к примеру: переменная count является локальной переменной для функции increment. Но при каждом вызове inc (именно при вызове inc, increment здесь возвращает функцию, а сама функция возвращает число) мы обращаемся к переменной count.


## Функция init

init - зарезервированное слово для функции. Функция вызывается при инициализации пакета. **Функция init всегда срабатывает перед вызовом функции main.**

Пример
```go
package main
 

import "fmt"


var msg string

func init() {
	msg = "from init"
}


func main() {
	fmt.Println(msg)
}
```


## Указатели
Указатели представляют собой объекты, значением которых служат адреса других объектов (например, переменных).

Указатель определяется как обычная переменная, только перед типом данных ставится символ звездочки `*`. 
```go
var p *int
```

Нулевой тип указателя - nil. Изменить значение указателя можно изменив его номер в ячейке. Например, указав номер другой переменной.
```go
var p *int
number := 5

p=&number // теперь p и number хранят в себе номер ячейки в памяти
```

Если для переменной необходимо указать значение (вместо номера ячейки в памяти), то можно использовать так называемый **дереференсинг**.

```go
var p *int
*p = 10
fmt.Println(p) // 10
```

**Примечание**. При изменении переменной в другой функции (Например при помощи +=) создаётся новая переменная (по сути копия). 

Пример
```go
package main


import "fmt"
  

func main() {
	msg := "from"
	changeMessage(msg)
	fmt.Println(msg)
}


func changeMessage(msg string) {
	msg += " changed"
	fmt.Println(msg)
}

// Вывод: 
// from changed
// from
```

Т.е. функция changeMessage создала новую переменную и не изменила переменную в main. Обе переменные имеют разный адрес в оперативной памяти. Условно говоря `0x1234` и `0x1235`.

В случае, если мы хотим изменить исходную переменную (использовать исходную ячейку памяти), то стоит использовать `*<тип аргумента>` при дефиниции функции и передавать указатель на тип string (о указателях ниже) как `<&переменная>`.

Пример
```go
package main


import "fmt"


func main() {
	msg := "from"
	changeMessage(&msg) // Передаём ссылку (область в памяти)
	fmt.Println(msg)
	// fmt.Println(&msg) // Вывод номера ячейки памяти

}

  
  

func changeMessage(msg *string) {
	*msg += " changed" //Изменяем значение исходной переменной
}

//Вывод: from changed
```


## Цикл for

Выполняется, пока условие истинно.
Пример
```go
for x:=0; x<10; x++ {
	fmt.Println(x)
}
```

Бесконечный цикл можно создать, создав условие всегда равное true.

**Каждый из элементов (x<10; x++) можно убрать**.

Примеры
```go
for x:=0; x<10; {
	fmt.Println(x)
}

for x:=0; x<10 {
	// Чтобы цикл был конечным, то нужно делать инкрементацию в цикле (x++)
	fmt.Println(x)
}


x:=0
for true {
	x++
	fmt.Println(x)
}
```

В Go существует специальная конструкция `range` для работы со слайсами/массивами. Она позволяет пройти циклом по длине слайса (делать то количество итераций, которое равно его длине). При итерации мы можем получить индексы и значения внутри 

Пример
```go
package main


import (
	"fmt"
)

  
  

func main() {
	messages := [4]string{"a", "b", "c", "d"}
	for index, value := range messages { // Если value не обязателен, то его можно не писать. Если не обязателен индекс, то вместо него можно постваить _ (фиктивную переменную)
		fmt.Println(index, value)
	}
}
```

Для остановки цикла можно использовать функцию `break`.
```go
func main() {
	messages := []string{"a", "b", "c", "d"}
	messages = append(messages, "d")
	for index, value := range messages {
		if value == "c" {
			break
		}
		fmt.Println(index, value)
	}
}
```
## Матрица

Базовый пример матрицы (связанного списка) в Go.
```go
package main

import (
	"fmt"
)


func main() {
	matrix := make([][]int, 10)
	for x := 0; x<10; x++ {
		for y := 0; y<10; y++ {
			matrix[y] = make([]int, 10)
			matrix[y][y] = x
		}
	fmt.Println(matrix[x])
	}
}
```

## Паника

Паника - ситуация, когда компилятор не показывает ошибку, но она возникает при запуске программы.

Один из примеров, когда к слайсу добавляется какой-то значение (без append).
Панику можно вызвать самому при помощи функции `panic`.

**Необработанные паники прекращают работу приложения. Это принципиально отличает их от ошибок, которые позволяют не обрабатывать себя.**

Примеры
```go
package main

func main() {
	panic("aaaaaaaaa help")
}
```

Чтобы обработать панику нужно использовать кодовое слово `recover`.
```go
package main

import "fmt"

func main() {
	defer handlePanic()

	messages := []string{"a", "b", "c"}
	messages[3] = "d"
	fmt.Println("Абра") // Не сработает, так как сверху паника функция заканчивает работу (перед этим сработает defer)
}

  
func handlePanic() {

	if r := recover(); r != nil { // r - просто название переменной.
		fmt.Println(r)
	}

	fmt.Println("Паника успешно обработана")
}

// Вывод Паника успешно обработана
```
## Кодовое слово defer

Кодовое слово defer позволяет откладывать выполнение функции (при вызове) перед тем, как функция выйдет из приложения.

Пример

```go
package main


import "fmt"
  
func main() {
	defer printMessages()
	fmt.Println("main")
}
 

func printMessages() {
	fmt.Println("From messages")
}

// Вывод: main \n From messages
```

Вызов defer имеет небольшое over head (добавляет ~50мс к выполнению).


## Мапы

Мапа - словарь.

Пример
```go
package main

import "fmt"


func main() {
	users := map[string]int{
		"mark": 12,
		"petya": 23,
		"ivan": 55,
	}
	fmt.Println(users)
}

// Вывод: map[ivan:55 mark:12 petya:23]
```

Для получения значения
```go
users := map[string]int{
	"mark": 12,
	"petya": 23,
	"ivan": 55,
}

fmt.Println(users["mark"]) //12
```

Также мы можем:
1. Проверять существование элемента
```go
users := map[string]int{
	"mark": 12,
	"petya": 23,
	"ivan": 55,
}

age, exists = users["mark"] // 12, true
```

2. Изменять элемент
```go
users["mark"] = 14
```

3. Пройтись циклом по мапе
```go
for key, value := range users {
	fmt.Println(key, value)
}
```

4. Удалять элемент
```go
delete(users, "mark")
```

5. Инициализировать в make()
```go
make(map[string]int)
```


## Структуры и кастомные типы

Структура - это кастомный тип. Который может хранить набор дополнительных полей. Может обладать различными методами. На основе структуры мы можем объекты (объекты этой структуры). По сути похожа на класс.

Пример
```go
package main


import (
	"fmt"
)

func main() {
	user := struct{
		name string
		age int
		gender string
		weight int
		height int
	} {"Mark", 23, "Male", 100, 196,}

	fmt.Printf("%+v\n", user) // Печать в формате {name:Mark age:23 gender:Male weight:100 height:196}

}
```

**Переинициализировать данную структуру нельзя.** Для того, чтобы её можно было переинициализировать, используется `type`.

Пример (наиболее популярная практика)

```go
package main


import (
	"fmt"
)  

type User struct{
	name string
	age int
	gender string
	weight int
	height int
}
	
func main() {
	user := User{"Mark", 23, "Male", 100, 196,}
	fmt.Printf("%+v\n", user)
}
```

Также можно обратиться к конкретному полю структуры
```go
user := User{"Mark", 23, "Male", 100, 196,}
fmt.Println(user.name)
```


### Конструктор

Конструктор - это функция, которая инициализирует структуру/тип.

Пример
```go
package main

import (
	"fmt"
)
  

type User struct{
	name string
	age int
	gender string
	weight int
	height int
}


func NewUser (name string, age int, gender string, weight int, height int) User {

	return User{
		name: name,
		age: age,
		gender: gender,
		weight: weight,
		height: height,
	}

}

  
func main() {
	user := NewUser("Mark", 23, "Male", 100, 196)
	fmt.Println(user)
}
```

### Методы

Методы бывает  двух типов. 
* ValueReveiver 
```go
package main

import (
	"fmt"
)


type User struct{
	name string
	age int
	gender string
	weight int
	height int
}


func (u User) printUserInfo(name string) {
	u.name = name
	fmt.Println(u.name, u.age, u.gender, u.weight, u.height)
}
  

func NewUser (name string, age int, gender string, weight int, height int) User {
	return User{
		name: name,
		age: age,
		gender: gender,
		weight: weight,
		height: height,
	}
}


func main() {
	user := NewUser("Mark", 23, "Male", 100, 196)
	user.printUserInfo("Petya")
	fmt.Println(user.name) // Petya 23 Male 100 196
						   // Mark
}
```

* PointerReceiver
```go
package main

import (
	"fmt"
)


type User struct{
	name string
	age int
	gender string
	weight int
	height int
}


func (u *User) printUserInfo(name string) {
	u.name = name
	fmt.Println(u.name, u.age, u.gender, u.weight, u.height)
}
  

func NewUser (name string, age int, gender string, weight int, height int) User {
	return User{
		name: name,
		age: age,
		gender: gender,
		weight: weight,
		height: height,
	}
}


func main() {
	user := NewUser("Mark", 23, "Male", 100, 196)
	user.printUserInfo("Petya")
	fmt.Println(user.name) // Petya 23 Male 100 196
						   // Petya
}
```

Разница в том, в ValueReceiver мы работает только со значением, а в PointerReceiver мы работаем с областью памяти (ссылочным объектом). Следовательно во втором варианте изменённое значение сохраняется (см. Выводы в примерах)

### Кастомные типы

Пример создания типа
```go
type Age int
```

Этот пример удобен тем, что теперь для Age мы можем создавать кастомные типы, а для обычного int не можем.

Пример
```go
type Age int

func (a Age) isAdult() bool {
	return a>=18
}
```

Кастомные типы можно использовать и в структурах.

```go
type Age int

func (a Age) isAdult() bool {
	return a>=18
}

type User struct {
	name string
	age Age
	...
}
```


## Интерфейсы
Это своего рода _определение_. Он определяет и описывает конкретные методы, которые должны быть у _какого-то другого типа_.

Пример интерфейса
```go
package main

  
import (
	"fmt"
	"math"
)
  

type Shape interface {
	Area() float32
}


type Square struct {
	side float32
}


func (s Square) Area() float32 {
	return s.side * s.side
}


type Circle struct {
	radius float32
}


func (c Circle) Area() float32 {
	return c.radius * c.radius * math.Pi
}


func main() {
	square := Square{5}
	circle := Circle{8}

	printShapeArea(square)
	printShapeArea(circle)
}


func printShapeArea(shape Shape) {
	fmt.Println(shape.Area())
}
```

### Type switch
```go
func printInterface(i interface{}) {
	switch value := i.(type) {
		case int:
			fmt.Println("int", value)
		case bool:
			fmt.Println("bool", value)
		default:
			fmt.Println("unknown type", value)
	}
}
```


## Пакеты и система модулей

В Go есть система модулей. 
Создаётся следующим образом
```go
go mod init <название модуля>
```

Команда создаёт файл go.mod формата
```go.mod
module goland-ninja
go 1.23.4
```

В этом файле будут храниться все необходимые зависимости. Далее можно запустить:
```go
go mod download
```
Которая запустит все необходимые зависимости. 

Также это позволяет разбивать проект на пакеты и выполнять навигацию.
Пример:
1. Запустим команду `go mod init golang-ninja`
2. Создадим папку `shape`
3. В `shape` создадим файл `shape.go` со следующим содержимым:
```go
package shape // Название пакета должно отличаться

import (
	"fmt"
	"math"
)  

type Shape interface {
	Area() float32
}


type Square struct {
	side float32
}


func (s Square) Area() float32 {
	return s.side * s.side
}


type Circle struct {
	radius float32
}


func (c Circle) Area() float32 {
	return c.radius * c.radius * math.Pi
}


func main() {
	square := Square{5}
	circle := Circle{8}

	printShapeArea(square)
	printShapeArea(circle)
}


func printShapeArea(shape Shape) {
	fmt.Println(shape.Area())
}


func NewSquare(length float32) Square {
	return Square{
		side: length,
	}
}
```

4. Теперь можно импортировать `shape.go` из `main.go`
```go
package main

import (
	"fmt"
	"goland-ninja/shape"
)  

func main() {
	square := shape.NewSquare(5)
	fmt.Println(square)
}
```


**ПРИМЕЧАНИЕ**. В Go область видимости для импорта определяется при помощи регистра. Т.е. получить доступ к `side` из `Square` вне модуля невозможно. (т.к. side - с маленькой буквы).

Следовательно такая структура
```go
square := shape.Square{5}
```

Вызовет ошибку. Чтобы избежать её можно создать конструктор для работы с square.
```go
	square := shape.NewSquare(5)
```

Для добавления внешний пакетов (например с GitHub)

```go
go get: <название модуля>
```

Пример
```go
go get github.com/zhashkevych/scheduler
```

Теперь файл `go.mod` выглядит следующим образом
```go
module goland-ninja

go 1.23.4  

require github.com/zhashkevych/scheduler v1.0.0 // indirect
```

Теперь для импорта
```go
import (
	"fmt"
	"goland-ninja/shape"
	"github.com/zhashkevych/scheduler" // внешний модуль
)
```


## Дженерики

Дженерик - позволяет выполнять обобщения типов.

Пример
Для того, чтобы посчитать суммы для int64 и float64 нам нужно использовать две функции
```go
package main
  
import "fmt"


func main() {
	a := []int64{1,2,3}
	b := []float64{1.1, 2.2, 3.3}

	res_int64 := sumOfInt64(a)
	res_float64 := sumOfFloat64(b)

	fmt.Println(res_int64)
	fmt.Println(res_float64)
}


func sumOfInt64(arr []int64) int64 {
	var result int64

	for _, number := range arr {
		result += number
	}

	return result
}


func sumOfFloat64(arr []float64) float64 {
	var result float64

	for _, number := range arr {
		result += number
	}

	return result
}
```

Это не сильно удобно. Вместо этого можно использовать дженерики.
```go
package main

  

import "fmt"


func main() {
	a := []int64{1,2,3}
	b := []float64{1.1, 2.2, 3.3}

	fmt.Println(sum(a))
	fmt.Println(sum(b))
}


func sum[V int64 | float64](arr []V) V {
	var result V

	for _, number := range arr {
		result += number
	}

	return result
}
```

Функция sum принимает интерфейс типов int64 или float64.

Также интерфейс можно создать напрямую
```go
package main

  

import "fmt"

type Number interface {
	int64 | float64
}

func main() {
	a := []int64{1,2,3}
	b := []float64{1.1, 2.2, 3.3}

	fmt.Println(sum(a))
	fmt.Println(sum(b))
}


func sum[V Number](arr []V) V {
	var result V

	for _, number := range arr {
		result += number
	}

	return result
}
```

