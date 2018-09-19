#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import timedelta, date
import datetime
from dateutil import relativedelta
import calendar
# Importar calendário de São Paulo porque mostra Carnaval
#from workalendar.america import Brazil
from workalendar.america import BrazilSaoPauloCity

# Inicializar revisões
rev_ons = 0 # 1a semana operativa do mês é REV0/PMO
rev_prev = 1 # Terminação do arquivo a ser previsto
h = 6 # Número de colunas a serem previstas

# Inicializar datas
year_ini = 2018
year_end = year_ini + 10
month = 1
start_date = date(year_ini, 1, 1)
end_date = date(year_end, 12, 31)

# Definir função para escrever datas em intervalo
def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days+1)):
		yield start_date + timedelta(n)

# Montar lista de todos os feriados do periodo
cal = BrazilSaoPauloCity()
feriados = list()
for year in range(year_ini,year_end+1):
	lst = cal.holidays(year)
	for x in lst:
		# Cortar feriados especificos da cidade/estado
		if (x[0] != datetime.date(year, 1, 25) and x[0] != datetime.date(year, 7, 9)):
			feriados.append(x[0])

# Montar objeto de calendário geral
cal = calendar.Calendar()
# Redefinir início das semanas como sendo sábado
cal.setfirstweekday(calendar.SATURDAY)

# Abrir arquivo para gravar linha por linha
with open('datas_rev.csv', 'wb') as f:
	f.write('data,rev_ons,rev_prev,h,mes_prev,sem_op\n')
	for single_date in daterange(start_date, end_date):
		print(single_date)
		date_str = single_date.strftime("%Y-%m-%d")
		mes_prev = single_date.strftime("%Y-%m-01")
		# 0-SEG 1-TER 2-QUA 3-QUI 4-SEX 5-SAB 6-DOM
		day_week = single_date.weekday()
		
		# Criar lista com semanas operativas e os dias do mês, incluindo os dias dos meses anterior/posterior que completam as semanas operativas
		ano = int(single_date.strftime("%Y"))
		mes = int(single_date.strftime("%m"))
		dias_sem_op = cal.monthdatescalendar(ano, mes)
		# 1o sábado da 1a semana operacional do mês
		primeiro_sabado = str(dias_sem_op[0][0])
		
		# Quando deve gerar previsao de REV0, pegar antepenúltima quinta e sexta do "mes operativo" - exceto se último dia do mês for sexta-feira do próprio mês
		# (na semana seguinte, os arquivos REV0 do ONS já estão disponíveis)
		if (dias_sem_op[-1][-1].weekday() == 4 and dias_sem_op[-1][-1].month == single_date.month):
			quinta_virada = dias_sem_op[-2][-2]
			sexta_virada = dias_sem_op[-2][-1]
		else:
			quinta_virada = dias_sem_op[-3][-2]
			sexta_virada = dias_sem_op[-3][-1]
		
		# Se for QUI e tiver feriado quinta ou sexta, ONS ja liberou arquivos QUA~20h
		# Se for SEX, ONS ja liberou arquivos QUI~20h se ja nao tiver liberado na quarta
		new_files = 'FALSE'
		if day_week == 3:
			single_date_next = single_date + timedelta(days=1)
			if single_date in feriados or single_date_next in feriados:
				new_files = 'TRUE'
		if day_week == 4:
			single_date_last = single_date - timedelta(days=1)
			if single_date in feriados or single_date_last in feriados:
				new_files = 'FALSE'
			else:
				new_files = 'TRUE'
		# Se tiver arquivos novos, deve mudar revisao
		if new_files == 'TRUE':
			# Verificar se deve gerar REV0 (se for dia de virada) ou só avançar comparando data de 1a semana operativa
			if (single_date == quinta_virada or single_date == sexta_virada):
				# Gerar REV0
				rev_prev = 0
				h = 6
			else:
				# Gerar REV1/2/3/4
				rev_prev = rev_prev + 1
				# Atualizar número de colunas previstas (deve copiar colunas que são completamente formadas de dias passados)
				if rev_prev > 1:
					h = h - 1
			# Atualiza terminação do arquivo do ONS
			if rev_prev == 1:
				rev_ons = 0
			else:
				rev_ons = rev_ons + 1
		
		# Se for fim de mês e tiver que gerar previsão a partir do próximo mês
		if (rev_prev <= 2):
			day_actual = single_date.day
			if day_actual >= 15:
				nextmonth = single_date + relativedelta.relativedelta(months=1)
				mes_prev = nextmonth.strftime("%Y-%m-01")
				# Atualizar primeiro sábado para o próximo "mês operativo"
				ano = int(nextmonth.strftime("%Y"))
				mes = int(nextmonth.strftime("%m"))
				dias_sem_op = cal.monthdatescalendar(ano, mes)
				# 1o sábado da 1a semana operacional do mês
				primeiro_sabado = str(dias_sem_op[0][0])

		#print(date_str,rev_ons,rev_prev,h,mes_prev,primeiro_sabado)
		#exit()
		f.write("%s,%d,%d,%d,%s,%s\n" %(date_str,rev_ons,rev_prev,h,mes_prev,primeiro_sabado))
