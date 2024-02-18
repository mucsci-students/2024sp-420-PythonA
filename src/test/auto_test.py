import sys
import os
import subprocess

# Add parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Get the current directory
current_dir = os.getcwd()
# Navigate to the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Change directory to the parent directory
os.chdir(parent_dir)

def run(input: str) -> str:
    try:
        result = subprocess.run(input, capture_output=True, text=True, check=True, shell=True)
    except subprocess.CalledProcessError:
        return 'Program terminated not as expected!'
    return result.stdout

def generate_execution_cmd(test_name: str) -> str:
    return 'cat test/{}_input.txt | python -O main.py'.format(test_name)

def generate_test_output_file(test_name: str) -> None:
    input = generate_execution_cmd(test_name)
    output = run(input=input)
    open('test/{}_output.txt'.format(test_name), 'w').write(output)

def test(test_name: str) -> bool:
    input = generate_execution_cmd(test_name)
    output = run(input=input)
    expected = open('test/{}_output.txt'.format(test_name), 'r').read()
    return output == expected

def check_test_input_file_exists(test_name: str):
    return os.path.exists('test/{}_input.txt'.format(test_name))

def check_test_output_file_exists(test_name: str):
    return os.path.exists('test/{}_output.txt'.format(test_name))

if __name__ == '__main__':
    total = 0
    input_not_found = 0
    passed = 0
    failed = 0
    skipped = 0
    for test_name in open('test/auto_test_list.txt', 'r').read().strip().split('\n'):
        total += 1
        if not check_test_input_file_exists(test_name):
            print('test: {} - input not found'.format(test_name))
            input_not_found += 1
            continue
        if check_test_output_file_exists(test_name):
            res = test(test_name)
            print('test: {} - {}'.format(test_name, 'passed' if res else 'failed'))
            if res:
                passed += 1
            else:
                failed += 1
        else:
            if input('output file of test <{}> does not exist. Type "Yes" to generate one: '.format(test_name)) == 'Yes':
                generate_test_output_file(test_name)
                print('Output file for test: <{}> has been generated'.format(test_name))
            else:
                print('test: {} - skipped'.format(test_name))
            skipped += 1
    print('passed/total: ({}/{})'.format(passed, total))
    print('input_not_found/total: ({}/{})'.format(input_not_found, total))
    print('failed/total: ({}/{})'.format(failed, total))
    print('skipped/total: ({}/{})'.format(skipped, total))
    generated = total - passed - failed - input_not_found - skipped
    if generated:
        print('generated/total: ({}/{})'.format(generated, total))