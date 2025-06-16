import math
import numpy as np
from sympy import symbols, diff, sympify, lambdify

def print_menu():
    print("\n=== Métodos para calcular raízes ===")
    opcoes = ["a) Bissecção", "b) Newton", "c) Secantes", "d) Posição Falsa", "e) Ponto Fixo", "f) Sair"]
    print("\n".join(opcoes))
    print("===========================")

def print_resultados_bissecao(raiz_encontrada, historico):
    if raiz_encontrada is not None:
        print(f"\nRaiz encontrada: {raiz_encontrada:.4f}")
    else:
        print("\nNão foi possível encontrar a raiz.")

    print("\nHistórico das Iterações - Método da Bisseção:")
    print("=" * 90)
    print(f"{'n':<3} | {'a':<10} | {'b':<10} | {'f(a)':<10} | {'f(b)':<10} | {'m':<10} | {'f(m)':<10} | {'Erro':<10}")
    print("=" * 90)
    for item in historico:
        if item[0] == 1:
            print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {item[3]:<10.4f} | {item[4]:<10.4f} | {item[5]:<10.4f} | {item[6]:<10.4f} | {"-----"}")
        else:
            print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {item[3]:<10.4f} | {item[4]:<10.4f} | {item[5]:<10.4f} | {item[6]:<10.4f} | {item[7]:<10.4f}")
    print("=" * 90)

def print_resultados_newton(raiz_encontrada, historico):
    if raiz_encontrada is not None:
        print(f"\nRaiz encontrada: {raiz_encontrada:.4f}")
    else:
        print("\nNão foi possível encontrar a raiz.")

    print("\nHistórico das Iterações - Método de Newton:")
    print("=" * 60)
    print(f"{'n':<3} | {'x_n':<12} | {'f(x_n)':<12} | {'Erro':<12}")
    print("=" * 60)
    for item in historico:
        if len(item) >= 4:
            if item[0] == 1:
                print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {"-----"}")
            else:
                print(f"{item[0]:<3.0f} | {item[1]:<12.4f} | {item[2]:<12.4f} | {item[3]:<12.4f}")
    print("=" * 60)

def print_resultados_secante(raiz_encontrada, historico):
    if raiz_encontrada is not None:
        print(f"\nRaiz encontrada: {raiz_encontrada:.4f}")
    else:
        print("\nNão foi possível encontrar a raiz.")

    print("\nHistórico das Iterações - Método da Secante:")
    print("=" * 110)
    print(f"{'n':<3} | {'x_{k-1}':<10} | {'x_k':<10} | {'f(x_{k-1})':<12} | {'f(x_k)':<12} | {'x_{k+1}':<10} | {'f(x_{k+1})':<12} | {'Erro':<10}")
    print("=" * 110)
    for item in historico:
        if len(item) >= 8:
            if item[0] == 1:
                print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {item[3]:<10.4f} | {item[4]:<10.4f} | {item[5]:<10.4f} | {item[6]:<10.4f} | {"-----"}")
            else:
                print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {item[3]:<12.4f} | {item[4]:<12.4f} | {item[5]:<10.4f} | {item[6]:<12.4f} | {item[7]:<10.4f}")
    print("=" * 110)

def print_resultados_regula_falsi(raiz_encontrada, historico):
    if raiz_encontrada is not None:
        print(f"\nRaiz encontrada: {raiz_encontrada:.4f}")
    else:
        print("\nNão foi possível encontrar a raiz.")

    print("\nHistórico das Iterações - Método da Posição Falsa:")
    print("=" * 100)
    print(f"{'n':<3} | {'x0':<10} | {'x1':<10} | {'f(x0)':<10} | {'f(x1)':<10} | {'xc':<10} | {'f(xc)':<10} | {'Erro':<10}")
    print("=" * 100)
    for item in historico:
        if len(item) >= 8:
            if item[0] == 1:
                print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {item[3]:<10.4f} | {item[4]:<10.4f} | {item[5]:<10.4f} | {item[6]:<10.4f} | {"-----"}")
            else:
                print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {item[3]:<10.4f} | {item[4]:<10.4f} | {item[5]:<10.4f} | {item[6]:<10.4f} | {item[7]:<10.4f}")
    print("=" * 100)

def print_resultados_ponto_fixo(raiz_encontrada, historico):
    if raiz_encontrada is not None:
        print(f"\nRaiz encontrada (Ponto Fixo): {raiz_encontrada:.4f}")
    else:
        print("\nNão foi possível encontrar o ponto fixo.")

    print("\nHistórico das Iterações - Método do Ponto Fixo:")
    print("=" * 60)
    print(f"{'n':<3} | {'x':<12} | {'f(x)':<12} | {'Erro':<12}")
    print("=" * 60)
    for item in historico:
        # item: [iteracao, x_n, f_xn, erro]
        if len(item) >= 4:
            if item[0] == 1:
                print(f"{item[0]:<3.0f} | {item[1]:<10.4f} | {item[2]:<10.4f} | {"-----"}")
            else:
                print(f"{item[0]:<3.0f} | {item[1]:<12.4f} | {item[2]:<12.4f} | {item[3]:<12.4f}")
    print("=" * 60)



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

def bissecao(f, tol, max_iter):
    historico_iteracoes = []
    iteracao = 0
    a,b = bracket_selection()
    f_a, f_b = f(a), f(b)
    
    if f_a * f_b >= 0:
        print("Erro: f(a) e f(b) devem ter sinais opostos para o método da bisseção.")
        return None, [0, a, b, f_a, f_b, (a+b)/2, f((a+b)/2), float('inf')]

    for i in range(max_iter):
        m = (a + b) / 2 
        f_m = f(m)    
        erro = (b - a) / 2

        historico_iteracoes.append([i+1, a, b, f_a, f_b, m, f_m, erro])

        if erro < tol or abs(f_m) < 1e-12: 
            return m, historico_iteracoes
        
        if f_a * f_m < 0:
            b, f_b = m, f_m
        elif f_b * f_m < 0:
            a, f_a = m, f_m
        elif f_m == 0:  # Raiz exata encontrada
            return m, historico_iteracoes

    return (a + b) / 2, historico_iteracoes

def newton(f, tol, max_iter):
    x0 = x_selection()
    historico_iteracoes = []
    x_n = x0
    iteracao = 0
    df =  safe_create_function(input("Insira a derivada f(x)"))

    for n in range(max_iter):
        iteracao = n + 1
        f_xn = f(x_n)
        df_xn = df(x_n)

        if abs(df_xn) < 1e-12:
            historico_iteracoes.append([iteracao, x_n, f_xn, float('inf')])
            return None, historico_iteracoes

        x_n_mais_1 = x_n - f_xn / df_xn
        erro = abs(x_n_mais_1 - x_n)
        historico_iteracoes.append([iteracao, x_n, f_xn, erro])

        if erro < tol:
            historico_iteracoes.append([iteracao + 1, x_n_mais_1, f(x_n_mais_1), erro])
            return x_n_mais_1, historico_iteracoes

        x_n = x_n_mais_1
    return x_n, historico_iteracoes

def secante(f,tol,max_iter):
    historico_iteracoes = []
    iteracao = 0

    x0 = x_selection("Forneça o primeiro ponto inicial x0 (ex.: '5'): ")
    x1 = x_selection("Forneça o segundo ponto inicial x1 (ex.: '6.5'): ")

    x_k_minus_1 = x0
    x_k = x1

    for n_iter in range(max_iter):
        iteracao = n_iter + 1
        f_xk_minus_1 = f(x_k_minus_1)
        f_xk = f(x_k)
        denominador = f_xk - f_xk_minus_1

        if abs(denominador) < 1e-12:  
            print("Denominador muito próximo de zero. O método pode não convergir.")
            historico_iteracoes.append([iteracao, x_k_minus_1, x_k, f_xk_minus_1, f_xk, None, None, float('inf')])
            return None, historico_iteracoes

        x_k_plus_1 = x_k - f_xk * (x_k - x_k_minus_1) / denominador
        f_xk_plus_1 = f(x_k_plus_1)
        erro = abs(x_k_plus_1 - x_k)

        # [n, x_k-1, x_k, f(x_k-1), f(x_k), x_k+1, f(x_k+1), erro_k]
        historico_iteracoes.append([iteracao, x_k_minus_1, x_k, f_xk_minus_1, f_xk, x_k_plus_1, f_xk_plus_1, erro])
        # Critério de parada
        if erro < tol or abs(f_xk_plus_1) < 1e-12 : 
            return x_k_plus_1, historico_iteracoes

        # Atualiza os pontos para a próxima iteração
        x_k_minus_1 = x_k
        x_k = x_k_plus_1

    return x_k, historico_iteracoes # Retorna a última aproximaç


def regula_falsi(f, tol, max_iter):
    historico_iteracoes = []
    x0 = x_selection("Forneça o primeiro ponto inicial x0 (ex.: '5'): ")
    x1 = x_selection("Forneça o segundo ponto inicial x1 (ex.: '6.5'): ")

    f_x0 = f(x0)
    f_x1 = f(x1)

    if f_x0 * f_x1 >= 0:
        print("Erro: Os valores iniciais f(x0) e f(x1) devem ter sinais opostos.")
        historico_iteracoes.append([0, x0, x1, f_x0, f_x1, None, None, float('inf')])
        return None, historico_iteracoes

    xc = None

    for n_iter in range(1, max_iter + 1):
       
        f_x0 = f(x0)
        f_x1 = f(x1)

        denominador = f_x1 - f_x0
        if abs(denominador) < 1e-12:
            print("Denominador muito próximo de zero. O método pode não convergir.")
            historico_iteracoes.append([n_iter, x0, x1, f_x0, f_x1, None, None, float('inf')])
            return xc, historico_iteracoes 

        xc = x1 - f_x1 * (x1 - x0) / denominador

        f_xc = f(xc)
        erro_atual = abs(f_xc)

        historico_iteracoes.append([n_iter, x0, x1, f_x0, f_x1, xc, f_xc, erro_atual])

        if erro_atual < tol:
            return xc, historico_iteracoes

        if f_x0 * f_xc < 0:
            x1 = xc

        elif f_x1 * f_xc < 0: 
            x0 = xc

        elif f_xc == 0:
             return xc, historico_iteracoes
        else:
            print("Erro inesperado: os sinais não permitem o estreitamento do intervalo.")
            return xc, historico_iteracoes


    print("Número máximo de iterações atingido. A solução pode não ter convergido para a tolerância desejada.")
    return xc, historico_iteracoes

def ponto_fixo(f, tol, max_iter):
    g = safe_create_function(input("Forneça a função g(x) (ex.: 'sqrt(x + 1)' ou 'cos(x)'): "))
    x0 = x_selection("Forneça o ponto inicial x0 para f(x): ")
    historico_iteracoes = []
    x_n = x0
    
    for iteracao_num in range(1, max_iter + 1):
        g_xn = g(x_n)
        erro = abs(g_xn - x_n)
        
        historico_iteracoes.append([iteracao_num, x_n,f(x_n), erro])
        
        if erro < tol:
            return g_xn, historico_iteracoes
        
        x_n = g_xn
        
    print("Número máximo de iterações atingido. A solução pode não ter convergido.")
    return x_n, historico_iteracoes


if __name__ == "__main__":

    tolerancia, maximo_iteracoes = 1e-4, 30

    print_menu()
    option = input("Escolha uma opção (a-f): ").lower()
    if option == "f": exit()
    
    expression = input("Forneça a função f(x) (ex.: 'x**2 - 4' ou 'sin(x) + math.pi'): ").strip()
    f = safe_create_function(expression)

    match option:
        case "a":
            raiz, historico = bissecao(f, tolerancia, maximo_iteracoes)
            print_resultados_bissecao(raiz, historico)
        case "b":
            raiz, historico = newton(f, tolerancia, maximo_iteracoes)
            print_resultados_newton(raiz, historico)
        case "c":
            raiz, historico = secante(f, tolerancia, maximo_iteracoes)
            print_resultados_secante(raiz, historico)
        case "d":
            raiz, historico = regula_falsi(f, tolerancia, maximo_iteracoes)
            print_resultados_regula_falsi(raiz, historico)
        case "e":
            raiz, historico = ponto_fixo(f, tolerancia, maximo_iteracoes)
            print_resultados_ponto_fixo(raiz, historico)
        case _:
            print("Opção inválida.")