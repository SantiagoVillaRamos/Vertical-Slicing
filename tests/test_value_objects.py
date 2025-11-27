"""
Tests unitarios para los Value Objects del dominio de Catálogo.
"""
import pytest
from src.modules.catalogo.domain.value_objects import SKU, Price, Stock
from src.core.exceptions import ValidationError


class TestSKU:
    """Tests para el Value Object SKU."""
    
    def test_create_valid_sku(self):
        """Debe crear un SKU válido."""
        sku = SKU(value="PROD-12345")
        assert str(sku) == "PROD-12345"
    
    def test_sku_too_short(self):
        """Debe rechazar SKU con menos de 5 caracteres."""
        with pytest.raises(ValidationError, match="al menos 5 caracteres"):
            SKU(value="ABC")
    
    def test_sku_empty(self):
        """Debe rechazar SKU vacío."""
        with pytest.raises(ValidationError, match="no puede estar vacío"):
            SKU(value="")
    
    def test_sku_invalid_characters(self):
        """Debe rechazar SKU con caracteres inválidos."""
        with pytest.raises(ValidationError, match="alfanuméricos y guiones"):
            SKU(value="PROD@12345")


class TestPrice:
    """Tests para el Value Object Price."""
    
    def test_create_valid_price(self):
        """Debe crear un precio válido."""
        price = Price(amount=99.99, currency="USD")
        assert price.amount == 99.99
        assert price.currency == "USD"
        assert str(price) == "99.99 USD"
    
    def test_price_negative(self):
        """Debe rechazar precio negativo."""
        with pytest.raises(ValidationError, match="mayor que 0"):
            Price(amount=-10.0)
    
    def test_price_zero(self):
        """Debe rechazar precio cero."""
        with pytest.raises(ValidationError, match="mayor que 0"):
            Price(amount=0.0)
    
    def test_price_too_many_decimals(self):
        """Debe rechazar precio con más de 2 decimales."""
        with pytest.raises(ValidationError, match="más de 2 decimales"):
            Price(amount=99.999)
    
    def test_price_addition(self):
        """Debe sumar precios correctamente."""
        price1 = Price(amount=10.50, currency="USD")
        price2 = Price(amount=5.25, currency="USD")
        result = price1 + price2
        assert result.amount == 15.75
    
    def test_price_addition_different_currency(self):
        """Debe rechazar suma de precios con diferentes monedas."""
        price1 = Price(amount=10.0, currency="USD")
        price2 = Price(amount=5.0, currency="EUR")
        with pytest.raises(ValidationError, match="diferentes monedas"):
            price1 + price2
    
    def test_price_multiplication(self):
        """Debe multiplicar precio por cantidad."""
        price = Price(amount=10.50, currency="USD")
        result = price * 3
        assert result.amount == 31.50


class TestStock:
    """Tests para el Value Object Stock."""
    
    def test_create_valid_stock(self):
        """Debe crear stock válido."""
        stock = Stock(quantity=100)
        assert stock.quantity == 100
    
    def test_stock_negative(self):
        """Debe rechazar stock negativo."""
        with pytest.raises(ValidationError, match="no puede ser negativo"):
            Stock(quantity=-10)
    
    def test_stock_is_available(self):
        """Debe verificar disponibilidad correctamente."""
        stock = Stock(quantity=10)
        assert stock.is_available(5) is True
        assert stock.is_available(10) is True
        assert stock.is_available(11) is False
    
    def test_stock_decrease(self):
        """Debe reducir stock correctamente."""
        stock = Stock(quantity=10)
        new_stock = stock.decrease(3)
        assert new_stock.quantity == 7
        assert stock.quantity == 10  # Inmutabilidad
    
    def test_stock_decrease_insufficient(self):
        """Debe rechazar reducción que excede el stock."""
        stock = Stock(quantity=5)
        with pytest.raises(ValidationError, match="Stock insuficiente"):
            stock.decrease(10)
    
    def test_stock_increase(self):
        """Debe aumentar stock correctamente."""
        stock = Stock(quantity=10)
        new_stock = stock.increase(5)
        assert new_stock.quantity == 15
        assert stock.quantity == 10  # Inmutabilidad
