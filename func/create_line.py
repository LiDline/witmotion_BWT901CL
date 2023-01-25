# Создадим шаблон для каждой линии
def create_line(fig, row, col=1, showlegend = True):
    names = ['OX', 'OY', 'OZ']
    color = ['red', 'blue', 'green']
    # Сразу вызовем по 3 линии на каждый график
    for i in range(3): 
        fig.add_scatter(line=dict(color=color[i]), mode = 'lines', legendgroup = f'group{i}',
        showlegend=showlegend, name = names[i], row=row, col=col)