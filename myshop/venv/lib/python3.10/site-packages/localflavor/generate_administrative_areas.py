import os
import os.path
current_path = os.path.abspath(os.path.curdir)

administrative_area_type = (
    ('provinces', 'province'),
    ('cantons', 'canton'),
    ('states', 'state'),
    ('municipalities', 'municipality'),
    ('prefectures', 'prefecture'),
    ('counties', 'county'),
    ('regions', 'region'),
)

import_lines = {}
administrative_areas_dict = {}

for d in os.listdir('.'):
    if len(d) > 3:
        continue
    found = False
    _dir = os.path.join(current_path, d)
    code = d.replace('_', '')
    for area_type_plural, _ in administrative_area_type:
        _module_name = f'{code}_{area_type_plural}'
        _module_path = os.path.join(_dir, _module_name + '.py')

        if os.path.isfile(_module_path):
            print(f'Found {_module_name}')
            found = True
            break

    if not found:
        other_files = [_ for _ in os.listdir(_dir) if _ not in (
            'forms.py', '__init__.py', '__pycache__') and 'postalcodes' not in _]
        if other_files:
            print(f'Found nothing in {d}, but there are {other_files}')

    if found:
        with open(_module_path) as f:
            area_type = dict(administrative_area_type)[area_type_plural].upper()
            choices_name = f'{area_type}_CHOICES'
            if choices_name in f.read():
                import_name = f'{code.upper()}_{area_type}_CHOICES'
                line = f'from .{d}.{_module_name} import {choices_name} as {import_name}'
                print(f'Found "{line}"')
                import_lines[code.upper()] = line
                administrative_areas_dict[code.upper()] = (area_type, import_name)

with open('administrative_areas.py', 'w+') as f:
    for code in sorted(import_lines.keys()):
        line = import_lines[code]
        f.write(f'{line}\n')

    f.write('\nADMINISTRATIVE_AREAS = {\n')
    for country_code in sorted(administrative_areas_dict.keys()):
        area_type, import_name = administrative_areas_dict[country_code]
        f.write(f"    '{country_code.upper()}': {{" + '\n')
        f.write(f"        'used_in_address': False," + '\n')
        f.write(f"        'type': '{area_type.lower()}'," + '\n')
        f.write(f"        'choices': {import_name}," + '\n')
        f.write('    },\n')
    f.write('}\n')
