CREATE TABLE members (
    email CHAR,
    passwd CHAR,
    name CHAR,
    byear INT,
    faculty CHAR
);

CREATE TABLE books (
    book_id INT,
    title CHAR,
    author CHAR,
    pyear INT
);

CREATE TABLE borrowings (
    bid INT,
    member CHAR,
    book_id INT,
    start_date DATE,
    end_date DATE
);

CREATE TABLE penalties (
    pid INT,
    bid INT,
    amount CHAR,
    paid_amount CHAR
);

CREATE TABLE reviews (
    rid INT,
    book_id INT,
    member CHAR,
    rating INT,
    rtext CHAR,
    rdate DATE
);