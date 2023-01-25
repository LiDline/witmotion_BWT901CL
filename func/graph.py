from func.create_line import create_line
from datetime import date

def graph(fig):
    # Создадим линии для каждого графика
    create_line(fig, 1) 
    create_line(fig, 2, showlegend = False) 
    create_line(fig, 3, showlegend = False)

    # Оформление

    fig.update_layout(autosize=False, height=500, width=800,     # Размер окна в пикселях
        margin=dict(l=70, r=50,b=50,t=70,pad=0
            )
        )

    # Update xaxis properties
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_xaxes(visible=False, row=2, col=1)
    fig.update_xaxes(visible=False, row=3, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="a, м/с2", row=1, col=1)
    fig.update_yaxes(title_text="w, °/с", row=2, col=1)
    fig.update_yaxes(title_text="A, °", row=3, col=1)


    fig.update_layout(           #Позиционирование заголовка
               title={
                    'text': f"Получаемые характеристики датчика BWT901CL; дата: {date.today()}",
                    'y':0.97, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})