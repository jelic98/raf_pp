#!/usr/bin/python
# Copyright 2015 James Stallings
 
import os
import io
import sys
 
try:
    # Python 3
    import tkinter
    from tkinter import font, ttk, scrolledtext, _tkinter

except ImportError:
    # Python 2
    import Tkinter as tkinter
    from Tkinter import ttk
    import tkFont as font
    import ScrolledText as scrolledtext
 
from pygments.lexers.python import PythonLexer
from pygments.lexers.special import TextLexer
from pygments.lexers.html import HtmlLexer
from pygments.lexers.html import XmlLexer
from pygments.lexers.templates import HtmlPhpLexer
from pygments.lexers.perl import Perl6Lexer
from pygments.lexers.ruby import RubyLexer
from pygments.lexers.configs import IniLexer
from pygments.lexers.configs import ApacheConfLexer
from pygments.lexers.shell import BashLexer
from pygments.lexers.diff import DiffLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.lexers.sql import MySqlLexer
from pygments.styles import get_style_by_name
 
class CoreUI(object):
    def __init__(self, lexer):
        self.sourcestamp = {}
        self.filestamp = {}
        self.uiopts = []
        self.lexer = lexer
        self.lastRegexp = ""
        self.markedLine = 0
        self.root = tkinter.Tk()
        self.uiconfig()
        self.root.bind("<Key>", self.eventkey)
        self.text.bind('<Return>', self.autoindent)
        self.text.bind('<Tab>', self.tab2spaces4)
        self.root.bind('<Control-KeyPress-s>', self.eventsave)
        self.createtags()
        self.text.edit_modified(False)
        self.bootstrap = [self.recolorize]

        if len(sys.argv) > 1:
            self.eventload(sys.argv[1])
        else:
            self.eventload("untitled.raf")

    def uiconfig(self):
        self.uiopts = {"height": "60",
                        "width": "132",
                        "cursor": "xterm",
                        "bg": "#000000",
                        "fg": "#FFAC00",
                        "insertbackground": "#FFD310",
                        "insertborderwidth": "1",
                        "insertwidth": "3",
                        "exportselection": True,
                        "undo": True,
                        "selectbackground": "#E0000E",
                        "inactiveselectbackground": "#E0E0E0"
                       }
        self.text = scrolledtext.ScrolledText(master=self.root, **self.uiopts)
        self.text.vbar.configure(
            width = "5m",
            activebackground = "#FFD310",
            borderwidth = "0",
            background = "#68606E",
            highlightthickness = "0",
            highlightcolor = "#00062A",
            highlightbackground = "#00062A",
            troughcolor = "#20264A",
            relief = "flat")    
        self.cli = tkinter.Text(self.root,{"height": "1",
                                 "bg": "#191F44",
                                 "fg": "#FFC014",
                                 "insertbackground": "#FFD310",
                                 "insertborderwidth": "1",
                                 "insertwidth": "3",
                                 "exportselection": True,
                                 "undo": True,
                                 "selectbackground": "#E0000E",
                                 "inactiveselectbackground": "#E0E0E0"
                                })
        self.text.grid(column = 0, row = 0, sticky = ('nsew'))
        self.cli.grid(column = 0, row = 1, pady = 1, sticky = ('nsew'))
        self.cli.bind("<Return>", self.cmdlaunch)
        self.cli.visible = True
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 0)

    def updatetitlebar(self):            
        self.root.title(self.filename)
        self.root.update()

    def cmdlaunch(self, event):
        cmd = self.cli.get("1.0", tkinter.END).strip("\n")
        index_insert = self.text.index("insert")
        
        if index_insert == None:
            index_insert = "1.0"

        self.text.tag_delete("sel")
        
        if cmd[0] == '@':
            self.eventload(cmd[1:])
        else:
            os.system(cmd)
            
        return "break"

    def autoindent(self, event):
        indentation = ""
        lineindex = self.text.index("insert").split(".")[0]
        linetext = self.text.get(lineindex+".0", lineindex+".end")

        for character in linetext:
            if character in [" ","\t"]:
                indentation += character
            else:
                break
                
        self.text.insert(self.text.index("insert"), "\n"+indentation)
        return "break"

    def tab2spaces4(self, event):
        self.text.insert(self.text.index("insert"), "    ")
        return "break"

    def eventload(self, filename):
        self.filename = filename

        if not os.access(self.filename, os.R_OK):
            os.system("touch " + self.filename)

        self.updatetitlebar()

        with open(self.filename, "r") as f:
            text = f.read()

            if text:
                self.text.insert(tkinter.INSERT, text)
                self.text.tag_remove(tkinter.SEL, '1.0', tkinter.END)
                self.text.see(tkinter.INSERT)

    def eventkey(self, event):
        keycode = event.keycode
        char = event.char
        self.recolorize()
        self.updatetitlebar()
 
    def eventsave(self, event):
        with open(self.filename, "w") as filedescriptor:
            filedescriptor.write(self.text.get("1.0", tkinter.END)[:-1])
        
        self.text.edit_modified(False)
        self.root.title("{} [saved]".format(self.filename))
 
    def mainloop(self):
        for task in self.bootstrap:
            task()

        self.root.mainloop()
 
    def createtags(self):
        bold_font = font.Font(self.text, self.text.cget("font"))
        bold_font.configure(weight=font.BOLD)
        italic_font = font.Font(self.text, self.text.cget("font"))
        italic_font.configure(slant=font.ITALIC)
        bold_italic_font = font.Font(self.text, self.text.cget("font"))
        bold_italic_font.configure(weight=font.BOLD, slant=font.ITALIC)
        style = get_style_by_name('default')
        
        for ttype, ndef in style:
            tag_font = None
        
            if ndef['bold'] and ndef['italic']:
                tag_font = bold_italic_font
            elif ndef['bold']:
                tag_font = bold_font
            elif ndef['italic']:
                tag_font = italic_font
 
            if ndef['color']:
                foreground = "#%s" % ndef['color'] 
            else:
                foreground = None
 
            self.text.tag_configure(str(ttype), foreground=foreground, font=tag_font) 
 
    def recolorize(self):
        code = self.text.get("1.0", "end-1c")
        tokensource = self.lexer.get_tokens(code)
        start_line=1
        start_index = 0
        end_line=1
        end_index = 0
        
        for ttype, value in tokensource:
            if "\n" in value:
                end_line += value.count("\n")
                end_index = len(value.rsplit("\n",1)[1])
            else:
                end_index += len(value)
 
            if value not in (" ", "\n"):
                index1 = "%s.%s" % (start_line, start_index)
                index2 = "%s.%s" % (end_line, end_index)
 
                for tagname in self.text.tag_names(index1): # FIXME
                    self.text.tag_remove(tagname, index1, index2)
 
                self.text.tag_add(str(ttype), index1, index2)
 
            start_line = end_line
            start_index = end_index
 
if __name__ == "__main__":
    extens = ""

    try:
        extens = sys.argv[1].split('.')[1]
    except IndexError:
        pass
    
    if extens == "raf":
        ui_core = CoreUI(lexer = RafLexer())
    else:
        ui_core = CoreUI(lexer = PythonLexer())
    
    ui_core.mainloop()
