import os
import sys
import getopt
import vdf
from collections.abc import Mapping

htmlDocTemplate = '''<!DOCTYPE html>
<html lang='ko'>
<head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>맵 로테이션</title>
</head>
<body>
    <h1>맵 로테이션</h1>
    <ul>
{groups}
    </ul>
</body>
</html>'''

htmlMapGroupTemplate = '''<li>
    <p><strong>{groupName}</strong></p>
    <ul>
{options}
{maps}
    </ul>
</li>'''

htmlMapTemplate = '        <li>{mapName}</li>\r\n'
htmlOptionTemplate = '        <li>{key}: {value}</li>\r\n'

groupOptions = [
    'display-template',
    'maps_invote',
    'group_weight',
    'next_mapgroup',
    'default_min_players',
    'default_max_players',
    'default_min_time',
    'default_max_time',
    'default_allow_every',
    'command',
    'nominate_flags',
    'adminmenu_flags',
]


def main(argv):

    FILE_NAME = argv[0]      # command line arguments의 첫번째는 파일명
    MAPCYCLE_PATH = ''       # MAPCYCLE 초기화

    try:
        # opts: getopt 옵션에 따라 파싱 ex) [('-i', 'myinstancce1')]
        # etc_args: getopt 옵션 이외에 입력된 일반 Argument
        # argv 첫번째(index:0)는 파일명, 두번째(index:1)부터 Arguments
        opts, etc_args = getopt.getopt(argv[1:],
                                       'hm:', ['help', 'mapcycle='])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(FILE_NAME, '--mapcycle <umc_mapcycle path>')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        if opt in ('-h', '--help'):  # HELP 요청인 경우 사용법 출력
            print(FILE_NAME, '--mapcycle <umc_mapcycle path>')
            sys.exit()

        elif opt in ('-m', '--mapcycle'):  # 인스턴명 입력인 경우
            MAPCYCLE_PATH = arg

    if len(MAPCYCLE_PATH) < 1:  # 필수항목 값이 비어있다면
        print(FILE_NAME, '--mapcycle option is mandatory')  # 필수임을 출력
        sys.exit(2)

    if not os.path.isfile(MAPCYCLE_PATH):
        print(FILE_NAME, 'Invalid mapcycle path')
        sys.exit()
    
    with open(MAPCYCLE_PATH, 'r', encoding='UTF-8') as mapCycleFile:
        mapCycle = vdf.load(mapCycleFile)
    
    groups = ''
    
    for groupKey, groupValue in mapCycle['umc_mapcycle'].items():
        if not isinstance(groupValue, Mapping):
            continue

        options = ''
        maps = ''

        for key, value in groupValue.items():
            if key in groupOptions:
                if key == 'default_min_players':
                    options += htmlOptionTemplate.format(key='최소 인원수', value=value)
                elif key == 'default_max_players':
                    options += htmlOptionTemplate.format(key='최대 인원수', value=value)
                continue
            maps += htmlMapTemplate.format(mapName=key)
        
        groups += htmlMapGroupTemplate.format(groupName=groupKey, options=options, maps=maps)
        
    html = htmlDocTemplate.format(groups=groups)

    with open('output.html', 'w', encoding='UTF-8') as file:
        file.write(html)



if __name__ == '__main__':
    main(sys.argv)
