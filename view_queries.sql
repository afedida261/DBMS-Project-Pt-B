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

--Question 2
CREATE VIEW app_stats AS
SELECT a.aName,
       a.aCategory,
       AVG(au.rating) AS avgRating,
       COUNT(DISTINCT au.cName) AS downloadCount
FROM Applications a
JOIN AppUsers au ON a.aName = au.aName
GROUP BY a.aName, a.aCategory
HAVING COUNT(DISTINCT au.cName) >= 22;

CREATE VIEW leading_apps AS
    SELECT s1.aName,
           s1.aCategory
    FROM app_stats s1
    WHERE s1.avgRating = (
        SELECT MAX(s2.avgRating)
        FROM app_stats s2
        WHERE s2.aCategory = s1.aCategory
    );

CREATE VIEW contact_leading_counts AS
    SELECT au.cName,
           COUNT(DISTINCT au.aName) AS numLeadingApps
    FROM AppUsers au
    WHERE au.aName IN (SELECT aName FROM leading_apps)
    GROUP BY au.cName;

--Question 3
CREATE VIEW exceeding_contacts AS
    SELECT c.cName
    FROM Contacts c
    JOIN AppUsers au on c.cName = au.cName
    JOIN Applications a on au.aName = a.aName
    GROUP BY c.cName
    HAVING SUM(a.aSize) > 1200;

CREATE VIEW exceeding_cities AS
    SELECT c.city
    FROM Contacts c
    LEFT JOIN exceeding_contacts ec ON c.cName = ec.cName
    GROUP BY c.city
    HAVING COUNT(*) = COUNT(ec.cName);

CREATE VIEW app_downloads AS
    SELECT c.city,
           au.aName,
           COUNT(DISTINCT c.cName) AS downloadCount
    FROM Contacts c
    JOIN AppUsers au on c.cName = au.cName
    WHERE c.city IN (SELECT city FROM exceeding_cities)
    GROUP BY c.city, au.aName;


CREATE VIEW max_downloads AS
    SELECT city,
              MAX(downloadCount) AS maxDownloadCount
    FROM app_downloads
    GROUP BY city;