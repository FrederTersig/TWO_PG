#!/usr/bin/python
# This Python file uses the following encoding: utf-8
'''
@author: Federico Tersigni
'''
import justpy as jp
import sys


from Template.BackendDirectoryView import BackendDirectoryView
from Model.Run import Run
from Model.DAO.RunDAO import listaRunDirectory
from Model.DAO.RunDAO import deleteRun
from Model.DAO.AgenteDAO import deleteAgenteDir
from Model.DAO.DirectoryDAO import listaDirectory
from Model.DAO.DirectoryDAO import deleteDirectory

from Screens.Sessione import esisteSessione
from Screens.Sessione import creaSessione
from Screens.Sessione import showSessione
from Screens.Sessione import addElementoSessione
from Screens.Sessione import returnSessione
from Screens.Sessione import utenteLoggato


#Costanti delle Classi / Tailwind dei bottoni
agentiClasses = 'inline-block rounded w-32 h-16 m-2 bg-blue-600 text-white hover:bg-white focus:outline-white hover:text-gray-800'
agentiOnMouseOver = 'inline-block rounded w-32 h-16 bg-blue-600 m-2 text-white hover:bg-blue-400 focus:outline-white hover:text-white container'
buttonClasses = 'block rounded w-16 h-16 m-2 bg-blue-600 text-white hover:bg-white focus:outline-white hover:text-gray-800'
acceptClasses = 'block rounded w-16 h-16 m-2 bg-green-600 text-white hover:bg-green-300 focus:outline-white hover:text-gray-800'
rejectClasses = 'block rounded w-16 h-16 m-2 bg-red-600 text-white hover:bg-red-300 focus:outline-white hover:text-gray-800'
actionButtonClasses = 'block rounded w-32 h-16 m-2 bg-blue-600 text-white hover:bg-white focus:outline-white hover:text-gray-800'
#Codice della grafica della schermata di BACKEND

############################################

class BackendDirectoryScreen:


	async def backendDirectoryScreen(self,request):
		print('BACKEND Directory SCREEN')
		lista = listaDirectory()

		session_id = request.session_id
		if not esisteSessione(session_id):
			creaSessione(session_id,False)
			request.redirect='/'

		else:
			if utenteLoggato(session_id):
				session = returnSessione(session_id)
			else:
				request.redirect='/'
		session = returnSessione(session_id)
		wp = BackendDirectoryView(lista,self.cancella,session)
		
		return wp

	def cancella(self,msg):
		print('cancella elemento')
		xid = list(msg.target.idDirectory)
		#Cancella le run di questa directory
		#Cancella gli agenti di questa directory
		print(xid[0], ' - ', type(xid[0]))
		runs = listaRunDirectory(xid[0])
		print('Runs ? ', runs)
		for x in runs:
			deleteRun(x.getId())
		runs.clear()
		print('comincio a cancellare gli agenti')
		deleteAgenteDir(xid[0])
		deleteDirectory(xid[0])
		print('Fatto')
		msg.page.redirect = '/backend/gestioneDirectory/'