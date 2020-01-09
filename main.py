from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import json


class Manager(ScreenManager):
	pass


class Inicio(Screen):

	def on_pre_enter(self):
		# Faz com que o aplicativo chame a função "confirmExit quando for solicitado que feche"
		Window.bind(on_request_close=self.confirmExit) 


	# Cria um PopUp para o usuario confirmar que deseja sair
	def confirmExit(self, *args, **kwargs):
		#Toca o som do popUp
		global popSound
		popSound.play()

		box = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)
		botoes = BoxLayout(padding = 10, spacing = 10)

		pop = Popup(title = 'Deseja sair?', content=box, size_hint = (None, None), size = (100,100))

		sim = ButtonInicio(text= 'Sim', on_release = App.get_running_app().stop)
		nao = ButtonInicio(text = 'Não', on_release=pop.dismiss)

		botoes.add_widget(sim)
		botoes.add_widget(nao)

		atencao = Image(source='atencao.png')
		
		box.add_widget(atencao)
		box.add_widget(botoes)
		
		#Animações do texto do botão "sim": pisca nas cores preto e branco
		animText = Animation(color = (0,0,0,1), duration = 0.8) + Animation(color = (1,1,1,1), duration = 0.8)
		animText.repeat = True
		animText.start(sim)

		# Animações do PopUp: começa pequeno e atinge um tamanho maior
		anim = Animation(size =(300,180), duration = 0.15, t='out_back')
		anim.start(pop)

		pop.open()

		return True


class Listas(Screen):
	listas = []
	def on_pre_enter(self):
		# Deleta as listas pendentes na tela (para nao aparecer duplicado na tela)
		self.ids.box.clear_widgets()

		# path: pega o local do disposivo para salvar as informações. 
		# caso seja atualizado, não perderá esses dados
		self.path = App.get_running_app().user_data_dir + '/'

		#chama a função para ler listas armazenadas
		
		self.loadData()

		# Quando a tecla voltar for recebida (ou Esc), chama a função voltar
		Window.bind(on_keyboard = self.voltar)

		# Adiciona as lista da lista "lista" no widget de BoxLayout, para aparecer na tela
		for lista in self.listas:
			self.ids.box.add_widget(CardLista(text=lista))

	def on_pre_leave(self):
		# Cancela "Ficar esperando tecla voltar" para sair da tela 
		Window.unbind(on_keyboard = self.voltar)

	def voltar(self, window, key, *args):
		# key 27 = tecla Esc, se for recebida, volta para a tela Inicio
		if key == 27:
			App.get_running_app().root.current = 'inicio'
		return True  

	def addWidget(self):
		# Toca o som
		global poppapSound
		poppapSound.play()

		# Pega o texto do textInput
		text = self.ids.text.text

		# Adiciona o texto ao BoxLayout, para aparecer na tela
		self.ids.box.add_widget(CardLista(text))

		# Limpa o campo do textInput
		self.ids.text.text = ''

		# Adiciona o texto a lista de lista
		self.listas.append(text)

		# Salva
		self.saveData()
		
	def removeWidget(self, lista):
		# Toca o som
		global popSound
		popSound.play()

		# Guarda o texto que havia no widget (para remover da lista depois)
		text = lista.ids.button.text

		#remove o widget
		self.ids.box.remove_widget(lista)

		# Remove o texto da lista de lista
		self.listas.remove(text)

		# Salva
		self.saveData()
	
	def saveData(self, *args):
		# salva a data no diretorio
		with open(self.path+'listas.json', 'w') as data:
			json.dump(self.listas, data)

	def loadData(self, *args):
		# Tenta ler o arquivo data.json, caso não exista, não faz nada
		try:
			with open(self.path+'listas.json', 'r') as data:
				self.listas = json.load(data)
		except: # Para não dar erro caso não exista o arquivo
			pass

# Tela que contem as lista e um text input para adicionar novas lista
class Lista(Screen):
	lista = []
	path = ''
	
	
	# def __init__(self, name):
	# 	self.name = name


	def on_pre_enter(self):
		# Deleta as notas pendentes na tela (para nao aparecer duplicado na tela)
		self.ids.box.clear_widgets()

		# path: pega o local do disposivo para salvar as informações. 
		# caso seja atualizado, não perderá esses dados
		self.path = App.get_running_app().user_data_dir + '/'

		#chama a função para ler notas armazenadas
		self.loadData()

		# Quando a tecla voltar for recebida (ou Esc), chama a função voltar
		Window.bind(on_keyboard = self.voltar)

		# Adiciona as lista da lista "lista" no widget de BoxLayout, para aparecer na tela
		for nota in self.lista:
			self.ids.box.add_widget(Nota(text=nota))

	def on_pre_leave(self):
		# Cancela "Ficar esperando tecla voltar" para sair da tela 
		Window.unbind(on_keyboard = self.voltar)

	def voltar(self, window, key, *args):
		# key 27 = tecla Esc, se for recebida, volta para a tela Inicio
		if key == 27:
			App.get_running_app().root.current = 'inicio'
		return True  

	def saveData(self, *args):
		# salva a data no diretorio
		with open(self.path+self.name+'.json', 'w') as data:
			json.dump(self.lista, data)

	def addWidget(self):
		# Toca o som
		global poppapSound
		poppapSound.play()

		# Pega o texto do textInput
		text = self.ids.text.text

		# Adiciona o texto ao BoxLayout, para aparecer na tela
		self.ids.box.add_widget(Nota(text, self.name))

		# Limpa o campo do textInput
		self.ids.text.text = ''

		# Adiciona o texto a lista de lista
		self.lista.append(text)

		# Salva
		self.saveData()
		
	def removeWidget(self, nota):
		# Toca o som
		global popSound
		popSound.play()

		# Guarda o texto que havia no widget (para remover da lista depois)
		text = nota.ids.label.text

		#remove o widget
		self.ids.box.remove_widget(nota)

		# Remove o texto da lista de lista
		self.lista.remove(text)

		# Salva
		self.saveData()

	def loadData(self, *args):
		# Tenta ler o arquivo data.json, caso não exista, não faz nada
		try:
			with open(self.path+self.name+'.json', 'r') as data:
				self.lista = json.load(data)
		except: # Para não dar erro caso não exista o arquivo
			pass


class CardLista(BoxLayout):
	
	def __init__(self, text = '', **kwargs):
		super().__init__(**kwargs)
		self.ids.button.text = text
		self.lista = Lista(name = text)
		
		#self.lista.name = text
		App.get_running_app().root.add_widget(self.lista)


	def openLista(self):
		App.get_running_app().root.transition.direction = 'left'
		App.get_running_app().root.current = self.lista.name
		#App.get_running_app().root.switch_to(self.lista)

class Nota(BoxLayout):
	# Inicia o Widget de nota, com o texto
	def __init__(self, text = '',nome = '', **kwargs):
		super().__init__(**kwargs)
		self.ids.label.text = text
		self.lista_name = nome

# Botao personalisado, arredondado nas pontas 
class ButtonInicio(ButtonBehavior, Label):
	color_press = ListProperty([0.3, 0.7, 1, 1])
	color_release = ListProperty([0.1, 0.5, 0.7, 1])
	color_normal = ListProperty([0.1, 0.5, 0.7, 1])
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.refresh()

	# Quando mudar algum desses argumentos, atualiza o botão
	def on_pos(self, *args):
		self.refresh()
	def on_size(self, *args):
		self.refresh()
	def on_press(self, *args):
		self.color_normal = self.color_press
	def on_release(self, *args):
		self.color_normal = self.color_release
	def on_color_normal(self, *args):
		self.refresh()

	# Atualiza o botão
	def refresh(self, *args):
		# Primeiro limpa, para não deixar rastros
		self.canvas.before.clear()

		# canvas.before, para não ficar na frente dos textos
		with self.canvas.before:													
			# Desenha o botão, duas elipses nas pontas, e um retangulo no meio, algo parecido com isso:  (|||||||) 
			Color(rgba = self.color_normal)

			Ellipse(pos = self.pos, 
					size= (self.height, self.height))

			Ellipse(pos = (self.x + self.width - self.height, self.y), 
					size= (self.height, self.height))

			Rectangle(pos = (self.x + self.height/2.0, self.y),
						size= (self.width - self.height, self.height))


class Guarde(App):
	def build(self):	
		return Manager()

# Carrega os sons do apk
popSound = SoundLoader.load('pop.mp3')
poppapSound = SoundLoader.load('poppap.mp3')

# Inicia o programa
Guarde().run()