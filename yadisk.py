import subprocess


def connect_disk(username, disk_code):
    result = subprocess.run(f"powershell net use * https://webdav.yandex.ru /user:{username} {disk_code}", capture_output=True, text=True)
    out = result.stdout.encode('cp1251').decode('cp866')
    
    if not result.stderr:
        return (0, out.split()[1])
    else:
        return (1, result.stderr.encode('cp1251').decode('cp866'))
    