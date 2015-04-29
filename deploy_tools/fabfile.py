from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/nharsch/test_driven_python"


def deploy():
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host)
    source_folder = "{}/source".format(site_folder)
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenc(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {}/{}'.format(site_folder, subfolder)) # only create directories if they don't exist


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):  # if git repo exists on server
        run('cd {} && git fetch'.format(source_folder,))  # fetch new files
    else:
        run('git clone {}'.format(REPO_URL)) # if no repo, clone repo from github
    current_commit = local("git log -n 1 --format=%H", capture=True)  # get hash of current commit in local tree
    run('cd {} && git reset --hard {}'.format(source_folder, current_commit))  # reset repo to last commit, wiping and un pushed changes


def _update_settings(source_folder, site_name):
    settings_path = source_folder + "/superlists/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")  # make sure DEBUG is False
    sed(settings_path,
        'ALLOWED_HOSTS =.+$'
        'ALLOWED_HOSTS = [{}]'.format(site_name,)  # make sure site_name is in allowed hosts
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = {}".format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv_(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):  # create env if none exists
        run('virtualenv --python=python3 {}'.format(virtualenv_folder,))
    run('{}/bin/pip install -r {}/requirements.txt'.format(virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    run('cd {} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(
        source_folder
    ))

