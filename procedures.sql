CREATE OR REPLACE PROCEDURE update_order_status (
    p_order_id IN NUMBER,
    p_new_status IN VARCHAR2
)
AS
BEGIN
    IF UPPER(p_new_status) NOT IN
       ('PLACED', 'PREPARING', 'DELIVERED', 'CANCELLED') THEN
        RAISE_APPLICATION_ERROR(-20001, 'Invalid order status');
    END IF;

    UPDATE food_orders
    SET order_status = UPPER(p_new_status)
    WHERE order_id = p_order_id;

    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Order not found');
    END IF;
END;
/