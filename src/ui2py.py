import os


def convert_ui_to_py():
    """ Конвертирование .ui в .py """
    pyuic_main_command = "pyuic5 ../ui/main.ui -o main_app.py"
    pyrcc_main_command = "pyrcc5 ../res.qrc -o res_rc.py"
    os.system(pyuic_main_command)
    os.system(pyrcc_main_command)


if __name__ == "__main__":
    convert_ui_to_py()