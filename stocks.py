import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def moneyprinter(stock):
     
     # get current day and change format     
     current_date = datetime.today().strftime('%Y-%m-%d') 
     past_year = datetime.today() - timedelta(days=365) 
     past_week = datetime.today() - timedelta(days=7)
     
     # prints graphs for each stock ticker in the stonks array
     for i in stock:
          stick = yf.Ticker(i)
          print(i, "\n"*2, stick.major_holders, "\n"*2)
          holders(i)
          printgraph(i, past_year.strftime('%Y-%m-%d'), current_date)
          printgraph(i, past_week.strftime('%Y-%m-%d'), current_date)

def holders(stk): 
     stack = yf.Ticker(stk)
     largestshareholder = "Largest Shareholders for " + stk
     # pie chart of institutional holders
     fig = px.pie(stack.institutional_holders, values='Shares', names='Holder', hole=.3)
     fig.update_layout(title_text=largestshareholder, annotations=[dict(text=stk, x=0.5, y=0.5, font_size=20, showarrow=False)])
     fig.show()


def printgraph(stock, startdate, enddate):
     
     # downloads historical data into dataframe - reset_index() needed to use date column for some reason
     hist_df = yf.download(stock, start = startdate, end = enddate).reset_index()
     # converts date to usable format
     hist_df['Date'] = pd.to_datetime(hist_df['Date'])
     # sorts by date
     hist_df = hist_df.sort_values('Date', ascending=True)
     plotly_data = []
     layout = []
     # creates candlestick chart
     plotly_data.append(go.Candlestick(x=hist_df['Date'], 
                                        open=hist_df['Open'],
                                        high=hist_df['High'], 
                                        low=hist_df['Low'], 
                                        close=hist_df['Close'], 
                                        increasing_line_color= 'lime', 
                                        decreasing_line_color= 'red',
                                        name=stock))
     # chart layout options
     layout=go.Layout(title= stock, 
                    xaxis=dict(title='Date', 
                    rangeslider=dict(visible=False)), 
                    yaxis=dict(title='Price', showgrid=True, color='lime', gridwidth=1, gridcolor='black'), 
                    plot_bgcolor='slategrey', paper_bgcolor='slategrey')
     # the chart
     fig = go.Figure(data=plotly_data, layout=layout)
     fig.show()

# insert stock tickers into array
stonks = ["ASRT", "DARE", "DNN"] 

moneyprinter(stonks)



