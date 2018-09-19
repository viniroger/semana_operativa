#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import timedelta, date
import datetime

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days+1)):
		yield start_date + timedelta(n)

# Inicializa revisões
rev_ons = 0 # Semana que antecede primeiro sábado do mês sempre é REV0/PMO
rev_prev = 1 # Terminação do arquivo a ser previsto

# Inicializa datas
year_ini = 2018
year_end = year_ini + 10
month = 1
start_date = date(year_ini, 1, 1)
end_date = date(year_end, 12, 31)

# Abrir arquivo para gravar linha por linha
with open('datas_rev.csv', 'wb') as f:
	f.write('data,rev_ons,rev_prev,h\n')
	for single_date in daterange(start_date, end_date):
		date_str = single_date.strftime("%Y-%m-%d")
		# 0-SEG 1-TER 2-QUA 3-QUI 4-SEX 5-SAB 6-DOM
		day_week = single_date.weekday()
		# Se for sexta-feira (1 dia após a rodada do ONS, que sai QUI~19h)
		if day_week == 4:
			# Se próximo sábado for do mesmo mês, soma rev
			next_sat = single_date + timedelta(7)
			month_actual = next_sat.month
			rev_ons = rev_ons + 1
			rev_prev = rev_prev + 1
			# Se próximo-próximo sábado for do mês seguinte, rev_prev = 0
			next_next_sat = single_date + timedelta(14)
			month_next = next_next_sat.month
			if month_next != month:
				rev_prev = 0
			# Se próximo sábado for do mês seguinte, rev_ons = 0
			if month_actual != month:
				rev_ons = 0
				rev_prev = 1
				# Atualiza mês
				month = month_actual
		# Calcula número de semanas a serem previstas
		h = 6 - rev_prev
		#print(date_str,rev_ons,rev_prev,h)
		f.write("%s,%d,%d,%d\n" %(date_str,rev_ons,rev_prev,h))
