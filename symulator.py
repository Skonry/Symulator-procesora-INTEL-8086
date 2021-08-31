import re
import random

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class RadioButtons():
  def __init__(self, parent, label, columnNumber, rowNumber, buttonsNames, buttonsValues = None):
    if buttonsValues is None:
      buttonsValues = buttonsNames
    self.label = ttk.Label(parent, text=label)
    self.label.grid(column=columnNumber, row=rowNumber)
    self.stringVar = StringVar()
    for index in range(len(buttonsNames)):
      button = ttk.Radiobutton(
        parent, 
        text=buttonsNames[index], 
        variable=self.stringVar, 
        value=buttonsValues[index]
      )
      button.grid(column=columnNumber, row=rowNumber + index + 1)

class Register():
  def __init__(self, parent, name, rowNumber, validateRegisterValueCommand):
    self.stringVar = StringVar(value="0000")
    self.registerName = ttk.Label(parent, text=name)
    self.registerName.grid(column=0, row=rowNumber)
    self.result = ttk.Label(parent, textvariable=self.stringVar)
    self.result.grid(column=0, row=rowNumber + 1)
    self.entry = ttk.Entry(
      parent, 
      textvariable=self.stringVar, 
      validate='key', 
      validatecommand=validateRegisterValueCommand)
    self.entry.grid(column=0, row=rowNumber + 1)

class StackOperations():
  def __init__(self, parent, commitStackOperation):
    self.frame = ttk.Frame(parent)
    self.frame.grid(column=1, row=3)
    self.label = ttk.Label(self.frame, text="Operacje na stosie", padding=(10))
    self.label.grid(column=0, row=1, columnspan=2)
    self.operationRadioButtons = RadioButtons(
      self.frame,
      "Operacja",
      0,
      5,
      ["PUSH", "POP"]
    )
    self.registerRadioButtons = RadioButtons(
      self.frame,
      "Rejestr",
      1,
      5,
      ["AX", "BX", "CX", "DX"]
    )
    self.buttonFrame = ttk.Frame(self.frame, padding=(10))
    self.buttonFrame.grid(column=0, row=15, columnspan=2)
    self.commitOperationButton = ttk.Button(self.buttonFrame, text="Wykonaj", command=commitStackOperation)
    self.commitOperationButton.grid(column=0, row=0)

class IndexRegisters():
  def __init__(self, parent, validateRegisterValueCommand):
    self.frame = ttk.Frame(parent, padding=(20))
    self.frame.grid(column=0, row=2)
    self.label = ttk.Label(self.frame, text="Rejestry indeksowe i bazowe", padding=(10))
    self.label.grid(column=0, row=1)
    self.resetButton = ttk.Button(self.frame, text="Reset", command=self.resetRegisters)
    self.resetButton.grid(column=0, row=2)
    self.siRegister = Register(self.frame, 'SI', 10, validateRegisterValueCommand)
    self.diRegister = Register(self.frame, 'DI', 13, validateRegisterValueCommand)
    self.bpRegister = Register(self.frame, 'BP', 16, validateRegisterValueCommand)
    self.spRegister = Register(self.frame, 'SP', 19, validateRegisterValueCommand)
    self.dispRegister = Register(self.frame, 'DISP', 22, validateRegisterValueCommand)

  def resetRegisters(self):
    self.siRegister.stringVar.set("0000")
    self.diRegister.stringVar.set("0000")
    self.bpRegister.stringVar.set("0000")
    self.spRegister.stringVar.set("0000")
    self.dispRegister.stringVar.set("0000")

class MainRegisters():
  def __init__(self, parent, validateRegisterValueCommand):
    self.frame = ttk.Frame(parent, padding=(20))
    self.frame.grid(column=0, row=1)
    self.label = ttk.Label(self.frame, text="Rejestry ogólnego przeznaczenia", padding=(10))
    self.label.grid(column=0, row=0)
    self.resetButton = ttk.Button(self.frame, text="Reset", command=self.resetRegisters)
    self.resetButton.grid(column=0, row=1)
    self.randomizeButton = ttk.Button(self.frame, text="Random", command=self.randomizeRegisters)
    self.randomizeButton.grid(column=0, row=2)
    self.axRegister = Register(self.frame, 'AX', 10, validateRegisterValueCommand)
    self.bxRegister = Register(self.frame, 'BX', 13, validateRegisterValueCommand)
    self.cxRegister = Register(self.frame, 'CX', 16, validateRegisterValueCommand)
    self.dxRegister = Register(self.frame, 'DX', 19, validateRegisterValueCommand)

  def resetRegisters(self):
    self.axRegister.stringVar.set("0000")
    self.bxRegister.stringVar.set("0000")
    self.cxRegister.stringVar.set("0000")
    self.dxRegister.stringVar.set("0000")
  
  def randomizeRegisters(self):
    self.axRegister.stringVar.set(''.join(random.choices("0123456789ABCDEF", k=4)))
    self.bxRegister.stringVar.set(''.join(random.choices("0123456789ABCDEF", k=4)))
    self.cxRegister.stringVar.set(''.join(random.choices("0123456789ABCDEF", k=4)))
    self.dxRegister.stringVar.set(''.join(random.choices("0123456789ABCDEF", k=4)))

class IndexRegistersOperations():
  def __init__(self, parent, commitIndexRegistersOperations):
    self.frame = ttk.Frame(parent, padding=(20))
    self.frame.grid(column=1, row=2)
    self.label = ttk.Label(self.frame, text="Operacje na rejestrach indeksowych i bazowych", padding=(10))
    self.label.grid(column=0, row=1, columnspan=5)
    self.sourceAndDestinationRadioButtons = RadioButtons(
      self.frame,
      "Źródło i cel",
      0, 
      5, 
      ["z rejestru do pamięci", "z pamięci do rejestru"], 
      ["fromRegisterToMemory", "fromMemoryToRegister"]
    )
    self.addressingModeRadioButtons = RadioButtons(
      self.frame,
      "Tryb adresowania",
      1, 
      5, 
      ["indeksowy", "bazowy", "indeksowo-bazowy"], 
      ["indexedMode", "baseMode", "indexedBasedMode"]
    )
    self.indexRegisterRadioButtons = RadioButtons(
      self.frame,
      "Rejestr indeksowy",
      2,
      5,
      ["SI", "DI", "BX", "BP", "SI i BX", "DI i BX", "SI i BP", "DI i BP"],
      ["SI", "DI", "BX", "BP", "SI and BX", "DI and BX", "SI and BP", "DI and BP"]
    )
    self.mainRegisterRadioButtons = RadioButtons(
      self.frame,
      "Rejestr",
      3,
      5,
      ["AX", "BX", "CX", "DX"]
    )
    self.operationRadioButtons = RadioButtons(
      self.frame,
      "Operacja",
      4,
      5,
      ["MOV", "XCHG"]
    )
    self.buttonFrame = ttk.Frame(self.frame, padding=(10))
    self.buttonFrame.grid(column=0, row=20, columnspan=5)
    self.commitOperationButton = ttk.Button(
      self.buttonFrame, 
      text="Wykonaj", 
      command=commitIndexRegistersOperations
    )
    self.commitOperationButton.grid(column=0, row=0)

class MainRegistersOperations():
  def __init__(self, parent, commitMainRegistersOperation):
    self.frame = ttk.Frame(parent, padding=(20))
    self.frame.grid(column=1, row=1)
    self.label = ttk.Label(self.frame, text="Operacje na rejestrach ogólnego przeznaczenia", padding=(10))
    self.label.grid(column=0, row=1, columnspan=3)
    self.sourceRadioButtons = RadioButtons(self.frame, "Rejestr źródłowy", 0, 5, ["AX", "BX", "CX", "DX"])
    self.operationRadioButtons = RadioButtons(self.frame, "Operacja", 1, 5, ["MOV", "XCHG"])
    self.destinationRadioButtons = RadioButtons(self.frame, "Rejestr przeznaczenia", 2, 5, ["AX", "BX", "CX", "DX"])
    self.buttonFrame = ttk.Frame(self.frame, padding=(10))
    self.buttonFrame.grid(column=0, row=10, columnspan=3)
    self.commitOperationButton = ttk.Button(self.buttonFrame, text="Wykonaj", command=commitMainRegistersOperation)
    self.commitOperationButton.grid(column=0, row=0)

class Title():
  def __init__(self, parent):
    self.frame = ttk.Frame(parent, padding=(20))
    self.frame.grid(column=0, row=0, columnspan=2)
    self.label = ttk.Label(self.frame, text="Symulator rozkazów procesora INTEL 8086", font=("TkDefaultFont", 20))
    self.label.grid(column=0, row=0)

class MainFrame():
  def __init__(
    self, 
    parent, 
    validateRegisterValueCommand, 
    commitMainRegistersOperation, 
    commitIndexRegistersOperations,
    commitStackOperation
  ):
    self.frame = ttk.Frame(parent)
    self.frame.grid(column=0, row=0)
    self.title = Title(self.frame)
    self.mainRegisters = MainRegisters(self.frame, validateRegisterValueCommand)
    self.indexRegisters = IndexRegisters(self.frame, validateRegisterValueCommand)
    self.mainRegistersOperations = MainRegistersOperations(self.frame, commitMainRegistersOperation)
    self.indexRegistersOperations = IndexRegistersOperations(self.frame, commitIndexRegistersOperations)
    self.stackOperations = StackOperations(self.frame, commitStackOperation)

class Intel8086Simulator():
  def __init__(self):
    self.root = Tk()
    self.root.title('Symulator procesora')
    self.root.geometry('750x900')
    self.memorySegment = [0] * (64 * 1024)
    self.stackSegment = [0] * (64 * 1024)
    self.validateRegisterValueCommand = (self.root.register(self.validateRegisterValue), '%P', '%V')
    self.mainFrame = MainFrame(
      self.root, 
      self.validateRegisterValueCommand, 
      self.commitMainRegistersOperation,
      self.commitIndexRegistersOperations,
      self.commitStackOperation
    )
    self.root.mainloop()

  def validateRegisterValue(self, value, validationType):
    if validationType == 'key':
        match = re.search('^[a-fA-F0-9]?[a-fA-F0-9]?[a-fA-F0-9]?[a-fA-F0-9]?$', value)
        if match:
            return True
        return False

  def commitMainRegistersOperation(self):
    sourceStrVar = None
    if self.mainFrame.mainRegistersOperations.sourceRadioButtons.stringVar.get() == 'AX':
        sourceStrVar = self.mainFrame.mainRegisters.axRegister.stringVar
    elif self.mainFrame.mainRegistersOperations.sourceRadioButtons.stringVar.get() == 'BX':
        sourceStrVar = self.mainFrame.mainRegisters.bxRegister.stringVar
    elif self.mainFrame.mainRegistersOperations.sourceRadioButtons.stringVar.get() == 'CX':
        sourceStrVar = self.mainFrame.mainRegisters.cxRegister.stringVar
    elif self.mainFrame.mainRegistersOperations.sourceRadioButtons.stringVar.get() == 'DX':
        sourceStrVar = self.mainFrame.mainRegisters.dxRegister.stringVar
    
    destinationStrVar = None
    if self.mainFrame.mainRegistersOperations.destinationRadioButtons.stringVar.get() == 'AX':
        destinationStrVar = self.mainFrame.mainRegisters.axRegister.stringVar
    elif self.mainFrame.mainRegistersOperations.destinationRadioButtons.stringVar.get() == 'BX':
        destinationStrVar = self.mainFrame.mainRegisters.bxRegister.stringVar
    elif self.mainFrame.mainRegistersOperations.destinationRadioButtons.stringVar.get() == 'CX':
        destinationStrVar = self.mainFrame.mainRegisters.cxRegister.stringVar
    elif self.mainFrame.mainRegistersOperations.destinationRadioButtons.stringVar.get() == 'DX':
        destinationStrVar = self.mainFrame.mainRegisters.dxRegister.stringVar

    if self.mainFrame.mainRegistersOperations.operationRadioButtons.stringVar.get() == 'MOV':
        destinationStrVar.set(sourceStrVar.get())
    elif self.mainFrame.mainRegistersOperations.operationRadioButtons.stringVar.get() == 'XCHG':
        temp = destinationStrVar.get()
        destinationStrVar.set(sourceStrVar.get())
        sourceStrVar.set(temp)

  def commitIndexRegistersOperations(self):
    indexRegisterSelected = self.mainFrame.indexRegistersOperations.indexRegisterRadioButtons.stringVar.get()
    mainRegisterSelected = self.mainFrame.indexRegistersOperations.mainRegisterRadioButtons.stringVar.get()

    memorySegmentAddress = None
    if self.mainFrame.indexRegistersOperations.addressingModeRadioButtons.stringVar.get() == "indexedMode":
      if indexRegisterSelected == 'SI':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.siRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
      elif indexRegisterSelected == 'DI':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.diRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
    elif self.mainFrame.indexRegistersOperations.addressingModeRadioButtons.stringVar.get() == "baseMode":
      if indexRegisterSelected == 'BX':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.bxRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
      elif indexRegisterSelected == 'BP':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.bpRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
    elif self.mainFrame.indexRegistersOperations.addressingModeRadioButtons.stringVar.get() == "indexedBasedMode":
      if indexRegisterSelected == 'SI and BX':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.siRegister.stringVar.get(), 16) + \
          int(self.mainFrame.mainRegisters.bxRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
      elif indexRegisterSelected == 'DI and BX':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.diRegister.stringVar.get(), 16) + \
          int(self.mainFrame.mainRegisters.bxRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
      elif indexRegisterSelected == 'SI and BP':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.siRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.bpRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
      elif indexRegisterSelected == 'DI and BP':
          memorySegmentAddress = int(self.mainFrame.indexRegisters.diRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.bpRegister.stringVar.get(), 16) + \
          int(self.mainFrame.indexRegisters.dispRegister.stringVar.get(), 16)
    if (memorySegmentAddress == None):
      return
    
    mainRegisterStrVar = None
    if mainRegisterSelected == 'AX':
        mainRegisterStrVar = self.mainFrame.mainRegisters.axRegister.stringVar
    elif mainRegisterSelected == 'BX':
        mainRegisterStrVar = self.mainFrame.mainRegisters.bxRegister.stringVar
    elif mainRegisterSelected == 'CX':
        mainRegisterStrVar = self.mainFrame.mainRegisters.cxRegister.stringVar
    elif mainRegisterSelected == 'DX':
        mainRegisterStrVar = self.mainFrame.mainRegisters.dxRegister.stringVar
    if self.mainFrame.indexRegistersOperations.operationRadioButtons.stringVar.get() == 'MOV':
      if self.mainFrame.indexRegistersOperations.sourceAndDestinationRadioButtons.stringVar.get() == 'fromRegisterToMemory':
        self.memorySegment[memorySegmentAddress] = mainRegisterStrVar.get()
      elif self.mainFrame.indexRegistersOperations.sourceAndDestinationRadioButtons.stringVar.get() == 'fromMemoryToRegister':
        mainRegisterStrVar.set(self.memorySegment[memorySegmentAddress])
    elif self.mainFrame.indexRegistersOperations.operationRadioButtons.stringVar.get() == 'XCHG':
      
      temp = self.memorySegment[memorySegmentAddress]
      self.memorySegment[memorySegmentAddress] = mainRegisterStrVar.get()
      mainRegisterStrVar.set(temp)
    
  def commitStackOperation(self):
    stringVar = None
    if self.mainFrame.stackOperations.registerRadioButtons.stringVar.get() == 'AX':
        stringVar = self.mainFrame.mainRegisters.axRegister.stringVar
    elif self.mainFrame.stackOperations.registerRadioButtons.stringVar.get() == 'BX':
        stringVar = self.mainFrame.mainRegisters.bxRegister.stringVar
    elif self.mainFrame.stackOperations.registerRadioButtons.stringVar.get() == 'CX':
        stringVar = self.mainFrame.mainRegisters.cxRegister.stringVar
    elif self.mainFrame.stackOperations.registerRadioButtons.stringVar.get() == 'DX':
        stringVar = self.mainFrame.mainRegisters.dxRegister.stringVar

    if self.mainFrame.stackOperations.operationRadioButtons.stringVar.get() == 'PUSH':
        spDecimalValue = int(self.mainFrame.indexRegisters.spRegister.stringVar.get(), 16)
        self.stackSegment[spDecimalValue] = stringVar.get()
        spRegisterNewValue = hex(spDecimalValue + 2).split('x')[-1].rjust(4, '0')
        self.mainFrame.indexRegisters.spRegister.stringVar.set(spRegisterNewValue)

    elif self.mainFrame.stackOperations.operationRadioButtons.stringVar.get() == 'POP':
        spDecimalValue = int(self.mainFrame.indexRegisters.spRegister.stringVar.get(), 16)
        stringVar.set(self.stackSegment[spDecimalValue - 2])
        self.stackSegment[spDecimalValue - 2] = 0
        spRegisterNewValue = hex(spDecimalValue - 2).split('x')[-1].rjust(4, '0')
        self.mainFrame.indexRegisters.spRegister.stringVar.set(spRegisterNewValue)

if __name__ == "__main__":
  simulator = Intel8086Simulator()

