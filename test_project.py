from project import changeStatus, write, id_sort
import pytest

tasksArr = [
    {
        "id": 1,
        "task": "test 1",
        "status": "Pending"
    },
    {
        "id": 2,
        "task": "test 2",
        "status": "Pending"
    },
    {
        "id": 3,
        "task": "test 3",
        "status": "Pending"
    },
]
unsortedID = [
    {
        "id": 3,
        "task": "test 1",
        "status": "Pending"
    },
    {
        "id": 2,
        "task": "test 2",
        "status": "Pending"
    },
    {
        "id": 1,
        "task": "test 3",
        "status": "Pending"
    },
]


def test_id_sort():
    assert id_sort(unsortedID) == tasksArr

def test_write():
    assert write(tasksArr, 'test 4') == tasksArr
    assert write(tasksArr, 'test 5') == tasksArr

def test_changeStatus():
    assert changeStatus(tasksArr, "1 -c") == 'ID(1) is Completed.'
    assert changeStatus(tasksArr, "2 -p") == 'ID(2) is Pending.'
    with pytest.raises(ValueError):
        assert changeStatus(tasksArr, "1-c")
        assert changeStatus(tasksArr, "foo-c")

