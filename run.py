import os
os.system('docker login -u "dashy2004" -p "12345678qwerty123" repo.treescale.com')
os.system('docker build -t games-day .')
os.system('docker tag games-day repo.treescale.com/dashy2004/games-day:latest')
os.system('docker push repo.treescale.com/dashy2004/games-day:latest')
print('The build passed yay!')