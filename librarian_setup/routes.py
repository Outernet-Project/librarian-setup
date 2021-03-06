"""
setup.py: Basic setup wizard steps

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, redirect

from librarian_core.contrib.templates.renderer import view

from .tools import has_tuner


def iter_lines(lines):
    while lines:
        yield lines.pop()


@view('diag/diag')
def diag():
    if request.app.supervisor.exts.is_completed:
        redirect('/')

    logpath = request.app.config['logging.syslog']
    with open(logpath, 'rt') as log:
        logs = iter_lines(list(log)[-100:])

    return dict(logs=logs, has_tuner=has_tuner())


def enter_wizard():
    return request.app.supervisor.exts.setup_wizard()


def exit_wizard():
    next_path = request.params.get('next', '/')
    request.app.supervisor.exts.setup_wizard.exit()
    redirect(next_path)


def routes(app):
    return (
        ('setup:main', enter_wizard, ['GET', 'POST'], '/setup/', {}),
        ('setup:exit', exit_wizard, ['GET'], '/setup/exit/', {}),
        ('setup:diag', diag, 'GET', '/diag/', {}),
    )
