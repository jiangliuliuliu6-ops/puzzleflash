import os

# 定义要插入的图标标签和广告代码
favicon_tag = '<link rel="icon" href="/favicon.ico" type="image/x-icon">'
ads_code = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2745753897424989" crossorigin="anonymous"></script>'

def update_html_files():
    # 获取当前文件夹下所有 .html 文件
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    for file_name in files:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False
        # 1. 处理图标标签：如果不存在则准备插入
        if 'rel="icon"' not in content:
            if '</head>' in content:
                content = content.replace('</head>', f'    {favicon_tag}\n</head>')
                changed = True
                print(f"成功: {file_name} 已添加图标标签")

        # 2. 处理广告代码：如果不存在则准备插入
        if 'ca-pub-2745753897424989' not in content:
            if '</head>' in content:
                content = content.replace('</head>', f'    {ads_code}\n</head>')
                changed = True
                print(f"成功: {file_name} 已添加广告代码")

        # 如果有变化，写回文件
        if changed:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"跳过: {file_name} (标签已存在或未找到插入点)")

if __name__ == "__main__":
    update_html_files()