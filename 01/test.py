import main

def test_fuel_required():
  assert main.fuel_required(12) == 2
  assert main.fuel_required(14) == 2
  assert main.fuel_required(1969) == 654
  assert main.fuel_required(100756) == 33583

def test_fuel_required_with_additional_fuel():
  assert main.fuel_required_with_additional_fuel(14) == 2
  assert main.fuel_required_with_additional_fuel(1969) == 966
  assert main.fuel_required_with_additional_fuel(100756) == 50346

def test_sum_fuel_requirements():
  assert main.sum_fuel_requirements('input_test.txt', True) == 34241