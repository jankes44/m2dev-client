import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "IdleHuntingWindow",
	"style" : ("movable", "float",),
	
	"x" : 0,
	"y" : 0,
	
	"width" : 350,
	"height" : 300,
	
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" : 350,
			"height" : 300,
			
			"children" :
			(
				## Title Bar
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					
					"x" : 8,
					"y" : 7,
					
					"width" : 334,
					"color" : "yellow",
					
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":0, "text":"Idle Hunting", "all_align":"center" },
					),
				},
				
				## State Text
				{
					"name" : "StateText",
					"type" : "text",
					
					"x" : 0,
					"y" : 40,
					
					"text" : "Idle Hunting System",
					"all_align" : "center",
				},
				
				## Progress Bar
				{
					"name" : "ProgressBar",
					"type" : "gauge",
					
					"x" : 50,
					"y" : 60,
					
					"width" : 250,
					"color" : "red",
				},
				
				## Time Text
				{
					"name" : "TimeText",
					"type" : "text",
					
					"x" : 0,
					"y" : 70,
					
					"text" : "Daily Time: 0h 0m / 8h 0m",
					"horizontal_align" : "center",
                    "text_horizontal_align": "center",
				},
			),
		},
	),
}
