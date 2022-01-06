import os
import shutil
import sys


def build(source_path, build_path, install_path, targets):
    def _build():
        print(sys.version)
        print("\n[Building '%s'...]" % os.environ['REZ_BUILD_PROJECT_NAME'])
        src = os.path.join(source_path, 'src')
        dest = os.path.join(build_path, 'src')

        if os.path.exists(dest):
            print('\tDelete "%s"' % dest)
            shutil.rmtree(dest)

        print('\tCopy "%s" -> "%s"' % (src, dest))
        shutil.copytree(src, dest)#, dirs_exist_ok=True)
        print("[Build complete]")


    def _install():
        print("\n[Installing '%s'...]" % os.environ['REZ_BUILD_PROJECT_NAME'])
        src = os.path.join(build_path, 'src')

        if os.path.exists(install_path):
            shutil.rmtree(install_path)

        print('\tCopy "%s" -> "%s"' % (src, install_path))
        shutil.copytree(src, install_path)#, dirs_exist_ok=True)
        print('\tDelete "%s"' % build_path)
        shutil.rmtree(os.path.dirname(build_path), ignore_errors=True)
        print("[Install complete]")


    _build()

    if 'install' in (targets or []):
        _install()


if __name__ == '__main__':
    build(
        source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
        build_path=os.environ['REZ_BUILD_PATH'],
        install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
        targets=sys.argv[1:]
    )
