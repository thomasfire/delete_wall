#!/usr/bin/python3

#script deletes almost all post from your wall
import vk_api
import re
import fcrypto
import getpass


def getall(vk,userid):
    count=0
    listtodel=[]

    f=open('files/allowed.db','r')
    allowed=f.read().split()
    f.close()
    print(allowed)
    while count<200:
        try:
            currposts=vk.wall.get(owner_id=userid,offset=count*50, count=50)
            if not currposts['items']:
                break
            count+=1
            for x in currposts['items']:
                if 'copy_history' in x.keys() and str(x['copy_history'][0]['from_id']) not in allowed:
                    listtodel.append(str(x['id']))
        except Exception as e:
            print("Smth goes wrong at getting wall: ",e)

    f=open('files/todelete.db','w')
    f.write(' '.join(listtodel))
    f.close()


def deletewall(vk,userid):
    f=open('files/todelete.db','r')
    todelete=f.read().split()
    print(len(todelete))
    f.close()
    for x in todelete:
        vk.wall.delete(owner_id=userid,post_id=int(x))



def main(vk,userid):
    #getall(vk,userid)
    deletewall(vk,userid)


def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


if __name__ == '__main__':
    #auth
    psswd=fcrypto.getkey(getpass.getpass())
    settings=fcrypto.fdecrypt("files/vk.settings",psswd)
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    userid=int("".join(re.findall(r"userid=(\d+)#enduserid",settings)))
    try:
        vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
    except Exception as e:
        print('smth goes wrong at getting vk_session:',e)

    #authorization
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
    #getting api
    try:
        vk = vk_session.get_api()
    except Exception as e:
        print('smth goes wrong at getting vk api\n',e)

    main(vk,userid)
