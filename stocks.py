
# %%
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def moneyprinter(stock):
     current_date = datetime.today().strftime('%Y-%m-%d')
     past_year = datetime.today() - timedelta(days=365)
     past_week = datetime.today() - timedelta(days=7)
     for i in stock:
          stick = yf.Ticker(i)
          print(i, "\n"*2, stick.major_holders, "\n"*2)
          holders(i)
          printgraph(i, past_year.strftime('%Y-%m-%d'), current_date)
          printgraph(i, past_week.strftime('%Y-%m-%d'), current_date)

def holders(stk): 
     stack = yf.Ticker(stk)
     largestshareholder = "Largest Shareholders for " + stk
     fig = px.pie(stack.institutional_holders, values='Shares', names='Holder', hole=.3)
     fig.update_layout(title_text=largestshareholder, annotations=[dict(text=stk, x=0.5, y=0.5, font_size=20, showarrow=False)])
     fig.show()


def printgraph(stock, startdate, enddate):
     hist_df = yf.download(stock, start = startdate, end = enddate).reset_index()
     hist_df['Date'] = pd.to_datetime(hist_df['Date'])
     hist_df = hist_df.sort_values('Date', ascending=True)
     plotly_data = []
     layout = []
     plotly_data.append(go.Candlestick(x=hist_df['Date'], 
                                        open=hist_df['Open'],
                                        high=hist_df['High'], 
                                        low=hist_df['Low'], 
                                        close=hist_df['Close'], 
                                        increasing_line_color= 'lime', 
                                        decreasing_line_color= 'red',
                                        name=stock))
     layout=go.Layout(title= stock, 
                    xaxis=dict(title='Date', 
                    rangeslider=dict(visible=False)), 
                    yaxis=dict(title='Price', showgrid=True, color='lime', gridwidth=1, gridcolor='black'), 
                    plot_bgcolor='slategrey', paper_bgcolor='slategrey',)
     fig = go.Figure(data=plotly_data, layout=layout)
     fig.show()


stonks = ["ASRT", "DARE", "DNN"] #Insert stock tickers into array

moneyprinter(stonks)


# %%



