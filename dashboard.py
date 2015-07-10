#dashboard.py
#
#dashboard the results of the smart maintenance demo
#by Joe Hahn, jhahn@infochimps.com, 9 July 2015 
#
#to execute:    /home/$USER/anaconda/bin/python dashboard.py
#

#get imports 
import numpy as np
import pandas as pd
import pickle
from bokeh.plotting import figure, show, output_file, ColumnDataSource, vplot
from bokeh.models import HoverTool, Callback, BoxSelectTool, Line
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.io import vform

#read output of smart_maint.py
print '...generating dashboard...'
fp = open('events.pkl', 'r')
[events, xy_train, one_motor, operating_earnings, maintenance_cost, repair_cost, 
    run_interval] = pickle.load(fp)
fp.close()

#calculate earnings, expenses, and revenue
events['earnings'] = 0.0
events.loc[events.state == 'operating', 'earnings'] = operating_earnings
events['expenses'] = 0.0
events.loc[events.state == 'maintenance', 'expenses'] = maintenance_cost
events.loc[events.state == 'repair', 'expenses'] = repair_cost
money = events.groupby('Time').sum()[['earnings', 'expenses']]
money['revenue'] = money.earnings - money.expenses
money['cumulative_earnings'] = money.earnings.cumsum()
money['cumulative_expenses'] = money.expenses.cumsum()
money['cumulative_revenue'] = money.revenue.cumsum()

#map the (P,T) decision surface
T_min = 50
T_max = 150
P_min = 0
P_max = 100
T_axis = np.arange(T_min, T_max, 0.5)
P_axis = np.arange(P_min, P_max, 0.5)
x, y = np.meshgrid(T_axis, P_axis)
ttf = np.zeros((len(P_axis), len(T_axis)))
for p_idx in np.arange(len(P_axis)):
	for t_idx in np.arange(len(T_axis)):
		one_motor.Temp = T_axis[t_idx]
		one_motor.Pressure = P_axis[p_idx]
		ttf[p_idx, t_idx] = one_motor.predicted_time_to_fail()

#plot decision surface
output_file('dashboard.html', title='Smart Maintenance Dashboard')
source = ColumnDataSource(
	data=dict(
		x = xy_train.Temp,
		y = xy_train.Pressure,
		ttf = xy_train.time_to_fail,
		size = 0.6*xy_train.time_to_fail,
	)
)    
dec_fig = figure(x_range=[T_min, T_max], y_range=[P_min, P_max], 
    title='SVM Decision Surface    (click-drag to zoom)',
	x_axis_label='Temperature', y_axis_label='Pressure', tools='box_zoom,reset,hover,crosshair', 
	width=600, plot_height=600)
dec_fig.title_text_font_size = '18pt'
dec_fig.xaxis.axis_label_text_font_size = '14pt'
dec_fig.yaxis.axis_label_text_font_size = '14pt'
dec_fig.image(image=[-ttf], x=[T_min], y=[P_min], dw=[T_max - T_min], dh=[P_max - P_min], 
	palette='RdYlGn8')
dec_fig.x('x', 'y', size='size', source=source, fill_alpha=0.5, fill_color='navy', 
	line_color='navy', line_width=1, line_alpha=0.5)
hover = dec_fig.select(dict(type=HoverTool))
hover.tooltips = [
	("Temperature", "@x"),
	("Pressure", "@y"),
	("measured lifetime", "@ttf"),
]

#plot earnings vs time
source = ColumnDataSource(
	data=dict(
		t = money.index,
		earnings = money.cumulative_earnings/1.e6,
		expenses = money.cumulative_expenses/1.e6,
		revenue  = money.cumulative_revenue/1.e6,
		zero = money.cumulative_revenue*0,
	)
)
earn_fig = figure(title='Cumulative Earnings & Expenses    (click-drag to zoom)', 
    x_axis_label='Time', y_axis_label='Earnings & Expenses    (M$)', 
    tools='box_zoom,reset,hover,crosshair', 
	width=1000, plot_height=300, x_range=[0, 1200], y_range=[0, 120])
earn_fig.title_text_font_size = '15pt'
earn_fig.xaxis.axis_label_text_font_size = '11pt'
earn_fig.yaxis.axis_label_text_font_size = '11pt'
earn_fig.line('t', 'earnings', color='blue', source=source, line_width=5, legend='earnings')
earn_fig.line('t', 'expenses', color='red', source=source, line_width=5, legend='expenses', 
    alpha=0.8)
earn_fig.legend.orientation = "bottom_right"
earn_fig.patch([0, 200, 200, 0], [0, 0, 120, 120], color='lightsalmon', alpha=0.35, 
	line_width=0)
earn_fig.patch([200, 400, 400, 200], [0, 0, 120, 120], color='gold', alpha=0.35, 
	line_width=0)
earn_fig.patch([400, 1200, 1200, 400], [0, 0, 120, 120], color='darkseagreen', 
	alpha=0.35, line_width=0) 
earn_fig.text([45], [101], ['run-to-fail'])
earn_fig.text([245], [101], ['scheduled'])
earn_fig.text([245], [90], ['maintenance'])
earn_fig.text([445], [101], ['predictive'])
earn_fig.text([445], [90], ['maintenance'])
hover = earn_fig.select(dict(type=HoverTool))
hover.tooltips = [
	("         Time", "@t"),
	(" earning (M$)", "@earnings"),
	("expenses (M$)", "@expenses"),
]

#plot revenue vs time
rev_fig = figure(title='Cumulative Revenue    (click-drag to zoom)', x_axis_label='Time', 
	y_axis_label='Revenue    (M$)', tools='box_zoom,reset,hover,crosshair', 
	width=1000, plot_height=300, x_range=[0, 1200], y_range=[-15, 10])
rev_fig.title_text_font_size = '15pt'
rev_fig.xaxis.axis_label_text_font_size = '11pt'
rev_fig.yaxis.axis_label_text_font_size = '11pt'
rev_fig.line('t', 'revenue', color='green', source=source, line_width=5, legend='revenue')
rev_fig.line('t', 'zero', color='purple', source=source, line_width=3, alpha=0.5, 
	line_dash=[10, 5])
rev_fig.legend.orientation = "bottom_right"
rev_fig.patch([0, 200, 200, 0], [-15, -15, 10, 10], color='lightsalmon', alpha=0.35, 
	line_width=0)
rev_fig.patch([200, 400, 400, 200], [-15, -15, 10, 10], color='gold', alpha=0.35, 
	line_width=0)
rev_fig.patch([400, 1200, 1200, 400], [-15, -15, 10, 10], color='darkseagreen', 
	alpha=0.35, line_width=0)        
rev_fig.text([45], [5.3], ['run-to-fail'])
rev_fig.text([245], [5.3], ['scheduled'])
rev_fig.text([245], [2.7], ['maintenance'])
rev_fig.text([445], [5.3], ['predictive'])
rev_fig.text([445], [2.7], ['maintenance'])
hover = rev_fig.select(dict(type=HoverTool))
hover.tooltips = [
	("         Time", "@t"),
	(" revenue (M$)", "@revenue"),
]

#plot number of motors vs time
N = events.groupby(['Time', 'state']).count().unstack()['id'].reset_index()
N.fillna(value=0, inplace=True)
N['total'] = N.maintenance + N.operating + N.repair
motor_source = ColumnDataSource(
	data=dict(
		Time = N.Time.tolist(),
		operating = N.operating.tolist(),
		maintenance = N.maintenance.tolist(),
		repair = N.repair.tolist(),
		total = N.total.tolist(),
	)
)
motor_fig = figure(title='Number of Motors    (click-drag to zoom)', x_axis_label='Time', 
	y_axis_label='Number of motors', tools='box_zoom,reset,hover,crosshair',
	width=1000, plot_height=300, x_range=[0, 1200], y_range=[-10, 210])
motor_fig.title_text_font_size = '15pt'
motor_fig.xaxis.axis_label_text_font_size = '11pt'
motor_fig.yaxis.axis_label_text_font_size = '11pt'
motor_fig.line('Time', 'total', color='blue', source=source_motor, line_width=3, legend='total', 
    alpha=1.0)
motor_fig.line('Time', 'operating', color='green', source=source_motor, line_width=3, legend='operating', 
    alpha=1.0)
motor_fig.line('Time', 'maintenance', color='orange', source=source_motor, line_width=3, 
    legend='maintenance', alpha=0.75)
motor_fig.line('Time', 'repair', color='red', source=source_motor, line_width=3, legend='repair', 
    alpha=1.0)
motor_fig.legend.orientation = "top_right"
motor_fig.patch([0, 200, 200, 0], [-10, -10, 210, 210], color='lightsalmon', alpha=0.35, 
	line_width=0)
motor_fig.patch([200, 400, 400, 200], [-10, -10, 210, 210], color='gold', alpha=0.35, 
	line_width=0)
motor_fig.patch([400, 1200, 1200, 400], [-10, -10, 210, 210], color='darkseagreen', 
	alpha=0.35, line_width=0)   
motor_fig.text([ 45], [173], ['run-to-fail'])
motor_fig.text([245], [173], ['scheduled'])
motor_fig.text([245], [155], ['maintenance'])
motor_fig.text([445], [173], ['predictive'])
motor_fig.text([445], [155], ['maintenance'])

#export plot to html and return
#plot_grid = vplot(dec_fig, earn_fig, rev_fig, motor_fig, vform(N_table))
plot_grid = vplot(dec_fig, earn_fig, rev_fig, motor_fig)
show(plot_grid, new='tab')


##display N table
#columns = [
#	TableColumn(field='Time', title='Time'),
#	TableColumn(field='operating', title='operating'),
#	TableColumn(field='maintenance', title='maintenance'),
#	TableColumn(field='repair', title='repair'),
#	TableColumn(field='total', title='total'),
#]
#s2 = ColumnDataSource(
#	data=dict(
#		Time = [],
#		operating = [],
#		maintenance = [],
#		repair = [],
#		total = [],
#	)
#)
#N_table = DataTable(source=s2, columns=columns, width=600, height=300)
#callback = Callback(args=dict(source=source), code="""
#    var data = source.get('data')
#    data['Time'].push([0, 1, 2])
#    data['operating'].push([11, 12, 13])
#    data['maintenance'].push([222, 333, 444])
#    data['repair'].push([567, 890, 1023])
#    data['total'].push([4, 4, 4])
#    source.trigger('change');
#""")

#    for (i = 0; i < inds.length; i++) {
#        d2['Time'].push(d1['Time'][inds[i]])
#        d2['operating'].push(d1['operating'][inds[i]])
#        d2['maintenance'].push(d1['maintenance'][inds[i]])
#        d2['repair'].push(d1['repair'][inds[i]])
#        d2['total'].push(d1['total'][inds[i]])
#    }
