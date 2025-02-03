from django.db import connection
from django.db.models import Sum
from .models import Applications

def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def query1():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
            app.aName,
            ROUND(CAST(AVG(1.0 * app.rating) AS FLOAT), 2) as avgRating
        FROM
            InstalledAppUsers AS app
        WHERE
            app.aName IN (SELECT aName FROM HaifaApps)
        GROUP BY
            app.aName
        HAVING
            COUNT(app.cName) > 10
        ORDER BY
            avgRating DESC;
        """)
        query = dictfetchall(cursor)

    return query

def query2():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT c.cName,
               c.phone,
               COALESCE(clc.numLeadingApps, 0) AS numLeadingApps
        FROM Contacts c
        LEFT JOIN contact_leading_counts clc ON c.cName = clc.cName
        WHERE c.city = 'Haifa'
        ORDER BY numLeadingApps DESC, c.cName;
        """)

        query = dictfetchall(cursor)
    return query

def query3():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
            ad.city,
            ad.aName,
            ad.downloadCount
        FROM app_downloads ad
        JOIN max_downloads md ON ad.city = md.city
                             AND ad.downloadCount = md.maxDownloadCount
        WHERE ad.downloadCount > 2
        ORDER BY ad.city, ad.aName;
        """)
        query = dictfetchall(cursor)

    return query

def get_available_space():
    # Calculate the used space from installed apps (isinstalled = 1)
    used_space = Applications.objects.filter(isinstalled=1).aggregate(total=Sum('asize'))['total'] or 0
    return 1800 - used_space
