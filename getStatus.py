#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from decimal import *
from sisop import *
from config import *
from sisop.varios import *
from varios import *
from getVarios import *
from getJson import *

getcontext().prec = 30

def getStatus(s):
	banner()
	tipoCiudad = [bcolors.ENDC, bcolors.HEADER, bcolors.STONE, bcolors.BLUE, bcolors.WARNING]
	html = s.get()
	ids = re.findall(r'city_(\d+)', html)
	ids = set(ids)
	ids = sorted(ids)
	print('Barcos {:d}/{:d}'.format(getBarcosDisponibles(s), getBarcosTotales(s)))
	for unId in ids:
		html = s.get(urlCiudad + unId)
		ciudad = getCiudad(html)
		(wood, good, typeGood) = getProduccion(s, unId)
		print('\033[1m' + tipoCiudad[int(typeGood)] + ciudad['cityName'] + tipoCiudad[0])
		max = getRescursosDisponibles(html)
		capacidadDeAlmacenamiento = getCapacidadDeAlmacenamiento(html)
		crecursos = []
		for i in range(0,5):
			if max[i] == capacidadDeAlmacenamiento:
				crecursos.append(bcolors.RED)
			else:
				crecursos.append(bcolors.ENDC)
		print('Almacenamiento:')
		print(addPuntos(capacidadDeAlmacenamiento))
		print('Recursos:')
		print('Madera {1}{2}{0} Vino {3}{4}{0} Marmol {5}{6}{0} Cristal {7}{8}{0} Azufre {9}{10}{0}'.format(bcolors.ENDC, crecursos[0], addPuntos(max[0]), crecursos[1], addPuntos(max[1]), crecursos[2], addPuntos(max[2]), crecursos[3], addPuntos(max[3]), crecursos[4], addPuntos(max[4])))
		consumoXhr = getConsumoDeVino(html)
		tipo = tipoDeBien[typeGood]
		print('Producción:')
		print('Madera:{} {}:{}'.format(addPuntos(wood*3600), tipo, addPuntos(good*3600)))
		if consumoXhr == 0:
			print('{}{}No se consume vino!{}'.format(bcolors.RED, bcolors.BOLD, bcolors.ENDC))
		elif typeGood == 1 and (good*3600) > consumoXhr:
			print('Hay vino para:\n∞')
		else:
			consumoXseg = Decimal(consumoXhr) / Decimal(3600)
			segsRestantes = Decimal(int(max[1])) / Decimal(consumoXseg)
			(dias, horas, minutos) = diasHorasMinutos(segsRestantes)
			texto = ''
			if dias > 0:
				texto = str(dias) + 'D '
			if horas > 0:
				texto = texto + str(horas) + 'H '
			if minutos > 0 and dias == 0:
				texto = texto + str(minutos) + 'M '
			print('Hay vino para:\n{}'.format(texto))
		for edificio in ciudad['position']:
			if edificio['name'] == 'empty':
				continue
			if edificio['isMaxLevel'] is True:
				color = bcolors.BLACK
			elif edificio['canUpgrade'] is True:
				color = bcolors.GREEN
			else:
				color = bcolors.RED
			level = edificio['level']
			if int(level) < 10:
				level = ' ' + level
			if edificio['isBusy'] is True:
				level = level + '+'
			print('lv:{}\t{}{}{}'.format(level, color, edificio['name'], bcolors.ENDC))
		enter()
		print('')