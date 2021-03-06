import requests

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print('Status code:',r.status_code)

# 将API响应存储在一个变量中（这个API返回JSON格式的信息，使用json()将信息转换为一个字典）
response_dict = r.json()

#print(response_dict.keys())
print('Total repositories:',response_dict['total_count'])

# 仓库信息 获得了多少个仓库
repo_dicts = response_dict['items']
print('Repositories returned:',len(repo_dicts))

# 研究第一个仓库
repo_dict = repo_dicts[0]
print('\nKeys:',len(repo_dict))

for key in sorted(repo_dict.keys()):
    print(key)