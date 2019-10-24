"""
Get all messages need to be translated in target file, and output a `.po` file.
You can choose to translate directly or add your own translation later.

Put this in project path, or you need to change `BASE_PATH` to project path
"""
import re
import sys

BASE_PATH = sys.path[0]
DEFAULT_FILE = """# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: 2019-10-23 13:37+0800\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: pygettext.py 1.5\\n"


"""


def get_string(file_path):
    """Find all messages need to be translated in the file.

    :param file_path: relative path of the file
    :return: a list includes all the messages that need to be translated
    """
    path = BASE_PATH + '/' + file_path
    res = list()
    with open(path, 'r', encoding='utf-8')as f:
        content = f.read()
        pattern_single = re.compile(r'\W_\(\'(.*?)\'\)', re.S)
        pattern_double = re.compile(r'\W_\(\s*?\"(.*?)\"\)', re.S)
        res_single = re.findall(pattern_single, content)
        res_double = re.findall(pattern_double, content)
    for i in res_single:
        n = re.sub(r'\s{2,}', '', i)
        m = re.sub(r'(\'\'|\"\")', '', n)
        res.append(m)
    for i in res_double:
        n = re.sub(r'\s{2,}', '', i)
        m = re.sub(r'(\'\'|\"\")', '', n)
        res.append(m)
    return res


def handle_str(string_list, file):
    """Handle all message without translation"""
    res = '# from %s\n' % file
    for i in string_list:
        temp = 'msgid "%s"' % i + '\n' + 'msgstr ""\n'
        res += temp
    return res


def translate_str(string_list, file):
    """Handle all message with translation"""
    res = '# from %s\n' % file
    for i in string_list:
        translation = input(i + ' //--translation:\n')
        temp = 'msgid "%s"' % i + '\n' + 'msgstr "%s"\n' % translation
        res += temp
    return res


def write_in_file(file_name, string, entire_file):
    if entire_file:
        string = DEFAULT_FILE + string
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(string)


def main():
    message = """You can choose to output a entire `.po` file or just translation part.
Do you want to get a entire `.po` file? (Y/N)
"""
    choice = input(message)
    entire_file = True if choice == 'Y' or choice == 'y' else False
    file_path = input('Relative path of target file:\n')
    output_file_name = input('Output file name:\n')
    choice = input('Do you want to translate directly? (Y/N)\n')
    translate = True if choice == 'Y' or choice == 'y' else False
    str_list = get_string(file_path)
    if translate:
        final_string = translate_str(str_list, file_path)
    else:
        final_string = handle_str(str_list, file_path)
    write_in_file(output_file_name, final_string, entire_file)


if __name__ == '__main__':
    main()
