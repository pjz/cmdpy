#!/usr/bin/python

import sys

def debug_noop(*args, **kwargs):
    pass

def debug_real(func):
    print "DEBUG: ", func()

debug = debug_noop

UsageError = SyntaxError

class cmdfile_client(object):
    """
        A wrapper class to turn a module with some functions into a commandline program.

        In that module:
           command_prefix defines which methods will be paid attention to.  default: 'cmd_'
               If a command method raises SyntaxError, the help for that func will be shown.
           functions whose names start with the command_prefix will be turned into
               commandline subcommands.  They must take at least a single argument that's the
               rest of the arguments on the commandline. They MAY take keyword arguments,
               which are translated from arguments specified with a '--' prefix.
        
    """

    def __init__(self, cmdfilename=None, cmdmodule=None):
        if cmdfilename is not None:
            import imp
            cmdfile = imp.load_source('cmdfile', cmdfilename)
        elif cmdmodule is not None:
            import imp
            details = imp.find_module(cmdmodule)
            cmdfile = imp.load_module(cmdmodule, *details)
        else:
            print("Must specify a file or module!")
            raise ImportError

        self.cmdfile = cmdfile
        self.cmdprefix = getattr(cmdfile, 'command_prefix', 'cmd_')
        cp = self.cmdprefix
        cmdlist = [ c[len(cp):] for c in dir(cmdfile) if c.startswith(cp) ]

        if "help" not in cmdlist: 
            setattr(cmdfile, cp + "help", self.cmd_help)
            cmdlist += [ "help" ]

        if "cmdpy_debug" not in cmdlist: 
            setattr(cmdfile, cp + "cmdpy_debug", self.cmd_cmdpy_debug)
            # cmdlist += [ "cmdpy_debug" ] 

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
        cmdfunc = getattr(self.cmdfile, self.cmdprefix + cmd, None)

        if cmdfunc is None:
            print("Unknown command '%s'.  Try one of: %s." % (cmd, commands))
            return

        debug(lambda : "calling %s with args %s and kwargs %s" % (cmdfunc, cmdargs, kwargs))

        try:
            cmdfunc(cmdargs, **kwargs)
        except UsageError:
            print(cmdfunc.__doc__)
            sys.exit(1)

    def cmd_help(self, args, **kwargs):
        """help [cmd] - show either all the help or that of the specified command"""

        def _help_for(cmd):
            doc = getattr(self.cmdfile, self.cmdprefix + cmd).__doc__
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

    def cmd_cmdpy_debug(self, args, **kwargs):
        global debug
        debug = debug_real
        self.dispatch(args, **kwargs)


if __name__=='__main__':
    args = sys.argv
    if len(args) < 1:
        print("Usage:\ncmdpy <cmdfile>      - list all the commands in cmdfile")
        sys.exit(1)
    cmdfilename = args[1]
    cmdfileargs = args[2:]
    cmdfile = cmdfile_client(cmdfilename)
    cmdfile.execute(cmdfileargs)

