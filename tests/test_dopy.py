import sys
from dopy import dofile_client

def test_module(tmpdir):

    modname = 'echomod'
    mod = tmpdir.join(modname + ".py")
    mod.write('''

def ignored_func():
    """this function is ignored by dopy because it doesn't start
       with the default command prefix of 'do_'
    """
    pass

def do_echo(args, prefix="Echo: "):
    """echo [args]  - Echo the args you give it
    --prefix=Echo   - set the echo prefix. Default: "Echo: "
    """
    print(prefix + " ".join(args))

''')
    sys.path += [ str(tmpdir) ]
    print "sys.path is %r" % sys.path
    df = dofile_client(domodule=modname)
    assert 'echo' in df.commands
    sys.path.remove(str(tmpdir))

