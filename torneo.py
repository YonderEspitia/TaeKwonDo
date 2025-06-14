import random
import math

class TorneoTaekwondo:
    """Clase para gestionar un torneo de Taekwondo y generar pirámides."""

    def __init__(self, atletas):
        if not all('nombre' in a and 'edad' in a and 'peso' in a and 'cinturon' in a for a in atletas):
            raise ValueError("Cada atleta debe tener 'nombre', 'edad', 'peso' y 'cinturon'.")
        self.atletas = atletas
        self.categorias = self._categorizar_atletas()

    def _get_categoria_edad(self, edad):
        """Determina la categoría de edad del atleta."""
        if edad <= 11:
            return "Infantil"
        elif 12 <= edad <= 14:
            return "Cadete"
        elif 15 <= edad <= 17:
            return "Junior"
        elif 18 <= edad <= 30:
            return "Senior"
        else:
            return "Master"

    def _get_categoria_peso_senior(self, peso):
        """Determina la categoría de peso para Seniors."""
        if peso < 58:
            return "Fly (-58kg)"
        elif 58 <= peso < 68:
            return "Feather (-68kg)"
        elif 68 <= peso < 80:
            return "Welter (-80kg)"
        else:
            return "Heavy (+80kg)"

    def _get_categoria_cinturon(self, cinturon):
        """Agrupa los cinturones en categorías generales."""
        cinturon = cinturon.lower()
        if cinturon in ["blanco", "amarillo"]:
            return "Principiante (Blanco-Amarillo)"
        elif cinturon in ["verde", "azul"]:
            return "Intermedio (Verde-Azul)"
        elif cinturon in ["rojo", "negro"]:
            return "Avanzado (Rojo-Negro)"
        else:
            return "Otro"

    def _categorizar_atletas(self):
        """Agrupa a los atletas en categorías basadas en edad, nivel de cinturón y peso."""
        categorias = {}
        for atleta in self.atletas:
            cat_edad = self._get_categoria_edad(atleta['edad'])
            cat_cinturon = self._get_categoria_cinturon(atleta['cinturon'])

            if cat_edad == "Senior":
                cat_peso = self._get_categoria_peso_senior(atleta['peso'])
                llave_categoria = f"{cat_edad} - {cat_cinturon} - {cat_peso}"
            else:
                llave_categoria = f"{cat_edad} - {cat_cinturon}"

            categorias.setdefault(llave_categoria, []).append(atleta)
        return categorias

    def _imprimir_piramide(self, nombre_categoria, competidores):
        print("\n" + "="*50)
        print(f" CATEGORÍA: {nombre_categoria.upper()}")
        print(f" NÚMERO DE COMPETIDORES: {len(competidores)}")
        print("="*50)

        if len(competidores) < 2:
            print("\nNo hay suficientes competidores para generar una pirámide.\n")
            if competidores:
                print(f"Campeón por defecto: {competidores[0]['nombre']}")
            return

        random.shuffle(competidores)
        num_competidores = len(competidores)
        siguiente_potencia = 2**math.ceil(math.log2(num_competidores))
        num_byes = siguiente_potencia - num_competidores

        ronda_1 = [a['nombre'] for a in competidores] + ["BYE"] * num_byes
        random.shuffle(ronda_1)

        print("\n---------- PIRÁMIDE DE COMPETICIÓN ----------\n")
        print("RONDA 1:")

        for i in range(0, len(ronda_1), 2):
            p1 = ronda_1[i]
            p2 = ronda_1[i+1]
            if p2 == "BYE":
                print(f"  - {p1}  -> (Pasa por BYE)")
            else:
                print(f"  - {p1} vs {p2}")

        rondas_restantes = int(math.log2(siguiente_potencia)) - 1
        for i in range(rondas_restantes):
            num_ronda = i + 2
            print(f"\nRONDA {num_ronda}:")
            for j in range(siguiente_potencia // (2**(i+2))):
                print(f"  - Ganador Partido {j*2+1} vs Ganador Partido {j*2+2}")

        print("\nFINAL:")
        print("  - Ganador Semifinal 1 vs Ganador Semifinal 2")
        print("\n" + "="*50 + "\n")

    def generar_piramides(self):
        if not self.categorias:
            print("No hay atletas para procesar.")
            return

        print("--- GENERANDO PIRÁMIDES DEL TORNEO ---")
        for nombre_cat, lista_atletas in self.categorias.items():
            self._imprimir_piramide(nombre_cat, lista_atletas)
