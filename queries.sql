--Question 1
CREATE VIEW InstalledApps AS
    SELECT aName
    FROM Applications as app
    WHERE isInstalled = 1;

CREATE VIEW InstalledAppUsers AS
    SELECT cName, AppUsers.aName, rating
    FROM AppUsers
        INNER JOIN InstalledApps
        ON AppUsers.aName = InstalledApps.aName;

CREATE VIEW HaifaApps AS
    SELECT aName
    FROM
        InstalledAppUsers
        INNER JOIN Contacts
        ON InstalledAppUsers.cName = Contacts.cName
    WHERE city = 'Haifa';

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

--Question 2
CREATE VIEW EnoughDownloads AS
SELECT
    apps.aName,
    apps.aCategory,
    AVG(AppUsers.rating) as avgRating
FROM Applications AS apps
    JOIN AppUsers ON apps.aName = AppUsers.aName
GROUP BY
    apps.aName, apps.aCategory
HAVING
    COUNT(DISTINCT AppUsers.cName) >= 22;

CREATE VIEW LeadingApps AS
SELECT
    ed.aName,
    ed.aCategory,
    ed.avgRating
FROM EnoughDownloads AS ed
WHERE ed.avgRating = (
    SELECT MAX(ed_inner.avgRating)
    FROM EnoughDownloads AS ed_inner
    WHERE ed_inner.aCategory = ed.aCategory
);

SELECT Contacts.cName,
       phone,
       COUNT(DISTINCT AppUsers.aName) as numApps
FROM Contacts
LEFT OUTER JOIN AppUsers
    ON Contacts.cName = AppUsers.cName
    AND AppUsers.aName IN (SELECT aName FROM LeadingApps)
WHERE city = 'Haifa'
GROUP BY Contacts.cName, phone
ORDER BY numApps DESC, cName;





