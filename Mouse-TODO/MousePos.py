from subprocess import Popen, PIPE

'''
p = start()
x,y = mouse(p)
end(p) #p.kill()
'''

def start():
    from os.path import dirname,abspath
    return Popen('java -cp %s Portia'%dirname( abspath(__file__) ), shell=True, stdin=PIPE, stdout=PIPE)
def mouse(p):
    p.stdin.write('\n')
    p.stdin.flush()
    return tuple(int(i) for i in p.stdout.readline().split())
def end(p):
    '''p.kill()'''
    p.stdin.write('a\n')
    p.stdin.flush()

def main():
    p = start()
    a,b = 1,1 
    while a+b>0:
        x,y = mouse(p)
        if a!=x or b!=y: print x,y
        a,b = x,y
    end(p)

if __name__ == '__main__': main()