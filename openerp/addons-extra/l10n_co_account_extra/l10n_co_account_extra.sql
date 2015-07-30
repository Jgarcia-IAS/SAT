DROP FUNCTION fnc_account_invoice_line_discount() cascade;

CREATE OR REPLACE FUNCTION fnc_account_invoice_line_discount()
  RETURNS trigger AS
$BODY$
  BEGIN
     -- Copia varios campos desde la cotizaciÃ³n
     update account_invoice
     set discount = coalesce((select sum((quantity * price_unit)*discount/100) from account_invoice_line
                      where invoice_id = NEW.invoice_id),0)      
       where id = NEW.invoice_id;
          
     RETURN NEW;
  END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
  
CREATE TRIGGER trg_account_invoice_line_discount
  AFTER INSERT OR UPDATE
  ON account_invoice_line
  FOR EACH ROW
  EXECUTE PROCEDURE fnc_account_invoice_line_discount();  
 ---------------------------------------------------- 
 
 DROP FUNCTION fnc_account_invoice_tax_line_category() cascade;

CREATE OR REPLACE FUNCTION fnc_account_invoice_tax_line_category()
  RETURNS trigger AS
$BODY$
  BEGIN
      -- Actualiza los impuestos separados en la factura
      update account_invoice
         set amount_iva = coalesce((select sum(i.amount )from account_invoice_tax i
                            inner join account_tax t on (t.name = i.name)
                            inner join account_tax_category c on (c.id = t.tax_category_id)
                            where invoice_id = NEW.invoice_id
                            and c.type = 'IVA'),0),
         amount_reteiva = coalesce((select sum(i.amount )from account_invoice_tax i
                            inner join account_tax t on (t.name = i.name)
                            inner join account_tax_category c on (c.id = t.tax_category_id)
                            where invoice_id = NEW.invoice_id
                            and c.type = 'RVA'),0),
         amount_rte = coalesce((select sum(i.amount )from account_invoice_tax i
                            inner join account_tax t on (t.name = i.name)
                            inner join account_tax_category c on (c.id = t.tax_category_id)
                            where invoice_id = NEW.invoice_id
                            and c.type = 'RTE'),0),
         amount_cree = coalesce((select sum(i.amount )from account_invoice_tax i
                            inner join account_tax t on (t.name = i.name)
                            inner join account_tax_category c on (c.id = t.tax_category_id)
                            where invoice_id = NEW.invoice_id
                            and c.type = 'CRE'),0)                                                                           
       where id = NEW.invoice_id;    
                   
     RETURN NEW;
  END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
  
CREATE TRIGGER trg_account_invoice_tax_line_category
  AFTER INSERT OR UPDATE
  ON account_invoice_tax
  FOR EACH ROW
  EXECUTE PROCEDURE fnc_account_invoice_tax_line_category();  
------------------------------------------------------

DROP FUNCTION fnc_sale_order_extra() cascade;

CREATE OR REPLACE FUNCTION fnc_sale_order_extra()
  RETURNS trigger AS
$BODY$
  BEGIN
      -- Actualiza IVA y total pedido
      NEW.amount_tax = coalesce(NEW.amount_untaxed,0) * 0.16;
      NEW.amount_total = coalesce(NEW.amount_untaxed,0) + coalesce(NEW.amount_tax,0);   
                         
     RETURN NEW;
  END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE TRIGGER trg_sale_order_extra
  BEFORE INSERT OR UPDATE
  ON sale_order
  FOR EACH ROW
  EXECUTE PROCEDURE fnc_sale_order_extra();
-----------------------------------------------------

DROP FUNCTION fnc_sale_order_line_discount() cascade;

CREATE OR REPLACE FUNCTION fnc_sale_order_line_discount()
  RETURNS trigger AS
$BODY$
  BEGIN
     -- Copia varios campos desde la cotizaciÃ³n
     update sale_order
     set discount = (select sum((product_uos_qty * price_unit)*discount/100) from sale_order_line
                                         where order_id = NEW.order_id)
      where id = NEW.order_id;                                    
     
     RETURN NEW;
  END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
  
CREATE TRIGGER trg_sale_order_line_discount
  AFTER INSERT OR UPDATE
  ON sale_order_line
  FOR EACH ROW
  EXECUTE PROCEDURE fnc_sale_order_line_discount();
----------------------------------------------------

    
  
