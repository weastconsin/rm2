#
# Requirement Management Toolset
#
#  This is the main function - it is called from the 'rmtoo'
#  executable directly. 
#  It is stored here (in a seperate file) for (blackbox) testing
#  proposes. 
#
# (c) 2010 by flonatel
#
# For licencing details see COPYING
#
import sys
import git
from optparse import OptionParser
from rmtoo.lib.RequirementSet import RequirementSet
from rmtoo.lib.ReqsContinuum import ReqsContinuum
from rmtoo.lib.Modules import Modules
from rmtoo.lib.RMTException import RMTException
from rmtoo.lib.TopicHandler import TopicHandler
from rmtoo.lib.OutputHandler import OutputHandler

def parse_cmd_line_opts(args):
    parser = OptionParser()
    parser.add_option("-f", "--file-config", dest="config_file",
                  help="Config file")
    parser.add_option("-m", "--modules-directory", dest="modules_directory",
                  help="Directory with modules")
    parser.add_option("-c", "--create-makefile-dependencies",
                      dest="create_makefile_dependencies",
                      help="Create makefile dependencies")

    (options, args) = parser.parse_args(args=args)

    if options.modules_directory==None:
        # If there is no modules directory given, use the pycentral one.
        options.modules_directory = "/usr/share/pyshared"

    if options.config_file==None:
        print("+++ ERROR: no config_file option is specified")
        sys.exit(1)

    if len(args)>0:
        print("+++ ERROR: too many args")
        sys.exit(1)

    return options

def execute_cmds(opts, config, mods):
    # Checks are allways done - to be sure that e.g. the dependencies
    # are correct.
    try:
        rc = ReqsContinuum(mods, opts, config)
        reqs = rc.continnum_latest()
    except git.errors.GitCommandError, gce:
        print("+++ ERROR: Problem accessing git tree: '%s'" % gce)
        print("    Is the given version correct?");
        return

    # Setup the OutputHandler
    # Note: this can be more than one!
    # For the topic based output also all the Topics are needed -
    # before the OutputHandler itself - because different output
    # handler may reference the same Topic.
    topics = TopicHandler(config)
    topics.depict(reqs)
    ohandler = OutputHandler(config, topics)

    # When only the dependencies are needed, output them to the given
    # file. 
    if opts.create_makefile_dependencies!=None:
        ofile = file(opts.create_makefile_dependencies, "w")
        # Write out the REQS=
        rc.cmad_write_reqs_list(ofile)
        # Write out the rest
        ohandler.create_makefile_dependencies(ofile, rc)
        ofile.close()
        return

    # Output everything
    ohandler.output(rc)

def load_config(opts):
    # Load config file
    # ('execfile' does not work here.)
    f = file(opts.config_file, "r")
    conf_file = f.read()
    exec(conf_file)
    config = Config()
    f.close()
    return config

def main_impl(args):
    opts = parse_cmd_line_opts(args)
    config = load_config(opts)
    mods = Modules(opts.modules_directory, opts, config)
    execute_cmds(opts, config, mods)

def main(args):
    try:
        main_impl(args)
    except RMTException, rmte:
        print("+++ ERROR: Exception occured: %s" % rmte)
        sys.exit(1)

