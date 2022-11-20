import subprocess as sp
from tkinter import *

# 기본창
root = Tk()
root.title('DNS Changer')
root.geometry('400x360+400+200')
root.resizable(False, False)
root.iconphoto(False,PhotoImage(file='C:\wasab2_Work\Py\images\ico.png'))


# keep track on/off state
global is_on
is_on = False

  

label01 = Label(root, text='', width=0, height=0,
                font=('Consolas', 20), fg='darkgray')
label01.pack(pady=20)

label20 = Label(root, text='DHCP', font=('Consolas', 18),
                fg='darkgray').place(x=60, y=106)
label22 = Label(root, text='1.1.1.1', font=(
    'Consolas', 18), fg='#2a79f7').place(x=280, y=106)

# image path on/off
on_img = PhotoImage(file='C:\wasab2_Work\Py\images\on.png')
off_img = PhotoImage(file='C:\wasab2_Work\Py\images\off.png')

#define current dns info
def checkdns():
    global is_on
    currentDns=sp.Popen('netsh interface ipv4 show dnsservers name="이더넷"',shell=True,stdout=sp.PIPE,stderr=sp.PIPE)
    (stdout, stderr)= currentDns.communicate()

    data=stdout.decode('euc-kr').replace('\r\n','').replace('  ',' ').split(' ')
    data=list(filter(None, data))
    
    if 'DHCP를' in data:
        p=data.index('서버:')
        label01.config(text=f'DHCP-{data[p+1]}')
    
    else:
        p=data.index('서버:')
        label01.config(text=f'{data[p+1]}')
        
        if data[p+1] == '1.1.1.1':
            onetouch.config(image=on_img)
            is_on=True

# define switch button command       
def switch():
    global is_on
    if is_on:
        onetouch.config(image=off_img)
        sp.Popen('netsh int ip set dns name="이더넷" source=dhcp', shell=True).wait()
        label01.config(text='DHCP', fg='darkgray')
        is_on = False
    else:
        onetouch.config(image=on_img)
        sp.Popen('netsh int ip set dns name="이더넷" static 1.1.1.1', shell=True).wait()
        sp.Popen('netsh int ip add dns name="이더넷" addr=1.0.0.1 index=2', shell=True).wait()
        label01.config(text='Cloudflare', fg='#2a79f7')
        is_on = True

# define checkRadio command
def checkRadio():
    if RadioVar.get() == 1:
        sp.Popen('netsh int ip set dns name="이더넷" source=dhcp', shell=True).wait()
        label01.config(text='DHCP', fg='black')
    elif RadioVar.get() == 2:
        sp.Popen('netsh int ip set dns name="이더넷" static 8.8.8.8', shell=True).wait()
        sp.Popen('netsh int ip add dns name="이더넷" addr=8.8.4.4 index=2', shell=True).wait()
        label01.config(text='Google', fg='black')
    elif RadioVar.get() == 3:
        sp.Popen('netsh int ip set dns name="이더넷" static 1.1.1.1', shell=True).wait()
        sp.Popen('netsh int ip add dns name="이더넷" addr=1.0.0.1 index=2', shell=True).wait()
        label01.config(text='Cloudflare', fg='black')
    elif RadioVar.get() == 4:
        sp.Popen('netsh int ip set dns name="이더넷" static 210.220.163.82', shell=True).wait()
        sp.Popen(
            'netsh int ip add dns name="이더넷" addr= 219.250.36.130 index=2', shell=True).wait()
        label01.config(text='SKB', fg='black')
    elif RadioVar.get() == 5:
        sp.Popen('netsh int ip set dns name="이더넷" static 168.126.63.1', shell=True).wait()
        sp.Popen(
            'netsh int ip add dns name="이더넷" addr=168.126.63.2 index=2', shell=True).wait()
        label01.config(text='KT', fg='black')
    elif RadioVar.get() == 6:
        sp.Popen('netsh int ip set dns name="이더넷" static 164.124.101.2', shell=True).wait()
        sp.Popen(
            'netsh int ip add dns name="이더넷" addr=203.248.252.2 index=2', shell=True).wait()
        label01.config(text='U+', fg='black')
    else:
        label01.config(text='Error', fg='red')

# create one touch toggle btn
onetouch = Button(root, image=off_img, bd=0, command=switch)
onetouch.pack(pady=10)

# choose other server
label10 = Label(root, text='Choose Server', height=1,
                font=('Consolas', 10, 'bold'),)
label10.pack(pady=10)

# radio buttons
RadioVar = IntVar()
radio1 = Radiobutton(root, text=' 1. DHCP', value=1,
                     variable=RadioVar, command=checkRadio).place(x=150, y=210)
radio2 = Radiobutton(root, text=' 2. Google', value=2,
                     variable=RadioVar, command=checkRadio).place(x=150, y=230)
radio3 = Radiobutton(root, text=' 3. Cloudflare', value=3,
                     variable=RadioVar, command=checkRadio).place(x=150, y=250)
radio4 = Radiobutton(root, text=' 4. SKB', value=4,
                     variable=RadioVar, command=checkRadio).place(x=150, y=270)
radio5 = Radiobutton(root, text=' 5. KT', value=5,
                     variable=RadioVar, command=checkRadio).place(x=150, y=290)
radio6 = Radiobutton(root, text=' 6. U+', value=6,
                     variable=RadioVar, command=checkRadio).place(x=150, y=310)

# 실행
checkdns()
root.mainloop()
