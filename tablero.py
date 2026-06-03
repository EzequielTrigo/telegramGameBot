from typing import Final
from dotenv import load_dotenv
import os
# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from queue import Queue


class Tablero:
    def __init__(self):
        self.tablero = [["", "", ""],["", "", ""],["", "", ""]]
    
    def marcar_casilla(self, numero: int, simbolo: str) -> bool:
        if self.tablero[numero//3][numero%3] == "":
            self.tablero[numero//3][numero%3] = simbolo
            return True
        return False
    
    def anyoneHasWon(self):
        # Verificar filas y columnas
        for i in range(3):
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != "":
                return True
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != "":
                return True
        
        # Verificar diagonales
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != "":
            return True
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != "":
            return True
        
        return False
    
    def modify_tablero(self, numero:int, simbolo:str):
        self.tablero[numero//3][numero%3] = simbolo
        
    def deleteBox(self, numero:int):
        self.tablero[numero//3][numero%3] = ""

    def create_keyboard(self):
        keyboard = []
        for i in range(3):
            row = []
            for j in range(3):
                cell_value = self.tablero[i][j]
                button_text = cell_value if cell_value else " "
                row.append(InlineKeyboardButton(button_text, callback_data=str(i*3+j)))
            keyboard.append(row)
        return keyboard
    
    def boxOccupied(self, numero:int) -> bool:
        return self.tablero[numero//3][numero%3] != ""