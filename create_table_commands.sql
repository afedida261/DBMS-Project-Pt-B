CREATE TABLE Contacts(
    cName           VARCHAR(50) PRIMARY KEY,
    phone           CHAR(10),
    city            VARCHAR(50)
);

CREATE TABLE Applications(
    aName           VARCHAR(25) PRIMARY KEY,
    aCategory       VARCHAR(25),
    aSize           INTEGER,
    isInstalled     BIT
);

CREATE TABLE AppUsers(
    cName   VARCHAR(50),
    aName   VARCHAR(25),
    rating  INTEGER,
    PRIMARY KEY (cName, aName),
    CHECK (rating >= 1 AND rating <= 5),
    FOREIGN KEY (cName) REFERENCES Contacts ON DELETE CASCADE,
    FOREIGN KEY (aName) REFERENCES Applications ON DELETE CASCADE
);

