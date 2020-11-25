print('\n***本脚本仅在无需更新打卡数据的情况下使用，如有数据需要更新，请进入移动校园进行打卡\n\n'
      '***默认当日14：00前补昨日打卡，14：00-24：00打当日卡，所以通常情况在14：00后运行即可\n'
      '***默认打卡区域：四川省——成都市——青羊区\n\n'
      '***选择保存账号密码，仅会在本地生成swufe_check.pass文件，不会保存到服务器端\n'
      '***忘记账号密码：进入"https://authserver.swufe.edu.cn/"找回密码\n'
      '***修改账号密码：删除pass文件重新运行脚本\n\n'
      '**如有打卡失败等问题，请联系微信：cookie_pie_yolk\n'
      '**依赖包：requests  time  datetime\n')

import requests
from time import sleep
import datetime


# 得到账号密码
try:
    with open('swufe_check.pass', 'r') as f:
        print('(1/4)自动读取账号密码……')
        form_ = f.readlines()
        form_ = eval(form_[0])
        name = form_['name']
        password = form_['password']
except FileNotFoundError:
    if_remember = input('(1/4)是否需要记住账号密码？（Y/N）')
    name = input('请输入学号：')
    password = input('请输入密码：')
    form_ = {'name': name, 'password': password}
    if if_remember == 'Y':
        f = open('swufe_check.pass', 'w')
        f.write(str(form_))
        f.close()

# 判断是否是当天14点前打卡，14点前打当日卡，14点后打隔日卡
if int(datetime.datetime.now().strftime('%H')) <= 14:
    day = 0
else:
    day = 1

print('(2/4)正在获取Cookie……')

# 更新表单需要提交的数据
data_update = {
    'mymethod': 'POST',
    'myurl': 'https://10.9.249.17/api/v1/ncp/student/daka/update',
    'id': name+(datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d'),
    't1': '否',
    't2': '',
    't3': '否',
    'stsfyc': '否',
    'stsfycxq': '',
    'dqszdpro': '{"code":"510000","name":"四川省"}',
    'dqszdcity': '{"code":"510100","name":"成都市"}',
    'dqszdreg': '{"code":"510105","name":"青羊区"}',
    'sfdgyq': '否',
    'dgyqqt': '[]'
}

# 打卡表单需要提交的数据
data_store = {
    'mymethod': 'POST',
    'myurl': 'https://10.9.249.17/api/v1/ncp/student/daka/store',
    'id': name+(datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d'),
    't1': '否',
    't2': '',
    't3': '否',
    'stsfyc': '否',
    'stsfycxq': '',
    'dqszdpro': '{"code":"510000","name":"四川省"}',
    'dqszdcity': '{"code":"510100","name":"成都市"}',
    'dqszdreg': '{"code":"510105","name":"青羊区"}',
    'sfdgyq': '否',
    'dgyqqt': '[]'
}


# 从服务器获取cookie
def get_cookie():

    form = {'user_name': name, 'password': password}
    url = 'http://www.hi-cpy.xyz:805/login/'
    response_ = requests.post(url, data=form)

    return response_.text


try:
    # requests的请求头，其实应该只需要Cookie和User—Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.193 Safari/537.36',
        'Cookie': get_cookie(),
        'host': 'swufeapp.iswufe.info',
        'Origin': 'http://swufeapp.iswufe.info',
        'Referer': 'http://swufeapp.iswufe.info/NYDXY/',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    print('(3/4)已获取Cookie，正在打卡……')

    # 准备提交表单的链接
    url_ = 'http://swufeapp.iswufe.info/jinzhi/jump.php'

    # 生成一个线程
    s = requests.session()

    '''
    data_1 = {
        'mymethod': 'GET',
        'myurl': 'https://swufeapi.swufe.edu.cn/api/v1/ncp/student/daka'
    }
    模仿第一次post
    response = s.post('http://swufeapp.iswufe.info/jinzhi/jump.php', headers=headers, data=data_1)
    print(response.text)
    模仿第二次post
    response = s.post('http://swufeapp.iswufe.info/jinzhi/owninfo.php', headers=headers)
    print(response.text)
    提交打卡信息
    '''

    # 默认均不用修改信息，所以请求表单用data_store，如果需要更新，将data_store改为data_update即可
    response = s.post(url=url_, headers=headers, data=data_store)
    html = response.text
    print('(4/4)'+eval(html)['data']['message']+'!\n三秒后自动关闭……')
    sleep(4)

    '''data = {'mymethod': 'GET',
            'myurl': 'https://swufeapi.swufe.edu.cn/api/v1/ncp/stat/current/student'}
    打卡后返回信息
    response = s.post('http://swufeapp.iswufe.info/jinzhi/jump.php', headers=headers, data=data)
    print(response.text)'''
except:
    print('Cookie获取失败，请检查账号密码是否填写正确，如再次尝试失败，请联系管理员\n三秒后自动关闭……')
    sleep(4)
