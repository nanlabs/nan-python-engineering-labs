"""
Ejercicio Básico: Type Hints - Descuentos de Productos

OBJETIVO:
Crear una función que calcule el precio final de un producto
después de aplicar un descuento porcentual.

REQUISITOS:
1. Función calculate_discount que acepte:
   - price: float (precio original)
   - discount_percent: float (porcentaje de descuento 0-100)
2. Retornar el precio final como float
3. Validar que discount_percent esté entre 0 y 100
4. Si el descuento es inválido, retornar el precio original
5. TODOS los parámetros y el retorno deben tener type hints

EJEMPLO DE USO:
>>> calculate_discount(100.0, 20.0)
80.0
>>> calculate_discount(50.0, 150.0)  # Descuento inválido
50.0
"""


def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calcula el precio final después de aplicar un descuento.
    
    Args:
        price: Precio original del producto (debe ser positivo)
        discount_percent: Porcentaje de descuento a aplicar (0-100)
        
    Returns:
        El precio final después del descuento.
        Si el descuento es inválido (<0 o >100), retorna el precio original.
    
    Examples:
        >>> calculate_discount(100.0, 20.0)
        80.0
        >>> calculate_discount(150.0, 10.0)
        135.0
        >>> calculate_discount(50.0, -5.0)
        50.0
    """
    # TODO: Implementar la lógica de validación y cálculo
    # 1. Validar que discount_percent esté entre 0 y 100
    # 2. Si es válido, calcular: price - (price * discount_percent / 100)
    # 3. Si no es válido, retornar price sin modificar
    pass


if __name__ == "__main__":
    # Pruebas manuales - descomentar para probar tu implementación
    # print(calculate_discount(100.0, 20.0))  # Esperado: 80.0
    # print(calculate_discount(50.0, 50.0))   # Esperado: 25.0
    # print(calculate_discount(200.0, 15.0))  # Esperado: 170.0
    # print(calculate_discount(100.0, 110.0)) # Esperado: 100.0 (inválido)
    # print(calculate_discount(100.0, -10.0)) # Esperado: 100.0 (inválido)
    pass
