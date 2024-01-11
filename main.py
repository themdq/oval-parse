import xml.etree.ElementTree as ET

OVAL = "{http://oval.mitre.org/XMLSchema/oval-definitions-5}"
OVALLIN = "{http://oval.mitre.org/XMLSchema/oval-definitions-5#linux}"


def extract_criteria(element: ET.Element, operator: str, i: int) -> None:
    """Функция для парсинга критериев,
    вытаскивает логический оператор и комментарии критериев и выводит их на экран

    Args:
        element (ET.Element): Элемент (critera/criterion) из которого парсится информация
        operator (str): Логический оператор
        i (int): Количество отступов
    """
    i += 1
    for criterion in element.findall(f"{OVAL}criterion"):
        comment = criterion.get("comment")
        test_ref = criterion.get("test_ref")
        test_cond = root.find(f'.//{OVAL}tests/{OVALLIN}rpminfo_test[@id="{test_ref}"]')
        if test_cond is not None:
            object_ref = test_cond.find(f"{OVALLIN}object").get("object_ref")
            object_name = root.find(f'.//{OVAL}objects/{OVALLIN}rpminfo_object[@id="{object_ref}"]')
            object_name = f'(object - {object_name.find(f".//{OVALLIN}name").text})'
            state_ref = test_cond.find(f"{OVALLIN}state").get("state_ref")
            state_info = root.find(f'.//{OVAL}states/{OVALLIN}rpminfo_state[@id="{state_ref}"]')
            if state_info.find(f".//{OVALLIN}evr") is not None:
                evr = (
                    state_info.find(f".//{OVALLIN}evr").get("operation")
                    + " "
                    + state_info.find(f".//{OVALLIN}evr").text
                )
            else:
                evr = ""
            if state_info.find(f".//{OVALLIN}arch") is not None:
                arch = (
                    state_info.find(f".//{OVALLIN}arch").get("operation")
                    + " "
                    + state_info.find(f".//{OVALLIN}arch").text
                )
            else:
                arch = ""
            test_cond = test_cond.get("check")
            if evr == "" and arch == "":
                state = ""
            else:
                state = f"(state - {evr}; {arch})"
        else:
            test_cond = ""
            object_name = ""
            state = ""

        print(" " * i, comment, test_cond, object_name, state)
        print(" " * i, operator)
    for criteria in element.findall(f"{OVAL}criteria"):
        operator = criteria.get("operator")
        extract_criteria(criteria, operator, i)


# Для экономии памяти можно рассмотреть вариант с iterparse
tree = ET.parse(str(input("Введите путь до xml файла:")).strip(""""'"""))
root = tree.getroot()
check = "д"

for definition in root.findall(f".//{OVAL}definition"):
    if check == "д":
        print(definition.find(f".//{OVAL}title").text)
        print(f'{definition.get("id")} - {definition.get("class")}')
        print(f'Severity - {definition.find(f".//{OVAL}severity").text}')
        for item in definition.findall(f".//{OVAL}platform"):
            print(f"Platform - {item.text}")
        print(definition.find(f".//{OVAL}bugzilla").get("href"))
        print(definition.find(f".//{OVAL}issued").get("date"))
        print(definition.find(f".//{OVAL}description").text)
        print("\nCriteria:")
        extract_criteria(definition, "", 0)
        print("-" * 80)
        check = str(input("Введите 'д', чтобы продолжить или любой другой символ, чтобы остановиться:"))
    else:
        break
