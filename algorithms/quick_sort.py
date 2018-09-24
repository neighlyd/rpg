def quick_sort(alist):
    quick_sort_helper(alist, 0, len(alist)-1)


def quick_sort_helper(alist, low, high):
    # low < high checks to see if there is more than 1 item in the list, call partition function to sort list.
    if low < high:
        split_point = partition(alist, low, high)
        quick_sort_helper(alist, low, split_point-1)
        quick_sort_helper(alist, split_point+1, high)


def partition(alist, low, high):
    pivot_index = get_pivot(alist, low, high)
    pivot_value = alist[pivot_index]
    # swap the pivot element with the first element in the list.
    alist[pivot_index], alist[low] = alist[low], alist[pivot_index]
    border = low

    # walk through list, setting up a border and throwing items in front of it if they are less than the pivot.
    # If item is thrown before border, move border up one.
    for i in range(low, high+1):
        if alist[i] < pivot_value:
            border += 1
            alist[i], alist[border] = alist[border], alist[i]
    # we move our pivot value (now [low]) into the spot where our border is (i.e. where it stopped finding items lower
    # than the pivot index's value.
    alist[low], alist[border] = alist[border], alist[low]
    # return border as index for the pivot in quick_sort_helper()
    return border


def get_pivot(alist, low, high):
    mid = (high + low) // 2
    # assume that last element is pivot.
    pivot = high
    # check for median value between the three elements.
    if alist[low] < alist[mid]:
        if alist[mid] < alist[high]:
            pivot = mid
    elif alist[low] < alist[high]:
        pivot = low
    return pivot
