import datetime

#most_demanding_processus_placeholder =["w","c","s","f"]

#variable
current_date = datetime.datetime.now().strftime("%B %d, %Y")
current_date

#read template
html = open("template.html").read()

#replace variable
html = html.replace("{{date_test}}", current_date)

#html = html.replace("{{most_demanding_processus_placeholder}}", most_demanding_processus_placeholder)

#print and open to index
print(html)
with open("index.html", "w") as fp:
    fp.write(html)