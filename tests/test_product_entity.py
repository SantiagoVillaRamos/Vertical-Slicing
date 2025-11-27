"""
Tests unitarios para la entidad Product.
"""
import pytest
from datetime import datetime
from src.modules.catalogo.domain.entities import Product
from src.modules.catalogo.domain.value_objects import SKU, Price, Stock
from src.core.exceptions import BusinessRuleViolation


class TestProduct:
    """Tests para la entidad Product."""
    
    def test_create_valid_product(self):
        """Debe crear un producto válido."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            description="High-end laptop",
            price=Price(amount=1299.99, currency="USD"),
            stock=Stock(quantity=10)
        )
        
        assert str(product.sku) == "PROD-001"
        assert product.name == "Laptop"
        assert product.price.amount == 1299.99
        assert product.stock.quantity == 10
        assert product.is_active is True
    
    def test_product_name_too_short(self):
        """Debe rechazar nombre muy corto."""
        with pytest.raises(BusinessRuleViolation, match="al menos 3 caracteres"):
            Product(
                sku=SKU(value="PROD-001"),
                name="AB",
                price=Price(amount=10.0),
                stock=Stock(quantity=5)
            )
    
    def test_update_price_valid(self):
        """Debe actualizar precio dentro del límite permitido."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=10)
        )
        
        # Cambio del 40% (permitido)
        new_price = Price(amount=140.0)
        product.update_price(new_price)
        
        assert product.price.amount == 140.0
    
    def test_update_price_exceeds_limit(self):
        """Debe rechazar cambio de precio mayor al 50%."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=10)
        )
        
        # Cambio del 60% (no permitido)
        new_price = Price(amount=160.0)
        
        with pytest.raises(BusinessRuleViolation, match="más del 50%"):
            product.update_price(new_price)
    
    def test_reserve_stock_success(self):
        """Debe reservar stock correctamente."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=10)
        )
        
        product.reserve_stock(3)
        assert product.stock.quantity == 7
    
    def test_reserve_stock_insufficient(self):
        """Debe rechazar reserva con stock insuficiente."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=5)
        )
        
        with pytest.raises(BusinessRuleViolation, match="Stock insuficiente"):
            product.reserve_stock(10)
    
    def test_reserve_stock_inactive_product(self):
        """Debe rechazar reserva en producto inactivo."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=10),
            is_active=False
        )
        
        with pytest.raises(BusinessRuleViolation, match="producto inactivo"):
            product.reserve_stock(3)
    
    def test_replenish_stock(self):
        """Debe reponer stock correctamente."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=5)
        )
        
        product.replenish_stock(10)
        assert product.stock.quantity == 15
    
    def test_deactivate_product(self):
        """Debe desactivar producto."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=10)
        )
        
        product.deactivate()
        assert product.is_active is False
    
    def test_activate_product(self):
        """Debe activar producto."""
        product = Product(
            sku=SKU(value="PROD-001"),
            name="Laptop",
            price=Price(amount=100.0),
            stock=Stock(quantity=10),
            is_active=False
        )
        
        product.activate()
        assert product.is_active is True
