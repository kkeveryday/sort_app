import sys
from PyQt5 import QtWidgets
import random
from GUI.SortingTheList import sort


class Sort(QtWidgets.QMainWindow, sort.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.clearButton.clicked.connect(self.btnClear)
        self.bubbleButton.clicked.connect(self.btnBubble)
        self.selectionButton.clicked.connect(self.btnSelection_sort)
        self.insertionButton.clicked.connect(self.btnInsertion_sort)
        self.heapButton.clicked.connect(self.btnHeap_sort)
        self.mergeButton.clicked.connect(self.btnMerge_sort)
        self.quickButton.clicked.connect(self.btnQuick_sort)
        self.delButton.clicked.connect(self.btnDel)

    def btnClear(self):
        self.listWidget.clear()
        self.sortWidget.clear()

    def btnDel(self):
        self.lineEdit.clear()

    # Пузырьковая сортировка
    def btnBubble(self):
        listValue = [int(i) for i in self.lineEdit.text().split(',')]
        # Устанавливаем swapped в True, чтобы цикл запустился хотя бы один раз
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(listValue) - 1):
                if listValue[i] > listValue[i + 1]:
                    # Меняем элементы
                    listValue[i], listValue[i + 1] = listValue[i + 1], listValue[i]
                    # Устанавливаем swapped в True для следующей итерации
                    swapped = True

        self.listWidget.addItem(str(listValue))
        self.sortWidget.addItem('Пузырьковая')

    # Сортировка выборкой
    def btnSelection_sort(self):
        listValue = [int(i) for i in self.lineEdit.text().split(',')]
        # Значение i соответствует кол-ву отсортированных значений
        for i in range(len(listValue)):
            # Исходно считаем наименьшим первый элемент
            lowest_value_index = i
            # Этот цикл перебирает несортированные элементы
            for j in range(i + 1, len(listValue)):
                if listValue[j] < listValue[lowest_value_index]:
                    lowest_value_index = j
            # Самый маленький элемент меняем с первым в списке
            listValue[i], listValue[lowest_value_index] = listValue[lowest_value_index], listValue[i]

        self.listWidget.addItem(str(listValue))
        self.sortWidget.addItem('Выборкой')

    # Сортировка вставками
    def btnInsertion_sort(self):
        listValue = [int(i) for i in self.lineEdit.text().split(',')]
        # Сортировку начинаем со второго элемента, т.к. считается, что первый элемент уже отсортирован
        for i in range(1, len(listValue)):
            item_to_insert = listValue[i]
            # Сохраняем ссылку на индекс предыдущего элемента
            j = i - 1
            # Элементы отсортированного сегмента перемещаем вперёд, если они больше
            # элемента для вставки
            while j >= 0 and listValue[j] > item_to_insert:
                listValue[j + 1] = listValue[j]
                j -= 1
            # Вставляем элемент
            listValue[j + 1] = item_to_insert

        self.listWidget.addItem(str(listValue))
        self.sortWidget.addItem('Вставками')

    # Пирамидальная сортировка
    def btnHeap_sort(self):
        def heapify(nums, heap_size, root_index):
            # Индекс наибольшего элемента считаем корневым индексом
            largest = root_index
            left_child = (2 * root_index) + 1
            right_child = (2 * root_index) + 2
            # Если левый потомок корня — допустимый индекс, а элемент больше,
            # чем текущий наибольший, обновляем наибольший элемент
            if left_child < heap_size and nums[left_child] > nums[largest]:
                largest = left_child
            # То же самое для правого потомка корня
            if right_child < heap_size and nums[right_child] > nums[largest]:
                largest = right_child
            # Если наибольший элемент больше не корневой, они меняются местами
            if largest != root_index:
                nums[root_index], nums[largest] = nums[largest], nums[root_index]
                # Heapify the new root element to ensure it's the largest
                heapify(nums, heap_size, largest)

        listValue = [int(i) for i in self.lineEdit.text().split(',')]
        n = len(listValue)
        # Создаём Max Heap из списка
        # Второй аргумент означает остановку алгоритма перед элементом -1, т.е.
        # перед первым элементом списка
        # 3-й аргумент означает повторный проход по списку в обратном направлении,
        # уменьшая счётчик i на 1
        for i in range(n, -1, -1):
            heapify(listValue, n, i)
        # Перемещаем корень Max Heap в конец списка
        for i in range(n - 1, 0, -1):
            listValue[i], listValue[0] = listValue[0], listValue[i]
            heapify(listValue, i, 0)

        self.listWidget.addItem(str(listValue))
        self.sortWidget.addItem('Пирамидальная')

    # Сортировка слиянием
    def btnMerge_sort(self):
        def merge(left_list, right_list):
            sorted_list = []
            left_list_index = right_list_index = 0
            # Длина списков часто используется, поэтому создадим переменные для удобства
            left_list_length, right_list_length = len(left_list), len(right_list)
            for _ in range(left_list_length + right_list_length):
                if left_list_index < left_list_length and right_list_index < right_list_length:
                    # Сравниваем первые элементы в начале каждого списка
                    # Если первый элемент левого подсписка меньше, добавляем его
                    # в отсортированный массив
                    if left_list[left_list_index] <= right_list[right_list_index]:
                        sorted_list.append(left_list[left_list_index])
                        left_list_index += 1
                    # Если первый элемент правого подсписка меньше, добавляем его
                    # в отсортированный массив
                    else:
                        sorted_list.append(right_list[right_list_index])
                        right_list_index += 1
                # Если достигнут конец левого списка, элементы правого списка
                # добавляем в конец результирующего списка
                elif left_list_index == left_list_length:
                    sorted_list.append(right_list[right_list_index])
                    right_list_index += 1
                # Если достигнут конец правого списка, элементы левого списка
                # добавляем в отсортированный массив
                elif right_list_index == right_list_length:
                    sorted_list.append(left_list[left_list_index])
                    left_list_index += 1
            return sorted_list

        def merge_sort(nums):
            # Возвращаем список, если он состоит из одного элемента
            if len(nums) <= 1:
                return nums

            # Для того чтобы найти середину списка, используем деление без остатка
            # Индексы должны быть integer
            mid = len(nums) // 2

            # Сортируем и объединяем подсписки
            left_list = merge_sort(nums[:mid])
            right_list = merge_sort(nums[mid:])

            # Объединяем отсортированные списки в результирующий
            return merge(left_list, right_list)

        listValue = [int(i) for i in self.lineEdit.text().split(',')]
        self.listWidget.addItem(str(merge_sort(listValue)))
        self.sortWidget.addItem('Слиянием')

    # Быстрая сортировка
    def btnQuick_sort(self):
        def quick_sort(nums):
            if len(nums) <= 1:
                return nums
            else:
                q = random.choice(nums)
            l_nums = [n for n in nums if n < q]

            e_nums = [q] * nums.count(q)
            b_nums = [n for n in nums if n > q]
            return quick_sort(l_nums) + e_nums + quick_sort(b_nums)

        listValue = [int(i) for i in self.lineEdit.text().split(',')]
        self.listWidget.addItem(str(quick_sort(listValue)))
        self.sortWidget.addItem('Быстрая')


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Sort()  # Создаём объект класса Calculator
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()









