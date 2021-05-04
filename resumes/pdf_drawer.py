import reportlab.rl_config, reportlab, io
from reportlab.pdfgen          import canvas
from reportlab.pdfbase         import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from textwrap                  import wrap

from .models                   import Resume

reportlab.rl_config.warnOnMissingFontGlyphs = 0

pdfmetrics.registerFont(TTFont('Typo_PapyrusM', 'Typo_PapyrusM.ttf'))

def draw(resume_id):
    buffer             = io.BytesIO()
    careers            = Resume.objects.get(id=resume_id).career_set.all()
    career_information = ''
    resume             = Resume.objects.get(id=resume_id)

    wraped_introdution = "\n".join(wrap(resume.introduction, 30))

    p     = canvas.Canvas(buffer)
    title = p.beginText()
    title.setFont('Typo_PapyrusM', 22)
    title.setCharSpace(2)
    title.setTextOrigin(70, 770)
    title.textLines(f"""
                {resume.title}

                {resume.name}
                {resume.email}
                {resume.phone_number}

                {wraped_introdution}

            """)
    description = p.beginText()
    description.setFont('Typo_PapyrusM', 18)
    description.setCharSpace(1)
    description.setTextOrigin(70, 570)

    for career in careers:
        start_working = '0000-00-00'
        end_working   = '9999-99-99'
        if career.is_working:
            start_working = career.start_working
            end_working   = career.end_working

        wraped_description = "\n".join(wrap(career.description, 30))
        career_information += \
            f"""
                경력
                회사 이름 : {career.company_name}
                재직 기간 : {start_working}~{end_working}
                직책     : {career.department}
                업무 내용 : {wraped_description}
                """
    description.textLines(f"""
                {career_information}
            """)
    p.line(40, 750, 550, 750)
    p.line(40, 650, 550, 650)
    p.line(40, 590, 550, 590)
    p.rect(20, 50, 550, 750, 1, fill=0)

    p.drawText(title)
    p.drawText(description)
    p.showPage()
    p.save()

    buffer.seek(0)

    return buffer