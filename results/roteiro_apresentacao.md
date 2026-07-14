# Roteiro do Vídeo Executivo (até 5 minutos)

Baseado nos 10 slides de `apresentacao_executiva.pptx`. Tempos são estimativas a
um ritmo de fala tranquilo (~150 palavras/minuto); leia em voz alta uma vez
antes de gravar para calibrar o seu próprio ritmo. Soma total estimada: **~4min20s**,
com folga para pausas naturais.

Linguagem intencionalmente não técnica, como pede o enunciado do desafio.

---

## Slide 1 - Abertura (10-15s)

> "Boa tarde. Meu nome é Robério e hoje vou apresentar um projeto que usa
> ciência de dados para prever a qualidade de vinhos a partir de medições
> feitas na própria produção, antes mesmo da avaliação sensorial final."

---

## Slide 2 - O desafio de avaliar qualidade hoje (30-35s)

> "Hoje, avaliar a qualidade de um vinho depende de especialistas que
> degustam cada lote: um processo demorado e que varia conforme a
> experiência de quem avalia. Mas as medições físico-químicas, como acidez,
> açúcar e teor alcoólico, já são coletadas rotineiramente durante a
> produção, e raramente usadas para prever a qualidade final.
>
> A pergunta que guiou o projeto foi simples: dá para usar esses números
> para estimar, com antecedência, se um vinho tem perfil de alta qualidade?"

---

## Slide 3 - Traduzindo a nota em decisão prática (25-30s)

> "Cada vinho da nossa base tem uma nota de zero a dez, dada por
> especialistas. Para transformar isso em uma decisão de negócio,
> simplificamos essa nota em duas categorias: vinho Premium, com nota igual
> ou maior que sete, cerca de um em cada cinco vinhos da base; e vinho
> Padrão, a maioria, com boa qualidade, mas não excepcional."

---

## Slide 4 - A base analisada (18-20s)

> "A base analisada tem quase seis mil e quinhentas amostras de vinho, entre
> tintos e brancos, com onze medições físico-químicas cada uma. Não há dados
> faltantes, mas encontramos dezoito por cento de linhas duplicadas, que
> removemos antes de avaliar os modelos, para garantir um resultado
> confiável."

---

## Slide 5 - Um desafio escondido nos dados (25-30s)

> "Aqui está um ponto crítico da análise: apenas um em cada cinco vinhos é
> Premium. Isso muda o que significa acertar. Um modelo preguiçoso, que
> sempre dissesse que nenhum vinho é Premium, pareceria certo em oito de
> cada dez casos, mas seria completamente inútil na prática. Por isso,
> avaliamos os modelos pela capacidade real de encontrar os vinhos Premium,
> não apenas pela taxa de acerto geral."

---

## Slide 6 - O que mais diferencia um vinho Premium (30-35s)

> "Identificamos quais características mais diferenciam um vinho Premium.
> A mais importante, de longe, é o teor alcoólico: vinhos com mais álcool
> tendem a vir de uvas mais maduras e fermentação mais completa. Em seguida
> está a densidade: quanto mais baixa, mais ela está associada a um maior
> teor alcoólico e à qualidade Premium. Depois vem a acidez volátil: quanto
> menor, melhor, porque sinaliza ausência de defeitos de fermentação. E, por
> último, os cloretos, ligados a características do solo e da água usada no
> cultivo."

---

## Slide 7 - O modelo preditivo construído (25-30s)

> "Testamos três abordagens estatísticas de previsão, comparando o
> desempenho de cada uma na tarefa mais difícil: reconhecer corretamente os
> vinhos Premium, sem errar demais. O modelo baseado em árvores de decisão
> teve o melhor equilíbrio e foi o escolhido; os outros dois, um modelo
> linear e um modelo de reforço por árvores, tiveram desempenho um pouco
> inferior nessa métrica."

---

## Slide 8 - Quão confiável é o modelo escolhido (25s)

> "Traduzindo os números técnicos em termos de confiança: de cada dez
> vinhos que o modelo aponta como Premium, cerca de cinco a seis realmente
> são. De cada dez vinhos que são realmente Premium, o modelo encontra sete.
> E, de forma geral, o modelo separa corretamente vinhos Premium dos demais
> em oitenta e sete por cento dos casos avaliados."

---

## Slide 9 - Recomendações para o processo produtivo (35-40s)

> "A partir dessa análise, chegamos a quatro recomendações práticas.
> Primeiro: usar o modelo como apoio à triagem, não como substituto do
> especialista - a avaliação sensorial continua sendo a decisão final.
> Segundo: monitorar o teor alcoólico de perto, a principal alavanca de
> qualidade identificada. Terceiro: tratar a acidez volátil como um alerta
> precoce de defeito de fermentação, reforçando o controle sanitário. E
> quarto: recalibrar a dosagem de conservantes com base na proporção do que
> fica ativo, não apenas no volume total aplicado."

---

## Slide 10 - Próximos passos e encerramento (18-20s)

> "Como próximos passos, propomos ampliar a base com novas safras, testar o
> modelo em um piloto real de produção e ajustar os critérios de decisão com
> o retorno direto dos enólogos. Todo o código, os notebooks e o
> detalhamento técnico completo estão disponíveis no repositório do
> projeto. Obrigado."

---

## Dicas de gravação

* Fale olhando para a câmera, não para o slide - isso segura a atenção de
  quem assiste.
* Faça uma pausa breve entre um slide e outro; ajuda no corte/edição se
  precisar aparar algum trecho depois.
* Se passar de 5 minutos no ensaio, os cortes mais seguros são o Slide 6
  (citar só os 2 principais fatores) e o Slide 9 (juntar as recomendações 3
  e 4 em uma frase só).
* Não é necessário decorar palavra por palavra - use este roteiro como guia
  e fale com suas próprias palavras, mantendo os números e a ordem dos
  pontos.
