import numpy
import pytest
import sys
import math
import numpy as np

sys.path.insert(1, '../src/')

from src.window_logic import ResearchCalc, ErrorCodes


@pytest.fixture()
def calculator():
    return ResearchCalc()


def test_calc_semi_array_performance(calculator):
    """ Проверка на работоспособность при работе с массивами чисел """
    print('\n\n** Проверка работоспособности функции calc_semi при работе с массивами чисел. **\n')
    list_data = [36, 30, 26, 39, 49, 43, 53, 53, 56, 50, 25, 48]
    print('Введенный массив чисел:' + str(list_data))
    analytic_data = [42.33333333333333, 110.05555555555588, -485.25925925929914, -15207.879629630595, 12]
    print('Результат, рассчитанный аналитически: {' + ", ".join("%.4f" % f for f in analytic_data) + '}')
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: {' + ", ".join("%.4f" % f for f in input_data) + '}')

    assert np.allclose(analytic_data, input_data)


def test_calc_semi_histogram_performance(calculator):
    """ Проверка на работоспособность при работе с гистограммами """
    print('\n\n** Проверка работоспособности функции calc_semi при работе с гистограммами. **\n')
    list_data = [[2, 0], [3, 5], [4, 14], [5, 6]]
    print('Введенная гистограмма чисел: ' + str(list_data))
    analytic_data = [4.04, 0.43840000000000146, -0.012672000000037542, -0.1387673600004291, 25]
    print('Результат, рассчитанный аналитически: {' + ", ".join("%.4f" % f for f in analytic_data) + '}')
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: {' + ", ".join("%.4f" % f for f in input_data) + '}')

    assert np.allclose(analytic_data, input_data)


def test_calc_semi_array_small_tolerance(calculator):
    """ Проверка на работоспособность при работе с массивами чисел """
    print('\n\n** Проверка работоспособности функции calc_semi при работе с массивами очень маленьких чисел. **\n')
    list_data = (0.0000000362123, 0.0000000305123, 0.0000000286123, 0.0000000389123, 0.0000000479123)
    print('Введенный массив чисел:' + str(list_data))
    analytic_data = [3.64323*10 ** -8, 4.68376*10 ** -17, 1.68502*10 ** -25, -2.1064*10 ** -33, 5]
    print('Результат, рассчитанный аналитически: ' + str(analytic_data))
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert np.allclose(analytic_data, input_data)


def test_calc_semi_array_big_tolerance(calculator):
    """ Проверка на работоспособность при работе с массивами чисел """
    print('\n\n** Проверка работоспособности функции calc_semi при работе с массивами больших чисел. **\n')
    list_data = [36212349, 30512348, 28612348, 38912348, 47912347, 8912348]
    print('Введенный массив чисел:' + str(list_data))
    analytic_data = [95537044/3, 1297969964900003/9, -33813496227444724150000/27, -126756460437225535280000000000/27, 6]
    print('Результат, рассчитанный аналитически: ' + str(analytic_data))
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: ' + ", ".join("%.0f" % f for f in input_data))

    assert np.allclose(analytic_data, input_data)


def test_calc_semi_array_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с массивами чисел """
    print('\n\n** Проверка на отказоустойчивость при работе с массивами чисел. **\n')
    list_data = [36, 'hello', 26, 39, 'help', 43, 53, 53, 56, 'sun', 'good', 48]
    print('Введенный массив чисел:' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_STR_ARRAY.')
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_STR_ARRAY


def test_calc_semi_histogram_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с гистограммами """
    print('\n\n** Проверка на отказоустойчивость при работе с гистограммами. **\n')
    list_data = [[2, 'trip'], [3, 5], ['cat', 14], [5, 6]]
    print('Введенная гистограмма чисел: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_STR_HISTOGRAM.')
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_STR_HISTOGRAM


def test_calc_semi_histogram_fault_str_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с гистограммами """
    print('\n\n** Проверка на отказоустойчивость при работе с гистограммами. **\n')
    list_data = [[2, 0], (3, 5), [9, 14], [5, 6]]
    print('Введенная гистограмма чисел: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_STR_ARRAY.')
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_STR_ARRAY


def test_calc_semi_histogram_type_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с гистограммами """
    print('\n\n** Проверка на отказоустойчивость при работе с гистограммами. **\n')
    list_data = [[2, 5, 7], [3, 5, 8, 9], [0, 4, 6, 1, 14], [5]]
    print('Введенная гистограмма чисел: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_TYPE_HISTOGRAM.')
    input_data = calculator.calc_semi(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_TYPE_HISTOGRAM


def test_calc_three_points_performance(calculator):
    """ Проверка на работоспособность при работе с трехточками """
    print('\n\n** Проверка на работоспособность при работе с трехточками. **\n')
    list_data = [4.04, 0.43840000000000146, -0.012672000000037542, -0.1387673600004291, 25]
    print('Введенные данные: ' + str(list_data))
    analytic_data = [[3.027, 0.216], [4.040, 0.561], [5.025, 0.223]]
    print('Результат, рассчитанный аналитически: ' + str(analytic_data))
    input_data = calculator.calc_three_points(list_data)
    # print('Результат работы функции:' + str(input_data))
    str_itog = '[[' + str(", ".join("%.3f" % f for f in input_data[0])) + '], ['
    str_itog += str(", ".join("%.3f" % f for f in input_data[1])) + '], ['
    str_itog += str(", ".join("%.3f" % f for f in input_data[2])) + ']]'
    print('Результат работы функции: ' + str_itog)

    bool_flags = False
    for i in range(len(analytic_data)):
        if np.allclose(analytic_data[i], input_data[i], 0.001, 0.001):
            bool_flags = True
        else:
            bool_flags = False

    assert bool_flags


def test_calc_three_points_count_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с трехточками """
    print('\n\n** Проверка на отказоустойчивость при работе с трехточками. **\n')
    list_data = [4.04, 0.43840000000000146, -0.012672000000037542, -0.1387673600004291, 25, 35]
    print('Введенные данные: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_ELEMENT_COUNT.')
    input_data = calculator.calc_three_points(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_ELEMENT_COUNT


def test_calc_three_points_numeric_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с трехточками """
    print('\n\n** Проверка на отказоустойчивость при работе с трехточками. **\n')
    list_data = ['4.04', 0.43840000000000146, -0.012672000000037542, '25', '35']
    print('Введенные данные: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_NOT_NUMERIC.')
    input_data = calculator.calc_three_points(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_NOT_NUMERIC


def test_calc_three_points_dispersion_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с трехточками """
    print('\n\n** Проверка на отказоустойчивость при работе с трехточками. **\n')
    list_data = [4.04, 0, -0.012672000000037542, 25, 35]
    print('Введенные данные: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_DISPERSION_ZERO.')
    input_data = calculator.calc_three_points(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_DISPERSION_ZERO

def test_calc_three_points_root_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с трехточками """
    print('\n\n** Проверка на отказоустойчивость при работе с трехточками. **\n')
    list_data = [0, 0.01, 1, 0, 35]
    print('Введенные данные: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_UNDER_ROOT_NEGATIVE.')
    input_data = calculator.calc_three_points(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_UNDER_ROOT_NEGATIVE


def test_calc_three_points_q_zero_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с трехточками """
    print('\n\n** Проверка на отказоустойчивость при работе с трехточками. **\n')
    list_data = [0, 1, 0, -3, 35]
    print('Введенные данные: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_Q_ZERO.')
    input_data = calculator.calc_three_points(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_Q_ZERO


def test_calc_three_points_q_eccentricity_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с трехточками """
    print('\n\n** Проверка на отказоустойчивость при работе с трехточками. **\n')
    list_data = [0, 1, 1, -2, 35]
    print('Введенные данные: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_Q_ECCENTRICITY.')
    input_data = calculator.calc_three_points(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_Q_ECCENTRICITY


def test_calc_three_points_probability_fault_tolerance(calculator):
    """ Проверка на отказоустойчивость при работе с трехточками """
    print('\n\n** Проверка на отказоустойчивость при работе с трехточками. **\n')
    list_data = [0, 0.01, 0, 0, 35]
    print('Введенные данные: ' + str(list_data))
    print('Ожидаемый результат: ErrorCodes.ERROR_PROBABILITY_NOT_1.')
    input_data = calculator.calc_three_points(list_data)
    print('Результат работы функции: ' + str(input_data))

    assert input_data == ErrorCodes.ERROR_PROBABILITY_NOT_1



