from os import system, getcwd, path, mkdir
from time import strftime
from typing import List, Callable, Optional
from tabulate import tabulate

# tabulate.WIDE_CHARS_MODE = False
dist_path = path.join(getcwd(), 'dist')

if not path.exists(dist_path):
    mkdir(dist_path)


class ColumnSettingTest:
    caption: str
    field: str
    formatter: Optional[Callable]

    def __init__(self, caption: str, field: str, formatter: Optional[Callable] = None):
        self.caption = caption
        self.field = field
        self.formatter = formatter


def console_display(column_settings: List[ColumnSettingTest], data: list, prompt_field: str, is_order_acc: bool = True):
    cols = []
    new_data = []
    has_formatter = False
    for col_setting in column_settings:
        cols.append(f'{col_setting.caption}{"（asc）" if is_order_acc else "（des）" if col_setting.field == prompt_field else ""}')
        if col_setting.formatter is not None:
            has_formatter = True
    if has_formatter:
        for d in data:
            current_data = []
            for col_setting in column_settings:
                v = d.get(col_setting.field, '') if col_setting.formatter is None \
                    else col_setting.formatter(d.get(col_setting.field, ''))
                current_data.append(v)
            new_data.append(current_data)
    else:
        new_data = data
    output_string = tabulate(new_data, headers=cols, tablefmt='grid', numalign='left', stralign='left')
    file_path = path.join(dist_path, f'output-{strftime("%Y-%m-%d %H-%M-%S")}.txt')
    f = open(file_path, 'w', encoding='utf-8')
    f.write(output_string)
    f.close()
    system(f"start /B start cmd.exe @cmd /k \"chcp 65001 | type \"{file_path}\"\"")
