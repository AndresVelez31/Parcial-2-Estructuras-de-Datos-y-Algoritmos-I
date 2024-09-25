import sys

# Clase Nodo que representa cada nodo en el árbol
class Nodo:
    def __init__(self, valor, padre=None):
        self.valor = valor
        self.padre = padre
        self.izquierda = None
        self.derecha = None
        self.altura = 1

# Clase que representa un Árbol AVL
class ArbolAVL:
    def __init__(self):
        self.raiz = None

    # Método para insertar un nodo en el árbol
    def insertar(self, valor, nodo_actual):
        if not self.raiz:
            self.raiz = Nodo(valor)
            return
        
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda:
                self.insertar(valor, nodo_actual.izquierda)
            else:
                nodo_actual.izquierda = Nodo(valor, nodo_actual)
                self._revisar_insertar(nodo_actual.izquierda)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecha:
                self.insertar(valor, nodo_actual.derecha)
            else:
                nodo_actual.derecha = Nodo(valor, nodo_actual)
                self._revisar_insertar(nodo_actual.derecha)
        else:
            print("El Valor que estas insertando ya se encuentra en el arbol")
          
            
    # Método para verificar e inspeccionar si se necesita reequilibrar tras una inserción
    def _revisar_insertar(self, nodo_actual, camino=[]):
        if nodo_actual.padre is None: return
        camino = [nodo_actual] + camino

        balance = self._obtener_balance(nodo_actual.padre)

        if abs(balance) > 1:
            camino = [nodo_actual.padre] + camino
            self._reequilibrar_nodo(camino[0], camino[1], camino[2])
            return

        nueva_altura = 1 + nodo_actual.altura 
        if nueva_altura > nodo_actual.padre.altura:
            nodo_actual.padre.altura = nueva_altura

        self._revisar_insertar(nodo_actual.padre, camino)
        
        
    # Método para obtener el balance de un nodo
    def _obtener_balance(self, nodo_actual):
        if nodo_actual is None:
            return 0
        return self._obtener_altura(nodo_actual.izquierda) - self._obtener_altura(nodo_actual.derecha)
    
    # Método para obtener la altura de un nodo
    def _obtener_altura(self, nodo_actual):
        if nodo_actual is None: return 0
        return nodo_actual.altura


    # Método para reequilibrar el árbol en caso de que se desequilibre
    def _reequilibrar_nodo(self, z, y, x):
        if y == z.izquierda and x == y.izquierda:
            self._rotar_derecha(z)
        elif y == z.izquierda and x == y.derecha:
            self._rotar_izquierda(y)
            self._rotar_derecha(z)
        elif y == z.derecha and x == y.derecha:
            self._rotar_izquierda(z)
        elif y == z.derecha and x == y.izquierda:
            self._rotar_derecha(y)
            self._rotar_izquierda(z)
        else:
            raise Exception('_reequilibrar_nodo: ¡Configuración de nodos z, y, x no reconocida!')
    
    
    # Rotación a la derecha
    def _rotar_derecha(self, y):
        sub_raiz = y.padre
        z = y.izquierda
        t3 = z.derecha
        z.derecha = y
        y.padre = z
        y.izquierda = t3
        
        if t3 is not None: 
            t3.padre = y
            
        z.padre = sub_raiz
        
        if z.padre is None:
            self.raiz = z
        else:
            if z.padre.izquierda == y:
                z.padre.izquierda = z
            else:
                z.padre.derecha = z
                
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        
    
    # Rotación a la izquierda
    def _rotar_izquierda(self, z):
        sub_raiz = z.padre
        y = z.derecha
        t2 = y.izquierda
        y.izquierda = z
        z.padre = y
        z.derecha = t2
        
        if t2 is not None: 
            t2.padre = z
            
        y.padre = sub_raiz
        
        if y.padre is None:
            self.raiz = y
        else:
            if y.padre.izquierda == z:
                y.padre.izquierda = y
            else:
                y.padre.derecha = y
                
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
    
    
    # Método para eliminar un nodo del árbol
    def eliminar(self, valor, nodo_actual):
        if not self.raiz:
            print("El árbol está vacío, no se puede eliminar.")
            return
        
        if nodo_actual is None:
            print("El nodo no existe en el árbol.")
            return nodo_actual

        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self.eliminar(valor, nodo_actual.izquierda)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self.eliminar(valor, nodo_actual.derecha)
        else:
            if nodo_actual.izquierda is None:
                temp = nodo_actual.derecha
                nodo_actual = None
                return temp
            elif nodo_actual.derecha is None:
                temp = nodo_actual.izquierda
                nodo_actual = None
                return temp

            temp = self.obtener_minimo(nodo_actual.derecha)
            nodo_actual.valor = temp.valor
            nodo_actual.derecha = self.eliminar(temp.valor, nodo_actual.derecha)

        if nodo_actual is None:
            return nodo_actual

        nodo_actual.altura = 1 + max(self._obtener_altura(nodo_actual.izquierda), self._obtener_altura(nodo_actual.derecha))

        balance = self._obtener_balance(nodo_actual)

        if balance > 1 and self._obtener_balance(nodo_actual.izquierda) >= 0:
            return self._rotar_derecha(nodo_actual)

        if balance > 1 and self._obtener_balance(nodo_actual.izquierda) < 0:
            nodo_actual.izquierda = self._rotar_izquierda(nodo_actual.izquierda)
            return self._rotar_derecha(nodo_actual)

        if balance < -1 and self._obtener_balance(nodo_actual.derecha) <= 0:
            return self._rotar_izquierda(nodo_actual)

        if balance < -1 and self._obtener_balance(nodo_actual.derecha) > 0:
            nodo_actual.derecha = self._rotar_derecha(nodo_actual.derecha)
            return self._rotar_izquierda(nodo_actual)

        return nodo_actual

    # Método para obtener el valor mínimo en el árbol
    def obtener_minimo(self, nodo_actual):
        if nodo_actual is None or nodo_actual.izquierda is None:
            return nodo_actual
        return self.obtener_minimo(nodo_actual.izquierda)


    # Método para obtener el valor máximo en el árbol
    def obtener_maximo(self, nodo_actual):
        if nodo_actual is None or nodo_actual.derecha is None:
            return nodo_actual
        return self.obtener_maximo(nodo_actual.derecha)


    # Método para obtener la raíz del árbol
    def obtener_raiz(self):
        return self.raiz.valor

    # Recorrido en orden del árbol
    def recorrido_in_order(self, nodo):
        if nodo:
            self.recorrido_in_order(nodo.izquierda)
            print(nodo.valor, end=" - ")
            self.recorrido_in_order(nodo.derecha)
    
    
    # Recorrido en preorden del árbol
    def recorrido_pre_order(self, nodo):
        if nodo:
            print(nodo.valor, end=" - ")
            self.recorrido_pre_order(nodo.izquierda)
            self.recorrido_pre_order(nodo.derecha)


    # Recorrido en postorden del árbol
    def recorrido_post_order(self, nodo):
        if nodo:
            self.recorrido_post_order(nodo.izquierda)
            self.recorrido_post_order(nodo.derecha)
            print(nodo.valor, end=" - ")
    
    # Metodo para buscar en el arbol
    def buscar(self, nodo, valor):
        if not nodo or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self.buscar(nodo.izquierda, valor)
        return self.buscar(nodo.derecha, valor)


    # Método para imprimir el árbol
    def imprimir_arbol(self, nodo, nivel=0):
        if nodo is not None:
            self.imprimir_arbol(nodo.derecha, nivel + 1)
            print(" " * 4 * nivel + "-> " + str(nodo.valor))
            self.imprimir_arbol(nodo.izquierda, nivel + 1)


def main():
    arbol = ArbolAVL()

    while True:
        
        print("\n"
            +"-" * 40 
            + "\n\n\t Menú del Árbol AVL\n"
            + "\n1. ¿Esta vacio el Arbol?" 
            + "\n2. Insertar un nodo" 
            + "\n3. Eliminar un nodo" 
            + "\n4. Buscar un nodo" 
            + "\n5. Recorrido en preorden" 
            + "\n6. Recorrido en inorden" 
            + "\n7. Recorrido en postorden" 
            + "\n8. Obtener Raiz" 
            + "\n9. Obtener Valor Maximo del Arbol"
            + "\n10. Obtener Valor Minimo del Arbol"
            + "\n11. Obtener Factor de Balance de Cierto Nodo"
            + "\n12. Obtener Altura Total del Arbol"
            + "\n13. Imprimir árbol" 
            + "\n0. Salir\n\n" 
            + "-" * 40)
        
        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            if arbol.raiz is None:
                print("\nEl árbol está vacío.")
            else:
                print("\nEl árbol no está vacío.")
                
        elif opcion == "2":
            nodo = int(input("\nIngrese el valor del nodo: "))
            arbol.insertar(nodo, arbol.raiz)
            print(f"Clave {nodo} insertada.")

        elif opcion == "3":
            nodo = int(input("\nIngrese el valor del nodo a eliminar: "))
            arbol.eliminar(nodo, arbol.raiz)
            print(f"Clave {nodo} eliminada.")

        elif opcion == "4":
            nodo = int(input("\nIngrese el nodo a buscar: "))
            resultado = arbol.buscar(arbol.raiz, nodo)
            print(f"Búsqueda del nodo {nodo}: {'Encontrado' if resultado else 'No encontrado'}")

        elif opcion == "5":
            print("\nRecorrido en preorden: ", end="")
            arbol.recorrido_pre_order(arbol.raiz)
            print()

        elif opcion == "6":
            print("\nRecorrido en inorden: ", end="")
            arbol.recorrido_in_order(arbol.raiz)
            print()

        elif opcion == "7":
            print("\nRecorrido en postorden: ", end="")
            arbol.recorrido_post_order(arbol.raiz)
            print()
        
        elif opcion == "8":
            if arbol.raiz is None:
                print("\nEl árbol está vacío.")
            else:
                print("\nRaíz del árbol: ", arbol.obtener_raiz())
        
        elif opcion == "9":
            print(f"\nValor Maximo del Arbol: {arbol.obtener_maximo(arbol.raiz).valor}")
        
        elif opcion == "10":
            print(f"\nValor Minimo del Arbol: {arbol.obtener_minimo(arbol.raiz).valor}")
            
        elif opcion == "11":
            nodo = int(input("\nIngrese el nodo para obtener el factor de balance: "))
            print(f"\nEl Factor de balance del nodo {nodo} es {arbol._obtener_balance(arbol.buscar(arbol.raiz, nodo))}")
        
        elif opcion == "12":
            print(f"\nLa Altura Total del Arbol es {arbol._obtener_altura(arbol.raiz)}")
        
        elif opcion == "13":
            print("\nÁrbol AVL actual:\n")
            arbol.imprimir_arbol(arbol.raiz)

        elif opcion == "0":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Inténtalo de nuevo.")
            
# Función principal para ejecutar el programa
if __name__ == "__main__":
    main()