from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, NumericProperty, DictProperty

import PyPDF2
import docx

class Manager(ScreenManager):
    pass

texto=''
class Inicio(Screen):
    pass

class Escolha(Screen):
    def escolha(self, arq):
        global texto

        if '.pdf' in arq[-5:]:
            pdfFileObject = open(arq, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
            texto=' '.join([pdfReader.getPage(i).extractText() for i in range(pdfReader.numPages)])
            pdfFileObject.close()
            self.manager.current = 'exibir'

        elif '.txt' in arq[-5:]:
            doc = open(arq)
            texto= doc.read()
            doc.close()
            self.manager.current = 'exibir'

        elif '.docx' in arq[-5:]:
            texto = ' '.join([para.text for para in docx.Document(arq).paragraphs])
            self.manager.current = 'exibir'

class Exibidor(Screen):
    cont=0
    t=''
    klok=''

    def on_enter(self):
        global vel
        self.cont=0
        if texto.strip():
            self.t=[i for i in texto.replace('\n',' ').split(' ') if i and i!=' ']
            self.children[1].source='play.png'
        else:
            self.ids['texto'].text='NÃO FOI POSSILVEL\n    LER O ARQUIVO'
            self.children[1].source='nada.png'

    _play = 1
    def play(self):
        if texto.strip() and self.cont < len(self.t):
            if self._play:
                self.children[1].source='pausa.png'
                self.klok=Clock.schedule_interval(self.coisa, 60/vel)
                self._play = 0
            else:
                self.children[1].source='play.png'
                Clock.unschedule(self.klok)
                self._play = 1

    def coisa(self,x):
        self.ids['texto'].text=self.t[self.cont]
        self.cont+=1

        if self.cont >= len(self.t):
            Clock.unschedule(self.klok)
            self.children[1].source='nada.png'

    giro=1
    rotacao=NumericProperty(0)
    bt=DictProperty({"x":0, "top":1})
    bt_girar=DictProperty({"right":1, "top":1})
    bt_play=DictProperty({'center_x':.5, 'center_y':.25})
    def girar(self):
        if self.giro:
            self.rotacao=270
            self.giro=0
            self.bt={"right":1, "top":1}
            self.bt_girar={"right":1, "y":0}
            self.bt_play={'center_x':.25, 'center_y':.5}
        else:
            self.rotacao=0
            self.giro=1
            self.bt={"x":0, "top":1}
            self.bt_girar={"right":1, "top":1}
            self.bt_play={'center_x':.5, 'center_y':.25}

    def voltar(self):
        Clock.unschedule(self.klok)
        self.ids['texto'].text=''
        self.children[1].source='play.png'
        self._play = 1
        self.manager.current = 'inicio'

vel=0
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
        vel = int(self.text)

class Leitor_AgilApp(App):
    _1 = ListProperty([0.07450980392156863, 0.09803921568627451, 0.12941176470588237, 1.0])
    _2 = ListProperty([1.0, 0.6, 0.0, 1.0])
    def build(self):
        return Manager()

if __name__ == '__main__':
    Leitor_AgilApp().run()
