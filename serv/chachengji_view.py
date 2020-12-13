from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/chachengji")
async def view_lists_grades(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS cou_sn, name as cou_name FROM course ORDER BY name
        """)
        courses = list(db)

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

    return render_html(request, 'chachengji.html',
                       students=students,
                       courses=courses,
                       items=items)


@web_routes.get("/chachengji/edit/{stu_sn}")
def chachengji_edit(request):
    stu_sn = request.match_info.get("stu_sn")

    with db_block() as db:
        db.execute("""
        SELECT g.stu_sn, g.cou_sn,
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE stu_sn = %(stu_sn)s ;
        """, dict(stu_sn=stu_sn))

        items = list(db)

    return render_html(request, 'chachengji_edit.html', items=items)
