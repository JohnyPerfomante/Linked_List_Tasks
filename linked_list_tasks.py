class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def _repeat_until(count, step):
    if count == 0:
        return False
    if count == 1:
        return step()

    middle = count // 2
    if _repeat_until(middle, step):
        return True
    return _repeat_until(count - middle, step)


def _run_until_done(step, block_size=1):
    if _repeat_until(block_size, step):
        return
    _run_until_done(step, block_size * 2)


def build_list(values):
    dummy = ListNode()
    tail = dummy
    index = 0

    def append_node():
        nonlocal tail, index
        if index == len(values):
            return True
        tail.next = ListNode(values[index])
        tail = tail.next
        index += 1
        return False

    _run_until_done(append_node)
    return dummy.next


def to_list(head):
    values = []
    current = head

    def collect():
        nonlocal current
        if current is None:
            return True
        values.append(current.val)
        current = current.next
        return False

    _run_until_done(collect)
    return values


def _reverse_list(head):
    previous = None
    current = head

    def reverse_one():
        nonlocal previous, current
        if current is None:
            return True
        following = current.next
        current.next = previous
        previous = current
        current = following
        return False

    _run_until_done(reverse_one)
    return previous


# 1. Об'єднання двох відсортованих списків
def merge_two_lists(list1, list2):
    dummy = ListNode()
    tail = dummy
    first = list1
    second = list2

    def append_smallest():
        nonlocal tail, first, second
        if first is None:
            tail.next = second
            return True
        if second is None:
            tail.next = first
            return True

        if first.val <= second.val:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next
        tail = tail.next
        return False

    _run_until_done(append_smallest)
    return dummy.next


# 2. Видалення дублікатів із відсортованого списку
def delete_duplicates(head):
    if head is None or head.next is None:
        return head

    if head.val == head.next.val:
        head.next = head.next.next
        return delete_duplicates(head)

    head.next = delete_duplicates(head.next)
    return head


# 3. Виявлення циклу: повільний і швидкий вказівники
def has_cycle(head):
    slow = head
    fast = head
    found = False

    def advance():
        nonlocal slow, fast, found
        if fast is None or fast.next is None:
            return True

        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            found = True
            return True
        return False

    _run_until_done(advance)
    return found


# 4. Перевпорядкування L0 -> Ln -> L1 -> Ln-1 -> ...
def reorder_list(head):
    if head is None or head.next is None:
        return

    slow = head
    fast = head

    def find_middle():
        nonlocal slow, fast
        if fast.next is None or fast.next.next is None:
            return True
        slow = slow.next
        fast = fast.next.next
        return False

    _run_until_done(find_middle)
    second_half = slow.next
    slow.next = None
    right = _reverse_list(second_half)
    left = head

    def interleave():
        nonlocal left, right
        if right is None:
            return True

        left_next = left.next
        right_next = right.next
        left.next = right
        right.next = left_next
        left = left_next
        right = right_next
        return False

    _run_until_done(interleave)


# 5. Видалення вузла без доступу до голови списку
def delete_node(node):
    current = node

    def shift_value():
        nonlocal current
        following = current.next
        current.val = following.val
        if following.next is None:
            current.next = None
            return True
        current = following
        return False

    _run_until_done(shift_value)


# 6. Подвоєння числа, представленого цифрами у вузлах
def double_it(head):
    if head.val >= 5:
        head = ListNode(0, head)

    current = head

    def double_digit():
        nonlocal current
        if current is None:
            return True

        carry = 1 if current.next is not None and current.next.val >= 5 else 0
        current.val = (current.val * 2) % 10 + carry
        current = current.next
        return False

    _run_until_done(double_digit)
    return head


# 7. Об'єднання k відсортованих списків
def merge_k_lists(lists):
    def merge_range(start, stop):
        if start >= stop:
            return None
        if stop - start == 1:
            return lists[start]

        middle = (start + stop) // 2
        left = merge_range(start, middle)
        right = merge_range(middle, stop)
        return merge_two_lists(left, right)

    return merge_range(0, len(lists))


# 8. Розворот вузлів повними групами по k
def reverse_k_group(head, k):
    if head is None or k == 1:
        return head

    dummy = ListNode(0, head)
    previous_group = dummy

    def reverse_group():
        nonlocal previous_group
        kth = previous_group

        def find_next():
            nonlocal kth
            if kth.next is None:
                return True
            kth = kth.next
            return False

        if _repeat_until(k, find_next):
            return True

        first = previous_group.next
        current = first
        previous = kth.next

        def reverse_one():
            nonlocal previous, current
            following = current.next
            current.next = previous
            previous = current
            current = following
            return False

        _repeat_until(k, reverse_one)
        previous_group.next = previous
        previous_group = first
        return False

    _run_until_done(reverse_group)
    return dummy.next


# 9. Стабільний поділ списку відносно x
def partition(head, x):
    lower_dummy = ListNode()
    upper_dummy = ListNode()
    lower_tail = lower_dummy
    upper_tail = upper_dummy

    def distribute(node):
        nonlocal lower_tail, upper_tail
        if node is None:
            return

        following = node.next
        node.next = None
        if node.val < x:
            lower_tail.next = node
            lower_tail = node
        else:
            upper_tail.next = node
            upper_tail = node
        distribute(following)

    distribute(head)
    lower_tail.next = upper_dummy.next
    return lower_dummy.next


if __name__ == "__main__":
    print("1. Об'єднання двох відсортованих списків:")
    print(to_list(merge_two_lists(build_list([1, 2, 4]), build_list([1, 3, 4]))))
    print(to_list(merge_two_lists(build_list([]), build_list([]))))
    print(to_list(merge_two_lists(build_list([]), build_list([0]))))

    print("\n2. Видалення дублікатів:")
    print(to_list(delete_duplicates(build_list([1, 1, 2]))))
    print(to_list(delete_duplicates(build_list([1, 1, 2, 3, 3]))))

    print("\n3. Наявність циклу:")
    cycle_first = build_list([3, 2, 0, -4])
    cycle_first.next.next.next.next = cycle_first.next
    print(has_cycle(cycle_first))
    cycle_second = build_list([1, 2])
    cycle_second.next.next = cycle_second
    print(has_cycle(cycle_second))
    print(has_cycle(build_list([1])))

    print("\n4. Перевпорядкування списку:")
    reorder_first = build_list([1, 2, 3, 4])
    reorder_list(reorder_first)
    print(to_list(reorder_first))
    reorder_second = build_list([1, 2, 3, 4, 5])
    reorder_list(reorder_second)
    print(to_list(reorder_second))

    print("\n5. Видалення заданого вузла:")
    delete_first = build_list([4, 5, 1, 9])
    delete_node(delete_first.next)
    print(to_list(delete_first))
    delete_second = build_list([4, 5, 1, 9])
    delete_node(delete_second.next.next)
    print(to_list(delete_second))

    print("\n6. Подвоєння числа:")
    print(to_list(double_it(build_list([1, 8, 9]))))
    print(to_list(double_it(build_list([9, 9, 9]))))

    print("\n7. Об'єднання k відсортованих списків:")
    print(to_list(merge_k_lists([
        build_list([1, 4, 5]),
        build_list([1, 3, 4]),
        build_list([2, 6]),
    ])))
    print(to_list(merge_k_lists([])))
    print(to_list(merge_k_lists([build_list([])])))

    print("\n8. Розворот груп по k вузлів:")
    print(to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 2)))
    print(to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 3)))

    print("\n9. Поділ списку відносно x:")
    print(to_list(partition(build_list([1, 4, 3, 2, 5, 2]), 3)))
    print(to_list(partition(build_list([2, 1]), 2)))
    