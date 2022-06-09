from datetime import date,datetime

hora_atual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
hora_atual = datetime.strptime(hora_atual,"%d-%m-%Y %H:%M:%S")

criacao = '2022-05-20 16:04:14'
print(criacao)
criacao = datetime.strptime(criacao, '%Y-%m-%d %H:%M:%S')

print(criacao.timestamp() )


print(type(hora_atual))