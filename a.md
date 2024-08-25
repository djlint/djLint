```sql
CREATE TABLE Groups (
    gr_id NUMBER PRIMARY KEY,
    gr_name VARCHAR2(100) NOT NULL,
    gr_temp VARCHAR2(50) NOT NULL
);

CREATE TABLE Analysis (
    an_id NUMBER PRIMARY KEY,
    an_name VARCHAR2(100) NOT NULL,
    an_cost NUMBER(10, 2) NOT NULL,
    an_price NUMBER(10, 2) NOT NULL,
    an_group NUMBER,
    CONSTRAINT fk_an_group FOREIGN KEY (an_group) REFERENCES Groups (gr_id)
);

CREATE TABLE Orders (
    ord_id NUMBER PRIMARY KEY,
    ord_datetime TIMESTAMP NOT NULL,
    ord_an NUMBER,
    CONSTRAINT fk_ord_an FOREIGN KEY (ord_an) REFERENCES Analysis (an_id)
);

-- Выручка за второй квартал текущего года
SELECT
    SUM(a.an_price) AS revenue
FROM
    Orders o
    JOIN Analysis a ON o.ord_an = a.an_id
WHERE
    EXTRACT(
        YEAR
        FROM
            o.ord_datetime
    ) = EXTRACT(
        YEAR
        FROM
            SYSDATE
    )
    AND EXTRACT(
        MONTH
        FROM
            o.ord_datetime
    ) BETWEEN 4 AND 6;

-- Количество анализов, собранных за последний год
SELECT
    COUNT(*) AS analysis_count_last_year
FROM
    Orders
WHERE
    ord_datetime >= ADD_MONTHS(SYSDATE, -12);

-- Название и розничная цена анализов за август 2023
SELECT
    a.an_name AS Название,
    a.an_price AS Розничная_цена
FROM
    Analysis a
    JOIN Orders o ON a.an_id = o.ord_an
WHERE
    o.ord_datetime >= TIMESTAMP '2023-08-01 00:00:00'
    AND o.ord_datetime < TIMESTAMP '2023-09-01 00:00:00';

-- Самое популярное время заказа анализов
SELECT
    TO_CHAR(ord_datetime, 'HH24') AS order_hour,
    COUNT(*) AS order_count
FROM
    Orders
GROUP BY
    TO_CHAR(ord_datetime, 'HH24')
ORDER BY
    order_count DESC
FETCH FIRST
    1 ROWS ONLY;

-- Самый популярный температурный режим хранения
WITH
    StorageCount AS (
        SELECT
            g.gr_temp,
            COUNT(*) AS order_count
        FROM
            Orders o
            JOIN Analysis a ON o.ord_an = a.an_id
            JOIN Groups g ON a.an_group = g.gr_id
        GROUP BY
            g.gr_temp
    )
SELECT
    gr_temp
FROM
    StorageCount
ORDER BY
    order_count DESC
FETCH FIRST
    1 ROWS ONLY;

-- Количество повторов групп анализов за последний год
SELECT
    G.gr_name AS Группа_анализов,
    COUNT(O.ord_id) AS Количество_повторов
FROM
    Orders O
    JOIN Analysis A ON O.ord_an = A.an_id
    JOIN Groups G ON A.an_group = G.gr_id
WHERE
    O.ord_datetime >= ADD_MONTHS(SYSDATE, -12)
GROUP BY
    G.gr_name;

-- Название и цену для всех анализов, которые продавались 5 февраля 2023 и всю следующую неделю
SELECT
    a.an_name AS Название,
    a.an_price AS Цена
FROM
    Analysis a
    JOIN Orders o ON a.an_id = o.ord_an
WHERE
    o.ord_datetime >= TO_DATE('2023-02-05', 'YYYY-MM-DD')
    AND o.ord_datetime < TO_DATE('2023-02-12', 'YYYY-MM-DD')
ORDER BY
    a.an_name;
```
