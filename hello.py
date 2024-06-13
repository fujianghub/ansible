import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

# 定义教程的网址
base_url = "https://www.liaoxuefeng.com"
tutorial_url = f"{base_url}/wiki/896043488029600"

# 获取页面HTML内容的函数
def get_html_content(url):
    response = requests.get(url)
    return response.content

# 解析教程页面并创建PDF的函数
def create_pdf(tutorial_url):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 获取主页内容
    main_page_content = get_html_content(tutorial_url)
    soup = BeautifulSoup(main_page_content, "html.parser")

    # 提取教程章节和链接
    chapters = soup.select("ul.uk-nav.uk-nav-side a")
    for chapter in chapters:
        chapter_title = chapter.text.strip()
        chapter_url = base_url + chapter['href']
        
        # 添加章节标题到PDF
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(200, 10, txt=chapter_title, ln=True, align="L")
        pdf.set_font("Arial", size=12)
        
        # 获取章节内容
        chapter_content = get_html_content(chapter_url)
        chapter_soup = BeautifulSoup(chapter_content, "html.parser")
        content = chapter_soup.select_one(".x-wiki-content")

        # 添加章节内容到PDF
        if content:
            paragraphs = content.find_all(["p", "pre"])
            for paragraph in paragraphs:
                text = paragraph.get_text().encode('latin1', 'replace').decode('latin1')
                pdf.multi_cell(0, 10, text)
                
    # 保存PDF文件
    pdf.output("git_tutorial.pdf")

# 运行函数创建PDF
create_pdf(tutorial_url)
