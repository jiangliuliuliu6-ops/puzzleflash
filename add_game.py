import os
from PIL import Image

# 网站基础配置
DOMAIN = "PuzzleFlash"
GAMES_DIR = "games"
IMAGES_DIR = "assets/images"

# 风格统一的 HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Play {title} - {domain}</title>
    <meta name="description" content="Play {title} for free on {domain}. {desc}">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JQR49JQS45"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-JQR49JQS45');
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #facc15; --bg: #0f172a; --card-bg: #1e293b; --sidebar-bg: #020617; --text: #e5e7eb; --text-dim: #94a3b8; }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Poppins', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; display: flex; flex-direction: column; min-height: 100vh; }}
        a {{ text-decoration:none; color:inherit; transition: 0.3s; }}
        
        header {{ background: var(--sidebar-bg); padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; position: sticky; top:0; z-index: 1000; }}
        .logo {{ font-size: 26px; font-weight: 700; color: var(--primary); letter-spacing: 1px; }}
        nav a {{ margin-left: 20px; font-weight: 600; font-size: 13px; }}
        nav a:hover {{ color: var(--primary); }}

        .game-wrapper {{ flex-grow: 1; max-width: 1200px; margin: 40px auto; padding: 0 20px; width: 100%; text-align: center; }}
        .game-title {{ font-size: 28px; margin-bottom: 20px; color: var(--primary); }}
        .iframe-container {{ 
            width: 100%; max-width: 960px; height: 600px; margin: 0 auto; 
            background: #000; border: 2px solid #334155; border-radius: 12px; 
            overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        iframe {{ width: 100%; height: 100%; border: none; }}

        footer {{ text-align: center; padding: 30px; border-top: 1px solid #1e293b; color: var(--text-dim); font-size: 13px; margin-top: auto; background: var(--sidebar-bg); }}
        .footer-links {{ margin-bottom: 15px; }}
        .footer-links a {{ margin: 0 10px; text-decoration: underline; }}

        @media (max-width: 768px) {{
            .iframe-container {{ height: 400px; }}
            .logo {{ font-size: 20px; }}
            nav {{ display: none; }}
        }}
    </style>
</head>
<body>

<header>
    <a href="/" class="logo">{domain}</a>
    <nav>
        <a href="/">HOME</a>
        <a href="/about.html">ABOUT US</a>
        <a href="/privacy.html">PRIVACY POLICY</a>
        <a href="/contact.html">CONTACT</a>
    </nav>
</header>

<div class="game-wrapper">
    <h1 class="game-title">{title}</h1>
    <div class="iframe-container">
        <iframe src="{iframe_url}" allowfullscreen="true" scrolling="no"></iframe>
    </div>
</div>

<footer>
    <div class="footer-links">
        <a href="/about.html">About Us</a> | <a href="/privacy.html">Privacy Policy</a> | <a href="/contact.html">Contact Us</a>
    </div>
    <p>© 2026 {domain} - Built for Gamers.</p>
</footer>

</body>
</html>
"""

def process_image(input_img_path, slug):
    """裁剪并压缩图片为适合前台卡片的尺寸 (例如 600x300, 保持比例并优化)"""
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        
    output_path = os.path.join(IMAGES_DIR, f"{slug}.jpg")
    
    try:
        with Image.open(input_img_path) as img:
            # 转换为 RGB (防止透明 PNG 报错)
            img = img.convert('RGB')
            # 缩放并裁剪至 600x300 (2:1 比例最适合你的 height:140px 卡片)
            target_width, target_height = 600, 300
            
            # 居中裁剪逻辑
            aspect_ratio = img.width / img.height
            target_ratio = target_width / target_height
            
            if aspect_ratio > target_ratio:
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) / 2
                img = img.crop((left, 0, left + new_width, img.height))
            else:
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) / 2
                img = img.crop((0, top, img.width, top + new_height))
                
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            # 保存为 85% 质量的 JPG，平衡清晰度和加载速度
            img.save(output_path, "JPEG", quality=85)
            print(f"✅ 图片已成功处理并保存至: {output_path}")
            return True
    except Exception as e:
        print(f"❌ 图片处理失败: {e}")
        return False

def generate_game(title, desc, category, keywords, iframe_url, raw_image_path):
    # 生成文件名 (例如 "Geometry Dash Lite" -> "geometry-dash-lite")
    slug = title.lower().replace(" ", "-").replace(":", "").replace("'", "")
    
    # 1. 处理图片
    if not process_image(raw_image_path, slug):
        return

    # 2. 生成 HTML 页面
    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR)
        
    html_content = HTML_TEMPLATE.format(
        title=title,
        domain=DOMAIN,
        desc=desc,
        iframe_url=iframe_url
    )
    
    html_file_path = os.path.join(GAMES_DIR, f"{slug}.html")
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ 游戏页面已生成: {html_file_path}")

    # 3. 输出首页卡片代码
    card_code = f"""
<div class="card" data-title="{keywords.lower()}" data-category="{category}" onclick="window.location.href='/games/{slug}.html'">
    <div class="thumb"><img src="/assets/images/{slug}.jpg" alt="{title}"></div>
    <div class="card-body"><h3>{title}</h3><p>{desc}</p></div>
</div>
"""
    print("\n" + "="*50)
    print("🚀 请将以下代码复制并粘贴到 index.html 的 <div class=\"grid\" id=\"gameGrid\"> 中：")
    print(card_code)
    print("="*50 + "\n")


# ==========================================
# 在这里填入新游戏的信息，然后运行脚本即可！
# ==========================================
if __name__ == "__main__":
    # 示例：添加 Geometry Dash Lite
    generate_game(
        title="Geometry Dash Lite",
        desc="Rhythm-based action platformer.",
        category="arcade", # 可选: action, puzzle, idle, arcade, strategy
        keywords="geometry dash lite platformer rhythm action arcade",
        iframe_url="https://s.geometrydashgames.io/games/geometry-dash-lite/index.html",
        raw_image_path="raw_cover.png" # 运行前，随便把游戏原图丢进目录并命名为 raw_cover.png
    )