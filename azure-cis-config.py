import argparse
import json
import subprocess


def generate_checker_map(flag):
    response = subprocess.run(
        ["lacework api get /api/v1/external/recommendations/azure"],
        shell=True,
        capture_output=True)
    checkers = json.loads(response.stdout.decode("utf-8"))['data'][0]

    checkers_131 = [
        checker for checker in checkers
        if ("131" in checker or "LW_Azure_" in checker)
    ]
    checkers_10 = [checker for checker in checkers if ("131" not in checker)]

    checkers_131.sort()
    checkers_10.sort()

    disable_map_10 = {}
    enable_map_10 = {}
    for checker in checkers_10:
        disable_map_10[checker] = 'disable'
        enable_map_10[checker] = 'enable'

    disable_map_131 = {}
    enable_map_131 = {}
    for checker in checkers_131:
        disable_map_131[checker] = 'disable'
        enable_map_131[checker] = 'enable'

    if flag == 'disable_cis_10':
        disable_10 = json.dumps(disable_map_10)
        response = subprocess.run([
            "lacework api patch /api/v1/external/recommendations/azure -d '{}'"
                .format(disable_10)
        ],
            shell=True,
            capture_output=True)
        parse_response(response)

    elif flag == 'enable_cis_10':
        enable_10 = json.dumps(enable_map_10)
        response = subprocess.run([
            "lacework api patch /api/v1/external/recommendations/azure -d '{}'"
                .format(enable_10)
        ],
            shell=True,
            capture_output=True).stdout.decode('utf-8')
        print(response)

    elif flag == 'disable_cis_131':
        disable_131 = json.dumps(disable_map_131)
        response = subprocess.run([
            "lacework api patch /api/v1/external/recommendations/azure -d '{}'"
                .format(disable_131)
        ],
            shell=True,
            capture_output=True)
        parse_response(response)

    elif flag == 'enable_cis_131':
        enable_131 = json.dumps(enable_map_131)
        response = subprocess.run([
            "lacework api patch /api/v1/external/recommendations/azure -d '{}'"
                .format(enable_131)
        ],
            shell=True,
            capture_output=True)
        parse_response(response)

    elif flag == 'disable_all':
        disable_all = json.dumps({**disable_map_131, **disable_map_10})
        response = subprocess.run([
            "lacework api patch /api/v1/external/recommendations/azure -d '{}'"
                .format(disable_all)
        ],
            shell=True,
            capture_output=True)
        parse_response(response)

    elif flag == 'enable_all':
        enable_all = json.dumps({**enable_map_131, **enable_map_10})
        response = subprocess.run([
            "lacework api patch /api/v1/external/recommendations/azure -d '{}'"
                .format(enable_all)
        ],
            shell=True,
            capture_output=True)
        parse_response(response)


def parse_response(response):
    if response.returncode > 0:
        print("ERROR Response {}".format(response.stderr.decode('utf-8')))
        exit(response.returncode)
    else:
        print(response.stdout.decode('utf-8'))


def parse_args():
    parser = argparse.ArgumentParser(description='Enable/Disable checkers')
    parser.add_argument(
        'flag',
        action='store',
        help='Flag to determine which checkers should be enabled/disbaled. '
             'Accepts one of: [disable_cis_10|enable_cis_10|disable_cis_131|enable_cis_131|enable_all|disable_all]'
    )
    parser.add_argument(
        'lacework_tenant',
        action='store',
        help=
        'The lacework tenant you wish to target. MUST match the configure tenant on your Lacework CLI.'
    )
    args = parser.parse_args()
    flag = args.flag
    lacework_tenant = args.lacework_tenant

    lacework_cli_configured_tenant = subprocess.run(
        ["lacework configure list | grep \">\" | awk '{print $3}'"],
        shell=True,
        capture_output=True).stdout.decode("utf-8").strip()

    if lacework_tenant != lacework_cli_configured_tenant:
        print("Error: Provided lacework tenant: " + lacework_tenant +
              " does not match the configured tenant on the Lacework CLI: " +
              lacework_cli_configured_tenant)
        exit(1)

    generate_checker_map(flag)


if __name__ == '__main__':
    parse_args()
