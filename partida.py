from tablero import Tablero
from typing import Final
from dotenv import load_dotenv
import os
# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from queue import Queue
from globales import partidas

class Partida:
    def __init__(self, query):
        self.jugadores = (query.from_user.id, query.message.reply_to_message.from_user.id)
        self.nombre_jugadores = (query.from_user.first_name, query.message.reply_to_message.from_user.first_name)
        self.turno = 0
        self.tablero = Tablero()
        self.colas = (Queue(maxsize=3), Queue(maxsize=3))
        self.ganador = ""

    async def winningSequence(self, query, turno):
        keyboard = [
            [InlineKeyboardButton("Jugar", callback_data="jugar")],
            [InlineKeyboardButton("Salir", callback_data="salir")]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)   
        self.ganador = "1" if turno == 0 else "2"
        await query.message.edit_text(
                "¡El jugador " + ("1" if turno == 0 else "2") + " ha ganado!" + (", @" + query.from_user.username if query.from_user else "") + "!",
                reply_markup=reply_markup
            )
        del partidas[query.chat_instance]
        return keyboard

    async def keyboardBottonPress(self, query, context, numero):
        
        print("turno: " + str(self.turno))
        if query.from_user.id != self.jugadores[self.turno]: #"jugadores": (0.id, 1.id),"turno": 0,"tablero": [["", "", ""],["", "", ""],["", "", ""]]
            await query.answer("No es tu turno!") 
            print("no es tu turno: " + str(query.from_user.id) + " vs " + str(self.jugadores[self.turno]))
            return

        if self.tablero.boxOccupied(int(numero)):
            await query.answer("Esa casilla ya está ocupada!") 
            print("casilla ocupada: " + str(numero))
            return

        print(self)
        print("jugadores: " + str(self.jugadores)+ ", de patida: " + query.chat_instance)  
        keyboard=[]
    
        if numero!=None:
            self.tablero.modify_tablero(int(numero), "⚔" if self.turno == 0 else "⚫")

        if self.colas[self.turno].full():
            toDelete=self.colas[self.turno].get()
            self.tablero.deleteBox(int(toDelete))

        self.colas[self.turno].put(numero)
        self.turno=(self.turno+1)%2
        if self.colas[self.turno].full():
            numero=self.colas[self.turno].queue[0]
            self.tablero.modify_tablero(numero, "❌" if self.turno == 0 else "🔴")
    
        if self.tablero.anyoneHasWon():
            await self.winningSequence(query, self.turno)
            return
    
        await self.updateKeyboard(query)

    async def updateKeyboard(self, query):
        keyboard = self.tablero.create_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        print(self.nombre_jugadores)
        await query.message.edit_text("Turno del jugador "  + (", @" + self.nombre_jugadores[self.turno]) + "!" ,
            reply_markup=reply_markup
        )