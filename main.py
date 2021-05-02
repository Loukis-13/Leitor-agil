from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, NumericProperty, DictProperty

# from kivy.config import Config
# Config.set('graphics', 'width', '480')
# Config.set('graphics', 'height', '854')
# Config.write()

import PyPDF2
import docx
import os 

class Manager(ScreenManager):
    pass

with open('db.txt', 'r') as f:
    dicio=eval(f.read())

texto = nome = ''
class Inicio(Screen):
    pass

class Escolha(Screen):
    def escolha(self, arq):
        global texto, nome

        if "\\" in arq:
            nome = arq.split("\\")[-1]
        elif "/" in arq:
            nome = arq.split("/")[-1]

        if '.pdf' in arq[-5:]:
            with open(arq, 'rb') as pdfFileObject :
                pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
                texto=' '.join([pdfReader.getPage(i).extractText() for i in range(pdfReader.numPages)])

        elif '.txt' in arq[-5:]:
            with open(arq) as doc:
                texto= doc.read()

        elif '.docx' in arq[-5:]:
            texto = ' '.join([para.text for para in docx.Document(arq).paragraphs])

        self.manager.current = 'exibir'

class Exibidor(Screen):
    cont=0
    t=''
    klok=''

    def on_enter(self):
        global vel, nome
        
        self.cont = dicio['arquivos'][nome] if dicio['arquivos'].get(nome) else 0

        if texto.strip():
            self.t=[i for i in texto.replace('\n',' ').split(' ') if i and i!=' ']
            if self.cont >= len(self.t)-1:
                self.cont=0
            self.ids['texto'].text=self.t[self.cont]
            self.ids['play'].source=os.path.join('img','play.png')
        else:
            self.ids['texto'].text='NÃO FOI POSSILVEL\n    LER O ARQUIVO'
            self.ids['play'].source=os.path.join('img','nada.png')

    def coisa(self,x):
        self.ids['texto'].text=self.t[self.cont]
        dicio['arquivos'][nome]=self.cont
        self.cont+=1

        if self.cont >= len(self.t):
            Clock.unschedule(self.klok)
            self.cont=0
            self.ids['play'].source=os.path.join('img','nada.png')

    _play = 1
    def play(self):
        if texto.strip() and self.cont <= len(self.t):
            if self._play:
                self.ids['play'].source=os.path.join('img','pausa.png')
                self.klok=Clock.schedule_interval(self.coisa, 60/int(vel))
                self._play = 0

            else:
                self.ids['play'].source=os.path.join('img','play.png')
                Clock.unschedule(self.klok)
                with open('db.txt', 'w') as f:
                    f.write(str(dicio))
                self._play = 1

    def restart(self):
        self.cont=0
        dicio['arquivos'][nome]=self.cont
        if self._play == 0:
            self.play()
        else:
            with open('db.txt', 'w') as f:
                f.write(str(dicio))
        self.ids['texto'].text=self.t[self.cont]

    def retro(self):
        if 5<=self.cont:
            self.cont-=5
        else:
            self.cont=0
        self.ids['texto'].text=self.t[self.cont]
        with open('db.txt', 'w') as f:
            f.write(str(dicio))

    giro=1
    rotacao=NumericProperty(0)
    bt_voltar=DictProperty({"x":0, "top":1})
    bt_girar=DictProperty({"right":1, "top":1})
    bt_play=DictProperty({'center_x':.5, 'center_y':.25})
    bt_restart=DictProperty({'center_x':.25, 'center_y':.25})
    bt_retro=DictProperty({'center_x':.75, 'center_y':.25})
    def girar(self):
        if self.giro:
            self.rotacao=270
            self.giro=0
            self.bt_voltar={"right":1, "top":1}
            self.bt_girar={"right":1, "y":0}
            self.bt_play={'center_x':.25, 'center_y':.5}
            self.bt_restart={'center_x':.25, 'center_y':.75}
            self.bt_retro={'center_x':.25, 'center_y':.25}
        else:
            self.rotacao=0
            self.giro=1
            self.bt_voltar={"x":0, "top":1}
            self.bt_girar={"right":1, "top":1}
            self.bt_play={'center_x':.5, 'center_y':.25}
            self.bt_restart={'center_x':.25, 'center_y':.25}
            self.bt_retro={'center_x':.75, 'center_y':.25}

    def voltar(self):
        Clock.unschedule(self.klok)
        self.ids['texto'].text=''
        self.ids['play'].source=os.path.join('img/play.png')
        self._play = 1
        self.manager.current = 'inicio'

vel=dicio['vel']
class VelInput(TextInput):
    pat = '0123456789'
    def insert_text(self, substring, from_undo=False):
        s = substring if substring in self.pat else ''
        return super(VelInput, self).insert_text(s, from_undo=from_undo)

    def on_text(self, instance, value):
        if not value:
            self.text = '1'
        elif int(value) < 0:
            self.text = '1'
        elif int(value) > 1001:
            self.text = '1000'

        global vel
        vel = self.text
        dicio['vel']=vel
        with open('db.txt', 'w') as f:
            f.write(str(dicio))

class Leitor_AgilApp(App):
    cores = ListProperty(dicio['cores'])
    vel=dicio['vel']

    def on_cores(s, i, v): 
        dicio.update({'cores': v})
        with open('db.txt', 'w') as f:
            f.write(str(dicio))

    def build(self):
        return Manager()

if __name__ == '__main__':
    Leitor_AgilApp().run()
