import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def build(path, file, name):
    path += '/'
    sysdrv = os.getenv('SystemDrive')
    csc = '/csc.exe'
    fwpath = '/windows/microsoft.net/framework/'
    netver = ['v4.8',
              'v4.7.2', 'v4.7.1', 'v4.7'
              'v4.6.51500', 'v4.6.01590', 'v4.6.2', 'v4.6.1', 'v4.6',
              'v4.5.50938', 'v4.5.50709', 'v4.5.2', 'v4.5.1', 'v4.5',
              'v4.0.30319', 'v4.0.30128', 'v4.0.21006', 'v4.0.20506', 'v4.0',
              'v3.5.30729', 'v3.5.594', 'v3.5.30428', 'v3.5.21022', 'v3.5.20706', 'v3.5.20404', 'v3.5']
    defaultNet = []
    for i in netver: defaultNet.append(sysdrv+fwpath+i+csc) 
    print(defaultNet)
    netpath = 0
    
    for i in defaultNet:
        try:
            open(i).close()
            netpath = i
            break 
        except: pass
    if not netpath: return 0

    print('actual net: ', netpath)
    
    temp_sharp = open(path+'abbat_sharp_temp_source.cs', 'w')
    temp_batch = open(path+'abbat_batch_temp_source.bat', 'w')
    pack_batch = open(path+file, 'r').read()
    char_batch = '{'
    for i in pack_batch:
        if i == '\n': char_batch += "'"+';'+"', "
        else: char_batch += "'"+i+"', "
    char_batch += '}'
    temp_sharp.write('''
using System;
using System.Diagnostics;
using System.IO;
class bat{
    static void Main(){
        char[] cmd = '''+char_batch+''';
        string com = new String(cmd);
        var process = new Process(){
            StartInfo = new ProcessStartInfo{
                FileName = "cmd.exe",
                RedirectStandardInput = true,
                UseShellExecute = false
            }
        };
        process.Start();
        using(StreamWriter pWriter = process.StandardInput){
            if(pWriter.BaseStream.CanWrite) foreach(var i in com.Split(';')) pWriter.WriteLine(i);
        }
    }
}''')
    temp_sharp.close()
    temp_batch.write('cd '+path+'\n'+netpath+''' abbat_sharp_temp_source.cs
ren "abbat_sharp_temp_source.exe" "'''+name+'''.exe"
del abbat_sharp_temp_source.cs
del abbat_batch_temp_source.bat
pause''')
    temp_batch.close()
    os.system(path+'abbat_batch_temp_source.bat')

    return 1

def confirm_build(path, file, name = ''):
    print(path, file, name)
    if path == '' or file == '':
        messagebox.showinfo('Error', 'Path and file required')
        return 0
    if name == '':
        messagebox.showinfo('', 'Name is undefined, wrapped batch will be saved as default.exe')
        name = 'default'
    if build(path, file, name): messagebox.showinfo('Info', 'Bat wrapped to exe successfully.')
    else: messagebox.showinfo('Error', 'Bat didnt wrapped')

def parse_path(path, strpath, strfile):
    file = ''
    for i in range(len(path)):
        if path[-1] != '/' and path[-1] != '\\': file += path[-1]; path = path[:-1]
        else: break
    file = file[::-1]
    strpath.set(path)
    strfile.set(file)

def main():
    root = Tk()
    root.geometry('640x480')
    root.title('abBat')
    path, file, name = StringVar(), StringVar(), StringVar()
    
    Label(text = 'Path to file:').pack()
    Entry(textvariable = path).pack()
    Label(text = 'File name:').pack()
    Entry(textvariable = file).pack()
    Button(text = 'Select file', command = lambda: parse_path(filedialog.askopenfilename(), path, file)).pack()
    Label(text = 'Executed file name:').pack()
    Entry(textvariable = name).pack()
    btn2 = Button(text = 'Build .exe', command = lambda: confirm_build(path.get(), file.get(), name.get()))
    btn2.pack()
    
    root.mainloop()
    
main()
#build('C:/$abstracd/fodyssey/test', 'launch.bat', 'default')
