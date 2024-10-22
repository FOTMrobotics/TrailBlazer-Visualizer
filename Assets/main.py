import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import numpy as np
import os
import tools
import json



class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Path Visualizer")

        self.geometry('1050x1000')

        self.directory = os.path.dirname(__file__)

        # Grabs configuration from config.json
        os.chdir(self.directory)
        os.chdir('..')
        with open(os.path.join(os.getcwd(), 'config.json'), 'r') as f:
            self.config = json.load(f)

        print(f"\nSettings: {self.config}\n")

        self.font = tkFont.Font(family=self.config['font'], size=self.config['fontSize'])

        self.configure(bg=self.config['primaryColor'])

        self.drawField()

        objectFrame = tk.Frame(self, bg=self.config['primaryColor'])
        objectFrame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.N)

        addPointButton = tk.Button(objectFrame, text="Add Point", font=self.font, fg=self.config['textColor'], bg=self.config['tertiaryColor'], activebackground=self.config['primaryColor'], command=self.addPoint)
        addPointButton.grid(column=0, row=0, padx=5, pady=5, sticky=tk.N)

        self.numPoints = 0
        self.points = []
        self.pointList = tk.Listbox(objectFrame, font=self.font, fg=self.config['textColor'], height=15, width=15, bg=self.config['secondaryColor'], highlightbackground=self.config['borderColor'], highlightcolor=self.config['borderColor'], highlightthickness=self.config['borderThickness'], exportselection=False)
        self.pointList.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
        self.pointList.bind('<<ListboxSelect>>', self.pointSelected)

        addEventButton = tk.Button(objectFrame, text='Add Event', font=self.font, fg=self.config['textColor'], bg=self.config['tertiaryColor'], activebackground=self.config['primaryColor'], command=self.addEvent)
        addEventButton.grid(column=0, row=2, padx=5, pady=5)

        self.numEvents = 0
        self.events = []
        self.eventList = tk.Listbox(objectFrame, font=self.font, fg=self.config['textColor'], height=15, width=15, bg=self.config['secondaryColor'], highlightbackground=self.config['borderColor'], highlightcolor=self.config['borderColor'], highlightthickness=self.config['borderThickness'], exportselection=False)
        self.eventList.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
        self.eventList.bind('<<ListboxSelect>>', self.eventSelected)



    # Displays the point editing frame
    def pointSelected(self, event):
        # Gets selected point
        selection = self.pointList.curselection()
        try:self.selectedPoint = selection[0]
        except:pass

        try:self.eventList.selection_clear(0, tk.END)
        except:pass

        try:self.eventEditFrame.destroy()
        except:pass

        try:self.pointEditFrame.destroy()
        except:pass
        
        # Creates frame
        self.pointEditFrame = tk.LabelFrame(self, text=f"Point {self.selectedPoint+1}", font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.pointEditFrame.grid(column=2, row=0, padx=10, pady=10, sticky=tk.N)

        if self.numPoints == 0:
            try:self.pointEditFrame.destroy()
            except:pass
            pass

        # Heading editing

        self.headingSelectFrame = tk.Frame(self.pointEditFrame, bg=self.config['primaryColor'])
        self.headingSelectFrame.grid(column=0, row=0, padx=5, pady=5)

        self.headingSelectLabel = tk.Label(self.headingSelectFrame, text='Heading Type:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.headingSelectLabel.grid(column=0, row=0, padx=5, pady=5)
        self.headingSelect = ttk.Combobox(self.headingSelectFrame, font=self.font, background=self.config['secondaryColor'])
        if self.points[self.selectedPoint][1][0] is not None:
            self.headingSelect.set(self.points[self.selectedPoint][1][0])
        else:
            self.headingSelect.set('Follow')
        self.headingSelect.grid(column=0, row=1, padx=5, pady=5)

        # Options
        self.headingSelect['values'] = ('Follow', 'Constant', 'Offset')

        headingLabel = tk.Label(self.headingSelectFrame, text='Heading:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        headingLabel.grid(column=0, row=2, padx=5, pady=5)
        self.headingEntry = tk.Entry(self.headingSelectFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
        self.headingEntry.grid(column=0, row=3, padx=5, pady=5)
        if self.points[self.selectedPoint][1][1] is not None:
            self.headingEntry.delete(0, tk.END)
            self.headingEntry.insert(0, self.points[self.selectedPoint][1][1])

        # Disables entry for when 'Follow' heading is not selected
        self.headingSelect.bind('<<ComboboxSelected>>', self.updateHeadingSelect)
        self.updateHeadingSelect(0)

        # Position editing

        posFrame = tk.Frame(self.pointEditFrame, bg=self.config['primaryColor'])
        posFrame.grid(column=0, row=1, padx=5, pady=5)

        # X position
        self.xPosLabel = tk.Label(posFrame, text='X:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.xPosLabel.grid(column=0,row=0, padx=5, pady=5)
        self.xPosEntry = tk.Entry(posFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
        self.xPosEntry.grid(column=0,row=1, padx=5, pady=5)
        if self.points[self.selectedPoint][0][0] is not None:
            self.xPosEntry.delete(0, tk.END)
            self.xPosEntry.insert(0, str(self.points[self.selectedPoint][0][0]))

        # Y position
        self.yPosLabel = tk.Label(posFrame, text='Y:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.yPosLabel.grid(column=0,row=2, padx=5, pady=5)
        self.yPosEntry = tk.Entry(posFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
        self.yPosEntry.grid(column=0,row=3, padx=5, pady=5)
        if self.points[self.selectedPoint][0][1] is not None:
            self.yPosEntry.delete(0, tk.END)
            self.yPosEntry.insert(0, str(self.points[self.selectedPoint][0][1]))

        # Edit and delete buttons

        pointButtons = tk.Frame(self.pointEditFrame, bg=self.config['primaryColor'])
        pointButtons.grid(column=0, row=2, padx=5, pady=5)

        editButton = tk.Button(pointButtons, text="Edit", font=self.font, fg=self.config['textColor'], bg=self.config['tertiaryColor'], activebackground=self.config['primaryColor'], command=self.editPoint)
        editButton.grid(column=0, row=0, padx=5, pady=5)

        deleteButton = tk.Button(pointButtons, text='Delete', font=self.font, fg=self.config['textColor'], bg=self.config['tertiaryColor'], activebackground=self.config['primaryColor'], command=self.deletePoint)
        deleteButton.grid(column=1, row=0, padx=5, pady=5)

    # Disables entry for when 'Follow' heading is not selected
    def updateHeadingSelect(self, event):
        value = self.headingSelect.get()

        if value != 'Follow':
            self.headingEntry['state'] = tk.NORMAL
        else:
            self.headingEntry['state'] = tk.DISABLED



    # Displays the event editing frame
    def eventSelected(self, event):
        # Gets selected event
        selection = self.eventList.curselection()
        try:self.selectedEvent = selection[0]
        except:pass
           
        try:self.pointList.selection_clear(0, tk.END)
        except:pass
        
        try:self.pointEditFrame.destroy()
        except:pass

        try:self.eventEditFrame.destroy()
        except:pass

        self.eventEditFrame = tk.LabelFrame(self, text=f"Event {self.selectedEvent+1}", font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.eventEditFrame.grid(column=2, row=0, padx=10, pady=10, sticky=tk.N)
        
        if self.numEvents == 0:
            try:self.eventEditFrame.destroy()
            except:pass
            pass

        # Type of event

        self.eventFrame = tk.Frame(self.eventEditFrame, bg=self.config['primaryColor'])
        self.eventFrame.grid(column=0, row=0, padx=5, pady=5)

        self.eventSelectLabel = tk.Label(self.eventFrame, text='Event Type:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.eventSelectLabel.grid(column=0, row=0, padx=5, pady=5)
        self.eventSelect = ttk.Combobox(self.eventFrame, font=self.font, background=self.config['secondaryColor'])
        if self.events[self.selectedEvent][1][0] is not None:
            self.eventSelect.set(self.events[self.selectedEvent][1][0])
            self.displayEventType()
        else:
            self.eventSelect.set('Choose an Option')
        self.eventSelect.grid(column=0, row=1, padx=5, pady=5)

        # Options
        self.eventSelect['values'] = ('Action', 'Speed', 'Follow Distance', 'Stop', 'Turn')

        # Type of position

        self.eventPosFrame = tk.Frame(self.eventEditFrame, bg=self.config['primaryColor'])
        self.eventPosFrame.grid(column=0, row=1, padx=5, pady=5)

        self.eventPosSelectLabel = tk.Label(self.eventPosFrame, text='Position Type:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.eventPosSelectLabel.grid(column=0, row=0, padx=5, pady=5)
        self.eventPosSelect = ttk.Combobox(self.eventPosFrame, font=self.font, background=self.config['secondaryColor'])
        if self.events[self.selectedEvent][0][0] is not None:
            #self.eventPosSelect.set('Point')
            self.displayEventPoint()
        self.eventPosSelect.set('Choose an Option')
        self.eventPosSelect.grid(column=0, row=1, padx=5, pady=5)

        # Options
        self.eventPosSelect['values'] = ('Point', 'At Point', 'Along Segment')

        self.eventSelect.bind('<<ComboboxSelected>>', self.eventChange)
        self.eventPosSelect.bind('<<ComboboxSelected>>', self.eventChange)

        # Edit and delete buttons

        eventButtons = tk.Frame(self.eventEditFrame, bg=self.config['primaryColor'])
        eventButtons.grid(column=0, row=2, padx=5, pady=5)

        editButton = tk.Button(eventButtons, text="Edit", font=self.font, fg=self.config['textColor'], bg=self.config['tertiaryColor'], activebackground=self.config['primaryColor'], command=self.editEvent)
        editButton.grid(column=0, row=0, padx=5, pady=5)

        deleteButton = tk.Button(eventButtons, text='Delete', font=self.font, fg=self.config['textColor'], bg=self.config['tertiaryColor'], activebackground=self.config['primaryColor'], command=self.deleteEvent)
        deleteButton.grid(column=1, row=0, padx=5, pady=5)

    def eventChange(self, event):
        self.eventType = self.eventSelect.get()
        self.posType = self.eventPosSelect.get()

        self.eventEditFrame.destroy()
        self.eventSelected(0)

        self.eventSelect.set(self.eventType)
        self.eventPosSelect.set(self.posType)

        self.displayEventType()

        match self.posType:
            case 'Point':
                self.displayEventPoint()
            case 'At Point':
                self.displayEventAtPoint()
            case 'Along Segment':
                self.displayEventAlongSegment()

        self.eventEditFrame.grid(column=2, row=0, padx=10, pady=10, sticky=tk.N)

    def displayEventType(self):
        match self.eventType:
            case 'Action':
                pass
            case 'Speed':
                speedLabel = tk.Label(self.eventFrame, text='Speed:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
                speedLabel.grid(column=0, row=2, padx=5, pady=5)
                self.eventValue = tk.Entry(self.eventFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
                self.eventValue.grid(column=0, row=3, padx=5, pady=5)
            case 'Follow Distance':
                fdLabel = tk.Label(self.eventFrame, text='Follow Distance:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
                fdLabel.grid(column=0, row=2, padx=5, pady=5)
                self.eventValue = tk.Entry(self.eventFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
                self.eventValue.grid(column=0, row=3, padx=5, pady=5)
            case 'Stop':
                waitLabel = tk.Label(self.eventFrame, text='Wait Time:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
                waitLabel.grid(column=0, row=2, padx=5, pady=5)
                self.eventValue = tk.Entry(self.eventFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
                self.eventValue.grid(column=0, row=3, padx=5, pady=5)
            case 'Turn':
                turnLabel = tk.Label(self.eventFrame, text='Angle:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
                turnLabel.grid(column=0, row=2, padx=5, pady=5)
                self.eventValue = tk.Entry(self.eventFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
                self.eventValue.grid(column=0, row=3, padx=5, pady=5)

        if self.eventType != 'Action':
            if self.events[self.selectedEvent][1][1] is not None:
                self.eventValue.delete(0, tk.END)
                self.eventValue.insert(0, str(self.events[self.selectedEvent][1][1]))

    def displayEventPoint(self):
        # Frame
        self.posEventLabelFrame = tk.Frame(self.eventPosFrame, bg=self.config['primaryColor'])
        self.posEventLabelFrame.grid(column=0, row=2, padx=5, pady=5)

        # X position
        self.xPosEventLabel = tk.Label(self.posEventLabelFrame, text='X:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.xPosEventLabel.grid(column=0,row=0, padx=5, pady=5)
        self.xPosEventEntry = tk.Entry(self.posEventLabelFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
        self.xPosEventEntry.grid(column=0,row=1, padx=5, pady=5)
        if self.events[self.selectedEvent][0][0] is not None:
            self.xPosEventEntry.delete(0, tk.END)
            self.xPosEventEntry.insert(0, str(self.events[self.selectedEvent][0][0]))

        # Y position
        self.yPosEventLabel = tk.Label(self.posEventLabelFrame, text='Y:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        self.yPosEventLabel.grid(column=0,row=2, padx=5, pady=5)
        self.yPosEventEntry = tk.Entry(self.posEventLabelFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
        self.yPosEventEntry.grid(column=0,row=3, padx=5, pady=5)
        if self.events[self.selectedEvent][0][1] is not None:
            self.yPosEventEntry.delete(0, tk.END)
            self.yPosEventEntry.insert(0, str(self.events[self.selectedEvent][0][1]))

    def displayEventAtPoint(self):
        # Fix for widgets not going away
        try:self.posEventLabelFrame.destroy()
        except:pass

        atPointFrame = tk.Frame(self.eventPosFrame, bg=self.config['primaryColor'])
        atPointFrame.grid(column=0, row=2, padx=5, pady=5)

        pointLabel = tk.Label(atPointFrame, text='Point:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        pointLabel.grid(column=0, row=0, padx=5, pady=5)
        self.pointCombobox = ttk.Combobox(atPointFrame, font=self.font, background=self.config['secondaryColor'])
        self.pointCombobox.grid(column=0, row=1, padx=5, pady=5)

        self.pointCombobox.set('Select a Point')

        for i in range(len(self.points)):
            self.pointCombobox['values'] = list(self.pointCombobox['values']) + [f'Point {i+1}']

    def displayEventAlongSegment(self):
        alongSegmentFrame = tk.Frame(self.eventPosFrame, bg=self.config['primaryColor'])
        alongSegmentFrame.grid(column=0, row=2, padx=5, pady=5)

        pointLabel1 = tk.Label(alongSegmentFrame, text='Point 1:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        pointLabel1.grid(column=0, row=0, padx=5, pady=5)
        self.pointCombobox1 = ttk.Combobox(alongSegmentFrame, font=self.font, background=self.config['secondaryColor'])
        self.pointCombobox1.grid(column=0, row=1, padx=5, pady=5)
                
        self.pointCombobox1.set('Select a Point')

        for i in range(len(self.points)):
            self.pointCombobox1['values'] = list(self.pointCombobox1['values']) + [f'Point {i+1}']

        pointLabel2 = tk.Label(alongSegmentFrame, text='Point 2:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        pointLabel2.grid(column=0, row=2, padx=5, pady=5)
        self.pointCombobox2 = ttk.Combobox(alongSegmentFrame, font=self.font, background=self.config['secondaryColor'])
        self.pointCombobox2.grid(column=0, row=3, padx=5, pady=5)
                
        self.pointCombobox2.set('Select a Point')

        for i in range(len(self.points)):
            self.pointCombobox2['values'] = list(self.pointCombobox2['values']) + [f'Point {i+1}']

        percentageLabel = tk.Label(alongSegmentFrame, text='Percentage:', font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        percentageLabel.grid(column=0, row=4, padx=5, pady=5)

        self.scale = tk.Scale(alongSegmentFrame, from_=0.0, to=1.0, digits=3, resolution=0.01, orient=tk.HORIZONTAL, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'], activebackground=self.config['primaryColor'])
        self.scale.grid(column=0, row=6, padx=5, pady=5)
        self.scaleEntry = tk.Entry(alongSegmentFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
        self.scaleEntry.grid(column=0, row=5, padx=5, pady=5)

        self.scale.bind('<ButtonRelease-1>', self.linkScaleEntry)
        self.scaleEntry.bind('<KeyRelease>', self.linkEntryScale)


    def linkScaleEntry(self, event):
        self.scaleEntry.delete(0, tk.END)
        self.scaleEntry.insert(0, self.scale.get())

    def linkEntryScale(self, event):
        self.scale.set(self.scaleEntry.get())



# Add/Delete/Edit point
    # Adds point to list
    def addPoint(self):
        try:selected = self.selectedPoint
        except:selected = self.numPoints - 1

        self.numPoints += 1
        # [Positon, Heading]
        self.points.insert(selected + 1, [[None, None], [None, None]])
        self.refreshLists()
        self.pointList.selection_clear(0, tk.END)
        self.pointList.select_set(selected + 1)
        self.pointList.event_generate('<<ListboxSelect>>')

    # Removed point from list
    def deletePoint(self):
        selected = self.selectedPoint

        self.numPoints -= 1
        
        self.points.pop(self.selectedPoint)
        self.refreshLists()

        self.pointEditFrame.destroy()

        print(f"\nPoints: {self.points}\n")

        self.pointList.selection_clear(0, tk.END)
        self.pointList.select_set(selected-1)
        self.pointList.event_generate('<<ListboxSelect>>')

        # Updates field
        try:self.updateField()
        except:pass

    # Changes point in list
    def editPoint(self):
        self.points[self.selectedPoint][0][0] = float(self.xPosEntry.get())
        self.points[self.selectedPoint][0][1] = float(self.yPosEntry.get())
        self.points[self.selectedPoint][1][0] = self.headingSelect.get()
        if self.points[self.selectedPoint][1][0] != 'Follow':
            self.points[self.selectedPoint][1][1] = float(self.headingEntry.get())
        else:
            self.points[self.selectedPoint][1][1] = None

        # Updates point editing frame
        self.pointSelected(0)

        print(f"\nPoints: {self.points}\n")

        # Updates field
        try:self.updateField()
        except:pass

# Add/Delete/Edit event
    # Adds event to list
    def addEvent(self):
        try:selected = self.selectedEvent
        except:selected = self.numEvents - 1

        self.numEvents += 1
        # [Position, Type]
        self.events.insert(selected + 1, [[None, None], [None, None]])
        self.refreshLists()
        self.eventList.selection_clear(0, tk.END)
        self.eventList.select_set(selected + 1)
        self.eventList.event_generate('<<ListboxSelect>>')

    # Removed event from list
    def deleteEvent(self):
        selected = self.selectedEvent

        self.numEvents -= 1
        
        self.events.pop(self.selectedEvent)
        self.refreshLists()

        self.eventEditFrame.destroy()

        print(f"\nEvents: {self.events}\n")
        
        self.eventList.selection_clear(0, tk.END)
        self.eventList.select_set(selected-1)
        self.eventList.event_generate('<<ListboxSelect>>')

        try:self.updateField()
        except:pass

    # Changes event in list
    def editEvent(self):
        match self.posType:
            case 'Point':
                self.events[self.selectedEvent][0][0] = float(self.xPosEventEntry.get())
                self.events[self.selectedEvent][0][1] = float(self.yPosEventEntry.get())
            case 'At Point':
                selectedPoint = int(self.pointCombobox.get()[-1]) - 1
                self.events[self.selectedEvent][0] = self.points[selectedPoint][0]
            case 'Along Segment':
                selectedPoint1 = int(self.pointCombobox1.get()[-1]) - 1
                selectedPoint2 = int(self.pointCombobox2.get()[-1]) - 1

                if selectedPoint1 == 0:
                    P0 = np.array(self.points[selectedPoint1][0])
                else:
                    P0 = np.array(self.points[selectedPoint1 - 1][0])

                P1 = np.array(self.points[selectedPoint1][0])
                P2 = np.array(self.points[selectedPoint2][0])

                if selectedPoint2 == self.numPoints - 1:
                    P3 = np.array(self.points[selectedPoint2][0])
                else:
                    P3 = np.array(self.points[selectedPoint2 + 1][0])

                self.events[self.selectedEvent][0] = tools.catmullRomSplineInterpolation(P0, P1, P2, P3, self.scale.get()).tolist()

        self.events[self.selectedEvent][1][0] = self.eventType
        if self.eventType != 'Action':
            self.events[self.selectedEvent][1][1] = self.eventValue.get()
        else:
            self.events[self.selectedEvent][1][1] = None

        # Updates event editing frame
        self.eventSelected(0)

        print(f"\nEvents: {self.events}\n")

        # Updates field
        try:self.updateField()
        except:pass

    def refreshLists(self):
        self.pointList.delete(0,tk.END)
        for i in range(len(self.points)):
            self.pointList.insert(i, f"Point {i+1}")

        self.eventList.delete(0,tk.END)
        for i in range(len(self.events)):
            self.eventList.insert(i, f"Event {i+1}")



    # Creates field frame
    def drawField(self):
        self.fieldFrame = tk.Frame(self, bg=self.config['primaryColor'])
        self.fieldFrame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.N)

        self.field = tk.Canvas(self.fieldFrame, width=640, height=640, highlightbackground=self.config['borderColor'], highlightcolor=self.config['borderColor'], highlightthickness=self.config['borderThickness'])
        self.field.grid(column=0, row=1, padx=5, pady=5)

        # Show field image
        fieldImage = tk.PhotoImage(file=os.path.join(self.directory, self.config['fieldImage']))
        self.field.create_image((self.config['borderThickness'],self.config['borderThickness']), image=fieldImage, anchor=tk.NW)

        # Fix to show image
        imageLabel = tk.Label(self.fieldFrame, image=fieldImage)
        imageLabel.photo = fieldImage

    # Clears path on field
    def resetField(self):
        self.fieldFrame.destroy()
        self.drawField()

    # Displays path on field image and gives code
    def updateField(self):
        self.resetField()

        IMAGESIZE = 640
        FIELDSIZEINCH = 144
        FIELDSIZECM = FIELDSIZEINCH * 2.54

        if self.config['unit'] == 'inch':
            SCALE = IMAGESIZE / FIELDSIZEINCH
        elif self.config['unit'] == 'cm':
            SCALE = IMAGESIZE / FIELDSIZECM

        controlPoints = []
        for i in self.points:
            controlPoints.append(i[0])
        controlPoints.insert(0, self.points[0][0])
        controlPoints.append(self.points[-1][0])
        controlPoints = np.array(controlPoints)
        controlPoints = controlPoints * SCALE

        splinePoints = tools.catmullRomChain(controlPoints)

        CIRCLESIZE = 5
        for i in range(len(controlPoints) - 1):
            self.field.create_oval(controlPoints[i][0] - CIRCLESIZE, controlPoints[i][1] - CIRCLESIZE, controlPoints[i][0] + CIRCLESIZE, controlPoints[i][1] + CIRCLESIZE, fill=self.config['pointColor'])
        for i in range(len(splinePoints) - 1):
            self.field.create_line(splinePoints[i][0], splinePoints[i][1], splinePoints[i+1][0], splinePoints[i+1][1], fill=self.config['pathColor'], width=self.config['pathSize'])

        if self.numEvents != 0:
            for i in range(self.numEvents):
                self.field.create_oval(self.events[i][0][0]*SCALE - CIRCLESIZE, self.events[i][0][1]*SCALE - CIRCLESIZE, self.events[i][0][0]*SCALE + CIRCLESIZE, self.events[i][0][1]*SCALE + CIRCLESIZE, fill=self.config['eventColor'])

        self.displayCode()

        print("\nUpdated\n")

    # Creates code frame
    def displayCode(self):
        codeFrame = tk.LabelFrame(self, text="Code", font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        codeFrame.grid(column=0, row=1, padx=10, pady=10)

        textBox = tk.Text(codeFrame, font=self.font, fg=self.config['textColor'], bg=self.config['secondaryColor'])
        textBox.grid(column=0, row=0, padx=5, pady=5)

        text = f"Path pathName = drive.pathBuilder(new Vector2D({self.points[0][0][0]}, {self.points[0][0][1]}))"

        for i in range(len(self.points) - 1):
            text += f"\n\t.pt({self.points[i+1][0][0]}, {self.points[i+1][0][1]})"

        text += f"\n\t.build()"

        textBox.insert(tk.END, text)



    # For error messages (Unused for now)
    def confirmationMenu(self, text):
        menu = tk.Toplevel()
        menu.title("Message")
        menu.configure(bg=self.config['primaryColor'])
        message = tk.Label(menu, text=text, font=self.font, fg=self.config['textColor'], bg=self.config['primaryColor'])
        message.grid(column=0, row=0, padx=10, pady=10)
        button = tk.Button(menu, text="Ok", font=self.font, fg=self.config['textColor'], bg=self.config['tertiaryColor'], activebackground=self.config['primaryColor'], command=lambda:menu.destroy())
        button.grid(column=0, row=1, padx=10, pady=10)



if __name__ == "__main__":
    root = Main()
    root.mainloop()
