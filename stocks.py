# %%
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Insert stock tickers into array as strings
stonks = ["ASRT", "DARE"] 


# prints graphs for each ticker in stonks[]
def moneyprinter(stock):
     current_date = datetime.today().strftime('%Y-%m-%d')
     past_year = datetime.today() - timedelta(days=365)
     past_3month = datetime.today() - timedelta(days=91)
     for i in stock:
          stick = yf.Ticker(i)
          print(i, "\n"*2, stick.major_holders, "\n"*2)
          holders(i)
          printgraph(i, past_year.strftime('%Y-%m-%d'), current_date, "1 year")
          printgraph(i, past_3month.strftime('%Y-%m-%d'), current_date, "3 months")

# pie chart of largest institutional holders
def holders(stk): 
     stack = yf.Ticker(stk)
     largestshareholder = "Largest Shareholders for " + stk
     fig = px.pie(stack.institutional_holders, values='Shares', names='Holder', hole=.3)
     fig.update_layout(title_text=largestshareholder, annotations=[dict(text=stk, x=0.5, y=0.5, font_size=20, showarrow=False)])
     fig.show()

# candlestick chart with 5 and 20 day moving average trendlines, with volume bar chart on bottom
def printgraph(stock, startdate, enddate, period):
     
     # gets the data, converts date to correct format, and sorts by date
     hist_df = yf.download(stock, start = startdate, end = enddate).reset_index()
     hist_df['Date'] = pd.to_datetime(hist_df['Date'])
     hist_df = hist_df.sort_values('Date', ascending=True)
     
     # creates 5 and 20 day moving average columns
     hist_df['MA5'] = hist_df['Close'].rolling(5).mean()
     hist_df['MA20'] = hist_df['Close'].rolling(20).mean()

     # splits into two subplots with shared x axis
     fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.1, subplot_titles=(period, 'Volume'), 
               row_width=[0.2, 0.7])
     
     # candlestick chart
     fig.add_trace(go.Candlestick(x=hist_df['Date'], 
                                        open=hist_df['Open'],
                                        high=hist_df['High'], 
                                        low=hist_df['Low'], 
                                        close=hist_df['Close'], 
                                        increasing_line_color='green', 
                                        decreasing_line_color='red',
                                        name=stock), 
                                        row=1, col=1)
     
     # 5 day moving average line
     fig.add_trace(go.Scatter(x=hist_df['Date'], 
                                   y=hist_df['MA5'], 
                                   line=dict(color='blue', width=1)), 
                                   row=1, col=1)
     
     # 20 day moving average line
     fig.add_trace(go.Scatter(x=hist_df['Date'], 
                                   y=hist_df['MA20'], 
                                   line=dict(color='orange', width=1)), 
                                   row=1, col=1)
                    
     # volume bar chart
     fig.add_trace(go.Bar(x=hist_df['Date'], 
                              y=hist_df['Volume'], 
                              showlegend=False), 
                              row=2, col=1)
     
     # change layout
     fig.update_layout(title= stock, 
                         xaxis=dict(rangeslider=dict(visible=False)), 
                         yaxis_tickprefix = '$',
                         yaxis=dict(title='Price', showgrid=True, color='black', gridwidth=1, gridcolor='black'), 
                         plot_bgcolor='white', 
                         paper_bgcolor='white')
     fig.show()

moneyprinter(stonks)
