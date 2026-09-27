import json
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'traza.json').read_text(encoding='utf-8'))
BG = '#0B1020'
INK = '#EEF3FF'
MUTED = '#9BAAC8'
CYAN = '#49D9E8'
GOLD = '#FFD166'
PURPLE = '#A78BFA'
GREEN = '#5BE0A5'
config.background_color = BG


class FenwickVideo(Scene):
    def text(self, content, size=28, color=INK, width=12):
        t = Text(str(content), font='Segoe UI', font_size=size, color=color)
        if t.width > width:
            t.scale_to_fit_width(width)
        return t

    def header(self, number, title, subtitle):
        self.play(FadeOut(Group(*self.mobjects)), run_time=.5) if self.mobjects else None
        tag = self.text(f'FENWICK TREE   /   {number:02d}', 16, CYAN).move_to([-4.9, 3.52, 0])
        title_m = self.text(title, 38).move_to([0, 2.98, 0])
        sub = self.text(subtitle, 21, MUTED).move_to([0, 2.40, 0])
        line = Line([-6.35, 2.08, 0], [6.35, 2.08, 0], color='#283650')
        self.play(FadeIn(tag), Write(title_m), FadeIn(sub), Create(line), run_time=1.1)

    def note(self, content, color=CYAN):
        t = self.text(content, 24, color, 11.7).move_to([0, -3.25, 0])
        box = RoundedRectangle(width=12.5, height=.62, corner_radius=.13,
                               stroke_color='#283650', fill_color='#131E34', fill_opacity=1)
        box.move_to(t)
        g = VGroup(box, t)
        if hasattr(self, 'footer') and self.footer in self.mobjects:
            self.play(ReplacementTransform(self.footer, g), run_time=.35)
        else:
            self.play(FadeIn(g), run_time=.35)
        self.footer = g

    def array(self, values, y=-1.95):
        cells, labels = [], []
        for k, value in enumerate(values):
            x = (k-3.5)*1.14
            rect = RoundedRectangle(width=.94, height=.60, corner_radius=.10,
                                    stroke_color='#506180', fill_color='#152139', fill_opacity=1)
            rect.move_to([x,y,0])
            number = self.text(value, 27).move_to(rect)
            idx = self.text(k+1, 16, MUTED).move_to([x,y-.52,0])
            cells.append(rect); labels.append(number)
            self.add(idx)
        self.play(LaggedStart(*[FadeIn(VGroup(c,t), shift=UP*.12) for c,t in zip(cells,labels)], lag_ratio=.07), run_time=.8)
        return cells, labels

    def tree(self):

        positions = {8:(0,1.40),4:(-2.15,.35),6:(2.15,.35),7:(4.3,.35),
                     2:(-3.3,-.70),3:(-1.05,-.70),5:(2.15,-.70),1:(-4.4,-1.40)}
        nodes = {}; edges = VGroup()
        for d in DATA['nodes']:
            i=d['i']; x,y=positions[i]
            circle=Circle(radius=.30, stroke_color=CYAN, fill_color=BG, fill_opacity=1).move_to([x,y,0])
            label=self.text(i,24).move_to(circle)
            nodes[i]=VGroup(circle,label).set_z_index(2)
        for d in DATA['nodes']:
            if d['parent']<=8:
                edges.add(Line(nodes[d['i']].get_center(), nodes[d['parent']].get_center(), buff=.33, color='#465874'))
        self.play(LaggedStart(*[Create(e) for e in edges],lag_ratio=.08),run_time=.8)
        self.play(LaggedStart(*[GrowFromCenter(n) for n in nodes.values()],lag_ratio=.06),run_time=.8)
        return nodes

    def bit_row(self):
        values=[n['value'] for n in DATA['nodes']]
        cells, labels=self.array(values, y=.65)
        self.add(self.text('BIT',18,CYAN).move_to([-5.45,.65,0]))
        return cells,labels

    def construct(self):
        self.header(1,'Fenwick Tree','Sumas que cambian. Respuestas rápidas.')
        bars=VGroup(*[RoundedRectangle(width=.64,height=v*.20,corner_radius=.07,
                    fill_color=CYAN,fill_opacity=.75,stroke_width=0).move_to([(i-3.5)*1.05,-.6+v*.10,0])
                    for i,v in enumerate(DATA['values'])])
        self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.1),run_time=1.5)
        self.play(Write(self.text('Ventas diarias  →  total de un intervalo',28).move_to([0,-1.45,0])))
        self.note('TDA: arreglo numérico con actualización puntual y consulta de suma.')
        self.wait(5)
        self.header(2,'El problema','Consultar es fácil… hasta que los valores cambian.')
        cells,labels=self.array(DATA['values'],y=.6)
        for c in cells:
            self.play(c.animate.set_fill(CYAN,.55),run_time=.16)
        self.play(Write(self.text('Recorrer el arreglo: O(n) por consulta',30).move_to([0,-.55,0])))
        self.play(Write(self.text('Prefijos precalculados: actualizar puede costar O(n)',25,MUTED).move_to([0,-1.3,0])))
        self.note('Fenwick equilibra ambas operaciones: O(log n).')
        self.wait(4)
        self.header(3,'La clave está en los bits','lowbit(i) = i & (-i): el bit encendido menos significativo.')
        rows=VGroup()
        for y,i in zip([1.15,.20,-.75],[4,6,8]):
            d=DATA['nodes'][i-1]
            row=self.text(f'i = {i}     {i:04b}     →     lowbit = {d["lowbit"]}',31,width=10).move_to([0,y,0])
            rows.add(row)
            self.play(Write(row),run_time=1)
            self.play(Indicate(row,color=GOLD),run_time=.65)
        self.note('Cada BIT[i] guarda lowbit(i) elementos consecutivos.')
        self.wait(4)
        self.header(4,'¿Qué guarda cada nodo?','BIT[i] = suma desde i − lowbit(i) + 1 hasta i.')
        nodes=self.tree()
        cells,labels=self.array(DATA['values'],y=-2.23)

        for i in [2,4,6,8]:
            d=DATA['nodes'][i-1]
            selected=cells[d['start']-1:i]
            self.play(nodes[i][0].animate.set_fill(GOLD,.7),
                      *[c.animate.set_fill(CYAN,.50) for c in selected],run_time=.45)
            expression=' + '.join(str(v) for v in DATA['values'][d['start']-1:i])
            self.note(f'BIT[{i}]   ·   [{d["start"]}..{i}]   ·   {expression} = {d["value"]}',GOLD)
            pulses=VGroup(*[Dot(c.get_top(),radius=.055,color=GOLD) for c in selected])
            self.add(pulses)
            self.play(*[p.animate.move_to(nodes[i].get_center()) for p in pulses],run_time=.85)
            self.remove(pulses)
            self.play(Indicate(nodes[i],color=GOLD,scale_factor=1.12),run_time=.45)
            self.wait(2)
            self.play(nodes[i][0].animate.set_fill(BG,1),*[c.animate.set_fill('#152139',1) for c in selected],run_time=.3)
        self.header(5,'Consultar un prefijo','prefix(7): sumar A[1] hasta A[7], sin visitar cada casilla.')
        bit_cells,bit_labels=self.bit_row()
        cells,labels=self.array(DATA['values'],y=-1.65)
        accumulator=self.text('suma = 0',34,GOLD).move_to([0,-.4,0]);self.play(FadeIn(accumulator))
        path=[]
        for step in DATA['query']:
            i=step['i'];d=DATA['nodes'][i-1];path.append(str(i))
            self.play(bit_cells[i-1].animate.set_fill(GOLD,.5),
                      *[cells[j-1].animate.set_fill(CYAN,.5) for j in range(d['start'],i+1)],run_time=.5)
            new=self.text(f'suma = {step["sum"]}',34,GOLD).move_to(accumulator)
            self.play(Transform(accumulator,new),Indicate(bit_labels[i-1],color=GOLD),run_time=.65)
            self.note(f'i = {i}  →  i − lowbit(i) = {step["next"]}     |     recorrido: '+ ' → '.join(path))
            self.wait(2.5)
        self.note(f'prefix(7) = {DATA["query_result"]}   ·   3 bloques disjuntos; ningún elemento se cuenta dos veces.',GREEN)
        self.wait(3)
        self.header(6,'Consultar cualquier intervalo','sum(l, r) = prefix(r) − prefix(l − 1)')
        cells,labels=self.array(DATA['values'],y=.9)
        self.play(*[cells[j].animate.set_fill(CYAN,.55) for j in range(7)],run_time=.7)
        self.play(Write(self.text(f'prefix(7) = {DATA["query_result"]}',32,CYAN).move_to([0,-.15,0])))
        for step in DATA['left_query']:
            self.play(*[cells[j].animate.set_fill(PURPLE,.7) for j in range(step['i'])],run_time=.6)
        left=DATA['left_query'][-1]['sum']
        self.play(Write(self.text(f'Quitamos prefix(2) = {left}',28,PURPLE).move_to([0,-.9,0])))
        self.play(*[cells[j].animate.set_fill('#152139',1) for j in range(2)],run_time=.6)
        self.play(Write(self.text(f'sum(3, 7) = {DATA["query_result"]} − {left} = {DATA["range_result"]}',34,GOLD).move_to([0,-1.8,0])))
        self.note('Dos consultas de prefijo siguen costando O(log n).')
        self.wait(5)
        self.header(7,'Actualizar un valor','add(3, +4): A[3] pasa de 5 a 9.')
        bit_cells,bit_labels=self.bit_row()
        cells,labels=self.array(DATA['values'],y=-1.65)
        self.play(cells[2].animate.set_fill(GREEN,.5),Transform(labels[2],self.text(9,27).move_to(labels[2])),run_time=.7)
        for step in DATA['update']:
            i=step['i']
            self.note(f'BIT[{i}]: {step["before"]} + 4 = {step["after"]}     |     siguiente: {i} + lowbit({i}) = {step["next"]}',GREEN)
            pulse=Dot(cells[2].get_top(),color=GREEN);self.add(pulse)
            self.play(pulse.animate.move_to(bit_cells[i-1]),run_time=.7);self.remove(pulse)
            self.play(bit_cells[i-1].animate.set_fill(GREEN,.5),Transform(bit_labels[i-1],self.text(step['after'],27).move_to(bit_labels[i-1])),run_time=.65)
            self.wait(2)
        self.play(Write(self.text('3 → 4 → 8 → 16: salimos del arreglo',27,GREEN).move_to([0,-.45,0])))
        self.wait(2)
        terms=' + '.join(str(s['value']) for s in DATA['updated_query'])
        self.note(f'Nueva consulta: prefix(7) = {terms} = {DATA["updated_result"]}',GREEN)
        self.wait(4)
        self.header(8,'Caso borde: el prefijo vacío','Cuando i = 0, la consulta termina sin acceder a BIT[0].')
        zero=self.text('prefix(0) = 0',55,GOLD).move_to([0,.8,0]);self.play(Write(zero))
        self.play(Write(self.text('sum(1, r) = prefix(r) − prefix(0)',32).move_to([0,-.25,0])))
        self.play(Write(self.text(f'Un solo elemento: [9]  →  prefix(1) = {DATA["single"]}',28,GREEN).move_to([0,-1.25,0])))
        assert DATA['zero']==0
        self.note('Las actualizaciones usan índices de 1 a n; el índice 0 no se actualiza.')
        self.wait(5)
        self.header(9,'¿Por qué O(log n)?','La consulta elimina un bit encendido en cada salto.')
        bits=VGroup(*[self.text(s,39,CYAN).move_to([x,.95,0]) for x,s in zip([-4.6,-1.55,1.55,4.6],['0111','0110','0100','0000'])])
        self.play(LaggedStart(*[Write(b) for b in bits],lag_ratio=.5),run_time=2)
        arrows=VGroup(*[Arrow(bits[i].get_right(),bits[i+1].get_left(),buff=.15,color=MUTED) for i in range(3)])
        self.play(Create(arrows),run_time=.8)
        for y,line in zip([-.10,-.70,-1.30,-1.90],['Consulta de prefijo / rango     O(log n)','Actualización puntual             O(log n)','Memoria del arreglo BIT          O(n)','Construcción usada aquí           O(n log n)']):
            self.play(FadeIn(self.text(line,27).move_to([0,y,0]),shift=UP*.1),run_time=.45)
        self.note('Actualizar salta hacia bloques mayores: también hay O(log n) saltos.')
        self.wait(5)
        self.header(10,'Pequeños bloques. Grandes ahorros.','Fenwick Tree · Binary Indexed Tree')
        for y,line,color in [(1.1,'Guardar sumas parciales',CYAN),(.15,'Consultar bajando: i − lowbit(i)',GOLD),(-.8,'Actualizar subiendo: i + lowbit(i)',GREEN)]:
            self.play(Write(self.text(line,32,color).move_to([0,y,0])),run_time=.8)
        self.play(FadeIn(self.text('Proyecto de Algoritmos y Estructuras de Datos',22,MUTED).move_to([0,-2.05,0])))
        self.note('Implementación propia en C++ · Animación generada con Manim')
        self.wait(5)
        self.play(FadeOut(Group(*self.mobjects)),run_time=1)
