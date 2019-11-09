import math

# Analiza el estado del campo
# Decide cuando rotar
# Hacer lanzamiento a la porteria con probabilidad de desvio
# random pelota random carro

'''
Propuestas para variables de entrada crisp
--- HACIA LA PELOTA
- Distancia a la pelota
x -> [0:1] creciente polinomica
- Direccion hacia la pelota basado en signos de catetos
x, y -> NO | NE | SO | SE
'''

'''
Dimensiones del tablero
- HEIGHT 100
- WIDTH 100
'''

'''
Clausulas de Horn propuestas
            | NO      | NE       | SO        | SE
[0.0 : 0.2] | (45, 1) | (135, 1) | (315, 1)  | (225, 1)
[0.2 : 0.7] | (45, 5) | (135, 5) | (315, 5)  | (225, 5)
[0.7 : 1.0] | (45, 10)| (135, 10)| (315, 10) | (225, 10)
Direccion y Maginitud

Clausulas de Horn propuestas V2.0
            | NO      | NE       | SO        | SE
[0.0 : 0.2] | (1, 1)  | (-1, 1)  | (1, -1)   | (-10, -1)
[0.2 : 0.7] | (5, 5)  | (-5, 5)  | (5, -5)   | (-10, -5)
[0.7 : 1.0] | (10, 10)| (-10, 10)| (10, -10) | (-10, -10)
Cambio en X y Y 
''' 

'''
Reglas
IF x = [0.0 : 0.2] AND x, y = NO then m = (1, 1) -> moveto(x+1, y+1) 
..el resto..
'''


# return the absolute distance between two points
abs_dist = lambda x, y: math.sqrt(x**2 + y**2)

# return the angle adjacent to x in a right triangle
abs_angle = lambda x, y: math.degrees(math.atan(y/x))

# return the sign of a value
sign = lambda x: (1, -1)[x < 0]

# FUNCIONES LINGUISTICAS
# return the modeled value based on the function provided
distance_ling = lambda x: 0.02551565 + 0.01470778*x - 0.00005531812*x**2 if x < 142 else 0

# return the direction based on the signs of the triangle legs REQUIRES SIGNED INPUT
orientation_ling = lambda x, y: 'NO' if (x == 1 and y == 1) else ('NE' if (x == -1 and y == 1) else ('SE' if (x ==-1 and y ==-1) else ('SO' if (x ==1 and y ==-1) else 0)))

a = 6
b = -7
print(orientation_ling(sign(a), sign(b))) 

# not used
# orientation_ling = lambda a: 'N' if (a > 45 and a < 135) else ('O' if (a > 135 and a < 180) else ('E' if (a > 0 and a < 45) else 0))
