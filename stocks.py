import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def moneyprinter(stock):
     current_date = datetime.today().strftime('%Y-%m-%d')
     past_year = datetime.today() - timedelta(days=365)
     # prints graphs for every stock ticker in stonks[]
     for i in stock:
          stick = yf.Ticker(i)
          print(i, "\n"*2, stick.major_holders, "\n"*2)
          holders(i)
          printgraph(i, past_year.strftime('%Y-%m-%d'), current_date)

def holders(stk): 
     stack = yf.Ticker(stk)
     largestshareholder = "Largest Shareholders for " + stk
     # pie chart of institutional holders
     fig = px.pie(stack.institutional_holders, values='Shares', names='Holder', hole=.3)
     fig.update_layout(title_text=largestshareholder, 
                       annotations=[dict(text=stk, x=0.5, y=0.5, 
                       font_size=20, showarrow=False)])
     fig.show()


def printgraph(stock, startdate, enddate):
     # reset_index() is needed to use date column
     hist_df = yf.download(stock, start = startdate, end = enddate).reset_index()
     # convert date to usable format
     hist_df['Date'] = pd.to_datetime(hist_df['Date'])
     hist_df = hist_df.sort_values('Date', ascending=True)
     fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.03, subplot_titles=(stock, 'Volume'), 
               row_width=[0.2, 0.7])
     fig.add_trace(go.Candlestick(x=hist_df['Date'], 
                                        open=hist_df['Open'],
                                        high=hist_df['High'], 
                                        low=hist_df['Low'], 
                                        close=hist_df['Close'], 
                                        increasing_line_color= 'lime', 
                                        decreasing_line_color= 'red',
                                        name=stock), row=1, col=1)
     fig.add_trace(go.Bar(x=hist_df['Date'], y=hist_df['Volume'], showlegend=False), row=2, col=1)
     layout=go.Layout(title= stock, 
                    xaxis=dict(title='Date', 
                    rangeslider=dict(visible=False)), 
                    yaxis=dict(title='Price', showgrid=True, color='lime', gridwidth=1, gridcolor='black'), 
                    plot_bgcolor='slategrey', paper_bgcolor='slategrey')
     fig.update(layout_xaxis_rangeslider_visible=False)
     fig.show()

# Insert stock tickers as string into array
stonks = [] 

moneyprinter(stonks)
