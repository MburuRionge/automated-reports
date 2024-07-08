import jinja2
import random
import datetime as dt
import io
import base64
import matplotlib.pyplot as plt
import requests


# step 1 - create jinja template object from a string
template = jinja2.Environment(
    loader=jinja2.FileSystemLoader("./templates"),
    #autoescape=jinja2.select_autoescape
    autoescape=False
).get_template("sales_report.html")

#step 2 - create data for report
todayStr = dt.datetime.now().strftime("%d.%b.%Y")

salesTb1Rows = []
for k in range(10):
    costPu = random.randint(1, 15)
    nUnits = random.randint(100, 500)
    salesTb1Rows.append({"sNo": k+1, "name": "Item "+str(k+1),
                         "cPu": costPu, "nUnits": nUnits, "revenue": costPu*nUnits})
    
topItems = [x["name"] for x in sorted(
    salesTb1Rows, key=lambda x: x["revenue"], reverse=True)][0:3]

# create logo image from file
with open("templates/Gold Luxury Initial Circle Logo.png", "rb") as f:
    logoImg = base64.b64encode(f.read()).decode()
    
# GENERATE SALES BAR CHART
plotImgBytes = io.BytesIO()
fig, ax = plt.subplots()
ax.bar([x["name"] for x in salesTb1Rows], [x["revenue"] for x in salesTb1Rows])
fig.tight_layout()
fig.savefig(plotImgBytes, format="jpg")
plotImgBytes.seek(0)
plotImgStr = base64.b64encode(plotImgBytes.read()).decode()

# data for injecting into jinja2 template
context = {
    "reportDtStr": todayStr,
    "salesTb1Rows": salesTb1Rows,
    "topItemsRows": topItems,
    # "salesBarCharting": plotImgStr,
    "logoImg": logoImg,
    # "bootstrapCss": requests.get("<https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css>").text,
    # "bootstrapJs": requests.get("<https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js>").text
}

# step 3 - render data in jinja template
reportText = template.render(context)

# step 4 - save generate text as a HTML FILE
with open("reports/sales_report_{todayStr}.html", mode='w') as f:
    f.write(reportText)



# Render data in jinja template object
#context = {"name": "Mburu wa Ng\'ang\'a", "age": 24, "city": "Nairobi"}

#renderedText = template.render(context)

#print(renderedText)

# write output into a text file
#with open(f"./bio.txt", mode='w') as f:
#   f.write(renderedText)
    
#templateContext = {
#    "recipientName": "",
#    "eventDtStr": "04-july-2024",
#    "venueStr": "Westlands ABC Place Mall",
#    "senderName": "Mburu wa Ng\'ang\'a"
#}

#guests = ["Ng\'ang\'a wa Rionge", "Kariuki wa Ng\'ang\'a", "Njeri wa Ng\'ang\'a", "Karanja wa Kimani",
#          "Karanja wa Ng\'ang\'a", "Karanja wa Mwaura", "Gathoni wa Mwaura"]

#for g in guests:
#    templateContext["recipientName"] = g
    
    # render data in jinja template
#    inviteText = template.render(templateContext)
    
    # print(inviteText)
#    with open(f"./invites/{g}.txt", mode='w') as f:
#        f.write(inviteText)