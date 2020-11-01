
from todo.custom_exceptions import UserExitException
from todo.models import BaseItem
from todo.reflection import find_classes


class BaseCommand(object):
    label: str

    def perform(self, store):
        raise NotImplementedError()


def _read_task_index(max_index):
    task_index = int(input('Input task index: '))
    if task_index < 0:
        raise IndexError('Index needs to be > 0')
    if task_index > max_index:
        raise IndexError('Index is to big')
    return task_index


class DoneCommand(BaseCommand):
    label = 'done'

    def perform(self, store):
        while True:
            try:
                task_index = _read_task_index(len(store.items) - 1)
                store.items[task_index].done = True
            except IndexError as ex:
                print(str(ex))
            else:
                break


class UndoneCommand(BaseCommand):
    label = 'undone'

    def perform(self, store):
        while True:
            try:
                task_index = _read_task_index(len(store.items) - 1)
                store.items[task_index].done = False
            except IndexError as ex:
                print(str(ex))
            else:
                break


class ListCommand(BaseCommand):
    label = 'list'

    def perform(self, store):
        if len(store.items) == 0:
            print('There are no items in the storage.')
            return

        for index, obj in enumerate(store.items):
            print('{0}: {1} {2}'.format(index, self._done_sign(obj), str(obj)))

    def _done_sign(self, obj):
        return '+' if obj.done else '-'


class NewCommand(BaseCommand):
    label = 'new'

    def perform(self, store):
        classes = self._load_item_classes()

        print('Select item type:')
        for index, name in enumerate(classes.keys()):
            print('{0}: {1}'.format(index, name))

        selection = None
        selected_key = None

        while True:
            try:
                selected_key = self._select_item(classes)
            except ValueError:
                print('Bad input, try again.')
            except IndexError:
                print('Wrong index, try again.')
            else:
                break

        selected_class = classes[selected_key]
        print('Selected: {0}'.format(selected_class.__name__))
        print()

        new_object = selected_class.construct()
        print('new:', new_object)
        store.items.append(new_object)
        print('Added {0}'.format(str(new_object)))
        print()
        return new_object

    def _load_item_classes(self) -> dict:
        # Dynamic load:
        return dict(find_classes(BaseItem))

    def _select_item(self, classes):
        selection = int(input('Input number: '))
        if selection < 0:
            raise IndexError('Index needs to be >0')
        return list(classes.keys())[selection]


class ExitCommand(BaseCommand):
    label = 'exit'

    def perform(self, _store):
        raise UserExitException('See you next time!')
