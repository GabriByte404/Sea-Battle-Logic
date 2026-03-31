import tkinter as tk
from tkinter import ttk
from tkinter import font
from random import randint
from PIL import ImageTk, Image, ImageDraw
from tkinter import messagebox
import pygame
import os
import json
import datetime

class BattleShip_Window(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('BattleShip | The Game')
		self.geometry('940x690')
		self.resizable(True, True)
		self.configure(bg='grey')
		self.create_menu()
		self.flagdati = False
		self.protocol("WM_DELETE_WINDOW", self.chiudi)

	def chiudi(self):
		if self.flagdati:
			risposta = messagebox.askyesno("Conferma chiusura", "Vuoi salvare i dati?")
			if risposta:
				self.salvataggio()
		self.destroy()

	def create_menu(self):
		self.Sval = tk.IntVar()
		self.Levels = tk.IntVar(value=1)
		# Label principale
		self.label_frame = tk.LabelFrame(self, text="THE BATTLESHIP", font=("Press Start 2P", 25, "bold"), fg="dark blue", bg="#44627d", borderwidth=10)
		self.label_frame.pack(fill=tk.BOTH, expand=True)

		# Canvas all'interno del LabelFrame
		self.canvas = tk.Canvas(self.label_frame)
		self.canvas.pack(fill="both", expand=True)

		# immagini:
		self.background_image = tk.PhotoImage(file="img/backmenu.png")
		self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

		# Button
		self.Sett__ = tk.PhotoImage(file="img/icon/OptionMenu.png")
		self.Setting__ = self.Sett__.zoom(2)
		self.Rank__ = tk.PhotoImage(file="img/icon/Book.png")
		self.Ranking__ = self.Rank__.zoom(2)
		self.Pl__ = tk.PhotoImage(file="img/icon/Play.png")
		self.Play__ = self.Pl__.zoom(2)
		self.Qt__ = tk.PhotoImage(file="img/icon/Exit.png")
		self.Quit__ = self.Qt__.zoom(2)
		self.As__ = tk.PhotoImage(file="img/icon/SpeakerOn.png")
		self.Ayes__ = self.As__.zoom(2)
		self.An__ = tk.PhotoImage(file="img/icon/SpeakerMute.png")
		self.Ano__ = self.An__.zoom(2)

		# Frame per i bottoni
		self.button_frame = tk.Frame(self.canvas, bg="lightblue")
		self.button_frame.pack(pady=(180, 10))

		# Button
		button_width = 200
		button_height = 80

		option_button = tk.Button(self.button_frame, width=button_width, height=button_height, image=self.Setting__, relief="ridge", borderwidth=4, bg="#44627d", command=self.OpenMenu)
		option_button.pack(ipadx=20)

		play_button = tk.Button(self.button_frame, width=button_width, height=button_height, image=self.Play__, relief="ridge", borderwidth=4, bg="#44627d", command=self.play)
		play_button.pack(ipadx=20)

		quit_button = tk.Button(self.button_frame, width=button_width, height=button_height, image=self.Ranking__, relief="ridge", borderwidth=4, bg="#44627d", command=self.take)
		quit_button.pack(ipadx=20)

		ranking_button = tk.Button(self.button_frame, width=button_width, height=button_height, image=self.Quit__, relief="ridge", borderwidth=4, bg="#44627d", command=self.quit)
		ranking_button.pack(ipadx=20)
		
	#Funzione per aprire il menu di impostazioni:
	def OpenMenu(self):
		# CENTRARE MENU
		menu_width = 750
		menu_height = 500
		# Calcola le coordinate per il centro della finestra principale
		x_pos = self.winfo_rootx() + (self.winfo_width() // 2) - (menu_width // 2)
		y_pos = self.winfo_rooty() + (self.winfo_height() // 2) - (menu_height // 2)

		# Crea una nuova finestra di dialogo per il menu
		menu_window = tk.Toplevel(self)
		menu_window.title("Options")
		menu_window.geometry(f"{menu_width}x{menu_height}+{x_pos}+{y_pos}")
		menu_window.resizable(False, False)
		menu_window.transient(self)
		menu_window.config(bg="lightblue")

		# Aggiungi il LabelFrame al menu
		levels_frame = tk.LabelFrame(menu_window, text="Levels", font=("Press Start 2P", 14), bg="dark blue", fg='white')
		levels_frame.pack(padx=10, pady=10, expand=True, fill="both")

		# Livelli:
		self.easy_level = tk.Radiobutton(levels_frame, text="EASY", font=("Arial", 12), variable=self.Levels, value=1, bg="lightblue", fg="blue")
		self.easy_level.grid(row=0, column=0, padx=50, pady=20, ipadx=100, sticky="w")

		self.medium_level = tk.Radiobutton(levels_frame, text="MEDIUM", font=("Arial", 12), variable=self.Levels, value=2, bg="light blue", fg="blue")
		self.medium_level.grid(row=0, column=1, padx=30, pady=20, ipadx=100, sticky="w")

		self.hard_level = tk.Radiobutton(levels_frame, text="HARD", font=("Arial", 12), variable=self.Levels, value=3, bg="light blue", fg="blue")
		self.hard_level.grid(row=1, column=0, columnspan=2, padx=30, pady=20, ipadx=100)

		# Frame sound:
		sound_frame = tk.LabelFrame(menu_window, text="Sound", font=("Press Start 2P", 14), bg="dark blue", fg='white')
		sound_frame.pack(padx=10, pady=10, expand=True, fill="both")

		self.volume_scale = tk.Scale(sound_frame, from_=0, to=10, orient=tk.HORIZONTAL, label="Volume in game", font=("Arial", 10), bg="light blue", fg="blue", variable=self.Sval)
		self.volume_scale.pack(padx=55, pady=55, ipadx=300)

		yesaudio_button = tk.Button(sound_frame, image=self.Ayes__, command=self.yesAudio, font=("Arial", 10), bg="light blue", fg="blue")
		yesaudio_button.pack(side=tk.LEFT, padx=(250, 0), pady=(0, 50), ipadx=30, ipady=10)

		noaudio_button = tk.Button(sound_frame, image=self.Ano__, command=self.noAudio, font=("Arial", 10), bg="light blue", fg="blue")
		noaudio_button.pack(side=tk.LEFT, padx=10, pady=(0, 50), ipadx=30, ipady=10)

		#Funzione per chiudere il menu nel modo corretto:
		def close_menu():
			menu_window.destroy()

		menu_window.protocol("WM_DELETE_WINDOW", close_menu)  # Gestisci la chiusura della finestra

		# Blocca l'interazione con la finestra principale
		menu_window.grab_set()
		# Attendi la chiusura del menu
		menu_window.wait_window(menu_window)
		# Ripristina l'interazione con la finestra principale
		self.grab_release()

	#Funzione per avviare il gioco:
	def play(self):
		self.risposta = False
		self.label_frame.destroy()
		self.inizializza()

		if os.path.exists('salvataggio.json') and os.path.getsize('salvataggio.json') > 0:
			with open('salvataggio.json', 'r') as file:
				data = json.load(file)
				data['save'] = [item for item in data['save'] if not item['player']['finito']]

			if len(data['save']) == 1:
				self.risposta = messagebox.askyesno("Riprendi", "Vuoi finire la vecchia partita ?")
				if self.risposta:
					self.nickname = data['save'][0]['player']['id']
					self.level = data['save'][0]['player']['level']
					if self.level == 'easy':
						self.Levels.set(value=1)
					elif self.level == 'medium':
						self.Levels.set(value=2)
					else:
						self.Levels.set(value=3)

					self.timer_val.set(value=data['save'][0]['player']['timer'])
					self.moves = data['save'][0]['player']['moves']
					self.ship = data['save'][0]['player']['ship']['remaining']
					self.hit = data['save'][0]['player']['ship']['hit']
					self.image_path = data['save'][0]['player']['path']

					self.progressBar()
				else:
					with open('salvataggio.json', 'r') as file:
						data = json.load(file)
						data['save'] = [item for item in data['save'] if item['player']['finito']]

					with open('salvataggio.json', 'w') as file:
						json.dump(data, file, indent=4)
					self.set_profile()
			else:
				self.set_profile()
		else:
			self.set_profile()

	#Funzione per la classifica:
	def take(self):
		self.grab_set()

		# CENTRARE MENU
		menu_width = 750
		menu_height = 500
		# Calcola le coordinate per il centro della finestra principale
		x_pos = self.winfo_rootx() + (self.winfo_width() // 2) - (menu_width // 2)
		y_pos = self.winfo_rooty() + (self.winfo_height() // 2) - (menu_height // 2)

		# Crea una nuova finestra di dialogo per il menu
		menu_window = tk.Toplevel(self)
		menu_window.title("Ranking")
		menu_window.geometry(f"{menu_width}x{menu_height}+{x_pos}+{y_pos}")
		menu_window.resizable(False, False)
		menu_window.transient(self)
		menu_window.config(bg="lightblue")

		# Aggiungi il LabelFrame al menu
		ranking_frame = tk.LabelFrame(menu_window, text="Informazioni", font=("Arial", 10), fg="darkblue", bg="lightblue")
		ranking_frame.pack(padx=10, pady=10, fill="both", expand=True)

		# Classifica:
		self.ranking_label_frame = tk.LabelFrame(ranking_frame, text="Classifica", font=("Arial", 10), width=500, height=200, bg="lightblue", fg="darkblue")
		self.ranking_label_frame.pack(padx=10, pady=10, fill="both", expand=True)

		try:
			if os.path.exists('salvataggio.json') and os.path.getsize('salvataggio.json') > 0:
				self.classifica()
			else:
				messagebox.showwarning("Errore", "La classifica è vuota")
		except FileNotFoundError:
			# Crea il file "salvataggio.json" se non esiste
			with open('salvataggio.json', 'a+'):
				pass
			messagebox.showinfo("Informazione", "File 'salvataggio.json' creato")

		# Blocca l'interazione con la finestra principale
		menu_window.grab_set()
		# Attendi la chiusura del menu
		menu_window.wait_window(menu_window)
		# Ripristina l'interazione con la finestra principale
		self.grab_release()

	def classifica(self):
		self.ordina()

		self.lista = tk.Listbox(self.ranking_label_frame, width=80, height=20, font=("Arial", 10))
		self.lista.pack(fill="both", expand=True)

		i = 1

		with open('salvataggio.json', 'r') as file:
			data = json.load(file)
			data['save'] = [item for item in data['save'] if item['player']['finito']]

		for dato in data['save']:
			stampa = 'Nome: {}\t Livello: {}\t Tempo: {}\t Data: {}'.format(dato['player']['id'], dato['player']['level'], dato['player']['timer'], dato['player']['data'])
			self.lista.insert(i, stampa)
			i = i + 1

	def ordina(self):
		with open('salvataggio.json', 'r') as file:
			data = json.load(file)
			lista = data['save']
			l = len(lista)
		for i in range(l - 1):
			for j in range(l - i - 1):
				if lista[j]['player']['timer'] > lista[j + 1]['player']['timer']:
					lista[j], lista[j + 1] = lista[j + 1], lista[j]

		data = {'save': lista}

		with open('salvataggio.json', 'w') as file:
			json.dump(data, file, indent=4)

	#Funzione per chiudere il gioco:
	def quit(self):
		elem = messagebox.askyesno(title="QUIT", message="Confermi di voler uscire dal gioco?")
		if elem:
			self.destroy()

	#Funzione per regolare il volume della canzone:
	def yesAudio(self):
		self.volume_scale.set(value=10)
	
	def noAudio(self):
		self.volume_scale.set(value=0)

	def background_music(self, music):
		pygame.mixer.init()
		pygame.mixer.music.load(music)
		self.change_volume()
		pygame.mixer.music.play(-1)  # Riproduci la musica in loop infinito

	def stop_audio(self):
		pygame.mixer.music.stop()

	def set_profile(self):
		custom_font = font.Font(family="Arial", size=12, weight="bold")

		# Frame set_profile
		self.ProfileFrame = tk.LabelFrame(self, text="Registrati", font=("Press Start 2P", 18), fg="dark blue", bg="#44627d", borderwidth=5)
		self.ProfileFrame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

		# Imposta il ridimensionamento verticale del frame
		self.ProfileFrame.grid_rowconfigure(0, weight=1)
		self.ProfileFrame.grid_columnconfigure(0, weight=1)
		self.ProfileFrame.grid_rowconfigure(1, weight=1)
		self.ProfileFrame.grid_rowconfigure(2, weight=1)
		self.ProfileFrame.grid_rowconfigure(3, weight=2)

		# Creazione dei widget
		# Lista delle immagini predefinite
		self.image_choices = [
			{"path": "img/profile_image/linux.jpeg", "name": "LINUX"},
			{"path": "img/profile_image/babyJoda.png", "name": "JODA"},
			{"path": "img/profile_image/cane.jpg", "name": "DOG"},
			{"path": "img/profile_image/gatto.jpg", "name": "CAT"},
			{"path": "img/profile_image/spongebob.jpg", "name": "S.B"},
			{"path": "img/profile_image/griffin.jpeg", "name": "PETER"}
		]

		self.selected_image = tk.StringVar(self.ProfileFrame)
		self.selected_image.set(self.image_choices[0]["name"])  # Imposta l'immagine di default

		self.image_button = tk.Button(self.ProfileFrame, text="SCEGLI LA TUA IMMAGINE PROFILO", command=self.open_image_menu, font=("Press Start 2P", 12, "bold"), bg="yellow", fg="darkblue", relief=tk.RAISED, borderwidth=10, activebackground='blue')
		self.image_button.grid(row=0, column=0, pady=10, sticky="nsew")

		self.nickname_label = tk.Label(self.ProfileFrame, text="SCELI IL TUO NICKNAME:", font=("Press Start 2P", 12, "bold"), fg="yellow", bg="blue", borderwidth=10, relief=tk.RAISED)
		self.nickname_label.grid(row=1, column=0, sticky="nsew")

		self.nickname_entry = tk.Entry(self.ProfileFrame, font=("Press Start 2P", 20), fg="darkblue", relief=tk.SOLID, bg='light blue', justify=tk.CENTER)
		self.nickname_entry.grid(row=2, column=0, pady=(0,10), sticky="nsew")

		self.save_button = tk.Button(self.ProfileFrame, text="START", command=self.save_profile, font=("Press Start 2P", 25, "bold"), bg="dark blue", fg="red", relief=tk.RAISED, borderwidth=15, activebackground='yellow')
		self.save_button.grid(row=3, column=0, pady=10, sticky="nsew")

		# Menu a tendina per le immagini
		self.image_menu = tk.Menu(self.ProfileFrame, tearoff=0)  # --> tearoff=0 no riga separazione
		self.image_menu_images = {}  # Dizionario per memorizzare le immagini associate alle voci di menu

		for image_data in self.image_choices:
			image = Image.open(image_data["path"])
			image.thumbnail((50, 50))  # --> setta la dimensione dell'immagine mantenedo le proporzioni
			image_tk = ImageTk.PhotoImage(image)
			self.image_menu.add_radiobutton(
				label=image_data["name"],
				variable=self.selected_image,
				value=image_data["name"],
				image=image_tk,
				compound=tk.CENTER,
				foreground='blue',  # Imposta il testo in azzurro
				activeforeground='dark blue',  # Imposta il testo in blu quando passa sopra il mouse
				background='yellow',
				font=custom_font  # Imposta il font e la dimensione personalizzati
			)
			self.image_menu_images[image_data["name"]] = image_tk  # Memorizza l'immagine nel dizionario


	def open_image_menu(self):
		# Mostra il menu a tendina delle immagini
		self.image_menu.post(self.image_button.winfo_rootx(), self.image_button.winfo_rooty() + self.image_button.winfo_height())

	def save_profile(self):
		# Ottieni il nome dell'immagine selezionata
		self.image_name = self.selected_image.get()

		# Ottieni il percorso dell'immagine corrispondente
		self.image_path = next((image["path"] for image in self.image_choices if image["name"] == self.image_name), "")

		# Ottieni il nickname
		self.nickname = self.nickname_entry.get()

		if self.nickname != '' and self.image_path != None and self.image_name != None:
			self.ProfileFrame.destroy()
			self.progressBar()
		else:
			tk.messagebox.showerror(title='Compilazione non completa', message='Assicurati di complire correttamente tutti i campi.')

	def progressBar(self):
		# Frame ProgressBar
		self.PbFrame = tk.Frame(self)
		self.PbFrame.configure(bg='black')
		self.PbFrame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

		# image background
		image = Image.open("img/background.jpg")
		imageDim = image.resize((self.PbFrame.winfo_width(), self.PbFrame.winfo_height()))
		background_image = ImageTk.PhotoImage(image)
		background_label = tk.Label(self.PbFrame, image=background_image)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image

		# PROGRESSBAR
		self.progressbar = ttk.Progressbar(self.PbFrame, length=200, mode="determinate")
		self.progressbar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		self.start_progress()

	def start_progress(self):
		self.progressbar["value"] = 0
		self.progressbar["maximum"] = 50
		self.update_progress()

	def update_progress(self):
		value = self.progressbar["value"]
		if value < self.progressbar["maximum"]:
			value += 1
			self.progressbar["value"] = value
			self.after(100, self.update_progress)  # Aggiorna ogni 100 millisecondi (0.1 secondi)
		else:
			self.game_view()
			self.PbFrame.destroy()

	def inizializza(self):
		self.moves = 0
		self.button = []	#--> lista con i buttun salvati
		self.ship = dict()
		self.hit = dict()
		self.card = dict()
		self.timer_running = True
		self.onlyOne = False
		self.timer_val = tk.DoubleVar(value=0)

	def game_view(self):
		self.mainFrame = tk.Frame(self)
		self.mainFrame.configure(bg='grey')
		self.mainFrame.pack(expand=True, fill=tk.BOTH)
		
		self.background_music(music="audio/musicBack.mp3")

		self.flagdati = True
		# Carica l'immagine utilizzando Pillow
		image = Image.open("img/background.jpg")

		# Ridimensiona l'immagine alle dimensioni del frame mainFrame
		imageDim = image.resize((self.mainFrame.winfo_width(), self.mainFrame.winfo_height()))

		# Crea un oggetto PhotoImage da utilizzare come sfondo
		background_image = ImageTk.PhotoImage(image)

		# Crea un'etichetta con l'immagine come sfondo
		background_label = tk.Label(self.mainFrame, image=background_image)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image

		# TUTTE COSE DA SETTARE NEL MENU
		# livello difficoltà (3=easy, 5=medium, 7=hard)
		# seleziona dimensione campo (8=easy, 10=medium, 15=hard)
		if self.Levels.get() == 1:
			self.level = 3
			self.dim_x = 8
			self.dim_y = 8
			self.MAXmoves = 50
		elif self.Levels.get() == 2:
			self.level = 5
			self.dim_x = 10
			self.dim_y = 10
			self.MAXmoves = 55
		elif self.Levels.get() == 3:
			self.level = 7
			self.dim_x = 15
			self.dim_y = 15
			self.MAXmoves = 58

		# CAMPO
		self.build_field()	#--> crea il campo
		if self.risposta == True:
			for button_id in self.hit:
				try:
					for i in self.hit[button_id]:
						self.button[i[0]][i[1]].config(bg='red')
						self.button[i[0]][i[1]].config(state="disabled")
						image = tk.PhotoImage(file="img/ship/explosion.png")
						self.button[i[0]][i[1]].config(image=image)
						self.button[i[0]][i[1]].image = image
				except:
					pass

		# PARTE SOTTO IL CAMPO
		self.underFrame = tk.Frame(self.mainFrame)
		self.underFrame.grid(row=self.dim_y, column=0, columnspan=self.dim_x+2, sticky="nsew", pady=(5,0))

		# Carica l'immagine utilizzando Pillow
		image = Image.open(self.image_path)
		# Ridimensiona l'immagine a una dimensione massima di 50x50 pixel
		image.thumbnail((50, 50))
		
		# Crea un'immagine vuota con uno sfondo trasparente
		rounded_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
		mask = Image.new("L", image.size, 0)
			
		# Crea un oggetto draw per disegnare il bordo del cerchio
		draw = ImageDraw.Draw(mask)
		draw.ellipse((0, 0, image.width, image.height), fill=255)
		
		# Applica la maschera all'immagine originale
		rounded_image.paste(image, (0, 0), mask)
			
		# Crea un oggetto PhotoImage da utilizzare con il widget Label
		self.profile_photo = ImageTk.PhotoImage(rounded_image)
		self.photoPlayer = tk.Label(self.underFrame, image=self.profile_photo, fg='black', bg='yellow')
		self.photoPlayer.grid(row=0, column=0, sticky="nsew")

		textNickName = 'Nickname:',self.nickname
		self.namePlayer = tk.Label(self.underFrame, text=textNickName, bg='dark blue', fg='yellow' , font=("Press Start 2P", 18,'bold'))
		self.namePlayer.grid(row=0, column=1, sticky="nsew")

		txtMosse = 'Mosse: '+str(self.moves)
		self.moveLabel = tk.Label(self.underFrame, text=txtMosse, bg='light blue', fg='black' , font=("Courier", 18,'bold'))
		self.moveLabel.grid(row=0, column=2, sticky="nsew")

		# Imposta il peso delle colonne nel frame
		self.underFrame.grid_columnconfigure(0, weight=1)
		self.underFrame.grid_columnconfigure(1, weight=6)	#--> la colonna 1 occupa i 3/4
		self.underFrame.grid_columnconfigure(2, weight=1)

		# PARTE LATERALE DX
		self.sideFrame = tk.Frame(self.mainFrame, bg='blue')
		self.sideFrame.grid(row=0, column=self.dim_x+1, padx=(75,50), pady=10, rowspan=self.dim_y, sticky='nsew')

		# Contenuto del frame laterale
		# Nuovi Frame (interagivano negativamente con il campo)
		self.menuGFRame = tk.Frame(self.sideFrame, bg='blue')
		self.menuGFRame.pack(fill=tk.BOTH, pady=(10,0))

		self.timerFrame = tk.LabelFrame(self.sideFrame, relief="solid", text='TIMER', bg='dark blue', fg='light blue', font=("Press Start 2P", 12), borderwidth=2)
		self.timerFrame.pack(fill=tk.BOTH, pady=5)

		self.cardShipFrame = tk.LabelFrame(self.sideFrame, relief="solid", text='RESOCONTO NAVI:', bg='dark blue', fg='light blue', font=("Press Start 2P", 10), borderwidth=2)
		self.cardShipFrame.pack(fill=tk.BOTH, expand=True)

		# Button per il 'menu game'
		iconOption = tk.PhotoImage(file="img/icon/Option.png")
		self.menuGame = tk.Button(self.menuGFRame, image=iconOption, bg='blue', relief='flat', activebackground="light blue", command=self.open_menu)
		self.menuGame.image = iconOption
		self.menuGame.pack(expand=False, pady=5)
		self.menuGame.configure(height=22)

		# Label Timer e Card
		self.timer = tk.Label(self.timerFrame, textvariable=self.timer_val, bg="blue", fg="yellow", font=("Press Start 2P", 10),borderwidth=2)
		self.timer.pack(fill=tk.BOTH, expand=True)
		self.timer.configure(height=1)
		self.start_time()

		# Imposta il peso delle colonne nel frame principale
		self.mainFrame.grid_columnconfigure(self.dim_x, weight=1)
		self.mainFrame.grid_columnconfigure(self.dim_x+1, weight=0)  # Il frame laterale non viene ridimensionato

		# Collega la funzione di callback ai bottoni
		for y in range(self.dim_y):
			for x in range(self.dim_x):
				self.button[x][y].configure(command=lambda x=x, y=y: self.button_click(x, y))

		# creazione nave (a seconda del livello aggiungiamo navi e segliamo la lunghezza e le coordinate con un random, tanto le controlla la funzione)
		if self.risposta == False:
			for i in range(self.level):
				rtn = None
				while rtn != True:
					x = self.random(0,self.dim_x-1)
					y = self.random(0,self.dim_x-1)
					leng = self.random(1,4)	#--> lunghezze possibili da gestire con i livelli (dobbiamo associare ad ogni livello delle lunghezza massime)
					direction = self.random(0,1)
					rtn = self.add_ship(x, y, leng, i, orizzontale=direction)
		
		self.cardShip()

		# RIDIMENSIONA
		self.bind('<Configure>', self.resize)	#--> funzione per rendere il campo responsive (si aggiorna quando viene ridimensionata la finestra)
	# fine game-view()

	def resize(self, event):
		width = self.mainFrame.winfo_width()
		height = self.mainFrame.winfo_height()

	def build_field(self):
		image = tk.PhotoImage(file="img/water.png")
		button_width = 10
		button_height = 10

		for y in range(self.dim_y):
			row = []
			for x in range(self.dim_x):
				btn = tk.Button(self.mainFrame, width=button_width, height=button_height, image=image, borderwidth=1, bg='#44627d')
				btn.image = image
				if y == 0 and x == 0:
					btn.grid(row=y, column=x, sticky="nsew", pady=(100,0), padx=(100,0))
				else:
					if y == 0:
						btn.grid(row=y, column=x, sticky="nsew", pady=(100,0))
					else:
						if x == 0 and y != self.dim_x-1:
							btn.grid(row=y, column=x, sticky="nsew", padx=(100,0))
						else:
							if y == self.dim_x-1 and x != 0:
								btn.grid(row=y, column=x, sticky="nsew", pady=(0,100))
							else:
								if y == self.dim_x-1 and x == 0:
									btn.grid(row=y, column=x, sticky="nsew", pady=(0,100), padx=(100,0))
								else:
									btn.grid(row=y, column=x, sticky="nsew")

				row.append(btn)
			self.button.append(row)

		# Configura il ridimensionamento delle righe e delle colonne
		# Ciò significa che tutte le colonne avranno lo stesso peso e condivideranno equamente lo spazio extra disponibile quando viene ridimensionata la finestra.
		for i in range(self.dim_x):
			self.mainFrame.grid_columnconfigure(i, weight=1)
		for j in range(self.dim_y):
			self.mainFrame.grid_rowconfigure(j, weight=1)

	def add_ship(self, x, y, lunghezza, n, orizzontale=True):
		listTemp = []
		# Controllo dei limiti
		if x < 0 or x >= len(self.button[0]) or y < 0 or y >= len(self.button):
			# print("Posizione non valida")
			return

		# Controllo spazio disponibile
		if orizzontale:
			if x + lunghezza > len(self.button[0]):
				# print("Nave troppo lunga per la posizione specificata")
				return
			for i in range(x, x + lunghezza):
				if self.button[y][i]["text"][0:4] == "Nave":
					# print("Collisione con un'altra nave")
					return
		else:
			if y + lunghezza > len(self.button):
				# print("Nave troppo lunga per la posizione specificata")
				return
			for i in range(y, y + lunghezza):
				if self.button[i][x]["text"][0:4] == "Nave":
					# print("Collisione con un'altra nave")
					return

		# Inserimento della nave
		contTemp = 1
		if orizzontale:
			key = str(lunghezza)+'.'+str(n)
			# print('Direzione: orizzontale, x:',x,', y:',y,', lunghezza:',lunghezza)
			for i in range(x, x + lunghezza):
				listTemp.append((y,i))
				self.button[y][i]['text'] = 'NaveO'+str(contTemp)+str(lunghezza)
				# self.button[y][i].configure(bg='red')	#--> rimuovere
				contTemp = contTemp + 1
			self.ship[key] = listTemp
			contTemp = 1
		else:
			key = str(lunghezza)+'.'+str(n)
			# print('Direzione: verticale, x:',x,', y:',y,', lunghezza:',lunghezza)
			for i in range(y, y + lunghezza):
				listTemp.append((i,x))
				self.button[i][x]['text'] = 'NaveV'+str(contTemp)+str(lunghezza)
				# self.button[i][x].configure(bg='red')	#--> rimuovere
				contTemp = contTemp + 1
			self.ship[key] = listTemp
			contTemp = 1
		return True

	def cardShip(self):
		for numShip in self.ship:
			if numShip[0] == '1':
				image = tk.PhotoImage(file="img/ship/1/ship_1.png")
			else:
				if numShip[0] == '2':
					image = tk.PhotoImage(file="img/ship/2/ship_2.png")
				else:
					if numShip[0] == '3':
						image = tk.PhotoImage(file="img/ship/3/ship_3.png")
					else:
						image = tk.PhotoImage(file="img/ship/4/ship_4.png")

			txtLabel = 'Nave lunga '+numShip[0]
			self.labelframe = tk.LabelFrame(self.cardShipFrame, text=txtLabel, bg='blue', fg='#ffff40', font=("Press Start 2P", 10), borderwidth=5)
			self.labelframe.pack(fill="both", expand=True)
			self.cardShipL = tk.Label(self.labelframe, image=image, bg="light blue", fg="white", borderwidth=1, relief="solid")
			self.cardShipL.image = image
			self.cardShipL.grid(row=0, column=0, columnspan=2, sticky="nsew")
			self.cardShipL.configure(width=40, height=23)

			txtHit = 'Pezzi colpititi: ' + str(0)
			self.labelHit = tk.Label(self.labelframe, text=txtHit, bg="light blue", fg="green", borderwidth=1, relief="solid")
			self.labelHit.grid(row=1, column=0, columnspan=1, sticky="nsew")
			self.labelHit.configure(width=15, anchor="center") 

			txtRest = 'Pezzi restanti: ' + numShip[0]
			self.labelRest = tk.Label(self.labelframe, text=txtRest, bg="light blue", fg="red", borderwidth=1, relief="solid")
			self.labelRest.grid(row=1, column=1, columnspan=1, sticky="nsew")
			self.labelRest.configure(width=15, anchor="center")

			self.card[numShip] = [0,int(numShip[0]),self.labelHit,self.labelRest]

	def random(self,a=0, b=1):
		nRand =  randint(a, b)
		return nRand

	def button_click(self, x, y, flg=False):	#--> funzione per capire quale button hai cliccato
		listTemp = []
		for i in self.ship:
			if i not in self.hit:
				self.hit[i] = []
			if (x,y) in self.ship[i]:
				if isinstance(self.hit[i], list):
					self.hit[i].append((x,y))
				else:
					listTemp.append((x,y))
					self.hit[i] = listTemp

				if i[0] == '1':
					image = tk.PhotoImage(file="img/ship/1/ship_1a.png")
				elif i[0] == '2':
					if self.button[x][y]['text'][4:5] == 'O':
						if self.button[x][y]['text'][5:6] == '1':
							image = tk.PhotoImage(file="img/ship/2/ship_2a.png")
						elif self.button[x][y]['text'][5:6] == '2':
							image = tk.PhotoImage(file="img/ship/2/ship_2b.png")
					else:
						if self.button[x][y]['text'][5:6] == '1':
							image = tk.PhotoImage(file="img/ship/2/ship_2a2.png")
						elif self.button[x][y]['text'][5:6] == '2':
							image = tk.PhotoImage(file="img/ship/2/ship_2b2.png")
				elif i[0] == '3':
					if self.button[x][y]['text'][4:5] == 'O':
						if self.button[x][y]['text'][5:6] == '1':
							image = tk.PhotoImage(file="img/ship/3/ship_3a.png")
						elif self.button[x][y]['text'][5:6] == '2':
							image = tk.PhotoImage(file="img/ship/3/ship_3b.png")
						elif self.button[x][y]['text'][5:6] == '3':
							image = tk.PhotoImage(file="img/ship/3/ship_3c.png")
					else:
						if self.button[x][y]['text'][5:6] == '1':
							image = tk.PhotoImage(file="img/ship/3/ship_3a2.png")
						elif self.button[x][y]['text'][5:6] == '2':
							image = tk.PhotoImage(file="img/ship/3/ship_3b2.png")
						elif self.button[x][y]['text'][5:6] == '3':
							image = tk.PhotoImage(file="img/ship/3/ship_3c2.png")
				elif i[0] == '4':
					if self.button[x][y]['text'][4:5] == 'O':
						if self.button[x][y]['text'][5:6] == '1':
							image = tk.PhotoImage(file="img/ship/4/ship_4a.png")
						elif self.button[x][y]['text'][5:6] == '2':
							image = tk.PhotoImage(file="img/ship/4/ship_4b.png")
						elif self.button[x][y]['text'][5:6] == '3':
							image = tk.PhotoImage(file="img/ship/4/ship_4c.png")
						elif self.button[x][y]['text'][5:6] == '4':
							image = tk.PhotoImage(file="img/ship/4/ship_4d.png")
					else:
						if self.button[x][y]['text'][5:6] == '1':
							image = tk.PhotoImage(file="img/ship/4/ship_4a2.png")
						elif self.button[x][y]['text'][5:6] == '2':
							image = tk.PhotoImage(file="img/ship/4/ship_4b2.png")
						elif self.button[x][y]['text'][5:6] == '3':
							image = tk.PhotoImage(file="img/ship/4/ship_4c2.png")
						elif self.button[x][y]['text'][5:6] == '4':
							image = tk.PhotoImage(file="img/ship/4/ship_4d2.png")

				self.button[x][y].config(image=image)
				self.button[x][y].image = image
				# rimuovere dal dict ship la nave colpita
				self.ship[i].remove((x, y))
				flg = True
				# contatori
				self.counter(i)

		if flg == False:
			for i in self.hit:
				if (x,y) in self.hit[i]:
					flg = True
			if flg == False:
				image = tk.PhotoImage(file="img/waterNoShip.png")
				self.button[x][y].config(image=image)
				self.button[x][y].image = image
				self.moves += 1  # Incrementa il contatore delle mosse
				self.update_moves_label()  # Aggiorna la label delle mosse

				if self.moves >= self.MAXmoves:
					self.lose()

		self.victory()

	def counter(self, i):
		self.card[i][0] = self.card[i][0] + 1
		self.card[i][1] = self.card[i][1] - 1
		self.card[i][2]['text'] = 'Pezzi colpititi: ' + str(self.card[i][0])
		self.card[i][3]['text'] = 'Pezzi restanti: ' + str(self.card[i][1])

	def victory(self):
		ships_to_remove = []

		# Itera sul dizionario self.ship
		for s in self.ship:
			if len(self.ship[s]) == 0:
				name = s[0]
				self.littleWindow(225,100,100,'Nave Abbattuta',name)
				ships_to_remove.append(s)

		# Rimuovi le navi abbattute dal dizionario self.ship
		for s in ships_to_remove:
			del self.ship[s]
		
		if len(self.ship) == 0:
			if not self.onlyOne:
				self.onlyOne = True
				self.timer_running = False
				self.after(2000, lambda: self.littleWindow(350, 350, 0, 'Hai vinto', popUp=False, img='img/winBattle.png'))		
				self.salvataggio(f = True)
				self.flagdati = False
				self.stop_audio()

	def update_moves_label(self):
		moves_label_text = f"Mosse: {self.moves}"	
		self.moveLabel.config(text=moves_label_text)

	def lose(self):
		self.stop_audio()
		if not self.onlyOne:
			self.onlyOne = True
			self.timer_running = False
			self.littleWindow(350, 350, 0, 'Hai perso', popUp=False, img='img/gameOver.png')
			self.flagdati = False

	def littleWindow(self, pop_width, pop_height, decentralized=0, tit='', ship_name='', popUp=True, img=''):
		# Calcola le coordinate per il centro superiore della finestra principale
		x_pos = self.winfo_rootx() + (self.winfo_width() // 2) - (pop_width // 2)
		y_pos = self.winfo_rooty() + (self.winfo_height() // 2) - (pop_height // 2) - decentralized  # Sottrai 100 per spostarlo verso l'alto
		self.popUp_window = tk.Toplevel(self)
		self.popUp_window.title(tit)
		self.popUp_window.resizable(False, False)
		self.popUp_window.geometry(f"{pop_width}x{pop_height}+{x_pos}+{y_pos}")

		if popUp:
			label = tk.Label(self.popUp_window, text=f"Nave di lunghezza {ship_name} è stata abbattuta!")
			label.pack(expand=True)
			self.grab_set()
			self.popUp_window.transient(self)
			self.after(2000, lambda: self.destroy_popUp())
		else:
			background_image = tk.PhotoImage(file=img)
			background_label = tk.Label(self.popUp_window, image=background_image)
			background_label.place(x=0, y=0, relwidth=1, relheight=1)
			background_label.image = background_image
			if tit == 'Hai perso':
				label = tk.Label(self.popUp_window, text='GAME OVER!', font=("Press Start 2P", 20), bg='yellow', fg='red')
				label.place(relx=0.5, rely=0.4, anchor='center')
			else:
				label = tk.Label(self.popUp_window, text='YOU WIN!', font=("Press Start 2P", 20), bg='blue', fg='yellow')
				label.place(relx=0.5, rely=0.4, anchor='center')
			rtnToMenu = tk.Button(self.popUp_window, text="Torna al menu", command=self.returnToMenu, bg='yellow', fg='dark blue',font=("Press Start 2P", 10))
			rtnToMenu.place(relx=0.5, rely=0.6, anchor='center')

		def close_menu():
			pass  # Non deve fare nulla

		self.popUp_window.protocol("WM_DELETE_WINDOW", close_menu)  # Disabilita il bottone di chiusura

		# Blocca l'interazione con la finestra principale
		self.popUp_window.grab_set()
		# Attendi la chiusura del menu
		self.popUp_window.wait_window(self.popUp_window)

	def destroy_popUp(self):
		if self.winfo_exists():  # Check if the main window still exists
			self.grab_release()
		self.popUp_window.destroy()

	def returnToMenu(self):
		response = tk.messagebox.askyesno(title='another game?', message="Vuoi fare un'altra partita?")
		if response == True:
			self.stop_audio()
			self.restart()
		else:
			self.destroy()
		
	def start_time(self):
		if self.timer_running:
			self.timer_value = self.timer_val.get() + 0.1  # Incrementa il valore del timer
			self.timer_val.set(round(self.timer_value, 2))  # Arrotonda il valore a due cifre decimali
			self.timer.config(text=f"Timer: {self.timer_value:.2f}")  # Aggiorna il label del timer
			self.after(100, self.start_time)  # Richiama la funzione dopo 0.1 secondo (100 millisecondi)

	def open_menu(self):
		# Blocca il timer
		self.timer_running = False

		# CENTRARE MENU
		menu_width = 425
		menu_height = 550
		# Calcola le coordinate per il centro della finestra principale
		x_pos = self.winfo_rootx() + (self.winfo_width() // 2) - (menu_width // 2)
		y_pos = self.winfo_rooty() + (self.winfo_height() // 2) - (menu_height // 2)

		# Crea una nuova finestra di dialogo per il menu
		menu_window = tk.Toplevel(self)
		menu_window.title("Menu")
		menu_window.geometry(f"{menu_width}x{menu_height}+{x_pos}+{y_pos}")  # --> indica dove 'spawna' la finestra
		menu_window.resizable(False, False)
		menu_window.transient(self)  # Imposta la finestra di dialogo come figlia della finestra principale

		# icone menu
		self.Rest__ = tk.PhotoImage(file="img/icon/Restart.png")
		self.Restart__ = self.Rest__.zoom(2)
		self.Mn__ = tk.PhotoImage(file="img/icon/Home.png")
		self.Menu__ = self.Mn__.zoom(2)
		self.Qt__ = tk.PhotoImage(file="img/icon/Exit.png")
		self.Quit__ = self.Qt__.zoom(2)

		# Carica l'immagine utilizzando Pillow
		image = Image.open("img/backMenuGame.jpg")

		# Ridimensiona l'immagine alle dimensioni della finestra del menu
		imageDim = image.resize((menu_width, menu_height))

		# Crea un oggetto PhotoImage da utilizzare come sfondo della finestra
		background_image = ImageTk.PhotoImage(imageDim)

		# Crea un Label per l'immagine di sfondo e posizionalo in alto a sinistra
		background_label = tk.Label(menu_window, image=background_image)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)

		menu_label = tk.Label(menu_window, text="MENU GAME", font=("Press Start 2P", 24), bg="#0b0f10", fg="#ffff40")
		menu_label.pack(pady=20)

		button_frame = tk.Frame(menu_window, bg='grey', bd=2, relief=tk.SOLID)  # Aggiunto il bordo intorno al frame
		button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrare il frame nella finestra

		def close_menu():
			self.timer_running = True
			self.start_time()
			menu_window.destroy()

		replay = tk.Button(button_frame, image=self.Restart__, bg='grey', relief='flat', activebackground='blue', command=close_menu)
		replay.pack(pady=20, padx=50)

		volume_scaleM = tk.Scale(button_frame, from_=0, to=10, orient=tk.HORIZONTAL, label="AUDIO:", font=("Arial", 10), bg="grey", fg="yellow", variable=self.Sval)
		volume_scaleM.pack(padx=50)
		confirmVolume = tk.Button(button_frame, font=("Press Start 2P", 10), text='CONFERMA', bg='dark blue', fg='white', relief='solid', borderwidth=5, activebackground='blue', command=self.change_volume)
		confirmVolume.pack(pady=(0,20), padx=50)

		menu = tk.Button(button_frame, image=self.Menu__, bg='grey', relief='flat', activebackground='blue', command=self.menu)
		menu.pack(pady=20, padx=50)

		# Disabilita la chiusura della finestra principale
		self.protocol("WM_DELETE_WINDOW", close_menu)

		# Blocca l'interazione con la finestra principale
		self.grab_set()
		menu_window.grab_set()  # Blocca anche l'interazione con la finestra del menu
		# Attendi la chiusura del menu
		menu_window.wait_window(menu_window)
		# Ripristina l'interazione con la finestra principale
		self.grab_release()

		# Ripristina l'interazione con la finestra principale
		self.timer_running = True

		# Riabilita la chiusura della finestra principale
		self.protocol("WM_DELETE_WINDOW", self.destroy)

	def change_volume(self):
		pygame.mixer.music.set_volume(self.Sval.get() / 10)

	def salvataggio(self, f = False):
		self.i = datetime.datetime.now()
		d = ("%s/%s/%s" % (self.i.day, self.i.month, self.i.year))

		if self.Levels.get() == 1:
			self.l = "easy"
		elif self.Levels.get() == 2:
			self.l = "medium"
		elif self.Levels.get() == 3:
			self.l = "hard"
				
		if not(os.path.isfile('salvataggio.json')):
			with open('salvataggio.json', 'w') as file:
				self.data = {'save': []}
				json.dump(self.data, file)

		if not(f):
			player = {'player': {'id': self.nickname,'level': self.l, 'timer': round(self.timer_value, 2), 'path': self.image_path, 'data': d, 'finito': False, 'moves': self.moves, 'ship': {'hit': self.hit, 'remaining': self.ship}}}
		else:
			player = {'player': {'id': self.nickname, 'level': self.l, 'timer': round(self.timer_value, 2), 'path': self.image_path, 'data': d, 'finito': True, 'moves': self.moves, 'ship': {'hit': self.hit, 'remaining': self.ship}}}
		
		with open('salvataggio.json', 'r') as file:
			if os.path.getsize('salvataggio.json') == 0:
				with open('salvataggio.json', 'w') as file:
					self.data = {'save': []}
					json.dump(self.data, file)
			else:
				self.data = json.load(file)
				self.data['save'] = [item for item in self.data['save'] if item['player']['finito']]


		self.data["save"].append(player)
		fp = open('salvataggio.json','w')
		json.dump(self.data, fp, indent = 4)
		fp.close()
	

	def restart(self):
		self.destroy()
		self.__init__()  # Crea una nuova istanza della classe

	def menu(self):
		if self.flagdati:
			risposta = messagebox.askyesno("Conferma chiusura", "Vuoi salvare i dati?")
			if risposta:
				self.salvataggio()
		self.stop_audio()
		self.destroy()
		self.__init__()  # Crea una nuova istanza della classe

	def run(self):
		self.mainloop()

def main():
	pulisci()
	w = BattleShip_Window()
	w.run()

def pulisci():
	os.system('clear')

main()