# Semanas operativas

O script em python gera um calendário com os números das revisões das semanas operativas do ONS (Operador Nacional do Sistema). Toda semana operativa começa no sábado. O mês civil deve estar todo contido nas semanas selecionadas, começando em um sábado e terminando em uma sexta. Como todo arquivo gerado pelo ONS sai às quintas-feiras à noite, considerou-se sexta-feira como o início da disponibilidade do arquivo gerado - a exceção é quando existe um feriado de quinta ou sexta, então o arquivo é liberado pelo ONS às quartas-feiras à noite.

O arquivo gerado contém 6 colunas:

- data: dia, no formato YYYY-MM-DD
- rev_ons: número da revisão (REV'rev_ons') do arquivo mais recente disponível
- rev_prev: número da revisão do arquivo a ser gerado na semana seguinte
- h: número de colunas previstas dentro do arquivo da semana seguinte (ou seja, não contém dias observados na semana representada na coluna)
- mes_prev: mês civil que contém a maioria das semanas/dias
- sem_op: primeiro sábado da primeira semana operativa do mes_prev (início do "mês operativo", ou seja, indica o início da primeira coluna do arquivo PREVS)

Como o arquivo é mensal e formado de 6 colunas, cada revisão realizada diminui o número de semanas previstas, que são substituídas pelas semanas revisadas (valores observados de vazão natural afluente, em m³/s, que podem ser alterados entre uma rodada e outra). Mais informações em https://www.monolitonimbus.com.br/definicoes-em-hidroeletricidade/

Obs.: na metodologia anterior (arquivos "v1"), a semana que antecede o primeiro sábado do mês (ou do ano) é a primeira semana operativa desse mês (ou desse ano), que valia para a maioria dos meses com exceção dos meses que iniciam em um sábado e/ou último dia cai de sexta-feira.

O novo script usa o módulo workalendar - https://peopledoc.github.io/workalendar/
