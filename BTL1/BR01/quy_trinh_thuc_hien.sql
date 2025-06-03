--CN1
CREATE USER DIRECTOR IDENTIFIED BY 123;
GRANT CONNECT, CREATE DATABASE LINK TO DIRECTOR;

CREATE USER EMPLOYEE IDENTIFIED BY 123;
GRANT CONNECT, CREATE DATABASE LINK TO EMPLOYEE;

CREATE USER MANAGER IDENTIFIED BY 123;
GRANT CONNECT, CREATE DATABASE LINK TO MANAGER;
---------------------------------------------------------------------------------
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.PRODUCT TO DIRECTOR;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.PRODUCT_STOCK_MANAGER TO DIRECTOR;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.PRODUCT_STOCK_EMPLOYEE TO DIRECTOR;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.INVOICE TO DIRECTOR;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.INVOICE_DETAIL TO DIRECTOR;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.EMPLOYEE TO DIRECTOR;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.CUSTOMER TO DIRECTOR;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.BRANCH TO DIRECTOR;


GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.INVOICE_DETAIL TO EMPLOYEE;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.INVOICE TO EMPLOYEE;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.PRODUCT TO EMPLOYEE;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.PRODUCT_STOCK_EMPLOYEE TO EMPLOYEE;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.CUSTOMER TO EMPLOYEE;
GRANT SELECT ON CN1.BRANCH TO EMPLOYEE;


GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.PRODUCT_STOCK_MANAGER TO MANAGER;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.INVOICE_DETAIL TO MANAGER;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.INVOICE TO MANAGER;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.EMPLOYEE TO MANAGER;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.PRODUCT TO MANAGER;
GRANT SELECT, INSERT, UPDATE, DELETE ON CN1.CUSTOMER TO MANAGER;
GRANT SELECT ON CN1.BRANCH TO MANAGER;


-----------------------------------------
connect DIRECTOR;

CREATE DATABASE LINK DIRECTOR_Link2
CONNECT TO DIRECTOR IDENTIFIED BY "123"
USING 'thuylink';

CREATE DATABASE LINK DIRECTOR_Link3
CONNECT TO DIRECTOR IDENTIFIED BY "123"
USING 'minh_link';
--------------------------------------------------
connect EMPLOYEE;

CREATE DATABASE LINK EMPLOYEE_Link2
CONNECT TO EMPLOYEE IDENTIFIED BY "123"
USING 'thuylink';

CREATE DATABASE LINK EMPLOYEE_Link3
CONNECT TO EMPLOYEE IDENTIFIED BY "123"
USING 'minh_link';
----------------------------------------------

connect MANAGER;

CREATE DATABASE LINK MANAGER_Link2
CONNECT TO MANAGER IDENTIFIED BY "123"
USING 'thuylink';

CREATE DATABASE LINK MANAGER_Link3
CONNECT TO MANAGER IDENTIFIED BY "123"
USING 'minh_link';



-----------------------------------------------------------------------------


---PROCEDURE-----
CREATE OR REPLACE PROCEDURE IMPORT_STOCK(
    p_product_id   IN VARCHAR2,
    p_qty          IN NUMBER
)
AS
    v_qty_br02   NUMBER := 0;
    v_qty_br03   NUMBER := 0;
    v_remaining  NUMBER := p_qty;
BEGIN
    -- Lấy tồn kho ở chi nhánh BR02 và BR03 (qua DB Link)
    BEGIN
        SELECT NVL(QUANTITY_IN_STOCK, 0)
        INTO v_qty_br02
        FROM CN2.PRODUCT_STOCK_MANAGER@MANAGER_Link2
        WHERE PRODUCT_ID = p_product_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_qty_br02 := 0;
    END;

    BEGIN
        SELECT NVL(QUANTITY_IN_STOCK, 0)
        INTO v_qty_br03
        FROM CN3.PRODUCT_STOCK_MANAGER@MANAGER_Link3
        WHERE PRODUCT_ID = p_product_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_qty_br03 := 0;
    END;

    -- Trường hợp 1: BR02 hoặc BR03 có đủ riêng lẻ
    IF v_qty_br02 >= p_qty AND v_qty_br02 >= v_qty_br03 THEN
        -- Rút từ BR02
        UPDATE CN2.PRODUCT_STOCK_MANAGER@MANAGER_Link2
        SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - p_qty
        WHERE PRODUCT_ID = p_product_id;

        -- Nhập về BR01
        UPDATE CN1.PRODUCT_STOCK_MANAGER
        SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK + p_qty
        WHERE PRODUCT_ID = p_product_id;

        DBMS_OUTPUT.PUT_LINE('Đã nhập ' || p_qty || ' sản phẩm từ BR02');

    ELSIF v_qty_br03 >= p_qty THEN
        -- Rút từ BR03
        UPDATE CN3.PRODUCT_STOCK_MANAGER@MANAGER_Link3
        SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - p_qty
        WHERE PRODUCT_ID = p_product_id;

        -- Nhập về BR01
        UPDATE CN1.PRODUCT_STOCK_MANAGER
        SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK + p_qty
        WHERE PRODUCT_ID = p_product_id;

        DBMS_OUTPUT.PUT_LINE('Đã nhập ' || p_qty || ' sản phẩm từ BR03');

    -- Trường hợp 2: Cả 2 không đủ riêng lẻ nhưng cộng lại đủ
    ELSIF v_qty_br02 + v_qty_br03 >= p_qty THEN
        DECLARE
            v_from_br02 NUMBER := 0;
            v_from_br03 NUMBER := 0;
        BEGIN
            -- Rút tối đa từ BR02
            IF v_qty_br02 > 0 THEN
                IF v_qty_br02 >= v_remaining THEN
                    v_from_br02 := v_remaining;
                ELSE
                    v_from_br02 := v_qty_br02;
                END IF;

                UPDATE CN2.PRODUCT_STOCK_MANAGER@MANAGER_Link2
                SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - v_from_br02
                WHERE PRODUCT_ID = p_product_id;

                UPDATE CN1.PRODUCT_STOCK_MANAGER
                SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK + v_from_br02
                WHERE PRODUCT_ID = p_product_id;

                v_remaining := v_remaining - v_from_br02;
            END IF;

            -- Rút phần còn lại từ BR03
            IF v_remaining > 0 AND v_qty_br03 >= v_remaining THEN
                v_from_br03 := v_remaining;

                UPDATE CN3.PRODUCT_STOCK_MANAGER@MANAGER_Link3
                SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - v_from_br03
                WHERE PRODUCT_ID = p_product_id;

                UPDATE CN1.PRODUCT_STOCK_MANAGER
                SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK + v_from_br03
                WHERE PRODUCT_ID = p_product_id;

                v_remaining := 0;
            END IF;

            DBMS_OUTPUT.PUT_LINE('Đã nhập từ BR02 (' || v_from_br02 || ') và BR03 (' || v_from_br03 || ') sản phẩm');
        END;

    -- Trường hợp 3: Không đủ từ cả 2
    ELSE
        DBMS_OUTPUT.PUT_LINE('Không đủ sản phẩm ở cả BR02 và BR03 để nhập ' || p_qty || ' sản phẩm');
    END IF;

    COMMIT;
END;


-----------FUNTION------
CREATE OR REPLACE FUNCTION get_total_revenue_all_branches
RETURN NUMBER
AS
  v_total_local   NUMBER := 0;
  v_total_br02    NUMBER := 0;
  v_total_br03    NUMBER := 0;
BEGIN
  -- 1. Doanh thu tại chi nhánh hiện tại (ví dụ: BR01)
  SELECT NVL(SUM(TOTAL_AMOUNT), 0)
  INTO v_total_local
  FROM CN1.INVOICE;

  -- 2. Doanh thu tại BR02
  SELECT NVL(SUM(TOTAL_AMOUNT), 0)
  INTO v_total_br02
  FROM CN2.INVOICE@MANAGER_Link2;

  -- 3. Doanh thu tại BR03
  SELECT NVL(SUM(TOTAL_AMOUNT), 0)
  INTO v_total_br03
  FROM CN3.INVOICE@MANAGER_Link3;

  -- 4. Trả về tổng cộng
  RETURN v_total_local + v_total_br02 + v_total_br03;
EXCEPTION
  WHEN OTHERS THEN
    -- Trong môi trường demo nếu 1 DB link bị lỗi, ta có thể trả về -1
    RETURN -1;
END;
/


------------------------TRIIGER--------------
CREATE OR REPLACE TRIGGER trg_update_stock_and_total
BEFORE INSERT ON INVOICE_DETAIL
FOR EACH ROW
DECLARE
    v_stock_qty    NUMBER := 0;
    v_unit_price   NUMBER := 0;
BEGIN
    -- 1. Lấy số lượng tồn kho (không cần kiểm tra BRANCH_ID)
    SELECT QUANTITY_IN_STOCK
    INTO v_stock_qty
    FROM CN1.PRODUCT_STOCK_MANAGER
    WHERE PRODUCT_ID = :NEW.PRODUCT_ID;

    -- 2. Kiểm tra tồn kho
    IF v_stock_qty < :NEW.QUANTITY THEN
        RAISE_APPLICATION_ERROR(-20001,
            'Không đủ số lượng tồn kho cho sản phẩm ID ' || :NEW.PRODUCT_ID);
    END IF;

    -- 3. Trừ tồn kho
    UPDATE CN1.PRODUCT_STOCK_MANAGER
    SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - :NEW.QUANTITY
    WHERE PRODUCT_ID = :NEW.PRODUCT_ID;

    -- 4. Lấy đơn giá
    SELECT UNIT_PRICE
    INTO v_unit_price
    FROM CN1.PRODUCT
    WHERE PRODUCT_ID = :NEW.PRODUCT_ID;

    -- 5. Cộng tổng tiền vào hóa đơn
    UPDATE CN1.INVOICE
    SET TOTAL_AMOUNT = NVL(TOTAL_AMOUNT, 0) + (v_unit_price * :NEW.QUANTITY)
    WHERE INVOICE_ID = :NEW.INVOICE_ID;
END;
/


CREATE OR REPLACE TRIGGER trg_force_total_zero_on_invoice
BEFORE INSERT ON INVOICE
FOR EACH ROW
BEGIN
    -- Ép giá trị tổng tiền về 0 bất kể người dùng nhập gì
    :NEW.TOTAL_AMOUNT := 0;
END;
/



----------------LOST UPDATE-----------
  ---CN1-
set transaction isolation level read committed;
SELECT * FROM CN1.CUSTOMER WHERE CUSTOMER_ID = 13085;
BEGIN
UPDATE CN1.CUSTOMER
SET FIRST_NAME = 'Sara',
LAST_NAME = 'Law',
PHONE = '935.435.8644'
WHERE CUSTOMER_ID = 13085;
END;

-----CN2-----
BEGIN
UPDATE CN1.CUSTOMER@MANAGER_Link1
SET FIRST_NAME = 'Sara',
LAST_NAME = 'Mary',
PHONE = '935.435.8644'
WHERE CUSTOMER_ID = 13085;
END;


----CN1---
COMMIT;

-----CN2-----
COMMIT;

----CN1---
SELECT FIRST_NAME, LAST_NAME, PHONE
FROM CN1.CUSTOMER WHERE CUSTOMER_ID = 13085;



---------------NON-REPEATEABLE-----------
----CN1----
set transaction isolation
level read committed;
SELECT FIRST_NAME, LAST_NAME, PHONE FROM CN1.CUSTOMER WHERE CUSTOMER_ID = 13085;


-----CN2---
BEGIN
UPDATE CN1.CUSTOMER@EMPLOYEE_Link1
SET FIRST_NAME = 'Sara',
LAST_NAME = 'Mit',
PHONE = '935.435.8644'
WHERE CUSTOMER_ID = 13085;
END;

------CN1------
SELECT FIRST_NAME, LAST_NAME, PHONE FROM CN1.CUSTOMER WHERE CUSTOMER_ID = 13085;



