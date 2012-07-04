from tkinter import *
from tkinter import ttk

class Display:
	def __init__(self, data, names, years):
		self.root = Tk()
		self.root.title("Tick-Talk")
		
		self.optionsframe = ttk.Frame(self.root, width = 1200, height = 100)
		self.optionsframe.pack(fill=X)
		
		self.canvas = Canvas(self.root, width=1200, height=1000)
		self.canvas.pack()
		
		self.drawList = Listbox(self.optionsframe, height=5, selectmode=SINGLE, exportselection=0)
		self.yearList = Listbox(self.optionsframe, height=5, selectmode=SINGLE, exportselection=0)
		self.timeList = Listbox(self.optionsframe, height=5, selectmode=SINGLE, exportselection=0)
		self.label = ttk.Label(self.optionsframe, text=" ")
		
		self.data = data
		self.names = names
		self.years = years
		
		self.drawList.insert(END, "Line count")
		self.drawList.insert(END, "Percentage")

		self.timeList.insert(END, "By year")
		self.timeList.insert(END, "Total")
		
		for year in self.years:
		    self.yearList.insert(END, year)
			
		self.label.pack(side = RIGHT)
		self.drawList.pack(side=LEFT, padx=30)
		self.timeList.pack(side=LEFT, padx=30)
		
	def drawValue(self, drawType, year, name, week):
		if drawType == "rawLines":
			return .25*self.data[year][name][week]
		elif drawType == "percentages":
			pass
			#if weekTotals[year][week] != 0:
			#	return (self.data[year][name][week]/weekTotals[year][week]*500)
				#return (peopleCounts[name][week]/weekTotals[week]*500)
			#else:
			
			#	return 0
	
	def nameLabel(self, currentTag):
		if len(currentTag) > 0:
			toTruncate = currentTag.index("current")
			#toTruncate = currentTag.index(" ")
			name = currentTag[0:toTruncate]
			return name
		else:
			return ""
	
	def drawYear(self, year):
		YOFFSET = 600
		xcoord = 1080
		bottomHeight = [YOFFSET]*108
		i = 0
		while i < 108:
			if i%2 == 0:
				bottomHeight[i] = xcoord
				xcoord = xcoord - 20
			i = i + 1

		num = 0 
		for name in self.names:
			topHeight = [0]*54;

			xcoord = 1080
			j = 53
			while j >= 0:
				topHeight[j] = xcoord
				topHeight.insert(j+1, self.drawValue("rawLines", year, name, j))
				xcoord = xcoord - 20
				j = j - 1

			for h in range(108):
				if h%2 == 1:
					topHeight[h] = bottomHeight[108 - h] - topHeight[h]  

			topHeight.append(topHeight[106])
			topHeight.append(bottomHeight[107])
			plotThis = topHeight + bottomHeight


			color = "lightblue"
			if num%10 == 8:
				color = "green"
			elif num%10 == 7: 
				color = "hot pink"
			elif num%10 == 6: 
				color = "yellow"
			elif num%10 == 5: 
				color = "gray"
			elif num%10 == 4:
				color = "pink"
			elif num%10 == 3:
				color = "purple"
			elif num%10 == 2:
				color = "orange"
			elif num%10 == 1:
				color = "blue"
			elif num%10 == 0:
				color = "red"

			self.canvas.create_polygon(plotThis,fill=color,outline="brown",width=2, smooth="true", tags=name)
			num = num + 1

			k = 0
			while k < 108:
				if k%2 == 1:
					bottomHeight[k] = topHeight[108 - k]
				k = k+1

			#canvas.bind('<Motion>', lambda e: label.configure(text = canvas.gettags(CURRENT)))
			self.canvas.bind('<Motion>', lambda e: self.label.configure(text = self.nameLabel(self.canvas.gettags(CURRENT))))		
			#canvas.bind('<Motion>', lambda e: canvas.itemconfig(canvas.find_withtag(canvas.gettags(CURRENT)), fill="blue"))	