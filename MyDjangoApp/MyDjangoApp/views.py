from bokeh.models import Range1d, LinearAxis, PrintfTickFormatter
from pylab import *
from scipy.interpolate import spline
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from bokeh.plotting import figure, output_file
from bokeh.embed import components
matplotlib.use('Agg')
@csrf_exempt
def index(request):
    if request.method == 'POST':

        #obtained points
        p1x = float(request.POST.get('p1x'))
        p1y = float(request.POST.get('p1y'))
        p2x = float(request.POST.get('p2x'))
        p2y = float(request.POST.get('p2y'))
        p3x = float(request.POST.get('p3x'))
        p3y = float(request.POST.get('p3y'))
        p4x = request.POST.get('p4x')
        p4y = request.POST.get('p4y')
        if not p4x or not p4y :
            val1 = [p1x, p2x, p3x]
            val2 = [p1y, p2y, p3y]

        else:
            val1 = [p1x, p2x, p3x,float(p4x)]
            val2 = [p1y, p2y, p3y,float(p4y)]
            revenue4 = int(float(p4x) * float(p4y))



        #min and max of values
        maxprice =max(val1)
        minquantity =min(val2)
        minprice = min(val1)
        maxquantity = max(val2)

        #calculating elasticity and revenue
        elasticity=round(((p2y-p1y)/(p2y+p1y))/((p2x-p1x)/(p2x+p1x)),2)
        revenue1=int(p1x*p1y)
        revenue2=int(p2x*p2y)
        revenue3=int(p3x*p3y)

        if not p4x or not p4y:
            val3 = [0,minprice*0.5,p1x, p2x, p3x,maxprice*1.2,maxprice*1.4]
            val4 = [maxquantity*3 , maxquantity*1.5,p1y, p2y, p3y,minquantity*0.5,0]
        else:
            val3 = [0, minprice * 0.5, p1x, p2x, p3x,float(p4x) , maxprice * 1.2, maxprice * 1.4]
            val4 = [maxquantity * 3,maxquantity * 1.5, p1y, p2y, p3y,float(p4y), minquantity * 0.5, 0]


        price = np.array(val3)
        quantity = np.array(val4)


        #first grph
        plt = figure(tools="hover", title="Demand and Revenue Curve" ,plot_width = 900, plot_height = 400,
                     toolbar_location=None,x_axis_label='Price',y_axis_label='Quantity')
        plt.background_fill_color = "beige"
        output_file("legend.html")


        #plotting demand curve
        xnew = np.linspace(price.min(), price.max(),300)  # 300 represents number of points to make between T.min and T.max
        power_smooth = spline(price, quantity, xnew, order=2)
        plt.line(xnew, power_smooth, color="red", legend="Demand")
        #interpolate points
        plt.circle(val1, val2, fill_color="blue", size=8)


        #plotting revenue curve
        revenue = np.array(xnew*power_smooth)
        xnew1 = np.linspace(price.min(), price.max(), 300)  # 300 represents number of points to make between T.min and T.max
        power_smooth1 = spline(xnew, revenue, xnew1, order=2)
        #extra y axis
        plt.extra_y_ranges = {"NumStations": Range1d(start=0, end=maxquantity * 30)}
        plt.add_layout(LinearAxis(y_range_name="NumStations", axis_label="Revenue"), 'right')
        plt.line(xnew1, power_smooth1, y_range_name='NumStations',color="green",legend="Revenue")

        #format of label in y axis
        plt.yaxis[0].formatter = PrintfTickFormatter(format="%f")
        plt.yaxis[1].formatter = PrintfTickFormatter(format="%f")


        optimalrevenuey = max(power_smooth1)
        for i in range(len(power_smooth1)):
            if power_smooth1[i] == optimalrevenuey:
                optimalprice=round(xnew1[i],2)
                optimalquantity=int(power_smooth[i])
                optimalrevenuex=round(power_smooth1[i],1)
                break
            else:
                optimalprice=0
                optimalquantity=0
        optimalrevenue=int(optimalquantity*optimalprice)
        op1=[optimalprice]
        op2=[optimalquantity]

        plt.circle(op1,op2, fill_color="yellow", size=8, legend="Optimal Value" )
        script, div = components(plt)



        if not p4x or not p4y:
            return render(request, 'pages/index.html',context={'script': script, 'div': div,
                                                               'price1':int(p1x),
                                                               'price2': int(p2x),
                                                               'price3': int(p3x),
                                                               'price4': request.POST.get('p4x'),
                                                               'optimalrevenue': optimalrevenue,
                                                               'elasticity' :elasticity,
                                                               'revenue1' :revenue1,'revenue2'
                                                               :revenue2,'revenue3' :revenue3,
                                                               'optimalprice' :optimalprice,
                                                               'optimalquantity' :optimalquantity})
        else:
            return render(request, 'pages/index.html', context={'script': script, 'div': div,
                                                                'price1': int(p1x),
                                                                'price2': int(p2x),
                                                                'price3': int(p3x),
                                                                'price4': request.POST.get('p4x'),
                                                                'optimalrevenue': optimalrevenue,
                                                                'elasticity': elasticity,
                                                                'revenue1': revenue1, 'revenue2'
                                                                : revenue2, 'revenue3': revenue3,
                                                                'revenue4': revenue4,
                                                                'optimalprice': optimalprice,
                                                                'optimalquantity': optimalquantity})


    else:
        plt = figure(tools="hover", title="Demand and Revenue Curve", plot_width=900, plot_height=400,
                     toolbar_location=None, x_axis_label='Price', y_axis_label='Quantity')
        plt.extra_y_ranges = {"NumStations": Range1d(start=0, end=30)}
        plt.add_layout(LinearAxis(y_range_name="NumStations", axis_label="Revnue"), 'right')
        output_file("legend.html")

        #sample values
        val1 = [10, 12, 15]
        val2 = [500, 450, 400]
        xnew = np.linspace(val1[0], val1[1], 300)  # 300 represents number of points to make between T.min and T.max
        power_smooth = spline(val1, val2, xnew, order=2)
        plt.line(xnew, power_smooth, y_range_name='NumStations')
        plt.background_fill_color = "beige"

        script, div = components(plt)

        return render(request, 'pages/index.html',
                      context={'script': script, 'div': div,'optimalrevenue':0,
                               'elasticity' :0,'revenue1' :0,'revenue2' :0,'revenue3' :0,'revenue4' :0,'optimalprice' :0,
                               'optimalquantity' :0})




