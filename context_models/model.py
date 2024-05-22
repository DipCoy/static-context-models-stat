from dataclasses import dataclass, field

from custom_types import Symbol


@dataclass
class SymbolStat:
    symbol: Symbol
    count: int


@dataclass
class ContextModel:
    string: str = ''
    count: int = 0
    next_symbols_stat: dict[str, SymbolStat] = field(default_factory=dict)

    def add_next_symbol(self, symbol: Symbol) -> None:
        if symbol not in self.next_symbols_stat:
            self.next_symbols_stat[symbol] = SymbolStat(symbol=symbol, count=1)
        else:
            self.next_symbols_stat[symbol].count += 1

    @property
    def bytes_size(self) -> int:
        count_int_type_size = 4  # unsigned int
        symbol_type_size = 1

        string_size = len(self.string) * symbol_type_size
        count_size = count_int_type_size

        next_symbols_counter_size = count_int_type_size
        next_symbols_size = len(self.next_symbols_stat) * symbol_type_size
        next_symbols_counters_size = len(self.next_symbols_stat) * count_int_type_size

        return string_size + count_size + next_symbols_counter_size + next_symbols_size + next_symbols_counters_size

    def __repr__(self):
        return (f'ContextModel('
                f'string="{self.string}", '
                f'count={self.count}, '
                f'next_symbols_count={len(self.next_symbols_stat)}, '
                f'next_symbols_stat={self.next_symbols_stat.__repr__()}'
                f')')
