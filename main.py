import os
import shutil
import proxy
import subprocess

if __name__ == '__main__':

    # if os.path.exists('repos/0x00-pl'):
    #     shutil.rmtree('repos/0x00-pl')
    subprocess.Popen(['python3', '-m', 'http.server', '8080'], cwd='repos')

    proxy.main([
    '--hostname', '::1',
    '--port', '8899',
    '--plugins', 'redirect_to_custom_server.RedirectToCustomServerPlugin2'
  ])
