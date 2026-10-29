CREATE OR REPLACE TRIGGER trg_update_order_total
AFTER INSERT OR UPDATE OR DELETE ON order_items
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        UPDATE food_orders
        SET order_total = order_total + :NEW.subtotal
        WHERE order_id = :NEW.order_id;

    ELSIF DELETING THEN
        UPDATE food_orders
        SET order_total = order_total - :OLD.subtotal
        WHERE order_id = :OLD.order_id;

    ELSIF UPDATING THEN
        IF :OLD.order_id = :NEW.order_id THEN
            UPDATE food_orders
            SET order_total = order_total
                - :OLD.subtotal + :NEW.subtotal
            WHERE order_id = :NEW.order_id;
        ELSE
            UPDATE food_orders
            SET order_total = order_total - :OLD.subtotal
            WHERE order_id = :OLD.order_id;

            UPDATE food_orders
            SET order_total = order_total + :NEW.subtotal
            WHERE order_id = :NEW.order_id;
        END IF;
    END IF;
END;
/