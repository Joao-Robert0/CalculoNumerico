import math
import numpy as np
from sympy import symbols, diff, sympify, lambdify
from scipy.optimize import bisect, newton

def print_menu():
    print("\n=== Métodos para calcular raízes ===")
    print("a) Bissecção")
    print("b) Newton")
    print("c) Secantes")
    print("d) Posição Falsa")
    print("d) Sair")
    print("===========================")

def safe_create_function(user_expr):
    def f(x):
        allowed = {"x": x}
        allowed.update({name: getattr(math, name) for name in dir(math) if not name.startswith("__")})
        return eval(user_expr, {"__builtins__": None}, allowed)
    return f

def bracket_selection():
    while True:
        bracket_input = input("Forneça o intervalo [a, b] (ex.: '1 5' ou '2.5,3.5'): ").strip()
        bracket_input = bracket_input.replace(',', ' ')
        parts = bracket_input.split()
        if len(parts) != 2:
            print("Erro: Insira exatamente dois números.")
            continue
        try:
            a, b = map(float, parts)
            return a, b
        except ValueError:
            print("Erro: Valores inválidos.")

def x_selection(prompt="Forneça o valor de x0 (ex.: '5' ou '6.5'): "):
    while True:
        x_input = input(prompt).strip()
        try:
            return float(x_input)
        except ValueError:
            print("Erro: Valor inválido.")

def compute_derivative(expression):
    x = symbols('x')
    try:
        f = sympify(expression)
        df_dx = diff(f, x)
        return lambdify(x, df_dx, modules=['numpy'])  # Converter para função numérica
    except Exception as e:
        raise ValueError(f"Erro ao calcular derivada: {e}")

def bisection_method(f):
    a, b = bracket_selection()
    result = bisect(f, a, b)
    return result

def newton_method(f, expression):
    x0 = x_selection()
    try:
        fprime = compute_derivative(expression)  # Obter função derivada
    except ValueError as e:
        print(e)
        return None
    result = newton(func=f, fprime=fprime, x0=x0)  # Parâmetro correto: func
    return result

def secant_method(f):
    x0 = x_selection("Forneça o primeiro ponto inicial x0 (ex.: '5'): ")
    x1 = x_selection("Forneça o segundo ponto inicial x1 (ex.: '6.5'): ")
    result = newton(func=f, x0=x0, x1=x1)  # Método da secante usa x0 e x1
    return result

def regula_falsi(f, tol=1e-5, max_iter=100):
    x0 = x_selection("Forneça o primeiro ponto inicial x0 (ex.: '5'): ")
    x1 = x_selection("Forneça o segundo ponto inicial x1 (ex.: '6.5'): ")
    if f(x0) * f(x1) >= 0:
        raise ValueError("Initial guesses must have opposite signs.")

    for _ in range(max_iter):
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        if abs(f(x2)) < tol:
            return x2
        if f(x0) * f(x2) < 0:
            x1 = x2
        else:
            x0 = x2

    return None  # No root found within the maximum iterations

if __name__ == "__main__":
    print_menu()
    option = input("Escolha uma opção (a-d): ").lower()
    if option == "e":
        exit()
    
    expression = input("Forneça a função f(x) (ex.: 'x**2 - 4' ou 'sin(x) + math.pi'): ").strip()
    f = safe_create_function(expression)
    
    match option:
        case "a":
            root = bisection_method(f)
            print(f"Raiz encontrada: {root:.6f}")
        case "b":
            root = newton_method(f, expression)
            if root is not None:
                print(f"Raiz encontrada: {root:.6f}")
        case "c":
            root = secant_method(f)
            print(f"Raiz encontrada: {root:.6f}")
        case "d":
            root = regula_falsi(f)
            print(f"Raiz encontrada: {root:.6f}")
        case _:
            print("Opção inválida.")