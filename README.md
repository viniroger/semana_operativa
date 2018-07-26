# Semanas operativas

O script em python gera um calendário com os números das revisões das semanas operativas do ONS (Operador Nacional do Sistema). Toda semana operativa começa no sábado. A semana que antecede o primeiro sábado do mês (ou do ano) é a primeira semana operativa desse mês (ou desse ano). Como todo arquivo gerado pelo ONS sai às quintas-feiras à noite, considerou-se sexta-feira como o início da disponibilidade do arquivo gerado.

O arquivo gerado contém 4 colunas:

- data: dia, no formato YYYY-MM-DD
- rev_ons: número da revisão (REV'rev_ons') do arquivo mais recente disponível
- rev_prev: número da revisão do arquivo a ser gerado na semana seguinte
- h: número de colunas previstas dentro do arquivo da semana seguinte

Como o arquivo é mensal e formado de 6 colunas, cada revisão realizada diminui o número de semanas previstas, que são substituídas pelas semanas revisadas (valores observados de vazão natural afluente, em m³/s, que podem ser alterados entre uma rodada e outra). Mais informações em https://www.monolitonimbus.com.br/definicoes-em-hidroeletricidade/
