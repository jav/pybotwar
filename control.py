# Copyright 2009-2012 Lee Harr
#
# This file is part of pybotwar.
#     http://pybotwar.googlecode.com/
#
# Pybotwar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pybotwar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pybotwar.  If not, see <http://www.gnu.org/licenses/>.


import os
from threading import Thread
from time import sleep

import util
from util import defaultNonedict

import conf

util.setup_conf()


_overtime_count = 0

def loop(r, i):
    data = i.split('|')
    sensors = defaultNonedict()
    for d in data:
        k, v = d.split(':')

        if ';' in v:
            # Some sensors send multiple values, separated by semicolon
            v = v.split(';')
            vconv = []
            for vv in v:
                try:
                    vvconv = int(vv)
                except:
                    vvconv = vv

                vconv.append(vvconv)

        else:
            try:
                vconv = int(v)
            except:
                vconv = v

        sensors[k] = vconv

    timeout = conf.tick_timeout

    user_thread = Thread(target=get_response, args=(r, sensors))
    response = None
    user_thread.start()

    user_thread.join(timeout)
    if user_thread.isAlive():
        global _overtime_count
        _overtime_count += 1
        response = 'TIMEOUT'
        if _overtime_count > 10:
            os.kill(os.getpid(), 9)
    else:
        _overtime_count = 0

    rresponse = r.response

    if rresponse == 'LOG':
        start_logging(r)
    elif rresponse == 'NOLOG':
        stop_logging(r)

    return response or rresponse

def get_response(r, sensors):
    try:
        r.sensors = sensors
        r.respond()
    except Exception, e:
        r.err()
        import traceback
        tb = traceback.format_exc()
        r.log(tb)

def communicate(r):
    while True:
        line = sys.stdin.readline().strip()
        if line == 'FINISH':
            break
        elif line == 'DEBUG':
            start_logging(r)
            continue
        elif line == 'NODEBUG':
            stop_logging(r)
            continue

        o = loop(r, line)
        if o is not None:
            oline = '%s\n' % (str(o))
            try:
                sys.stdout.write(oline)
                sys.stdout.flush()
            except IOError:
                break
        else:
            oline = 'END\n'
            try:
                sys.stdout.write(oline)
                sys.stdout.flush()
            except IOError:
                pass
            break


def robot_logfile(robotname):
    logfilename = '%s.log' % robotname
    logdir = os.path.join(conf.base_dir, conf.logdir)
    try:
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        logfilepath = os.path.join(logdir, logfilename)
        logfile = open(logfilepath, 'a')
    except (IOError, OSError):
        logfile = None
    logfile.write('Begin logging for %s.\n' % robotname)
    logfile.flush()
    return logfile

def start_logging(robot):
    logfile = robot_logfile(robot.name)
    robot.logfile = logfile

def stop_logging(robot):
    robot.logfile = None


def build_robot(modname, rfile, robotname, testmode, rbox):

    if testmode:
        logfile = robot_logfile(robotname)
    else:
        logfile = None

    try:
        import imp
        mod = imp.load_source(modname, rfile)
        r = mod.TheRobot(robotname)

        r.logfile = logfile

        r.initialize()

    except:
        rbox.append(None)

        import traceback
        tb = traceback.format_exc()
        if logfile is not None:
            logfile.write(tb)
            logfile.write('\n')
            logfile.flush()
        else:
            import sys
            sys.stderr.write(tb)
            sys.stderr.write('\n')
            sys.stderr.flush()

    else:
        rbox.append(r)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        raise SystemExit
    else:
        modname = sys.argv[1]
        rfile = sys.argv[2]
        robotname = sys.argv[3]
        testmode = bool(int(sys.argv[4]))

        timeout = conf.init_timeout

        rbox = [] # Store the robot here to pass it back from the thread
        user_thread = Thread(target=build_robot, args=(modname, rfile, robotname, testmode, rbox))
        user_thread.start()

        user_thread.join(timeout)
        if user_thread.isAlive():
            rbox = [None]

        robot = rbox[0]

        if robot is None:
            # robot failed to load properly
            oline = 'ERROR\n'
            sys.stdout.write(oline)
            sys.stdout.flush()

        else:
            oline = 'START\n'
            sys.stdout.write(oline)
            sys.stdout.flush()
            try:
                communicate(robot)
            except KeyboardInterrupt:
                pass
