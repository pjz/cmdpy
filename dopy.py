#!/usr/bin/python

import sys

def debug_noop(*args, **kwargs):
    pass

def debug_real(func):
    print "DEBUG: ", func()

debug = debug_noop

UsageError = SyntaxError

class dofile_client(object):
    """
        A wrapper class to turn a module with some functions into a commandline program.

        In that module:
           command_prefix defines which methods will be paid attention to.  default: 'do_'
               If a command method raises SyntaxError, the help for that func will be shown.
           functions whose names start with the command_prefix will be turned into
               commandline subcommands.  They must take at least a single argument that's the
               rest of the arguments on the commandline. They MAY take keyword arguments,
               which are translated from arguments specified with a '--' prefix.
        
    """

    def __init__(self, dofilename=None, domodule=None):
        if dofilename is not None:
            import imp
            dofile = imp.load_source('dofile', dofilename)
        elif domodule is not None:
            import imp
            details = imp.find_module(domodule)
            dofile = imp.load_module(domodule, *details)
        else:
            print("Must specify a file or module!")
            raise ImportError

        self.dofile = dofile
        self.cmdprefix = getattr(dofile, 'command_prefix', 'do_')
        cp = self.cmdprefix
        cmdlist = [ c[len(cp):] for c in dir(dofile) if c.startswith(cp) ]

        if "help" not in cmdlist: 
            setattr(dofile, cp + "help", self.do_help)
            cmdlist += [ "help" ]

        if "dopy_debug" not in cmdlist: 
            setattr(dofile, cp + "dopy_debug", self.do_dopy_debug)
            # cmdlist += [ "dopy_debug" ] 

        cmdlist.sort()
        self.commands = cmdlist

    def execute(self, rargs):

        kw = {}
        for a in rargs:
            if a.startswith('--'):
                if '=' in a:
                     k, v = a[2:].split('=')
                else:
                     k = a[2:]
                     v = True
                kw[k] = v

        args = [ x for x in rargs if not x.startswith('--') ]
 
        try:
            self.dispatch(args, **kw)
        except KeyboardInterrupt:
            print("Interrupted.")

    def dispatch(self, args, **kwargs):

        commands = ", ".join(self.commands)

        if not args:
            print("No command specified.  Try one of: %s." % commands)
            return
 
        cmd = args[0].strip()
        cmdargs = args[1:]
        cmdfunc = getattr(self.dofile, self.cmdprefix + cmd, None)

        if cmdfunc is None:
            print("Unknown command '%s'.  Try one of: %s." % (cmd, commands))
            return

        debug(lambda : "calling %s with args %s and kwargs %s" % (cmdfunc, cmdargs, kwargs))

        try:
            cmdfunc(cmdargs, **kwargs)
        except UsageError:
            print(cmdfunc.__doc__)
            sys.exit(1)

    def do_help(self, args, **kwargs):
        """help [cmd] - show either all the help or that of the specified command"""

        def _help_for(cmd):
            doc = getattr(self.dofile, self.cmdprefix + cmd).__doc__
            if not doc:
                doc = cmd
            return doc.strip()

        if not args:
            print("Commands:\n--------")
            for cmd in self.commands:
                print _help_for(cmd)
                if self.commands[-1] != cmd:
                    print
        elif args[0] in self.commands:
            print _help_for(args[0])
        else:
            print("Unknown Command '%s'.  try one of: %s." % (args[0], ', '.join(self.commands)))

    def do_dopy_debug(self, args, **kwargs):
        global debug
        debug = debug_real
        self.dispatch(args, **kwargs)


if __name__=='__main__':
    args = sys.argv
    if len(args) < 1:
        print("Usage:\ndopy <dofile>      - list all the commands in dofile")
        sys.exit(1)
    dofilename = args[1]
    dofileargs = args[2:]
    dofile = dofile_client(dofilename)
    dofile.execute(dofileargs)
