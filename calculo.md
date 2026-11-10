# Lote 3: Questões e Resoluções - Integrais de Linha e Campos Conservativos

---

## Questão 1: Integral de Linha de Campo Escalar (Centro de Massa)

**Enunciado:**  
Calcule a integral de linha do campo escalar $f(x, y) = x y^4$ ao longo da metade superior da circunferência $x^2 + y^2 = 16$, percorrida no sentido anti-horário:
$$\int_C x y^4 \, ds$$

---

### **Resolução Detalhada:**

1. **Parametrizar a curva $C$:**  
   Semicírculo de raio $R = 4$ na região superior ($y \ge 0$):
   $$\mathbf{r}(t) = (4\cos t, 4\sin t), \quad 0 \le t \le \pi$$

2. **Calcular o elemento de comprimento de arco $ds$:**  
   $$\mathbf{r}'(t) = (-4\sin t, 4\cos t)$$
   $$\|\mathbf{r}'(t)\| = \sqrt{(-4\sin t)^2 + (4\cos t)^2} = \sqrt{16\sin^2 t + 16\cos^2 t} = \sqrt{16} = 4$$
   $$ds = 4 \, dt$$

3. **Substituir a parametrização no campo escalar $f(\mathbf{r}(t))$:**  
   $$f(x(t), y(t)) = (4\cos t)(4\sin t)^4 = 4\cos t \cdot 256\sin^4 t = 1024 \sin^4 t \cos t$$

4. **Montar e resolver a integral:**  
   $$\int_C x y^4 \, ds = \int_{0}^{\pi} (1024 \sin^4 t \cos t) \cdot 4 \, dt = 4096 \int_{0}^{\pi} \sin^4 t \cos t \, dt$$

   Fazendo a substituição $u = \sin t \implies du = \cos t \, dt$:
   - Quando $t = 0 \implies u = \sin 0 = 0$
   - Quando $t = \pi \implies u = \sin \pi = 0$

   Como os limites de integração em $u$ vão de $0$ a $0$:
   $$4096 \int_{0}^{0} u^4 \, du = 0$$

   *(Nota geométrica: Por simetria, $x$ é uma função ímpar em relação ao eixo $y$, enquanto $y^4$ e $ds$ são pares. Logo, a integral em um domínio simétrico em $x$ resulta em $0$.)*

---

## Questão 2: Integral de Linha de Campo Vetorial em uma Curva Espacial

**Enunciado:**  
Calcule o trabalho $W = \int_C \mathbf{F} \cdot d\mathbf{r}$ realizado pelo campo vetorial $\mathbf{F}(x, y, z) = (y z, x z, x y)$ ao longo da hélice cúbica parametrizada por:
$$\mathbf{r}(t) = (t, t^2, t^3), \quad 0 \le t \le 1$$

---

### **Resolução Detalhada:**

1. **Obter o vetor diferencial $d\mathbf{r} = \mathbf{r}'(t) dt$:**  
   $$\mathbf{r}'(t) = (1, 2t, 3t^2) \implies d\mathbf{r} = (1, 2t, 3t^2) \, dt$$

2. **Substituir a parametrização no campo $\mathbf{F}(\mathbf{r}(t))$:**  
   Como $x = t$, $y = t^2$, $z = t^3$:
   $$\mathbf{F}(\mathbf{r}(t)) = ( (t^2)(t^3), (t)(t^3), (t)(t^2) ) = (t^5, t^4, t^3)$$

3. **Calcular o produto escalar $\mathbf{F}(\mathbf{r}(t)) \cdot \mathbf{r}'(t)$:**  
   $$\mathbf{F}(\mathbf{r}(t)) \cdot \mathbf{r}'(t) = (t^5, t^4, t^3) \cdot (1, 2t, 3t^2)$$
   $$= t^5(1) + t^4(2t) + t^3(3t^2) = t^5 + 2t^5 + 3t^5 = 6t^5$$

4. **Calcular a integral:**  
   $$W = \int_{0}^{1} 6t^5 \, dt = \left[ t^6 \right]_{0}^{1} = 1^6 - 0^6 = 1$$

---

## Questão 3: Campo Conservativo em 3D e Independência do Caminho

**Enunciado:**  
Dado o campo vetorial $\mathbf{F}(x, y, z) = (y e^{xy} + z, x e^{xy} + 2y z, x + y^2)$:
1. Mostre que $\mathbf{F}$ é conservativo ($\text{rot } \mathbf{F} = \mathbf{0}$).
2. Encontre uma função potencial $f(x, y, z)$ tal que $\nabla f = \mathbf{F}$.
3. Calcule $\int_C \mathbf{F} \cdot d\mathbf{r}$, onde $C$ é uma curva suave qualquer ligando $A(0, 0, 0)$ a $B(1, 1, 2)$.

---

### **Resolução Detalhada:**

#### **Parte 1: Verificação de Campo Conservativo**
Para $\mathbf{F} = (P, Q, R)$:
- $P = y e^{xy} + z$
- $Q = x e^{xy} + 2y z$
- $R = x + y^2$

Testando as derivadas parciais cruzadas:
- $\frac{\partial P}{\partial y} = e^{xy} + x y e^{xy}$, $\quad \frac{\partial Q}{\partial x} = e^{xy} + x y e^{xy} \implies \frac{\partial P}{\partial y} = \frac{\partial Q}{\partial x}$
- $\frac{\partial P}{\partial z} = 1$, $\quad \frac{\partial R}{\partial x} = 1 \implies \frac{\partial P}{\partial z} = \frac{\partial R}{\partial x}$
- $\frac{\partial Q}{\partial z} = 2y$, $\quad \frac{\partial R}{\partial y} = 2y \implies \frac{\partial Q}{\partial z} = \frac{\partial R}{\partial y}$

Como todas as derivadas cruzadas coincidem em todo o $\mathbb{R}^3$, **o campo $\mathbf{F}$ é conservativo**.

---

#### **Parte 2: Obtenção da Função Potencial $f(x, y, z)$**

1. Integrando $\frac{\partial f}{\partial x} = y e^{xy} + z$ em relação a $x$:
   $$f(x, y, z) = e^{xy} + x z + g(y, z)$$

2. Derivando em relação a $y$ e igualando a $Q$:
   $$\frac{\partial f}{\partial y} = x e^{xy} + \frac{\partial g}{\partial y} = x e^{xy} + 2y z \implies \frac{\partial g}{\partial y} = 2y z$$
   Integrando em relação a $y$:
   $$g(y, z) = y^2 z + h(z)$$
   Assim:
   $$f(x, y, z) = e^{xy} + x z + y^2 z + h(z)$$

3. Derivando em relação a $z$ e igualando a $R$:
   $$\frac{\partial f}{\partial z} = x + y^2 + h'(z) = x + y^2 \implies h'(z) = 0 \implies h(z) = C$$

Adotando a constante $C = 0$:
$$f(x, y, z) = e^{xy} + x z + y^2 z$$

---

#### **Parte 3: Cálculo da Integral pelo Teorema Fundamental**
$$\int_C \mathbf{F} \cdot d\mathbf{r} = f(1, 1, 2) - f(0, 0, 0)$$

Avaliando a função nos pontos limite:
- $f(0, 0, 0) = e^0 + (0)(0) + (0)^2(0) = 1$
- $f(1, 1, 2) = e^{(1)(1)} + (1)(2) + (1)^2(2) = e^1 + 2 + 2 = e + 4$

Portanto:
$$\int_C \mathbf{F} \cdot d\mathbf{r} = (e + 4) - 1 = e + 3$$