import sys
from cmdpy import cmdfile_client

def test_module(tmpdir):

    modname = 'echomod'
    mod = tmpdir.join(modname + ".py")
    mod.write('''

def ignored_func():
    """this function is ignored by cmdpy because it doesn't start
       with the default command prefix of 'cmd_'
    """
    pass

def cmd_echo(args, prefix="Echo: "):
    """echo [args]  - Echo the args you give it
    --prefix=Echo   - set the echo prefix. Default: "Echo: "
    """
    print(prefix + " ".join(args))

''')
    sys.path += [ str(tmpdir) ]
    print "sys.path is %r" % sys.path
    df = cmdfile_client(cmdmodule=modname)
    assert 'echo' in df.commands
    sys.path.remove(str(tmpdir))

