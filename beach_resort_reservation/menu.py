import dataclasses
from dataclasses import field, InitVar, dataclass
from typing import Callable, List, Dict, Optional, Any

from typeguard import typechecked
from valid8 import validate

from beach_resort_reservation import menu_utils
from validation.regex import pattern


@typechecked
@dataclass(order=True, frozen=True)
class Description:
    value: str

    def __post_init__(self):
        validate('Description.value', self.value, min_len=1, max_len=900, custom=pattern(menu_utils.DESCRIPTION_REGEX))

    def __str__(self):
        return self.value


@typechecked
@dataclass(order=True, frozen=True)
class Key:
    value: str

    def __post_init__(self):
        validate('Key.value', self.value, min_len=1, max_len=10, custom=pattern(menu_utils.KEY_REGEX))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class Entry:
    key: Key
    description: Description
    on_selected: Callable[[], None] = field(default=lambda: None)
    is_exit: bool = field(default=False)

    @staticmethod
    def create(key: str, description: str, on_selected: Callable[[], None] = lambda: None,
               is_exit: bool = False) -> 'Entry':
        return Entry(Key(key), Description(description), on_selected, is_exit)


@typechecked
@dataclass(frozen=True)
class Menu:
    description: Description
    __entries: List[Entry] = field(default_factory=list, repr=False, init=False)
    __key2entry: Dict[Key, Entry] = field(default_factory=dict, repr=False, init=False)
    __is_running: List[bool] = dataclasses.field(default_factory=lambda: [True], init=False)
    create_key: InitVar[Any] = field(default='')
    auto_select: Callable[[], None] = field(default=lambda: None)
    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key)

    def _add_entry(self, value: Entry, create_key: Any) -> None:
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key)
        validate('value.key', value.key, custom=lambda v: v not in self.__key2entry)
        self.__entries.append(value)
        self.__key2entry[value.key] = value

    def _has_exit(self) -> bool:
        return bool(list(filter(lambda e: e.is_exit, self.__entries)))

    def __print(self) -> None:
        length = len(str(self.description))
        fmt = '***{}{}{}***'
        print(fmt.format('*', '*' * length, '*'))
        print(fmt.format(' ', self.description.value, ' '))
        print(fmt.format('*', '*' * length, '*'))
        self.auto_select()
        for entry in self.__entries:
            print(f'{entry.key}:\t{entry.description}')

    def __select_from_input(self) -> bool:
        while True:
            try:
                line = input(" ? ")
                key = Key(line.strip())
                entry = self.__key2entry[key]
                entry.on_selected()
                return entry.is_exit
            except (KeyError, TypeError, ValueError):
                print(menu_utils.MENU_INVALID_KEY_SELECTION)

    def run(self) -> None:
        self.__is_running[0] = True
        while self.__is_running[0]==True:
            self.__print()
            is_exit = self.__select_from_input()
            if is_exit:
                self.stop()

    def stop(self) -> None:
       self.__is_running[0]=False

    @typechecked
    @dataclass()
    class Builder:
        __menu: Optional['Menu']
        __create_key = object()


        def __init__(self, description: Description  , auto_select: Callable[[], None] = lambda:None):
            self.__menu = Menu(description=description,auto_select=auto_select, create_key= self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == Menu.Builder.__create_key

        def with_entry(self, value: Entry) -> 'Menu.Builder':
            validate('menu', self.__menu)
            self.__menu._add_entry(value, self.__create_key)
            return self

        def build(self) -> 'Menu':
            validate('menu', self.__menu)
            validate('menu.entries', self.__menu._has_exit(), equals=True)
            res, self.__menu = self.__menu, None
            return res
