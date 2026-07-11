"""
PuzzleFlash SEO 修复脚本
- 5 个简版游戏页补 canonical/OG/Twitter/JSON-LD/GA4
- word-search.html 改品牌（WordMind → PuzzleFlash Word Guess）
- 4 个游戏页（snake/space-shooter/farm-idle/block-puzzle）加 GA4
- block-puzzle 修 canonical
- 3 个辅助页（about/contact/privacy）加 canonical + GA4
"""
import re
from pathlib import Path

ROOT = Path(r"D:\yy\puzzleflash-site\puzzleflash")

# ====== 通用 SEO 块构造器 ======

GA4_BLOCK = """
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JQR49JQS45"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-JQR49JQS45');
    </script>
"""


def make_game_seo(canonical_path, title, description, image_filename, schema_name,
                  schema_desc, genre_list, add_ga4=True, og_image="og-image.png"):
    """构造游戏页的 SEO 块（插在 </head> 前）"""
    if not image_filename.startswith("/"):
        image_path = f"https://puzzleflash.com/assets/images/{image_filename}"
    else:
        image_path = f"https://puzzleflash.com{image_filename}"
    og_image_url = f"https://puzzleflash.com/assets/images/{og_image}"
    genres = '","'.join(genre_list)
    ga4 = GA4_BLOCK if add_ga4 else ""
    return f"""
{ga4}    <link rel="canonical" href="https://puzzleflash.com{canonical_path}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="PuzzleFlash">
    <meta property="og:locale" content="en">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://puzzleflash.com{canonical_path}">
    <meta property="og:image" content="{image_path}">
    <meta property="og:image:secure_url" content="{image_path}">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1280">
    <meta property="og:image:height" content="720">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_path}">
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"VideoGame","name":"{schema_name}","url":"https://puzzleflash.com{canonical_path}","image":"{image_path}","description":"{schema_desc}","genre":["{genres}"],"playMode":"SinglePlayer","applicationCategory":"Game","operatingSystem":"Web Browser","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
"""


def make_simple_seo(canonical_path, title, description, add_ga4=True):
    """辅助页（about/contact/privacy）SEO 块"""
    ga4 = GA4_BLOCK if add_ga4 else ""
    return f"""
{ga4}    <link rel="canonical" href="https://puzzleflash.com{canonical_path}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="PuzzleFlash">
    <meta property="og:locale" content="en">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://puzzleflash.com{canonical_path}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
"""


# ====== 1. 5 个简版游戏页补 SEO ======

GAMES_SEO = [
    {
        "file": "2048.html",
        "title": "Block Blast 2048 - Play Free Online Merge Puzzle | PuzzleFlash",
        "description": "Play Block Blast 2048 on PuzzleFlash! A unique mix of block puzzles and 2048 math challenges. Merge numbers, blast blocks, and climb the leaderboard. No download needed!",
        "image": "2048.jpg",
        "schema_name": "Block Blast 2048",
        "schema_desc": "Block-dropping meets 2048 math. Merge numbers to reach the top.",
        "genre": ["Puzzle", "Strategy"],
    },
    {
        "file": "zombie-merge.html",
        "title": "Zombie Merge - Evolution & Defense Idle Game | PuzzleFlash",
        "description": "Merge and evolve your undead army in Zombie Merge! A thrilling idle evolution game where strategy meets survival. Play for free and discover powerful zombie mutations.",
        "image": "zombie-merge.jpg",
        "schema_name": "Zombie Merge",
        "schema_desc": "Idle evolution game where you merge zombies to build an unstoppable horde.",
        "genre": ["Idle", "Casual"],
    },
    {
        "file": "try-shoot-me.html",
        "title": "Try Shoot Me - Fast-Paced Reflex & Aim Trainer | PuzzleFlash",
        "description": "Test your reflexes in Try Shoot Me! A free online arcade shooting game where speed and precision are everything. No download required, play instantly in your browser.",
        "image": "try-shoot-me.jpg",
        "schema_name": "Try Shoot Me",
        "schema_desc": "Fast-paced reflex and aim trainer.",
        "genre": ["Action", "Arcade"],
    },
    {
        "file": "geometry-dash-lite.html",
        "title": "Play Geometry Dash Lite Unblocked - Best Rhythm Platformer | PuzzleFlash",
        "description": "Play Geometry Dash Lite for free on PuzzleFlash. Experience the ultimate rhythm-based action platformer. Jump, fly, and flip your way through dangerous passages and spiky obstacles. No download required!",
        "image": "geometry-dash-lite.png",
        "schema_name": "Geometry Dash Lite",
        "schema_desc": "Free rhythm-based platformer with jump, fly, and flip mechanics.",
        "genre": ["Arcade", "Action"],
    },
    {
        "file": "word-search.html",
        "title": "Word Guess - Free Daily Word Puzzle Game | PuzzleFlash",
        "description": "Play Word Guess free on PuzzleFlash. Guess the 5-letter word in 6 tries, train your vocabulary, and challenge your brain every day. No download needed.",
        "image": "word-search.jpg",
        "schema_name": "Word Guess",
        "schema_desc": "Guess the 5-letter word in 6 tries. Daily word puzzle.",
        "genre": ["Puzzle", "Word"],
    },
]


def insert_before_head_close(content, block):
    """在 </head> 前插入 block。失败则返回原内容。"""
    if "</head>" not in content:
        return content, False
    return content.replace("</head>", block + "</head>", 1), True


def patch_game_file(game_data, force_replace_title=False, old_title=None, new_title=None,
                    old_meta=None, new_meta=None):
    path = ROOT / "games" / game_data["file"]
    content = path.read_text(encoding="utf-8")
    original = content

    # 1) 替换 title（如果需要）
    if force_replace_title and old_title and new_title:
        content = content.replace(old_title, new_title, 1)

    # 2) 替换 author/description meta（如果需要）
    if old_meta and new_meta:
        content = content.replace(old_meta, new_meta, 1)

    # 3) 注入 SEO 块
    block = make_game_seo(
        canonical_path=f"/games/{game_data['file']}",
        title=game_data["title"],
        description=game_data["description"],
        image_filename=game_data["image"],
        schema_name=game_data["schema_name"],
        schema_desc=game_data["schema_desc"],
        genre_list=game_data["genre"],
        add_ga4=True,
    )
    content, ok = insert_before_head_close(content, block)

    if content != original and ok:
        path.write_text(content, encoding="utf-8")
        return True, f"OK ({game_data['file']})"
    return False, f"SKIP ({game_data['file']}) — already has SEO or no </head>"


# ====== 2. word-search 品牌修正 ======

def patch_word_search_brand():
    """把 WordMind 品牌改回 PuzzleFlash Word Guess。"""
    path = ROOT / "games" / "word-search.html"
    content = path.read_text(encoding="utf-8")
    original = content
    changes = []

    # 改 title
    if '<title>WordMind | Free Daily Word Puzzle Game</title>' in content:
        content = content.replace(
            '<title>WordMind | Free Daily Word Puzzle Game</title>',
            '<title>Word Guess - Free Daily Word Puzzle Game | PuzzleFlash</title>',
            1,
        )
        changes.append("title")

    # 改 author meta
    if '<meta name="author" content="WordMind">' in content:
        content = content.replace(
            '<meta name="author" content="WordMind">',
            '<meta name="author" content="PuzzleFlash">',
            1,
        )
        changes.append("author")

    # 改 description（替换 WordMind 品牌部分，但保留 Wordle 描述）
    if '<meta name="description" content="WordMind is a free daily word puzzle game where you guess the 5-letter word in 6 tries. Challenge your vocabulary and logic skills every day!">' in content:
        content = content.replace(
            '<meta name="description" content="WordMind is a free daily word puzzle game where you guess the 5-letter word in 6 tries. Challenge your vocabulary and logic skills every day!">',
            '<meta name="description" content="Play Word Guess free on PuzzleFlash. Guess the 5-letter word in 6 tries, train your vocabulary, and challenge your brain every day. No download needed.">',
            1,
        )
        changes.append("description")

    # 改 keywords
    if '<meta name="keywords" content="word game, word puzzle, daily puzzle, vocabulary game, brain game, word challenge, 5 letter word, free word game, online word game">' in content:
        content = content.replace(
            '<meta name="keywords" content="word game, word puzzle, daily puzzle, vocabulary game, brain game, word challenge, 5 letter word, free word game, online word game">',
            '<meta name="keywords" content="word guess, word game, word puzzle, daily puzzle, vocabulary game, brain game, word challenge, 5 letter word, free word game, online word game, PuzzleFlash">',
            1,
        )
        changes.append("keywords")

    return content, original, changes


# ====== 3. 4 个已有 SEO 游戏页加 GA4 ======

GAMES_NEED_GA4 = [
    "snake.html",
    "space-shooter.html",
    "farm-idle.html",
    "block-puzzle.html",
]


def add_ga4_to_existing(game_file):
    path = ROOT / "games" / game_file
    content = path.read_text(encoding="utf-8")
    if "G-JQR49JQS45" in content:
        return False, "already has GA4"
    content, ok = insert_before_head_close(content, GA4_BLOCK)
    if ok:
        path.write_text(content, encoding="utf-8")
        return True, "added"
    return False, "no </head>"


# ====== 4. block-puzzle 修 canonical ======

def fix_block_puzzle_canonical():
    path = ROOT / "games" / "block-puzzle.html"
    content = path.read_text(encoding="utf-8")
    original = content
    changes = []

    if '<link rel="canonical" href="https://blockpuzzleblitz.com/"/>' in content:
        content = content.replace(
            '<link rel="canonical" href="https://blockpuzzleblitz.com/"/>',
            '<link rel="canonical" href="https://puzzleflash.com/games/block-puzzle.html"/>',
            1,
        )
        changes.append("canonical")

    if '<meta property="og:url" content="https://blockpuzzleblitz.com/"/>' in content:
        content = content.replace(
            '<meta property="og:url" content="https://blockpuzzleblitz.com/"/>',
            '<meta property="og:url" content="https://puzzleflash.com/games/block-puzzle.html"/>',
            1,
        )
        changes.append("og:url")

    return content, original, changes


# ====== 5. 3 个辅助页加 SEO + GA4 ======

SIMPLE_PAGES = [
    {
        "file": "about.html",
        "canonical": "/about.html",
        "title": "About Us - PuzzleFlash | Premium HTML5 Gaming Portal",
        "description": "About PuzzleFlash - a premium digital destination for high-quality, free-to-play HTML5 games. Curated puzzles, action, idle, and arcade games that play instantly in any browser.",
    },
    {
        "file": "contact.html",
        "canonical": "/contact.html",
        "title": "Contact Us - PuzzleFlash",
        "description": "Get in touch with PuzzleFlash. Questions, feedback, or game suggestions? Our team usually responds within 24-48 hours.",
    },
    {
        "file": "privacy.html",
        "canonical": "/privacy.html",
        "title": "Privacy Policy - PuzzleFlash",
        "description": "PuzzleFlash privacy policy. Learn how we collect, use, and protect your information when you visit puzzleflash.com.",
    },
]


def patch_simple_page(page_data):
    path = ROOT / page_data["file"]
    content = path.read_text(encoding="utf-8")
    original = content
    if "G-JQR49JQS45" in content:
        return False, "already has GA4"
    block = make_simple_seo(
        canonical_path=page_data["canonical"],
        title=page_data["title"],
        description=page_data["description"],
        add_ga4=True,
    )
    content, ok = insert_before_head_close(content, block)
    if ok and content != original:
        path.write_text(content, encoding="utf-8")
        return True, "added"
    return False, "no </head> or no change"


# ====== 主流程 ======

def main():
    print("=" * 60)
    print("PuzzleFlash SEO 修复")
    print("=" * 60)

    # 1. word-search 品牌修正
    print("\n[1] word-search 品牌修正")
    content, original, changes = patch_word_search_brand()
    if changes:
        (ROOT / "games" / "word-search.html").write_text(content, encoding="utf-8")
        print(f"  改动: {', '.join(changes)}")
    else:
        print("  无需修改")

    # 2. 5 个简版游戏页补 SEO
    print("\n[2] 5 个简版游戏页补 SEO")
    for game in GAMES_SEO:
        ok, msg = patch_game_file(game)
        print(f"  {game['file']:30s} -> {msg}")

    # 3. 4 个已有 SEO 游戏页加 GA4
    print("\n[3] 4 个已有 SEO 游戏页加 GA4")
    for f in GAMES_NEED_GA4:
        ok, msg = add_ga4_to_existing(f)
        print(f"  {f:30s} -> {msg}")

    # 4. block-puzzle 修 canonical
    print("\n[4] block-puzzle.html 修 canonical")
    content, original, changes = fix_block_puzzle_canonical()
    if changes:
        (ROOT / "games" / "block-puzzle.html").write_text(content, encoding="utf-8")
        print(f"  改动: {', '.join(changes)}")
    else:
        print("  无需修改")

    # 5. 3 个辅助页加 SEO + GA4
    print("\n[5] 3 个辅助页加 SEO + GA4")
    for p in SIMPLE_PAGES:
        ok, msg = patch_simple_page(p)
        print(f"  {p['file']:30s} -> {msg}")

    print("\n" + "=" * 60)
    print("完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
