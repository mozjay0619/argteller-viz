try:

    from IPython.display import display
    import ipywidgets as widgets
    from ipywidgets import HBox, Label, VBox
    from ipywidgets import Button, Layout, HTML
    from traitlets import MetaHasTraits

except ModuleNotFoundError:

    class VBox():
        pass

    class MetaHasTraits():
        pass
        

class ParamTextWidget(VBox):
    
    def __init__(self, name, example=None, default_value=None, preset_value=None, optional=False, widget=None, initial_event=None, param_setter_event=None):

        if not isinstance(VBox, MetaHasTraits):

            return

        self.name = name

        self.initial = True
        self.initial_event = initial_event
        self.param_setter_event = param_setter_event
        
        style = style = {'description_width': 'initial'}
        layout = Layout(display='flex', 
                        flex_flow='column', 
                        align_items='flex-start', 
                        border=None, 
                        width='50%',
                        align_content='flex-start')
        
        if preset_value:
            label = widgets.HTML(f"<b><font size=2 color='blue'>{self.name}</b>")
        elif optional:
            label = widgets.HTML(f"<b><font size=2 color='grey'>{self.name}</b>")
        else:
            label = widgets.HTML(f"<b><font size=2 color='black'>{self.name}</b>")
        
        if widget:
            self.widget = widget
        else:
            if example is None:
                self.widget = widgets.Text(style=style, layout=layout)
            else:
                self.widget = widgets.Text(description='E.g. {}: '.format(example), style=style, layout=layout)

        if (self.initial and not self.initial_event.isSet()) or self.param_setter_event.isSet() :  # So that user input is not overwritten every time.

            if preset_value is not None:  # So that preset values take precedence over default values.
                self.widget.value = str(preset_value) 
                
            elif default_value is not None:  
                self.widget.value = str(default_value) 
                
            self.initial = False
        
        children = [label, self.widget]
        super().__init__(children=children)
        
    def get_value(self):
        
        return self.widget.value


class ParamChoiceWidget(VBox):
    
    def __init__(self, name, options, default_value=None, preset_value=None, optional=False, widget=None, initial_event=None, param_setter_event=None):

        if not isinstance(VBox, MetaHasTraits):
            return

        self.name = name
        
        self.initial = True
        self.initial_event = initial_event
        self.param_setter_event = param_setter_event
        
        if preset_value:
            label = widgets.HTML(f"<b><font size=2 color='blue'>{self.name}</b>")
        elif optional:
            label = widgets.HTML(f"<b><font size=2 color='grey'>{self.name}</b>")
        else:
            label = widgets.HTML(f"<b><font size=2 color='black'>{self.name}</b>")

        if widget:
            self.widget = widget
        else:
            self.widget = widgets.RadioButtons(options=options, disabled=False)

        if (self.initial and not self.initial_event.isSet()) or self.param_setter_event.isSet() :  # So that user input is not overwritten every time.

            if preset_value is not None:  # So that preset values take precedence over default values.
                self.widget.value = str(preset_value) 
                
            elif default_value is not None:  
                self.widget.value = str(default_value) 
                
            self.initial = False

        children = [label, self.widget]
        super().__init__(children=children)
        
    def get_value(self):
        
        return self.widget.value

class ParamSetterWidget(VBox):

    def __init__(self, name, widget, default_value=None, preset_value=None, initial_event=None, param_setter_event=None):

        # this widget already exists

        if not isinstance(VBox, MetaHasTraits):

            return

        self.name = name

        self.initial = True
        self.initial_event = initial_event
        self.param_setter_event = param_setter_event

        # This is just label for this widget. The values are actually being
        # set on different widgets.
        if default_value:
            label = widgets.HTML(f"<b><font size=2 color='blue'>{self.name}</b>")
        else:
            label = widgets.HTML(f"<b><font size=2 color='black'>{self.name}</b>")

        self.widget = widget

        if (self.initial and not self.initial_event.isSet()) or self.param_setter_event.isSet() :  # So that user input is not overwritten every time.

            if preset_value is not None:  # So that preset values take precedence over default values.
                self.widget.value = str(preset_value) 
                
            elif default_value is not None:  
                self.widget.value = str(default_value) 
                
            self.initial = False

      
        children = [label, self.widget]
        super().__init__(children=children)

        
class Custom1(VBox):
    
    def __init__(self):

        if not isinstance(VBox, MetaHasTraits):

            return

        self.name = 'custom1'
        
        layout = {'width': '600px'}
        style = {'description_width': 'initial'}

        w1=widgets.IntRangeSlider(
            value=[10, 150],
            min=0,
            max=300,
            step=1,
            description='Regs search range:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            layout=layout,
            style=style
        )

        layout = {'width': '150px'}
        style = {'description_width': 'initial'}
        w2=widgets.Dropdown(
            options=[str(elem) for elem in list(range(1, 10))],
            value='1',
            description='Search gaps:',
            disabled=False,
            layout=layout
        )


        layout = {'width': '600px'}
        style = {'description_width': 'initial'}

        w3=widgets.IntRangeSlider(
            value=[5, 60],
            min=0,
            max=120,
            step=1,
            description='Days search range:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            layout=layout,
            style=style
        )

        layout = {'width': '150px'}
        style = {'description_width': 'initial'}
        w4=widgets.Dropdown(
            options=[str(elem) for elem in list(range(1, 10))],
            value='1',
            description='Search gaps:',
            disabled=False,
            layout=layout
        )
        
        h1 = HBox([w1, w2])
        h2 = HBox([w3, w4])

        label = widgets.HTML(f"<b><font size=2 color='black'>{'search_space'}</b>")     
        
        children = [label, h1, h2]
        super().__init__(children=children)
        
    def get_value(self):
        
        region_range = self.children[0].children[0].value
        region_jump = self.children[0].children[1].value

        day_range = self.children[1].children[0].value
        day_jump = self.children[1].children[1].value
        
        d = {'num_days': list(range(*day_range, int(day_jump))),
             'num_regions': list(range(*region_range, int(region_jump)))}
        
        return d
       

