# UDVPython

# Capture
Скрипт для захвата пакетов через Tcpdump <br/>
Атрибуты для запуска указываются внутри capture.py

запуск через консоль: python3 capture.py

# Splitter
Скрипт для разделения PCAP файла на меньшие файлы <br/>
Способ запуска сплиттера через консоль: python3 pcapsplitter.py input.pcap output --mode size --value 10

Где "output" директория записи <br/>

--mode принимает <br/>size<br/> time<br/> packets<br/>

соответственно --value принимает:<br/>


Размер выходящего файла в MB<br/>

Промежуток времени в секундах<br/>

Количество пакетов<br/>


