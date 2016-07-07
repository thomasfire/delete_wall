#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is lib for easy using Twofish encryption
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

from twofish import Twofish
import hashlib
import codecs
import sys
import getpass
import os

#returns secure hash
def getkey(smstr):
    salt=hashlib.sha512(b'fghjfjkjlktycvq/.,ASS ON KEYBOARD t567 tx546e!@$^*#)%&/*-+-thgklh;xmnvhgjfty'+
    smstr.encode('ascii')).hexdigest()
    nhash=hashlib.sha256(salt.encode('ascii')+smstr.encode('ascii')).hexdigest()
    for x in range(2**18):
        nhash=hashlib.sha256(salt.encode('ascii')+nhash.encode('ascii')).hexdigest()
    return hashlib.sha256(salt.encode('ascii')+nhash.encode('ascii')).digest()


#encrypts file via password
def fencrypt(filen,password):
    f=open(filen,'r')
    smstr=f.read()
    f.close()
    if len(smstr)%16:
        nstr=str(smstr+'%'*(16-len(smstr)%16)).encode('utf-8')
    else:
        nstr=smstr.encode('utf-8')

    psswd=Twofish(password)
    encredstr=b''

    for x in range(int(len(nstr)/16)):
        encredstr+=psswd.encrypt(nstr[x*16:(x+1)*16])

    f=open(filen,'wb')
    f.write(encredstr)
    f.close()

#decrypts file via password,returns decrypted text
def fdecrypt(filen,password):
    f=open(filen,'rb')
    smstr=f.read()
    f.close()
    psswd=Twofish(password)
    decredstr=b''

    for x in range(int(len(smstr)/16)):
        decredstr+=psswd.decrypt(smstr[x*16:(x+1)*16])

    return codecs.decode(decredstr,'utf-8').strip('%')



def main():
    if len(sys.argv)>1 and sys.argv[1]=='-setup':
        vari=False
        while not vari:
            inone=getpass.getpass('Password to encrypt files: ')
            intwo=getpass.getpass('Re-enter : ')
            if inone==intwo:
                password=getkey(inone)
                vari=True
            else:
                print('Wrong validation,retry\n')

        f=open('files/vk.settings','w')
        f.write('login={0}#endlogin\n'.format(input('Enter login: ')))
        f.write('password={0}#endpass\n'.format(getpass.getpass('Enter password: ')))
        f.write('userid={0}#enduserid\n'.format(input('Enter user id: ')))
        f.write('ACHTUNG!THIS IS UNENCRYPTED TEXT!')
        f.close()
        fencrypt('files/vk.settings',password)

        print('Success,now you can run sript via $ python3 rundel.py')
    else:
        print('Usage: python3 fcrypto.py -setup')

#TODO доделать настройку и доделать остальные модули под секурность



if __name__ == '__main__':
    main()
